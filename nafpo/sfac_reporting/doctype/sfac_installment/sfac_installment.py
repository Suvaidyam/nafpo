# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SFACInstallment(Document):
    def before_save(self):
        fpo_profile_name = frappe.get_doc('FPO', self.fpo)
        self.fpo_copy = fpo_profile_name.fpo_name