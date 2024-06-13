import frappe
from frappe.model.document import Document

class OneTimeOrganizationRegistrationForms(Document):
    def before_validate(self):
        # Check if a document with the same financial year already exists
        exists = frappe.db.exists({
            "doctype": "One Time Organization Registration Forms", 
            "financial_year": self.financial_year
        })
        data_exists = bool(exists)
        if data_exists:
            frappe.throw(f"FPO already exists for the Financial Year {self.financial_year}")
