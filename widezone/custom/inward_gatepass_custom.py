# Copyright (c) 2015, Lucrumerp Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate, nowdate

def validate(self, method, for_validate=False):
    qty = 0
    for items in self.items:
        qty += items.qty
    self.total_qty = qty

    self.purchase_order = self.purchase_order

@frappe.whitelist()
def load_purchase_order_item(doc):
    print(doc)
    if doc:
        dn = frappe.get_doc("Purchase Order", doc)
        return dn
