

frappe.ui.form.on("Sales Order", {
	refresh: function(frm){
		if(frm.doc.docstatus == 0){
			frm.add_custom_button("Add Variants", function(){
				frm.trigger("add_multiple_variants");
			}).addClass("btn-primary");
		}
	},
	add_multiple_variants: function(frm){
		var multiple_variant_dialog = new frappe.ui.Dialog({
				title: __("Select Template and Variants"),
				fields: [
					{
						label: __("Variant"),
						fieldtype: "Link",
						fieldname: "item_template",
						options: "Item",
						reqd: 1,
						get_query: function(){
							return {
								filters: {
									has_variants: 1
								}
							}
						},
						onchange: function(){
							var item_template = multiple_variant_dialog.get_value("item_template");
							frappe.call({
								method: "frappe.client.get_list",
								args: {
									doctype: "Item Variant Attribute",
									filters: [
										["parent","=",item_template]
									],
									fields: ["*"],
									limit_page_length: 0,
									parent: "Item",
									order_by: "idx"
								}
							}).then((r) => {
								if(r.message) {
									multiple_variant_dialog.$body.find(".row.form-section:not(.visible-section)").remove();
									multiple_variant_dialog.disable_primary_action();
									multiple_variant_dialog.get_primary_btn().html("Select Variant");
									show_multiple_variants_dialog(frm, r.message, multiple_variant_dialog);
								}
							});
						}
					}
				]
			});

			multiple_variant_dialog.set_primary_action(__('Select Variants'), () => {
				let selected_attributes = get_selected_attributes(multiple_variant_dialog);
				multiple_variant_dialog.hide();
				frappe.call({
					method: "widezone.custom.sales_order_custom.add_or_make_variants",
					args: {
						"item": multiple_variant_dialog.get_value("item_template"),
						"args": selected_attributes
					},
					freeze: true,
					callback: function(r) {
						var already_added_items = [];
						$.each(frm.doc.items || [], function(i,v){
							already_added_items.push(v.item_code);
						});
						$.each(r.message || [], function(i,v){
							if(!already_added_items.includes(v)){
								var child = {};
								var doc = frm.add_child("items", child);
								frappe.model.set_value(doc.doctype, doc.name, "item_code", v);
							}
						});
						frm.refresh_field("items");
						frappe.show_alert({
							message: __("{0} variants added.", [r.message]),
							indicator: 'green'
						});
					}
				});
			});

			$($(multiple_variant_dialog.$wrapper.find('.form-column'))
				.find('.frappe-control')).css('margin-bottom', '0px');

			multiple_variant_dialog.disable_primary_action();
			multiple_variant_dialog.clear();
			multiple_variant_dialog.show();
	}
});

var show_multiple_variants_dialog = function(frm, attributes, multiple_variant_dialog) {

	let promises = [];
	let attr_val_fields = {};

	function make_fields_from_attribute_values(attr_dict) {
		let fields = [];
		Object.keys(attr_dict).forEach((name, i) => {
			if(i % 3 === 0){
				fields.push({fieldtype: 'Section Break'});
			}
			fields.push({fieldtype: 'Column Break', label: name});
			attr_dict[name].forEach(value => {
				fields.push({
					fieldtype: 'Check',
					label: value,
					fieldname: value,
					default: 0,
					onchange: function() {
						let selected_attributes = get_selected_attributes(multiple_variant_dialog);
						let lengths = [];
						Object.keys(selected_attributes).map(key => {
							lengths.push(selected_attributes[key].length);
						});
						if(lengths.includes(0)) {
							multiple_variant_dialog.get_primary_btn().html(__('Create Variants'));
							multiple_variant_dialog.disable_primary_action();
						} else {

							let no_of_combinations = lengths.reduce((a, b) => a * b, 1);
							let msg;
							if (no_of_combinations === 1) {
								msg = __("Add {0} Variant", [no_of_combinations]);
							} else {
								msg = __("Add {0} Variants", [no_of_combinations]);
							}
							multiple_variant_dialog.get_primary_btn().html(msg);
							multiple_variant_dialog.enable_primary_action();
						}
					}
				});
			});
		});
		return fields;
	}

	attributes.forEach(function(d) {
		let p = new Promise(resolve => {
			if(!d.numeric_values) {
				frappe.call({
					method: "frappe.client.get_list",
					args: {
						doctype: "Item Attribute Value",
						filters: [
							["parent","=", d.attribute]
						],
						fields: ["attribute_value"],
						limit_page_length: 0,
						parent: "Item Attribute",
						order_by: "idx"
					}
				}).then((r) => {
					if(r.message) {
						attr_val_fields[d.attribute] = r.message.map(function(d) { return d.attribute_value; });
						resolve();
					}
				});
			} else {
				frappe.call({
					method: "frappe.client.get",
					args: {
						doctype: "Item Attribute",
						name: d.attribute
					}
				}).then((r) => {
					if(r.message) {
						const from = r.message.from_range;
						const to = r.message.to_range;
						const increment = r.message.increment;

						let values = [];
						for(var i = from; i <= to; i = flt(i + increment, 6)) {
							values.push(i);
						}
						attr_val_fields[d.attribute] = values;
						resolve();
					}
				});
			}
		});

		promises.push(p);

	}, this);

	Promise.all(promises).then(() => {
		let fields = make_fields_from_attribute_values(attr_val_fields);
		multiple_variant_dialog.add_fields(fields);
	})

};

var get_selected_attributes = function(multiple_variant_dialog) {
		let selected_attributes = {};
		multiple_variant_dialog.$wrapper.find('.form-column').each((i, col) => {
			if(i===0) return;
			let attribute_name = $(col).find('label').html().trim();
			selected_attributes[attribute_name] = [];
			let checked_opts = $(col).find('.checkbox input');
			checked_opts.each((i, opt) => {
				if($(opt).is(':checked')) {
					selected_attributes[attribute_name].push($(opt).attr('data-fieldname'));
				}
			});
		});

		return selected_attributes;
}