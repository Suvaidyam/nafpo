# Import the necessary module from Frappe
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta

class FPOProfiling(Document):
    def before_save(self):
        fpo_profile_name = frappe.get_doc('FPO', self.name_of_the_fpo)
        self.name_of_the_fpo_copy = fpo_profile_name.fpo_name

        staff_details = self.staff_details_table
        for row in staff_details:
            existing_staff_name = frappe.db.exists("FPO Staff Child", {"name": row.name})
            if not existing_staff_name:
                new_fpo_staff = frappe.new_doc("FPO Staff")
                new_fpo_staff.name = row.name
                new_fpo_staff.fpo = self.name_of_the_fpo
                new_fpo_staff.position_designation = row.position_designation
                new_fpo_staff.name1 = f"{row.name1} - {row.position_designation}"
                new_fpo_staff.joining_date = row.joining_date
                new_fpo_staff.aadhar_no = row.aadhar_no
                new_fpo_staff.phone_no = row.phone_no
                new_fpo_staff.save()

    def before_validate(self):
        exists = frappe.db.exists({
            "doctype": "FPO Profiling",
            "name_of_the_fpo": self.name_of_the_fpo
        })
        data_exists = bool(exists)
        if data_exists and exists != self.name:
            frappe.throw(f"FPO already exists in FPO Profiling")

    def on_update(self):
        if self.date_of_registration:
            sfac_ins = frappe.db.exists("SFAC Installment", {'fpo': self.name_of_the_fpo})
            if sfac_ins:
                registration_date_str = self.date_of_registration
                registration_date = datetime.strptime(registration_date_str, '%Y-%m-%d').date()
                # Calculate due dates based on months using dateutil.relativedelta
                first_due_date = registration_date + relativedelta()
                second_due_date = registration_date + relativedelta(months=6)
                third_due_date = registration_date + relativedelta(months=12)
                fourth_due_date = registration_date + relativedelta(months=18)
                fifth_due_date = registration_date + relativedelta(months=24)
                six_due_date = registration_date + relativedelta(months=30)
                # Format dates as yyyy-mm-dd
                first_due_date_str = first_due_date.isoformat()
                second_due_date_str = second_due_date.isoformat()
                third_due_date_str = third_due_date.isoformat()
                fourth_due_date_str = fourth_due_date.isoformat()
                fifth_due_date_str = fifth_due_date.isoformat()
                six_due_date_str = six_due_date.isoformat()
                
                frappe.db.set_value('SFAC Installment',sfac_ins,
                                    {
                                        '1st_installment_due_date':first_due_date_str,
                                        '2nd_installment_due_date':second_due_date_str,
                                        '3rd_installment_due_date':third_due_date_str,
                                        '4th_installment_due_date':fourth_due_date_str,
                                        '5th_installment_due_date':fifth_due_date_str,
                                        '6th_installment_due_date':six_due_date_str
                                    }
                                    ,update_modified=False)