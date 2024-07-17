# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FinancialYear(Document):
	def before_save(self):
		if self.start_date > self.end_date:
			frappe.throw("End Date must be after Start Date")
		split_start_year = self.start_date.split('-')[0] if len(self.start_date.split('-')) > 0 else self.start_date
		split_end_year = self.end_date.split('-')[0][-2:4] if len(self.end_date.split('-')) > 0 else self.end_date
		self.financial_year_name = f"{split_start_year}-{split_end_year}"