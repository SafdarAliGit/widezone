# Copyright (c) 2023, LucrumERP and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import nowdate
from frappe.model.document import Document

class ManufacturingSheetWidezone(Document):
	pass

@frappe.whitelist()
def check_attributes(size,color,department,composition):
	attribtes = {"Size":size, "Colour":color, "Department":department, "Composition":composition}
	for k, v  in enumerate(attribtes):
		print(k)
		print(v)
		# doc = frappe.db.sql(""" select * from `tabItem Attribute Value` where parent = %(parent)s and attribute_value = %(value)s """, {"parent":k, "value":v}, as_dict=1)
		
		# if doc:
		# 	print("para hai")
		# else:
		# 	check = frappe.get_doc("Item Attribute", "k")
			
		# 	if check.value_type == 'Alpha' and (v.isnumeric() == True):
		# 		frappe.throw(_("Please enter only Alphabets on {0} Value field").format(v))
		# 	if check.value_type == 'Numeric' and (v.isnumeric() == False):
		# 		frappe.throw(_("Please enter only Alphabets on {0} Value field").format(v))
		# 	total = len(check.item_attribute_values)
		# 	item_attribute = frappe.new_doc("Item Attribute Value")
		# 	item_attribute.parent = "k"
		# 	item_attribute.parenttype = "Item Attribute"
		# 	item_attribute.parentfield = "item_attribute_values"
		# 	item_attribute.attribute_value = v
		# 	item_attribute.abbr = v.upper()
		# 	item_attribute.idx = total+1
		# 	item_attribute.save()

@frappe.whitelist()
def make_sheet_planing(source_name):
	source_name = frappe.get_doc("Manufacturing Sheet Widezone", source_name)
	doc = frappe.new_doc("Manufacturing Planing Sheet")
	
	for items in source_name.items:
		it = doc.append("items", {})
		it.template = items.template
		it.colour = items.colour
		it.size = items.size
		it.item = items.item
		it.order_quantity = items.order_quantity
		it.plan_quantity = items.plan_quantity
	
	for items in source_name.fabric_calculation:
		it = doc.append("fabric_calculation", {})
		it.body_parts = items.body_parts
		it.fabric_template = items.fabric_template
		it.composition = items.composition
		it.quality = items.quality
		it.fabric_item = items.fabric_item
		it.gsm = items.gsm
		it.consumption = items.consumption

	for items in source_name.fabric_extra:
		it = doc.append("fabric_extra", {})
		it.body_parts = items.body_parts
		it.colour = items.colour
		it.fabric_item = items.fabric_item
		it.production_quntity = items.production_quntity
		it.total_fabric = items.total_fabric
		
	for items in source_name.knitting_plan:
		it = doc.append("knitting_plan", {})
		it.fabric_type = items.fabric_type
		it.required_qty = items.required_qty
		
	for items in source_name.yarn_plan:
		it = doc.append("yarn_plan", {})
		it.fabric_item = items.fabric_item
		it.yarn_template = items.yarn_template
		it.composition = items.composition
		it.required_fabric = items.required_fabric
		it.ratio = items.ratio
		it.yarn_bag = items.yarn_bag
		it.actual_yarn_requirement = items.actual_yarn_requirement
		it.yarn_in_bag = items.yarn_in_bag
		
	for items in source_name.accesories:
		it = doc.append("accesories", {})
		it.item_template = items.item_template
		it.item_code = items.item_code
		it.quality = items.quality
		it.color = items.color
		it.operations = items.operations
		it.finish_item_quantity = items.finish_item_quantity
		it.consumption_per_price = items.consumption_per_price
		it.total_required = items.total_required
		
	for items in source_name.packing:
		it = doc.append("packing", {})
		it.item_template = items.item_template
		it.item_code = items.item_code
		it.quality = items.quality
		it.color = items.color
		it.operations = items.operations
		it.finish_item_quantity = items.finish_item_quantity
		it.consumption_per_price = items.consumption_per_price
		it.total_required = items.total_required
		
	for items in source_name.merchandizer_info:
		it = doc.append("merchandizer_info", {})
		it.pak_merchandizer = items.pak_merchandizer
		it.senior_merchandizer = items.senior_merchandizer
		it.comments = items.comments
		
	return doc


@frappe.whitelist()
def make_material_resource_planing(source_name):
	source_name = frappe.get_doc("Manufacturing Sheet Widezone", source_name)
	mrp_doc = frappe.new_doc("Material Resource Planing")

	# for items in source_name:
	mrp_doc.get_items_from ="MFG Sheet Widezone"
	mrp_doc.mfg_sheet_no =source_name.name

	for items in source_name.items:
		it = mrp_doc.append("po_items", {})
		it.item_code = items.template
		it.planned_start_date = nowdate()
		it.planned_qty = items.order_quantity


	for items in source_name.yarn_plan:
		it = mrp_doc.append("yarn_material", {})
		it.fabric_code = items.fabric_item
		it.yarn_code = items.yarn_template
		it.composition = items.composition
		it.fabric_qty = items.required_fabric
		it.planned_qty = items.yarn_in_bag
		it.blending_ratio = items.ratio
		it.qty = items.actual_yarn_requirement
		it.qty_in_bags = items.yarn_bag
		it.request_date = nowdate()

	for items in source_name.accesories:
		it = mrp_doc.append("accessory_material", {})
		it.item_template = items.item_template
		it.item_code = items.item_code
		it.qty = items.quality
		it.operation = items.operations
		it.request_date = nowdate()

	for items in source_name.packing:
		it = mrp_doc.append("mrp_packing_material", {})
		it.item_template = items.item_template
		it.item_code = items.item_code
		it.qty = items.quality
		it.operation = items.operations
		it.request_date = nowdate()

	return mrp_doc
