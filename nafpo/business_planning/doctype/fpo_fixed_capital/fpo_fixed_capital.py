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
	def on_update(self):
		sfac_ins = frappe.db.exists("Business Plannings", {'fpo': self.fpo})
		if sfac_ins:
			# Update Business Plannings document with the total value
			frappe.db.set_value(
				'Business Plannings',
				sfac_ins[0][0],  # Get the name of the document
				{'depreciation': self.total_value},
				update_modified=False
			)


