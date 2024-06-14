# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AnnualComplianceForms(Document):
    def before_validate(self):
        exists = frappe.db.exists({
            "doctype": "Annual Compliance Forms", 
            "financial_year": self.financial_year
        })
        data_exists = bool(exists)
        if data_exists:
            frappe.throw(f"FPO already exists for the Financial Year {self.financial_year}")
