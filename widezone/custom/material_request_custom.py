# Copyright (c) 2015, Lucrumerp Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate, nowdate

def validate(self, method, for_validate=False):
    num = 0
    self.check_approval = 0
    self.item_group = ''
    for items in self.items:

        check = frappe.db.sql(""" select a2.name, a2.is_group from `tabItem` a1 inner join `tabItem Group` a2 on a1.item_group = a2.name where a1.name = %(item)s """, {"item": items.item_code}, as_dict=1)
    
        if check[0].is_group == 1 and self.item_group=='':

            self.check_approval = 1
            self.item_group = check[0].name
            num = num+1
        elif check[0].is_group == 1 and self.item_group!='':
            if self.item_group == check[0].name:
                
                self.check_approval = 1
                self.item_group = check[0].name
                num = num+1
            else:

                frappe.throw(_("Not Allowed to enter more than 1 item of different item group"))