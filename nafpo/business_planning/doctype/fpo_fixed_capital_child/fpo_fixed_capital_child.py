# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FPOFixedCapitalChild(Document):
	def before_save(self):
		print('==========================================',self.value)
