# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from frappe import _
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
				"fpo":self.fpo
			})
		if exists and exists != self.name:
			fpo = frappe.get_doc('FPO',self.fpo)
			frappe.throw(_(f'{fpo.fpo_name} already exists for the Fpo Fixed Capital'))
	# def on_update(self):
	# 	# BP = frappe.db.get_list("Business Plannings", {'fpo': self.fpo}, fields=['name', 'depreciation_percent'])
	# 	BP = frappe.db.get_list("Business Plannings", filters={'fpo': self.fpo}, fields=['name', 'depreciation_percent'])
	# 	if BP:
	# 		for bp in BP:
	# 			frappe.db.set_value('Business Plannings',bp.name,'depreciation',self.total_value / bp.depreciation_percent ,update_modified=False)


