# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class NafpoUser(Document):
	def after_insert(self):
		new_user = frappe.new_doc("User")
		new_user.email = self.email
		new_user.first_name = self.name
		new_user.role_profile_name = self.level
		new_user.new_password = self.password
		new_user.save()


	def on_update(self):
		user_doc = frappe.get_doc("User", self.email)
		user_doc.email = self.email
		user_doc.first_name = self.name
		user_doc.role_profile_name = self.level
		user_doc.new_password = self.password
		user_doc.save()
		
	def on_trash(self):
		# Check if the user exists
		if frappe.db.exists("User", self.name):
			# Delete the user
			frappe.delete_doc("User", self.name, ignore_permissions=True)
			frappe.msgprint(f"The user {self.name} has been deleted.")
		else:
			frappe.msgprint(f"The user {self.name} does not exist.")
	
