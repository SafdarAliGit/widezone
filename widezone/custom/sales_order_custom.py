
from __future__ import unicode_literals

import frappe
from six import string_types
import json
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate, nowdate, date_diff
from lucrum.controllers.item_variant import (
    generate_keyed_value_combinations,
    get_variant,
    create_variant
)

def validate(self,method):
    if self.transaction_date and self.ex_factory_date and self.delivery_date:
        
        if self.ex_factory_date<self.transaction_date:
            frappe.throw(_("Ex-Factory Date "+self.ex_factory_date+" cannot be earlier then document posting date "+self.transaction_date))
        if self.ex_factory_date>self.delivery_date:
            frappe.throw(_("Ex-Factory Date "+self.ex_factory_date+" cannot be after delivery date "+self.delivery_date))

@frappe.whitelist()
def add_or_make_variants(item, args):
    count = 0
    if isinstance(args, string_types):
        args = json.loads(args)

    args_set = generate_keyed_value_combinations(args)
    variants = []
    for attribute_values in args_set:
        variant_name = get_variant(item, args=attribute_values)
        if not variant_name:
            variant = create_variant(item, attribute_values)
            variant.save()
            variant_name = variant.name
            #frappe.db.commit()
            count += 1
        variants.append(variant_name)

    return variants