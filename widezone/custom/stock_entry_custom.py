import frappe
from frappe import _

@frappe.whitelist()
def get_warehouse(item,company):
    if item and company:
        item_doc = frappe.get_doc("Item",item)
        for default in item_doc.item_defaults:
            if default.company == company:
                return default.default_warehouse


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_subContracting_items(doctype, txt, searchfield, start, page_len, filters):
    cond = ""
    if isinstance(filters, str):
        filters = json.loads(filters)
    
    fields = "name"
    searchfields = "name"

    transporter = frappe.db.sql("""select a1.name,a1.item_name from `tabItem` a1 inner join `tabPurchase Order Item` a2 on a1.item_code = a2.item_code where (a1.name like %(txt)s)	and  a2.parent = %(order)s order by
			if(locate(%(_txt)s, a1.name), locate(%(_txt)s, a1.name), 99999),
			a1.name asc
		limit {start}, {page_len}""".format(
			fields=", ".join(["`tabItem`.{0}".format(f) for f in fields]),
			cond=cond,
			scond=searchfields,
			start=start,
			page_len=page_len,
			key=searchfields
		), {
                                   'txt': "%%%s%%" % txt,
                                   '_txt': txt.replace("%", ""),
                                   'start': start,
                                   'page_len': page_len,
                                   'order': filters.get("order"),

                               })
    return transporter

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_balance_qty(doctype, txt, searchfield, start, page_len, filters):
    cond = ""
    if isinstance(filters, str):
        filters = json.loads(filters)
    
    fields = "name"
    searchfields = "name"
    balance_items = frappe.db.sql(
		"""select a2.name,a2.item_name from `tabStock Ledger Entry` a1 inner join `tabItem` a2 on a1.item_code = a2.name
		where a1.warehouse=%(s_warehouse)s and a1.is_cancelled=0 and a1.qty_after_transaction>0 and (a2.name like %(txt)s)
		order by
			if(locate(%(_txt)s, a2.name), locate(%(_txt)s, a2.name), 99999),
			a2.name asc
		limit {start}, {page_len}""".format(
			fields=", ".join(["`tabItem`.{0}".format(f) for f in fields]),
			cond=cond,
			scond=searchfields,
			start=start,
			page_len=page_len,
			key=searchfields
		),{
                                   'txt': "%%%s%%" % txt,
                                   '_txt': txt.replace("%", ""),
                                   'start': start,
                                   'page_len': page_len,
                                   's_warehouse': filters.get("s_warehouse"),

                               })
    return balance_items


@frappe.whitelist()
def make_ogp(source_name):
    source_name = frappe.get_doc("Stock Entry", source_name)
    print(source_name)
    doc = frappe.new_doc("Outward Gate Pass")

    doc.good_dispatched_type = 'Sub Contracting'
    doc.supplier = source_name.supplier
    doc.mrp_no = source_name.mrp_no
    doc.purchase_order = source_name.purchase_order


    for items in source_name.items:
        it = doc.append("items", {})
        it.item_code = items.item_code
        it.item_name = items.item_name
        it.uom = items.uom
        it.qty = items.qty
        
    return doc
