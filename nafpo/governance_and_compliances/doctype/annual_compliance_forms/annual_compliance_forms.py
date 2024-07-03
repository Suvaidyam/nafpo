import frappe
from frappe.model.document import Document
from frappe import _

class AnnualComplianceForms(Document):
    pass
    # def validate(self):
    #     self.check_fpo()

    # def check_fpo(self):
    #     try:
    #         exists = frappe.db.exists({
    #             "doctype": "Annual Compliance Forms",
    #             "financial_year": self.financial_year,
    #             "name": ["!=", self.name]
    #         })
    #         if exists:
    #             frappe.throw(_('FPO already exists for the Financial Year {0}').format(self.financial_year))
    #     except Exception as e:
    #         frappe.log_error(frappe.get_traceback(), 'Annual Compliance Forms Check FPO Error')
    #         raise e