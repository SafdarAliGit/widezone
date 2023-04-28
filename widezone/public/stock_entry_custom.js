frappe.ui.form.on("Stock Entry",{
    refresh: function(frm) {
        if(frm.doc.docstatus==1 && frm.doc.stock_entry_type=='Send to Subcontractor')
		{
			cur_frm.add_custom_button(__('OGP'), function() {
				frm.trigger("make_ogp");
			},
				__('Create'))
		}
        frm.set_query("subcontracted_item", "items", function(frm, cdt, cdn){
            console.log(frm.purchase_order)
			var child = locals[cdt][cdn];
			return {
				query: "widezone.custom.stock_entry_custom.get_subContracting_items",
				filters: {
					order: frm.purchase_order,
				}
			}
		});
			frm.set_query("item_code", "items", function(frm, cdt, cdn){
				console.log(frm.stock_entry_type)
				var child = locals[cdt][cdn];
				console.log(child.s_warehouse)
				if(frm.stock_entry_type == 'Material Issue')	{
				return {
					query: "widezone.custom.stock_entry_custom.get_balance_qty",
					filters: {
						s_warehouse: child.s_warehouse,
					}
				}
				}
			});
    },
	make_ogp: function(frm) {
		frappe.call({
			method: 'widezone.custom.stock_entry_custom.make_ogp',
			args: {
				'source_name': frm.doc.name
			},
			callback: function(r) {
				if (!r.exc) {
					console.log(r);
					frappe.model.sync(r.message);
					frappe.set_route("Form", r.message.doctype, r.message.name);
				}
			}
		});
	},

})

frappe.ui.form.on("Stock Entry Detail",{
    "item_code":function(frm,cdt,cdn){
        var doc = locals[cdt][cdn]
		if(frm.stock_entry_type != 'Material Issue')	{
			frappe.call({
				method: "widezone.custom.stock_entry_custom.get_warehouse",
				args: {
					"item": doc.item_code,
					"company":frm.doc.company
				},
				callback: function (r) {
					frappe.model.set_value(cdt,cdn,"s_warehouse",r.message)
				}
			});
		}
    }
	

})