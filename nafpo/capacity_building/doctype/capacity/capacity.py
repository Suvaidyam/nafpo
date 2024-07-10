# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Capacity(Document):
	def before_save(self):
		if self.category == "Membership System (FPO Member)":
			self.no_of_participants = len(self.fpo_member)
		if self.category == "Governance System (BOD)":
			self.no_of_participants = len(self.bod_kyc)
		if self.category == "Operation System (CEO/Account/other staff)":
			self.no_of_participants = len(self.operation_system)
		if self.category == "Other":
			if len(self.other) > 0:
				self.no_of_participants = 1
			if len(self.other) <= 0:
				self.no_of_participants = 0
