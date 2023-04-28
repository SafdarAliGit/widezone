frappe.ui.form.on("Quotation", {
	refresh: function(frm) {
			frm.set_query('item_code', 'items', (frm, cdt, cdn) => {
				var cdoc = locals[cdt][cdn]
				if (cdoc.item_template) {
					return {
						filters: {
							variant_of: cdoc.item_template
						}
					}
				}
			});
	},
	setup: function (frm) {
		frm.set_query("item_template", "items", function () {
			return {
				filters: {
					"has_variants": 1
				}
			};
		});
	}
});
frappe.ui.form.on("Quotation Item", {
	new_variant: function (frm, cdt, cdn) {
		var row = locals[cdt][cdn];
		if(row.item_template != undefined) {
		frappe.confirm('Do you want a new variant?',
			() => {

				var attributes = [];
				var template = row.item_template;
				frappe.call({
					method: "widezone.custom.quotation_custom.get_attributes",
					args: {
						'item': template
					},
					callback: function (r) {
						if (r.message) {
							attributes = r.message;
							create_variant(attributes, frm, template);
						}
					}
				})

			}, () => {

			})
		}	else {
			frappe.msgprint(__("First select Template"));
		}
	}
});
function create_variant(attributes, frm, item) {
	var fields = []
	for (var i = 0; i < attributes.length; i++) {
		var fieldtype, desc;
		var row = attributes[i];

		if (row.numeric_values) {
			fieldtype = "Float";
			desc = "Min Value: " + row.from_range + " , Max Value: " + row.to_range + ", in Increments of: " + row.increment
		}
		else {
			fieldtype = "Data";
			desc = ""
		}
		fields = fields.concat({
			"label": row.attribute,
			"fieldname": row.attribute,
			"fieldtype": fieldtype,
			"reqd": 0,
			"description": desc
		})
	}

	var d = new frappe.ui.Dialog({
		title: __('Create Variant'),
		fields: fields
	});

	d.set_primary_action(__('Create'), function () {
		var args = d.get_values();
		if (!args) return;
		frappe.call({
			method: "lucrum.controllers.item_variant.get_variant",
			btn: d.get_primary_btn(),
			args: {
				"template": item,
				"args": d.get_values()
			},
			callback: function (r) {
				// returns variant item
				if (r.message) {
					var variant = r.message;
					frappe.msgprint_dialog = frappe.msgprint(__("Item Variant {0} already exists with same attributes",
						[repl('<a href="/app/item/%(item_encoded)s" class="strong variant-click">%(item)s</a>', {
							item_encoded: encodeURIComponent(variant),
							item: variant
						})]
					));
					frappe.msgprint_dialog.hide_on_page_refresh = true;
					frappe.msgprint_dialog.$wrapper.find(".variant-click").on("click", function () {
						d.hide();
					});
				} else {
					d.hide();
					frappe.call({
						method: "lucrum.controllers.item_variant.create_variant",
						args: {
							"item": item,
							"args": d.get_values()
						},
						callback: function (r) {
							var doclist = frappe.model.sync(r.message);
							frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
						}
					});
				}
			}
		});
	});

	d.show();

	$.each(d.fields_dict, function (i, field) {

		if (field.df.fieldtype !== "Data") {
			return;
		}

		$(field.input_area).addClass("ui-front");

		var input = field.$input.get(0);
		input.awesomplete = new Awesomplete(input, {
			minChars: 0,
			maxItems: 99,
			autoFirst: true,
			list: [],
		});
		input.field = field;

		field.$input
			.on('input', function (e) {
				var term = e.target.value;
				frappe.call({
					method: "lucrum.stock.doctype.item.item.get_item_attribute",
					args: {
						parent: i,
						attribute_value: term
					},
					callback: function (r) {
						if (r.message) {
							e.target.awesomplete.list = r.message.map(function (d) { return d.attribute_value; });
						}
					}
				});
			})
			.on('focus', function (e) {
				$(e.target).val('').trigger('input');
			})
			.on("awesomplete-open", () => {
				let modal = field.$input.parents('.modal-dialog')[0];
				if (modal) {
					$(modal).removeClass("modal-dialog-scrollable");
				}
			})
			.on("awesomplete-close", () => {
				let modal = field.$input.parents('.modal-dialog')[0];
				if (modal) {
					$(modal).addClass("modal-dialog-scrollable");
				}
			});
	});
}