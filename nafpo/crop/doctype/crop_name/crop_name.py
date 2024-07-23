# Copyright (c) 2024, dhwaniris and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CropName(Document):
	def after_insert(self):
		crop_name = self.crop_variety_table
		if len(crop_name) > 0:
			for row in crop_name:
				new_crop_name = frappe.new_doc("Crop Name")
				new_crop_name.state_name = self.state_name
				new_crop_name.fpo = self.fpo
				new_crop_name.crops_types = self.crops_types
				new_crop_name.crop_variety = row.crop_variety
				new_crop_name.crops_name = self.crops_name
				new_crop_name.expected_yields_quintal_per_acre = row.expected_yields_quintal_per_acre
				new_crop_name.target_market_1 = row.target_market_1
				new_crop_name.target_market_2 = row.target_market_2
				new_crop_name.table_crop_name_child = []
				new_crop_name.insert()
			return frappe.delete_doc("Crop Name",self.name)