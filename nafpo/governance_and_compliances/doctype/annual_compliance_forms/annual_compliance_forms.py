import frappe
from frappe.model.document import Document
from frappe import _

class AnnualComplianceForms(Document):
    def before_save(self):
        exists = frappe.db.exists({
                "doctype": "Annual Compliance Forms",
                "financial_year": self.financial_year,
                "fpo":self.fpo
            })
        if exists and exists != self.name:
            fpo = frappe.get_doc('FPO',self.fpo)
            frappe.throw(_(f'Financial Year {self.financial_year} already exists for the {fpo.fpo_name}'))