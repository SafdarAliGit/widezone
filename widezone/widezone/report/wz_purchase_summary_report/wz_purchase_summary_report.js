// Copyright (c) 2023, LucrumERP and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["WZ Purchase Summary Report"] = {
	"filters": [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
		},
		{
			fieldname: "name",
			label: __("wz #"),
			fieldtype: "Link",
			options: "Material Resource Planing",

		},
		// {
		// 	fieldname: "parent_warehouse",
		// 	label: __("Parent Warehouse"),
		// 	fieldtype: "Link",
		// 	options: "Warehouse",
		// 	reqd: 1,
		// 	get_query: function(){
		// 		return {
		// 			filters:{
		// 				company: frappe.query_report.get_filter_value('company'),
		// 				is_group: 1
		// 			}
		// 		}
		// 	}
		// },
		// {
		// 	fieldname: "child_warehouse",
		// 	label: __("Child Warehouse"),
		// 	fieldtype: "MultiSelectList",
		// 	get_data: function(txt) {
		// 		var filters = {
		// 				company: frappe.query_report.get_filter_value('company'),
		// 				is_group: 0,
		// 				parent_warehouse: frappe.query_report.get_filter_value('parent_warehouse')
		// 			}
		// 		return frappe.db.get_link_options("Warehouse", txt, filters);
		// 	}
		// },
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.defaults.get_user_default("year_start_date"),
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.defaults.get_user_default("year_end_date"),
		},
	]
};
