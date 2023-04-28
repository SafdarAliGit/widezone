frappe.ui.form.on('Outward Gate Pass',{
    refresh:function(frm){

        frm.set_query('transporter', function (doc) {
			return {
				query: "widezone.custom.outward_gatepass_custom.get_transporter",
				filters: {

				}
			}
		});
    },
	setup: function(frm) {
		frm.set_query("purchase_order", function(){
			return {
				// query:"widezone.custom.outward_gatepass_custom.get_purchase_order",
				filters: {
					docstatus: 1,
					supplier: frm.doc.supplier,
				}
			}
		});
	},
	onload:function(frm){
		if(frm.doc.items.length>0 && frm.doc.docstatus!=1){
			var table = frm.doc.items
			var total =0
			table.forEach(item => {
				total+=item.qty
			});
			frm.set_value("total_qty",total)
		}
	},
	get_po_items:function(frm,cdt,cdn){
		frappe.call({
			method: "widezone.custom.outward_gatepass_custom.get_po_items",
			args: {
				'doc': frm.doc.purchase_order
			},
			callback: function (r) {
				cur_frm.clear_table("items");
				if(r.message=='No data found')	{
					cur_frm.refresh_fields("items");
					frappe.msgprint(__("No Stock entry present against PO {0}", [frm.doc.purchase_order]))
				}	else{
					r.message.items.forEach(function f(element) {
						var childTable = cur_frm.add_child("items");
						childTable.item_code=element['item_code'];
						childTable.item_name=element['item_name'];
						childTable.qty=element['qty'];
						childTable.uom=element['uom'];
						cur_frm.refresh_fields("items");
					});
				}
			}
		})
	}
})

frappe.ui.form.on('OGP Items',{
    qty:function(frm,cdt,cdn){
		var table = frm.doc.items
		var total = 0
		table.forEach(item => {
			total+=item.qty
		});
		frm.set_value("total_qty",total)
    }
})
