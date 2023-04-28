// Copyright (c) 2023, LucrumERP and contributors
// For license information, please see license.txt
/* eslint-disable */

// frappe.query_reports["Subcontract wz Summary"] = {
// 	"filters": [
//
// 	]
// };
// Copyright (c) 2016, Lucrumerp Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Subcontract wz Summary"] = {
    "filters": [
        {
            label: __("Company"),
            fieldname: "company",
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("Company"),
            reqd: 1
        },
        {
            label: __("From Date"),
            fieldname: "from_date",
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -6),
            reqd: 1
        },
        {
            label: __("To Date"),
            fieldname: "to_date",
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 1
        },
        {
            label: __("Purchase Order"),
            fieldname: "name",
            fieldtype: "Link",
            options: "Purchase Order",
            get_query: function () {
                return {
                    filters: {
                        docstatus: 1,
                        is_subcontracted: 'Yes',
                        company: frappe.query_report.get_filter_value('company')
                    }
                }
            }
        },
        {
            label: __("WZ #"),
            fieldname: "mrp_no",
            fieldtype: "Link",
            options: "Material Resource Planing",
            get_query: function () {
                return {
                    filters: {
                        docstatus: 1
                     }
                }
            }
        }
    ]
};
