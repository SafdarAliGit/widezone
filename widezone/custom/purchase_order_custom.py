# Copyright (c) 2015, Lucrumerp Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate, nowdate

def validate(self, method):
    
    if self.workflow_state == 'Pending':
        self.workflow_prepared_by = frappe.session.user
    elif self.workflow_state == 'Acknowledged':
        self.workflow_acknowledge_by = frappe.session.user
    elif self.workflow_state == 'Reject':
        self.workflow_rejected_by = frappe.session.user
    elif self.workflow_state == 'Approved':
        self.workflow_approved_by = frappe.session.user

def submit(self, method):
    
    if self.workflow_state == 'Approved':
        self.workflow_approved_by = frappe.session.user


@frappe.whitelist()
def make_stock_entry(source_name):
    source_name = frappe.get_doc("Purchase Order", source_name)
    print(source_name)
    doc = frappe.new_doc("Stock Entry")

    doc.purchase_order = source_name.name
    doc.stock_entry_type = 'Send to Subcontractor'
    doc.purpose = 'Send to Subcontractor'
    doc.to_warehouse = source_name.supplier_warehouse
    doc.mrp_no = source_name.mrp_no
        
    return doc

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_warehouse(doctype, txt, searchfield, start, page_len, filters):
    if isinstance(filters, str):
        filters = json.loads(filters)

    warehouse = frappe.db.sql("""select a1.name from `tabWarehouse` a1 left join `tabSupplier Warehouses` a2 on a1.name = a2.warehouse left join `tabSupplier` a3 on a2.parent = a3.name
		where (a1.name like %(txt)s)	and a3.name = %(supplier)s		
		order by
			if(locate(%(_txt)s, a1.name), locate(%(_txt)s, a1.name), 99999),
			a1.idx desc,
			a1.name
		limit %(start)s, %(page_len)s""".format(**{
        'key': searchfield
    }), {
                                   'txt': "%%%s%%" % txt,
                                   '_txt': txt.replace("%", ""),
                                   'start': start,
                                   'page_len': page_len,
                                   'supplier': filters.get('supplier')

                               })
    return warehouse

