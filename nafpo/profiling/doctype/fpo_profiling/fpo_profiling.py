# Import the necessary module from Frappe
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta

class FPOProfiling(Document):
    def before_save(self):
    # Check if an entry already exists
        check_otorf = frappe.db.exists({
            "doctype": "One Time Organization Registration Forms",
            'fpo': self.name_of_the_fpo
        })
        if check_otorf:
            new_otorf = frappe.get_doc("One Time Organization Registration Forms", check_otorf)
        else:
            new_otorf = frappe.new_doc("One Time Organization Registration Forms")
        registration_date = datetime.strptime(self.date_of_registration, '%Y-%m-%d').date()
        new_otorf.fpo = self.name_of_the_fpo
        new_otorf.inc_20_due_date = registration_date + relativedelta(days=180)
        new_otorf.inc_22_due_date = registration_date + relativedelta(days=30)
        new_otorf.adt_1_due_date = registration_date + relativedelta(days=30)
        new_otorf.save()
        if not self.is_new():
            # FPO MFR 10k
            if self.under_the_central_sector_scheme_10k_fpo_formation:
                check_fpo_mfr = frappe.db.exists({
                    "doctype": "FPO MFR 10K",
                    'fpo': self.name
                })
                if check_fpo_mfr:
                    new_fpo_mfr = frappe.get_doc("FPO MFR 10K", check_fpo_mfr)
                else:
                    new_fpo_mfr = frappe.new_doc("FPO MFR 10K")
                
                registration_date = datetime.strptime(self.date_of_registration, '%Y-%m-%d').date()
                new_fpo_mfr.fpo = self.name
                new_fpo_mfr.__dict__['1st_installment_due_date'] = registration_date
                new_fpo_mfr.__dict__['2nd_installment_due_date'] = registration_date + relativedelta(months=6)
                new_fpo_mfr.__dict__['3rd_installment_due_date'] = registration_date + relativedelta(months=12)
                new_fpo_mfr.__dict__['4th_installment_due_date'] = registration_date + relativedelta(months=18)
                new_fpo_mfr.__dict__['5th_installment_due_date'] = registration_date + relativedelta(months=24)
                new_fpo_mfr.__dict__['6th_installment_due_date'] = registration_date + relativedelta(months=30)
                new_fpo_mfr.save()
        
    def after_insert(self):
    # FPO MFR 10k
        if self.under_the_central_sector_scheme_10k_fpo_formation:
            check_fpo_mfr = frappe.db.exists({
                "doctype": "FPO MFR 10K",
                'fpo': self.name
            })
            if check_fpo_mfr:
                new_fpo_mfr = frappe.get_doc("FPO MFR 10K", check_fpo_mfr)
            else:
                new_fpo_mfr = frappe.new_doc("FPO MFR 10K")
            
            registration_date = datetime.strptime(self.date_of_registration, '%Y-%m-%d').date()
            new_fpo_mfr.fpo = self.name
            new_fpo_mfr.__dict__['1st_installment_due_date'] = registration_date
            new_fpo_mfr.__dict__['2nd_installment_due_date'] = registration_date + relativedelta(months=6)
            new_fpo_mfr.__dict__['3rd_installment_due_date'] = registration_date + relativedelta(months=12)
            new_fpo_mfr.__dict__['4th_installment_due_date'] = registration_date + relativedelta(months=18)
            new_fpo_mfr.__dict__['5th_installment_due_date'] = registration_date + relativedelta(months=24)
            new_fpo_mfr.__dict__['6th_installment_due_date'] = registration_date + relativedelta(months=30)
            new_fpo_mfr.save()


    def before_validate(self):
        exists = frappe.db.exists({
            "doctype": "FPO Profiling",
            "name_of_the_fpo": self.name_of_the_fpo
        })
        data_exists = bool(exists)
        if data_exists and exists != self.name:
            frappe.throw(f"FPO already exists in FPO Profiling")

    def on_update(self):
        if len(self.deleted_staff_rows) > 0:
            for row_id in self.deleted_staff_rows:
                existing_staff_name = frappe.db.exists("FPO Staff", {"child_reference": row_id})
                if existing_staff_name:
                    frappe.delete_doc("FPO Staff", existing_staff_name)
            
        staff_details = self.staff_details_table
        for row in staff_details:
            existing_staff_name = frappe.db.exists("FPO Staff", {"child_reference": row.name})
            if not existing_staff_name:
                new_fpo_staff = frappe.new_doc("FPO Staff")
                new_fpo_staff.fpo = self.name_of_the_fpo
                new_fpo_staff.position_designation = row.position_designation
                new_fpo_staff.name1 = f"{row.name1} - {row.position_designation}"
                new_fpo_staff.joining_date = row.joining_date
                new_fpo_staff.child_reference = row.name
                new_fpo_staff.aadhar_no = row.aadhar_no
                new_fpo_staff.phone_no = row.phone_no
                new_fpo_staff.insert()
            else:
                new_fpo_staff = frappe.get_doc("FPO Staff",existing_staff_name)
                new_fpo_staff.fpo = self.name_of_the_fpo
                new_fpo_staff.position_designation = row.position_designation
                new_fpo_staff.name1 = f"{row.name1} - {row.position_designation}"
                new_fpo_staff.joining_date = row.joining_date
                new_fpo_staff.child_reference = row.name
                new_fpo_staff.aadhar_no = row.aadhar_no
                new_fpo_staff.phone_no = row.phone_no
                new_fpo_staff.save()
                
        # if self.date_of_registration:
        #     sfac_ins = frappe.db.exists("FPO MFR 10K", {'fpo': self.name_of_the_fpo})
        #     if sfac_ins:
        #         registration_date_str = self.date_of_registration
        #         registration_date = datetime.strptime(registration_date_str, '%Y-%m-%d').date()
        #         # Calculate due dates based on months using dateutil.relativedelta
        #         first_due_date = registration_date + relativedelta()
        #         second_due_date = registration_date + relativedelta(months=6)
        #         third_due_date = registration_date + relativedelta(months=12)
        #         fourth_due_date = registration_date + relativedelta(months=18)
        #         fifth_due_date = registration_date + relativedelta(months=24)
        #         six_due_date = registration_date + relativedelta(months=30)
        #         # Format dates as yyyy-mm-dd
        #         first_due_date_str = first_due_date.isoformat()
        #         second_due_date_str = second_due_date.isoformat()
        #         third_due_date_str = third_due_date.isoformat()
        #         fourth_due_date_str = fourth_due_date.isoformat()
        #         fifth_due_date_str = fifth_due_date.isoformat()
        #         six_due_date_str = six_due_date.isoformat()
                
        #         frappe.db.set_value('FPO MFR 10K',sfac_ins,
        #                             {
        #                                 '1st_installment_due_date':first_due_date_str,
        #                                 '2nd_installment_due_date':second_due_date_str,
        #                                 '3rd_installment_due_date':third_due_date_str,
        #                                 '4th_installment_due_date':fourth_due_date_str,
        #                                 '5th_installment_due_date':fifth_due_date_str,
        #                                 '6th_installment_due_date':six_due_date_str
        #                             }
        #                             ,update_modified=False)