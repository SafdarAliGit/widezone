import frappe
from frappe import _

def before_naming(self,method):
    if self.department:
        department = frappe.get_doc("Department",self.department)
        if department and department.abbreviation:
            self.DEP = department.abbreviation