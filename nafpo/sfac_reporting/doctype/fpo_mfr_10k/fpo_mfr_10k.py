# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FPOMFR10K(Document):
    def before_save(self):
        fpo_profile_name = frappe.get_doc('FPO', self.fpo)
        self.fpo_copy = fpo_profile_name.fpo_name
    
    def before_validate(self):
        exists = frappe.db.exists({
            "doctype": "SFAC Installment", 
            "fpo": self.fpo
        })
        data_exists = bool(exists)
        if data_exists and exists != self.name:
            frappe.throw(f"FPO already exists in SFAC Installment")