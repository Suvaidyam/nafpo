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
            fy = frappe.get_doc('Financial Year', self.financial_year)
            frappe.throw(_(f'Financial Year {fy.financial_year_name} already exists for the {fpo.fpo_name}'))
        
        check_exist_profile = frappe.db.exists({
            "doctype": "FPO Profiling", 
            "name_of_the_fpo": self.fpo
        })
        if check_exist_profile == None:
            frappe.throw(f"FPO Profile doesn't exist. Please create FPO Profiling.")