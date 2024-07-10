# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FPOFixedCapital(Document):
	def before_save(self):
		total_value = 0
		fixed_capital_details_row = self.fixed_capital_details_table
		for row in fixed_capital_details_row:
			total_value += row.value
		self.total_value = total_value
	# Check FPO
		exists = frappe.db.exists({
				"doctype": "FPO Fixed Capital",
				"financial_year": self.financial_year,
				"fpo":self.fpo
			})
		if exists and exists != self.name:
			fpo = frappe.get_doc('FPO',self.fpo)
			frappe.throw(_(f'Financial Year {self.financial_year} already exists for the {fpo.fpo_name}'))
