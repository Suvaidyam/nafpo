# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FPOmemberdetails(Document):
	def before_save(self):
		self.total_owned_in_hectare = self.total_own_land * 0.404686
		self.total_own_irrigated_land_in_hectare = self.total_own_irrigated_land * 0.404686
		self.how_much_irrigated_leased_land_in_hectare = self.how_much_irrigated_leased_land_area_in_acre * 0.404686