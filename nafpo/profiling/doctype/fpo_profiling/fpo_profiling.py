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

                # Assuming you want to print these dates for demonstration
                print('1st_installment_due_date:', first_due_date_str)
                print('2nd_installment_due_date:', second_due_date_str)
                print('3rd_installment_due_date:', third_due_date_str)
                print('4th_installment_due_date:', fourth_due_date_str)
                print('5th_installment_due_date:', fifth_due_date_str)
                print('6th_installment_due_date:', six_due_date_str)
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