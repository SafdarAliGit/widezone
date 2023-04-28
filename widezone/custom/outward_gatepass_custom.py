from __future__ import unicode_literals
import json
import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate, nowdate


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_transporter(doctype, txt, searchfield, start, page_len, filters):
    if isinstance(filters, str):
        filters = json.loads(filters)

    transporter = frappe.db.sql("""select transporter_name,name from `tabTransporter`
		where ({key} like %(txt)s)			
		order by
			if(locate(%(_txt)s, name), locate(%(_txt)s, name), 99999),
			idx desc,
			name
		limit %(start)s, %(page_len)s""".format(**{
        'key': searchfield
    }), {
                                   'txt': "%%%s%%" % txt,
                                   '_txt': txt.replace("%", ""),
                                   'start': start,
                                   'page_len': page_len,

                               })
    return transporter


def validate(self, method):
    if len(self.items) > 0:
        self.total_qty = 0
        for item in self.items:
            self.total_qty += item.qty

def submit(self, method):
    if len(self.items) > 0:
        self.total_qty = 0
        for item in self.items:
            self.total_qty += item.qty


@frappe.whitelist()
def get_po_items(doc):
    stock = frappe.get_all("Stock Entry", filters={"purchase_order": doc} , fields=['name'])
    print(stock)
    if stock:
        mrpri = frappe.get_doc("Stock Entry", stock[0].name)
        return mrpri
    else:
        return "No data found"

@frappe.whitelist()
def get_purchase_order(doctype, txt, searchfield, start, page_len, filters):
    order = frappe.db.sql(""" select a1.name from `tabPurchase Order` a1 left join `tabOutward Gate Pass` a2 on a1.name = a2.purchase_order where a1.docstatus=1 and a1.name not in (select purchase_order from `tabOutward Gate Pass` ) """,  as_dict=1)
    return order