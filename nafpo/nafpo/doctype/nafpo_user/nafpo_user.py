# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class NafpoUser(Document):
	def after_insert(self):
		new_user = frappe.new_doc("User")
		new_user.email = self.email
		new_user.first_name = self.name1
		new_user.username = self.username
		new_user.mobile_no = self.mobile
		new_user.role_profile_name = self.level
		new_user.new_password = self.password
		new_user.save()


	def on_update(self):
		user_doc = frappe.get_doc("User", self.email)
		user_doc.email = self.email
		user_doc.first_name = self.name1
		user_doc.username = self.username
		user_doc.mobile_no = self.mobile
		user_doc.role_profile_name = self.level
		user_doc.new_password = self.password
		user_doc.save()
		if(self.level == "IA" and self.ia):
			ia_perm(self)
		if(self.level == "FPO" and self.fpo):
			fpo_perm(self)
		if(self.level == "CBBO" and self.cbbo):
			cbbo_perm(self)
		
	def on_trash(self):
		# Check if the user exists
		if frappe.db.exists("User", self.name):
			# Delete the user
			frappe.delete_doc("User", self.name, ignore_permissions=True)
			frappe.msgprint(f"The user {self.name} has been deleted.")
		else:
			frappe.msgprint(f"The user {self.name} does not exist.")


def ia_perm(self):
	ia_perm_doc = {
		'doctype': "User Permission",
		'allow': 'IA',
		'user':self.email
	}
	ia_perm_exist  = frappe.db.exists(ia_perm_doc)
	if ia_perm_exist:
		existing_doc = frappe.get_doc("User Permission",ia_perm_exist)
		existing_doc.for_value=self.ia
		existing_doc.save(ignore_permissions=True)
	else:
		perm_doc = frappe.get_doc(ia_perm_doc)
		perm_doc.for_value=self.ia
		perm_doc.insert(ignore_permissions=True)

def cbbo_perm(self):
	cbbo_perm_doc = {
		'doctype': "User Permission",
		'allow': 'CBBO',
		'user':self.email
	}
	cbbo_perm_exist  = frappe.db.exists(cbbo_perm_doc)
	if cbbo_perm_exist:
		existing_doc = frappe.get_doc("User Permission",cbbo_perm_exist)
		existing_doc.for_value=self.cbbo
		existing_doc.save(ignore_permissions=True)
	else:
		perm_doc = frappe.get_doc(cbbo_perm_doc)
		perm_doc.for_value=self.cbbo
		perm_doc.insert(ignore_permissions=True)

	cbbo_list = frappe.db.get_list('CBBO',
			filters={'name': self.cbbo},
			fields=['ia_name']
		)
	ia_names = cbbo_list[0].get('ia_name')

	# Set IA user permission directly within cbbo_perm
	ia_perm_doc = {
		'doctype': "User Permission",
		'allow': 'IA',
		'user': self.email
	}
	ia_perm_exist = frappe.db.exists(ia_perm_doc)
	if ia_perm_exist:
		existing_doc = frappe.get_doc("User Permission", ia_perm_exist)
		existing_doc.for_value = ia_names
		existing_doc.save(ignore_permissions=True)
	else:
		perm_doc = frappe.get_doc(ia_perm_doc)
		perm_doc.for_value = ia_names
		perm_doc.insert(ignore_permissions=True)

def fpo_perm(self):
	fpo_perm_doc = {
		'doctype': "User Permission",
		'allow': 'FPO',
		'user':self.email
	}
	fpo_perm_exist  = frappe.db.exists(fpo_perm_doc)
	if fpo_perm_exist:
		existing_doc = frappe.get_doc("User Permission",fpo_perm_exist)
		existing_doc.for_value=self.fpo
		existing_doc.save(ignore_permissions=True)
	else:
		perm_doc = frappe.get_doc(fpo_perm_doc)
		perm_doc.for_value=self.fpo
		perm_doc.insert(ignore_permissions=True)

	fpo_list = frappe.get_doc('FPO',
			self.fpo,
			fields=['cbbo_name']
		)

	cbbo_list = frappe.get_doc('CBBO',
			fpo_list.cbbo_name,
			fields=['ia_name']
		)
	
	# Set IA user permission directly within fpo_perm
	ia_perm_doc = {
		'doctype': "User Permission",
		'allow': 'IA',
		'user': self.email
	}
	ia_perm_exist = frappe.db.exists(ia_perm_doc)
	if ia_perm_exist:
		existing_doc = frappe.get_doc("User Permission", ia_perm_exist)
		existing_doc.for_value = cbbo_list.ia_name
		existing_doc.save(ignore_permissions=True)
	else:
		perm_doc = frappe.get_doc(ia_perm_doc)
		perm_doc.for_value = cbbo_list.ia_name
		perm_doc.insert(ignore_permissions=True)

	# Set CBBO user permission directly within fpo_perm
	cbbo_perm_doc = {
		'doctype': "User Permission",
		'allow': 'CBBO',
		'user':self.email
	}
	cbbo_perm_exist  = frappe.db.exists(cbbo_perm_doc)
	if cbbo_perm_exist:
		existing_doc = frappe.get_doc("User Permission",cbbo_perm_exist)
		existing_doc.for_value=fpo_list.cbbo_name
		existing_doc.save(ignore_permissions=True)
	else:
		perm_doc = frappe.get_doc(cbbo_perm_doc)
		perm_doc.for_value=fpo_list.cbbo_name
		perm_doc.insert(ignore_permissions=True)