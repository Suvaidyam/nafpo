# Import the necessary module from Frappe
import frappe
from frappe.model.document import Document

class FPOProfiling(Document):
    def before_save(self):
        fpo_profile_name = frappe.get_doc('FPO', self.name_of_the_fpo)
        self.name_of_the_fpo_copy = fpo_profile_name.fpo_name
        
    def on_update(self):
        if self.date_of_registration:
            sfac_ins = frappe.get_doc("SFAC Installment", {'fpo': self.name_of_the_fpo})
            if sfac_ins:
                sfac_ins.first_installment_due_date = self.date_of_registration
                sfac_ins.second_installment_due_date = self.date_of_registration
                sfac_ins.third_installment_due_date = self.date_of_registration
                sfac_ins.fourth_installment_due_date = self.date_of_registration
                sfac_ins.fifth_installment_due_date = self.date_of_registration
                sfac_ins.sixth_installment_due_date = self.date_of_registration
                sfac_ins.save(ignore_permissions=True)
