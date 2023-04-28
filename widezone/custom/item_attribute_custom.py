# Copyright (c) 2015, Lucrumerp Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _

def validate(self, method):
    for items in self.item_attribute_values:
        print(self.value_type)
        print(items.attribute_value.isnumeric())
        if self.value_type == 'Alpha' and ((items.attribute_value).isnumeric() == True):
            frappe.throw(_("Please enter only Alphabets on Attribute Value field"))
        if self.value_type == 'Numeric' and (items.attribute_value).isnumeric() == False:
            frappe.throw(_("Please enter only Numeric on Attribute Value field"))
        if self.value_type == 'Alpha Numeric':
            pass
            

