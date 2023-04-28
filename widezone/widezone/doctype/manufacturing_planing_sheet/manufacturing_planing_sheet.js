// Copyright (c) 2023, LucrumERP and contributors
// For license information, please see license.txt

frappe.ui.form.on('Manufacturing Planing Sheet', {
	refresh: function(frm) {
		demo(frm)
		if(frm.doc.docstatus==1)
		{
			// cur_frm.add_custom_button(__('Manufacturing Sheet Planing'), function() {
			// 	frm.trigger("make_sheet_planing");
			// },
				// __('Create')),
			// cur_frm.add_custom_button(__('Material Resource Planing'), function() {
			// 	frm.trigger("make_material_resource_planing");
			// }, __('Create'))

		}
		frm.set_query("item","items", function(frm, cdt, cdn){
			var child = locals[cdt][cdn];
			return {
				filters: {
					has_variants : 0,
					variant_of: child.template
				}
			}
		});
	},
	setup: function(frm) {
		frm.set_query("item_template", function(){
			return {
				filters: {
					has_variants : 1
				}
			}
		});
		frm.set_query("template", "items", function(){
			return {
				filters: {
					has_variants : 1
				}
			}
		});
		frm.set_query("fabric_template","fabric_calculation", function(){
			return {
				filters: {
					has_variants : 1,
					item_group: 'Fabric'
				}
			}
		});
		frm.set_query("fabric_item","fabric_calculation", function(frm, cdt, cdn){
			var child = locals[cdt][cdn];
			return {
				filters: {
					has_variants : 0,
					item_group : "Fabric",
					variant_of: child.fabric_template
				}
			}
		});
		frm.set_query("fabric_item","fabric_extra", function(frm){
			return {
				filters: {
					has_variants : 0,
					item_group : "Fabric"
				}
			}
		});
		frm.set_query("fabric_item","yarn_plan", function(){
			return {
				filters: {
					has_variants : 0,
					item_group: 'Fabric'
				}
			}
		});
		frm.set_query("yarn_template","fabric_extra", function(){
			return {
				filters: {
					has_variants : 1,
					item_group: 'Yarn'
				}
			}
		});
		frm.set_query("item_template","accesories", function(){
			return {
				filters: {
					has_variants : 1,
				}
			}
		});
		frm.set_query("item_code","accesories", function(frm, cdt, cdn){
			var child = locals[cdt][cdn];
			return {
				filters: {
					has_variants : 0,
					variant_of: child.item_template
				}
			}
		});
		frm.set_query("item_template","packing", function(){
			return {
				filters: {
					has_variants : 1,
				}
			}
		});
		frm.set_query("item_code","packing", function(frm, cdt, cdn){
			var child = locals[cdt][cdn];
			return {
				filters: {
					has_variants : 0,
					variant_of: child.item_template
				}
			}
		});
	},
	append: function(frm) {
		if(frm.doc.item_template!='' && frm.doc.size!='' && frm.doc.color!='')
		{
			console.log(frm.doc.size)
			console.log(frm.doc.color)
			frappe.call({
				method: "widezone.widezone.doctype.manufacturing_planing_sheet.manufacturing_planing_sheet.check_attributes",
				args: {
					'size': frm.doc.size,
					'color': frm.doc.color
				},
				callback: function (r) {
				}
			});
			var childTable = cur_frm.add_child("items");
			childTable.template=frm.doc.item_template;
			childTable.colour=frm.doc.color;
			childTable.size=frm.doc.size;
			cur_frm.refresh_fields("items");
			frm.set_value('item_template', '')
			frm.set_value('color', '')
			frm.set_value('size', '')
		}	else {
			frappe.msgprint(__("Please Enter All Template, Size, Color"))
		}
	},
	make_sheet_planing: function(frm) {
		frappe.call({
			method: 'widezone.widezone.doctype.manufacturing_planing_sheet.manufacturing_planing_sheet.make_sheet_planing',
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
	make_material_resource_planing: function(frm) {
		frappe.call({
			method: 'widezone.widezone.doctype.manufacturing_planing_sheet.manufacturing_planing_sheet.make_material_resource_planing',
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
});

function demo(frm)
{
	
	if(frm.fields_dict.color.df.fieldtype !== "Data") {
			return;
		}
		$(frm.fields_dict.color.input_area).addClass("ui-front");

		var input = frm.fields_dict.color.$input.get(0);


		input.awesomplete = new Awesomplete(input, {
			minChars: 0,
			maxItems: 99,
			autoFirst: true,
			list: [],
		});
		input = frm.fields_dict.color;

		frm.fields_dict.color.$input
			.on('input', function(e) {
				var term = e.target.value;
				frappe.call({
					method: "lucrum.stock.doctype.item.item.get_item_attribute",
					args: {
						parent: 'Colour',
						attribute_value: term
					},
					callback: function(r) {
						if (r.message) {
							e.target.awesomplete.list = r.message.map(function(d) { return d.attribute_value; });
						}
					}
				});
			})
			.on('focus', function(e) {
				$(e.target).val('').trigger('input');
			})
		if(frm.fields_dict.size.df.fieldtype !== "Data") {
				return;
		}
			$(frm.fields_dict.size.input_area).addClass("ui-front");
	
			var input = frm.fields_dict.size.$input.get(0);
	
	
			input.awesomplete = new Awesomplete(input, {
				minChars: 0,
				maxItems: 99,
				autoFirst: true,
				list: [],
			});
			input = frm.fields_dict.size;
	
			frm.fields_dict.size.$input
				.on('input', function(e) {
					var term = e.target.value;
					frappe.call({
						method: "lucrum.stock.doctype.item.item.get_item_attribute",
						args: {
							parent: 'Size',
							attribute_value: term
						},
						callback: function(r) {
							if (r.message) {
								e.target.awesomplete.list = r.message.map(function(d) { return d.attribute_value; });
							}
						}
					});
				})
				.on('focus', function(e) {
					$(e.target).val('').trigger('input');
				})
}