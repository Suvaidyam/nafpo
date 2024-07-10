import frappe
from frappe.model.document import Document

class CropType(Document):
	def after_insert(self):
		if len(self.fpo) > 0:
			for item in self.fpo:
				state = frappe.db.get_value("FPO",item.fpo,'state')
				new_crop = frappe.new_doc("Crop Type")
				new_crop.state = []
				new_crop.single_state = state
				new_crop.fpo = []
				new_crop.single_fpo = item.fpo
				new_crop.name1 = self.name1
				new_crop.insert()
			return frappe.delete_doc("Crop Type",self.name)