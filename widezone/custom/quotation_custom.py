# Copyright (c) 2015, Lucrumerp Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate, nowdate
from lucrum.controllers.accounts_controller import get_taxes_and_charges

from lucrum.controllers.selling_controller import SellingController

def validate(self, method, for_validate=False):
    pass
	# fitting_charges = True
	# delivery_charges = True
	# for d in self.taxes:
	# 	if self.get("fitting_charges") and d.template == self.get("fitting_charges"):
	# 		fitting_charges = False
	# 	if self.get("delivery_charges") and d.template == self.get("delivery_charges"):
	# 		delivery_charges = False
	# if self.get('fitting_charges') and fitting_charges:
	# 	taxes = get_taxes_and_charges('Sales Taxes and Charges Template', self.fitting_charges)
	# 	for tax in taxes:
	# 		tax['template'] = self.get('fitting_charges')
	# 		self.append('taxes', tax)
	# if self.get('delivery_charges') and delivery_charges:
	# 	taxes = get_taxes_and_charges('Sales Taxes and Charges Template', self.delivery_charges)
	# 	for tax in taxes:
	# 		tax['template'] = self.get('delivery_charges')
	# 		self.append('taxes', tax)

	# self.run_method("calculate_taxes_and_totals")

@frappe.whitelist()
def get_attributes(item):
	item = frappe.get_doc("Item", item)
	return item.attributes

@frappe.whitelist()
def make_production_form(source_name):
	source_name = frappe.get_doc("Quotation", source_name)
	doc = frappe.new_doc("Production Form")
	
	doc.customer = source_name.party_name
	doc.quotation = source_name.name
	for items in source_name.items:
		it = doc.append("template", {})
		it.item = items.item_template
		it.qty = 1
		
	return doc