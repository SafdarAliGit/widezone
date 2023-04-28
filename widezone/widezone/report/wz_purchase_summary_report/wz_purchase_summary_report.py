# Copyright (c) 2013, Lucrumerp Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import flt


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	columns = [



		{
			"label": _("Material Request Date"),
			"fieldname": "material_request_date",
			"fieldtype": "Date",
			"width": 140
		},
		{
			"label": _("WZ No"),
			# "options": "Purchase Order",
			"fieldname": "mrp_no",
			"fieldtype": "Data",
			"width": 140
		},
		{
			"label": _("Material Request No"),
			"options": "Material Request",
			"fieldname": "material_request_no",
			"fieldtype": "Link",
			"width": 140
		},
		{
			"label": _("Purpose"),
			"options": "",
			"fieldname": "material_request_type",
			"fieldtype": "Data",
			"width": 140
		},
		{
			"label": _("Cost Center"),
			"options": "Cost Center",
			"fieldname": "cost_center",
			"fieldtype": "Link",
			"width": 140
		},
		{
			"label": _("Requesting Site"),
			"options": "Warehouse",
			"fieldname": "requesting_site",
			"fieldtype": "Link",
			"width": 140
		},
		{
			"label": _("Requestor"),
			"options": "Employee",
			"fieldname": "requestor",
			"fieldtype": "Link",
			"width": 140
		},
		{
			"label": _("Item"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150
		},
		{
			"label": _("Quantity"),
			"fieldname": "quantity",
			"fieldtype": "Float",
			"width": 140
		},
		{
			"label": _("PO QTY"),
			"fieldname": "po_quantity",
			"fieldtype": "Float",
			"width": 140
		},
		{
			"label": _("PR Quantity"),
			"fieldname": "pr_quantity",
			"fieldtype": "Float",
			"width": 140
		},
		{
			"label": _("Unit of Measure"),
			"options": "UOM",
			"fieldname": "unit_of_measurement",
			"fieldtype": "Link",
			"width": 140
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "data",
			"width": 140
		},
		{
			"label": _("Purchase Order Date"),
			"fieldname": "purchase_order_date",
			"fieldtype": "Date",
			"width": 140
		},
		{
			"label": _("Purchase Order"),
			"options": "Purchase Order",
			"fieldname": "purchase_order",
			"fieldtype": "Link",
			"width": 140
		},
		{
			"label": _("Supplier"),
			"options": "Supplier",
			"fieldname": "supplier",
			"fieldtype": "Link",
			"width": 140
		},
		{
			"label": _("Estimated Cost"),
			"fieldname": "estimated_cost",
			"fieldtype": "Float",
			"width": 140
		},
		{
			"label": _("Actual Cost"),
			"fieldname": "actual_cost",
			"fieldtype": "Float",
			"width": 140
		},
		{
			"label": _("Purchase Order Amount"),
			"fieldname": "purchase_order_amt",
			"fieldtype": "Float",
			"width": 140
		},
		{
			"label": _("Expected Delivery Date"),
			"fieldname": "expected_delivery_date",
			"fieldtype": "Date",
			"width": 140
		},
		{
			"label": _("Actual Delivery Date"),
			"fieldname": "actual_delivery_date",
			"fieldtype": "Date",
			"width": 140
		},
		{
			"label": _("Purchase invocie no"),
			"options": "Purchase Invoice",
			"fieldname": "parent",
			"fieldtype": "Data",
			"width": 140
		},

		{
			"label": _("Supplier"),
			"options": "Purchase Invoice",
			"fieldname": "supplier",
			"fieldtype": "Data",
			"width": 140
		},
		{
			"label": _("PINV.Qty"),
			# "options": "Purchase Invoice",
			"fieldname": "quantity",
			"fieldtype": "Data",
			"width": 140
		},
		{
			"label": _("PINV. Amount"),
			# "options": "Purchase Invoice",
			"fieldname": "purchase_invoice_amt",
			"fieldtype": "Data",
			"width": 140
		},

	]
	return columns

def get_conditions(filters):
	conditions = ""

	if filters.get("company"):
		conditions += " AND parent.company=%s" % frappe.db.escape(filters.get('company'))

	# if filters.get("cost_center") or filters.get("project"):
	# 	conditions += """
	# 		AND (child.`cost_center`=%s OR child.`project`=%s)
	# 		""" % (frappe.db.escape(filters.get('cost_center')), frappe.db.escape(filters.get('project')))

	if filters.get("name"):
		conditions += " AND child.mrp_no='%s'" % filters.get('name')

	# if filters.get("from_date"):
	# 	conditions += " AND parent.transaction_date>='%s'" % filters.get('from_date')
	#
	# if filters.get("to_date"):
	# 	conditions += " AND parent.transaction_date<='%s'" % filters.get('to_date')

	# child_warehouses = frappe.get_list("Warehouse", filters={"parent_warehouse": filters.get("parent_warehouse"), "is_group": 0})
	# child_warehouses_in = ""
	# if child_warehouses and not filters.get("child_warehouse"):
	# 	child_warehouses_in = [a.name for a in child_warehouses]
	# 	conditions += " and child.warehouse in ('" + "','".join(child_warehouses_in) + "')"
	#
	# if filters.get("child_warehouse"):
	# 	conditions += " and child.warehouse in ('" + "','".join(filters["child_warehouse"]) + "')"

	return conditions


def get_data(filters):
	conditions = get_conditions(filters)
	purchase_order_entry = get_po_entries(conditions)
	purchase_invoice_entry = get_si_entries(conditions)

	mr_records, procurement_record_against_mr = get_mapped_mr_details(conditions)
	pr_records = get_mapped_pr_records()
	pi_records = get_mapped_pi_records()

	procurement_record=[]
	if procurement_record_against_mr:
		procurement_record += procurement_record_against_mr
	for po in purchase_order_entry:
		# fetch material records linked to the purchase order item
		mr_record = mr_records.get(po.material_request_item, [{}])[0]
		pr_record = pr_records.get(po.name, [{}])[0]
		procurement_detail = {
			# "material_request_date": mr_record.get('transaction_date'),
			"material_request_type": mr_record.get('material_request_type'),
			"mrp_no": mr_record.get('mrp_no'),
			"cost_center": po.cost_center,
			"project": po.project,
			"requesting_site": po.warehouse,
			"requestor": po.owner,
			"material_request_no": po.material_request,
			"item_code": po.item_code,
			"quantity": flt(mr_record.get('qty')) if mr_record.get('qty') else 0,
			"po_quantity": flt(po.qty) if po.qty else 0,
			"pr_quantity": flt(pr_record.get("qty")) if pr_record.get("qty") else 0,
			"unit_of_measurement": po.stock_uom,
			"status": po.status,
			# "purchase_order_date": po.transaction_date,
			"purchase_order": po.parent,
			"supplier": po.supplier,
			"estimated_cost": flt(mr_record.get('amount')),
			"actual_cost": flt(pi_records.get(po.name)),
			"purchase_order_amt": flt(po.amount),
			"purchase_order_amt_in_company_currency": flt(po.base_amount),
			"expected_delivery_date": po.schedule_date,
			"actual_delivery_date": pr_record.get("posting_date")
		}
		procurement_record.append(procurement_detail)
	return procurement_record

	si_record = []
	# if procurement_record_against_mr:
	si_record += procurement_record_against_mr
	for si in purchase_invoice_entry:
		# fetch material records linked to the purchase order item
		mr_record = mr_records.get(si.purchase_order, [{}])[0]
		pr_record = pr_records.get(si.po_detail, [{}])[0]
		si_detail = {
			"material_request_type": mr_record.get('material_request_type'),
			"mrp_no": mr_record.get('mrp_no'),
			"cost_center": si.cost_center,
			"project": si.project,
			"requesting_site": si.warehouse,
			"requestor": si.owner,
			"material_request_no": si.material_request,
			"item_code": si.item_code,
			"pi_qty": flt(mr_record.get('qty')) if mr_record.get('qty') else 0,
			"po_quantity": flt(si.qty) if si.qty else 0,
			"pr_quantity": flt(pr_record.get("qty")) if pr_record.get("qty") else 0,
			"unit_of_measurement": si.stock_uom,
			"status": si.status,
			"purchase_invoice": si.name,
			"supplier": si.supplier,
			"estimated_cost": flt(mr_record.get('amount')),
			"actual_cost": flt(pi_records.get(si.name)),
			"purchase_invoice_amt": flt(si.amount),
			"purchase_order_amt_in_company_currency": flt(si.base_amount),
			"expected_delivery_date": si.schedule_date,
			"actual_delivery_date": pr_record.get("posting_date")
		}
		si_record.append(si_detail)
		print(f"--------------{si_record}---------------")
	return si_record

def get_mapped_mr_details(conditions):
	mr_records = {}
	mr_details = frappe.db.sql("""
		SELECT
			# parent.transaction_date,
			parent.material_request_type,
			child.mrp_no,
			parent.per_ordered,
			parent.owner,
			child.name,
			child.parent,
			child.warehouse,
			child.amount,
			child.qty,
			child.item_code,
			child.uom,
			parent.status,
			child.project,
			child.cost_center,
			child.ordered_qty
		FROM `tabMaterial Request` parent, `tabMaterial Request Item` child
		WHERE
			parent.per_ordered>=0
			AND parent.name=child.parent
			# AND parent.docstatus=1
			{conditions}
		""".format(conditions=conditions), as_dict=1) #nosec

	procurement_record_against_mr = []
	for record in mr_details:
		if record.per_ordered and record.ordered_qty:
			mr_records.setdefault(record.name, []).append(frappe._dict(record))
		else:
			procurement_record_details = dict(
				# material_request_date=record.transaction_date,
				material_request_no=record.parent,
				material_request_type=record.material_request_type,
				po_quantity=0,
				pr_quantity=0,
				requesting_site=record.warehouse,
				requestor=record.owner,
				item_code=record.item_code,
				estimated_cost=flt(record.amount),
				quantity=flt(record.qty),
				unit_of_measurement=record.uom,
				status=record.status,
				actual_cost=0,
				purchase_order_amt=0,
				purchase_order_amt_in_company_currency=0,
				project = record.project,
				cost_center = record.cost_center,
				mrp_no = record.mrp_no
			)
			procurement_record_against_mr.append(procurement_record_details)
	return mr_records, procurement_record_against_mr

def get_mapped_pi_records():
	return frappe._dict(frappe.db.sql("""
		SELECT
			pi_item.po_detail,
			sum(pi_item.base_amount) as base_amount
		FROM `tabPurchase Invoice Item` as pi_item
		INNER JOIN `tabPurchase Order` as po
		ON pi_item.`purchase_order` = po.`name`
		WHERE
			# pi_item.docstatus = 1 AND
			po.status not in ("Cancelled")
			AND pi_item.po_detail IS NOT NULL
		GROUP BY
			pi_item.po_detail
		"""))

def get_mapped_pr_records():
	pr_records_dict = {}
	pr_records = frappe.db.sql("""
		SELECT
			pr_item.purchase_order_item,
			MAX(pr.posting_date) as posting_date,
			sum(pr_item.qty) as qty
		FROM `tabPurchase Receipt` pr, `tabPurchase Receipt Item` pr_item
		WHERE
			pr.docstatus=1
			AND pr.name=pr_item.parent
			AND pr_item.purchase_order_item IS NOT NULL
			AND pr.status not in  ("Cancelled")
		GROUP BY
			pr_item.purchase_order_item
		""", as_dict=True)
	for record in pr_records:
		pr_records_dict.setdefault(record.purchase_order_item, []).append(frappe._dict(record))
	return pr_records_dict

def get_po_entries(conditions):
	return frappe.db.sql("""
		SELECT
			child.name,
			child.parent,
			child.cost_center,
			child.mrp_no,
			child.project,
			child.warehouse,
			child.material_request,
			child.material_request_item,
			child.item_code,
			child.stock_uom,
			child.qty,
			child.amount,
			child.base_amount,
			child.schedule_date,
			# parent.transaction_date,
			parent.supplier,
			parent.status,
			parent.owner
		FROM `tabPurchase Order` parent, `tabPurchase Order Item` child
		WHERE
			# parent.docstatus = 1 AND
			parent.name = child.parent
			AND parent.status not in  ("Cancelled")
			{conditions}
		""".format(conditions=conditions), as_dict=1) #nosec

def get_si_entries(conditions):
	return frappe.db.sql("""
		SELECT
			child.name,
			# parent.transaction_date,
			child.parent,
			child.cost_center,
			child.mrp_no,
			child.project,
			child.warehouse,
			child.item_code,
			child.stock_uom,
			child.qty,
			child.amount,
			child.base_amount,
			parent.supplier,
			parent.status,
			parent.owner
		FROM `tabPurchase Invoice` parent, `tabPurchase Invoice Item` child
		# ,`tabPurchase Order Item` poitem
		WHERE
			# parent.docstatus = 1 AND
			parent.name = child.parent
			AND parent.status not in  ("Cancelled") 
			# AND child.po_detail=poitem.name
		""".format(), as_dict=1) #nosec
