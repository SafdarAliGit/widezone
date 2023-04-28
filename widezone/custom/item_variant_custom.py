# Copyright (c) 2015, Lucrumerp Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import copy
import json

import frappe
from frappe import _
from frappe.utils import cstr, flt
from six import string_types

@frappe.whitelist()
def create_variant_custom(item, args):
    if isinstance(args, string_types):
        args = json.loads(args)
    for key, value in args.items():
        
        doc = frappe.db.sql(""" select * from `tabItem Attribute Value` where parent = %(parent)s and attribute_value = %(value)s """, {"parent":key, "value":value}, as_dict=1)
        if doc:
            print("para hai")
        else:
            check = frappe.get_doc("Item Attribute", key)
            if check.value_type == 'Alpha' and (value.isnumeric() == True):
                frappe.throw(_("Please enter only Alphabets on {0} Value field").format(key))
            if check.value_type == 'Numeric' and (value.isnumeric() == False):
                frappe.throw(_("Please enter only Alphabets on {0} Value field").format(key))
            total = len(check.item_attribute_values)
            item_attribute = frappe.new_doc("Item Attribute Value")
            item_attribute.parent = key
            item_attribute.parenttype = "Item Attribute"
            item_attribute.parentfield = "item_attribute_values"
            item_attribute.attribute_value = value
            item_attribute.abbr = value.upper()
            item_attribute.idx = total+1
            item_attribute.save()

    from lucrum.controllers.item_variant import copy_attributes_to_variant
    from lucrum.controllers.item_variant import make_variant_item_code

    template = frappe.get_doc("Item", item)
    variant = frappe.new_doc("Item")
    variant.variant_based_on = "Item Attribute"
    variant_attributes = []

    for d in template.attributes:
        variant_attributes.append({"attribute": d.attribute, "attribute_value": args.get(d.attribute)})

    variant.set("attributes", variant_attributes)
    copy_attributes_to_variant(template, variant)
    make_variant_item_code(template.item_code, template.item_name, variant)

    return variant