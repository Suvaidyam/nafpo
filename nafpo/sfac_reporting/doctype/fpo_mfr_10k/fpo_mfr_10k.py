# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FPOMFR10K(Document):
    def before_validate(self):
        exists = frappe.db.exists({
            "doctype": "FPO MFR 10K", 
            "fpo": self.fpo
        })
        data_exists = bool(exists)
        if data_exists and exists != self.name:
            frappe.throw(f"This FPO are already exists in FPO MFR 10K")