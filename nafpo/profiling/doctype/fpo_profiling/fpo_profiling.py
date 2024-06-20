# Import the necessary module from Frappe
import frappe
from frappe.model.document import Document

class FPOProfiling(Document):
    def before_save(self):
        fpo_profile_name = frappe.get_doc('FPO', self.name_of_the_fpo)
        self.name_of_the_fpo_copy = fpo_profile_name.fpo_name
