# Copyright (c) 2021, nomi-g and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class OutwardGatePass(Document):
    print('i am custom gate pass py')
    def validate(self):
        settings = frappe.get_single("Gate Pass Settings")
        if settings.ogp_description_mandatory and not self.description:
            frappe.throw(_("description is manadatory"))

    @frappe.whitelist()
    def load_delivery_note_items(self):
        if self.delivery_note:
            self.total_qty = 0
            dn = frappe.get_doc("Delivery Note", self.delivery_note)
            self.items = {}
            for it in dn.items:
                item = self.append("items", {})
                item.item_code = it.item_code
                item.item_name = it.item_name
                item.description = it.description
                item.uom = it.uom
                item.qty = it.qty
                self.total_qty += it.qty
        else:
            self.items = {}
            self.total_qty = 0

    @frappe.whitelist()
    def get_po_items(self):
        mrpri = frappe.get_list("Purchase Order Item", filters={"parent": self.purchase_order},
                               fields=['item_code', 'item_name', 'qty', 'uom'], order_by="schedule_date")
        print(mrpri)
        self.set("items", [])
        for items in mrpri:
            self.append(
                "items",
                {
                    "item_code": items.item_code,
                    "item_name": items.item_name,
                    "qty": items.qty,
                    "uom": items.uom,

                },
            )
