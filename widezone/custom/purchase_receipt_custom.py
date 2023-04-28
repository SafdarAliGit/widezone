# Copyright (c) 2015, Lucrumerp Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from collections import defaultdict
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate, nowdate

def validate(self, method):
    if self.is_subcontracted == 'Yes':
        self.purchase_orders = []

        if self.doctype == "Purchase Order":
            return

        self.purchase_orders = [d.purchase_order for d in self.items if d.purchase_order]

        print(self.purchase_orders)
