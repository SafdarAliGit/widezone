// Copyright (c) 2023, LucrumERP and contributors
// For license information, please see license.txt

frappe.ui.form.on('Manufacturing Sheet Widezone', {
	refresh: function(frm) {
		demo(frm)
		if(frm.doc.docstatus==1)
		{
			cur_frm.add_custom_button(__('Manufacturing Sheet Planing'), function() {
				frm.trigger("make_sheet_planing");
			},
				__('Create')),
			cur_frm.add_custom_button(__('Material Resource Planing'), function() {
				frm.trigger("make_material_resource_planing");
			}, __('Create'))

		}
		frm.set_query("item","items", function(frm, cdt, cdn){
			var child = locals[cdt][cdn];
			return {
				// query: "widezone.widezone.custom.outward_gatepass_custom.get_transporter",
				filters: {
					has_variants : 0,
					variant_of: child.template,
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
		if(frm.doc.item_template!='' && frm.doc.size!='' && frm.doc.color!='' && frm.doc.department!='' && frm.doc.composition!='')
		{
			
			frappe.call({
				method: "widezone.widezone.doctype.manufacturing_sheet_widezone.manufacturing_sheet_widezone.check_attributes",
				args: {
					'size': frm.doc.size,
					'color': frm.doc.color,
					'department': frm.doc.department,
					'composition': frm.doc.composition,
				},
				callback: function (r) {
				}
			});
			var childTable = cur_frm.add_child("items");
			childTable.template=frm.doc.item_template;
			childTable.colour=frm.doc.color;
			childTable.size=frm.doc.size;
			childTable.department=frm.doc.department;
			childTable.composition=frm.doc.composition;
			cur_frm.refresh_fields("items");
			frm.set_value('item_template', '')
			frm.set_value('color', '')
			frm.set_value('size', '')
			frm.set_value('department', '')
			frm.set_value('composition', '')
		}	else {
			frappe.msgprint(__("Please Enter All fields Template and Attributes"))
		}
	},
	make_sheet_planing: function(frm) {
		frappe.call({
			method: 'widezone.widezone.doctype.manufacturing_sheet_widezone.manufacturing_sheet_widezone.make_sheet_planing',
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
			method: 'widezone.widezone.doctype.manufacturing_sheet_widezone.manufacturing_sheet_widezone.make_material_resource_planing',
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

frappe.ui.form.on('MS Items', {
	order_quantity: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		// if(child.plan_allowance=='' || child.plan_allowance==0)
		// {
		// 	plan_allowance = 1
		// }	else {
		// 	plan_allowance = child.plan_allowance
		// }
		if(child.plan_allowance>0)
		{
		var pqty = ((child.order_quantity * child.plan_allowance) / 100) + child.order_quantity;
		frappe.model.set_value(cdt,cdn,"plan_quantity", pqty)
		}
	},
	plan_allowance: function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		// if(child.plan_allowance=='' || child.plan_allowance==0)
		// {
		// 	plan_allowance = 1
		// }	else {
		// 	plan_allowance = child.plan_allowance
		// }
		if(child.order_quantity>0)
		{
		var pqty = ((child.order_quantity * child.plan_allowance) / 100) + child.order_quantity;
		frappe.model.set_value(cdt,cdn,"plan_quantity", pqty)
		}
	},
});
function demo(frm)
{
	var fields = {
		Colour:frm.fields_dict.color,
		Size:frm.fields_dict.size,
		Department:frm.fields_dict.department,
		Composition:frm.fields_dict.composition,
	}
	$.each(fields, function(i, field) {
	console.log(field)
	if(field.df.fieldtype !== "Data") {
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
		input = field;

		field.$input
			.on('input', function(e) {
				var term = e.target.value;
				frappe.call({
					method: "lucrum.stock.doctype.item.item.get_item_attribute",
					args: {
						parent: i,
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
		});
}