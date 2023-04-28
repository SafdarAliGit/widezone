frappe.ui.form.on("Purchase Order",{
    refresh: function(frm) {
        if(frm.doc.docstatus==1 && frm.doc.is_subcontracted=='Yes')
		{
			cur_frm.add_custom_button(__('Stock Entry'), function() {
				frm.trigger("make_stock_entry");
			},
				__('Create'))
		}

		frm.set_query("supplier_warehouse", function(){
			return {
				query:"widezone.custom.purchase_order_custom.get_warehouse",
				filters: {
					supplier: frm.doc.supplier,
				}
			}
		});
    },
	make_stock_entry: function(frm) {
		frappe.call({
			method: 'widezone.custom.purchase_order_custom.make_stock_entry',
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