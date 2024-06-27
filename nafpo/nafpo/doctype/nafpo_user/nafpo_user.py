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
		delete_existing_permissions(self)
		add_new_permissions(self)

	def on_trash(self):
		# Check if the user exists
		if frappe.db.exists("User", self.name):
			# Delete the user
			frappe.delete_doc("User", self.name, ignore_permissions=True)
			frappe.msgprint(f"The user {self.name} has been deleted.")
		else:
			frappe.msgprint(f"The user {self.name} does not exist.")


def delete_existing_permissions(self):
    roles = ["IA", "CBBO", "FPO"]
    for role in roles:
        delete_permission(role, self.email)


def delete_permission(role, email):
    perm_exist = frappe.db.exists("User Permission", {"allow": role, "user": email})
    if perm_exist:
        frappe.delete_doc("User Permission", perm_exist, ignore_permissions=True)


def add_new_permissions(self):
    if self.level == "IA" and self.ia:
        ia_perm(self)
    elif self.level == "CBBO" and self.cbbo:
        cbbo_perm(self)
    elif self.level == "FPO" and self.fpo:
        fpo_perm(self)

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
			fields=['*']
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

	# Set State user permission directly within fpo_perm
	state_perm_doc = {
		'doctype': "User Permission",
		'allow': 'State',
		'user':self.email
	}
	state_perm_exist  = frappe.db.exists(state_perm_doc)
	if state_perm_exist:
		existing_doc = frappe.get_doc("User Permission",state_perm_exist)
		existing_doc.for_value=fpo_list.state
		existing_doc.save(ignore_permissions=True)
	else:
		perm_doc = frappe.get_doc(state_perm_doc)
		perm_doc.for_value=fpo_list.state
		perm_doc.insert(ignore_permissions=True)

	# Set District user permission directly within fpo_perm
	district_perm_doc = {
		'doctype': "User Permission",
		'allow': 'District',
		'user':self.email
	}
	district_perm_exist  = frappe.db.exists(district_perm_doc)
	if district_perm_exist:
		existing_doc = frappe.get_doc("User Permission",district_perm_exist)
		existing_doc.for_value=fpo_list.district
		existing_doc.save(ignore_permissions=True)
	else:
		perm_doc = frappe.get_doc(district_perm_doc)
		perm_doc.for_value=fpo_list.district
		perm_doc.insert(ignore_permissions=True)
	# Set Block user permission directly within fpo_perm
	block_perms = frappe.db.get_list('User Permission',filters={'allow': 'Block','user':self.email},pluck='name')
	if len(block_perms):
		for bp in block_perms:
			frappe.delete_doc("User Permission",bp,ignore_permissions=True)
	if len(fpo_list.block):
		for b in fpo_list.block:
			block_perm_doc = {
				'doctype': "User Permission",
				'allow': 'Block',
				'user':self.email,
				'for_value':b.block
			}
			block_perm_exist = frappe.db.exists(block_perm_doc)
			if not block_perm_exist:
				perm_doc = frappe.get_doc(block_perm_doc)
				perm_doc.insert(ignore_permissions=True)