from __future__ import unicode_literals
import frappe
from frappe.utils import now, cint, get_datetime
from frappe.model.document import Document
from frappe import _

def before_naming(self,method):
    if self.get('company'):
        company = frappe.get_doc("Company",self.get('company'))
        if company:
            self.abbr = company.abbr

    if self.doctype in ('Item Group'):
        doctype = "{} Group".format(self.doctype)
        print(doctype)
        print(frappe.scrub(doctype))
        self.abbr = frappe.get_value(doctype, self.get(frappe.scrub(doctype)),"abbreviation")
        print(self.abbr)