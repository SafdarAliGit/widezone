
frappe.ui.form.on('Inward Gate Pass', {
	setup: function(frm) {
		frm.set_query("purchase_order", function(){
			return {
				filters: {
					docstatus: 1,
					supplier: frm.doc.supplier
				}
			}
		});
	},
    
});
