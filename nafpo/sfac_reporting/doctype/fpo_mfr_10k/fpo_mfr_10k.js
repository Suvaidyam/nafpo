// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("FPO MFR 10K", {
    refresh: async function (frm) {
        console.log('OUT :>> ', frappe.session.user);
        if (frappe.user.has_role('FPO') && !frappe.user.has_role('Administrator')) {
            console.log('frappe.session.user :>> ', frappe.session.user);
            try {
                let fpo = await frappe.call({
                    method: "frappe.client.get_single_value",
                    args: {
                        doctype: "NAFPO User", name: frappe.session.user, field: 'name'
                    }
                });
                console.log('fpo :>> ', fpo);
                frm.set_value('fpo', fpo);
                set_due_date(frm);
            } catch (e) {
                console.error('User data fetch error:', e);
            }
        }

        frm.set_df_property('1st_installment_due_date', 'read_only', 1);
        frm.set_df_property('2nd_installment_due_date', 'read_only', 1);
        frm.set_df_property('3rd_installment_due_date', 'read_only', 1);
        frm.set_df_property('4th_installment_due_date', 'read_only', 1);
        frm.set_df_property('5th_installment_due_date', 'read_only', 1);
        frm.set_df_property('6th_installment_due_date', 'read_only', 1);

        frm.set_df_property('1st_installment_date', 'read_only', 1);
        frm.set_df_property('2nd_installment_date', 'read_only', 1);
        frm.set_df_property('3rd_installment_date', 'read_only', 1);
        frm.set_df_property('4th_installment_date', 'read_only', 1);
        frm.set_df_property('5th_installment_date', 'read_only', 1);
        frm.set_df_property('6th_installment_date', 'read_only', 1);
    },
    fpo(frm) {
        set_due_date(frm)
    },
    are_you_received_1st_installment_fund(frm) {
        if (frm.doc.are_you_received_1st_installment_fund == "Yes") {
            let today_date = new Date();
            today_date.setMonth(today_date.getMonth());
            frm.set_value('1st_installment_date', today_date.toISOString().split('T')[0])
        } else if (frm.doc.are_you_received_1st_installment_fund == "No") {
            frm.set_value('1st_installment_date', '')
        }
    },
    are_you_received_2nd_installment_fund(frm) {
        if (frm.doc.are_you_received_2nd_installment_fund === "Yes") {
            let today_date = new Date();
            today_date.setMonth(today_date.getMonth());
            frm.set_value('2nd_installment_date', today_date.toISOString().split('T')[0])
        } else if (frm.doc.are_you_received_2nd_installment_fund === "No") {
            frm.set_value('2nd_installment_date', '')
        }
    },
    are_you_received_3rd_installment_fund(frm) {
        if (frm.doc.are_you_received_3rd_installment_fund === "Yes") {
            let today_date = new Date();
            today_date.setMonth(today_date.getMonth());
            frm.set_value('3rd_installment_date', today_date.toISOString().split('T')[0])
        } else if (frm.doc.are_you_received_3rd_installment_fund === "No") {
            frm.set_value('3rd_installment_date', '')
        }
    },
    are_you_received_4th_installment_fund(frm) {
        if (frm.doc.are_you_received_4th_installment_fund === "Yes") {
            let today_date = new Date();
            today_date.setMonth(today_date.getMonth());
            frm.set_value('4th_installment_date', today_date.toISOString().split('T')[0])
        } else if (frm.doc.are_you_received_4th_installment_fund === "No") {
            frm.set_value('4th_installment_date', '')
        }
    },
    are_you_received_5th_installment_fund(frm) {
        if (frm.doc.are_you_received_5th_installment_fund === "Yes") {
            let today_date = new Date();
            today_date.setMonth(today_date.getMonth());
            frm.set_value('5th_installment_date', today_date.toISOString().split('T')[0])
        } else if (frm.doc.are_you_received_5th_installment_fund === "No") {
            frm.set_value('5th_installment_date', '')
        }
    },
    are_you_received_6th_installment_fund(frm) {
        if (frm.doc.are_you_received_6th_installment_fund === "Yes") {
            let today_date = new Date();
            today_date.setMonth(today_date.getMonth());
            frm.set_value('6th_installment_date', today_date.toISOString().split('T')[0])
        } else if (frm.doc.are_you_received_6th_installment_fund === "No") {
            frm.set_value('6th_installment_date', '')
        }
    },
});


function set_due_date(frm) {
    frappe.call({
        method: "nafpo.apis.api.get_fpo_profile_doc",
        args: {
            doctype_name: 'FPO Profiling',
            filter: frm.doc.fpo
        },
        callback: function (response) {
            let registration_date = new Date(response.message.date_of_registration);
            let first_due_date = new Date(registration_date);
            let second_due_date = new Date(registration_date);
            let third_due_date = new Date(registration_date);
            let fourth_due_date = new Date(registration_date);
            let fifth_due_date = new Date(registration_date);
            let sixth_due_date = new Date(registration_date);

            first_due_date.setMonth(first_due_date.getMonth());
            second_due_date.setMonth(second_due_date.getMonth() + 6);
            third_due_date.setMonth(third_due_date.getMonth() + 12);
            fourth_due_date.setMonth(fourth_due_date.getMonth() + 18);
            fifth_due_date.setMonth(fifth_due_date.getMonth() + 24);
            sixth_due_date.setMonth(sixth_due_date.getMonth() + 30);

            frm.set_value('1st_installment_due_date', first_due_date.toISOString().split('T')[0]);
            frm.set_value('2nd_installment_due_date', second_due_date.toISOString().split('T')[0]);
            frm.set_value('3rd_installment_due_date', third_due_date.toISOString().split('T')[0]);
            frm.set_value('4th_installment_due_date', fourth_due_date.toISOString().split('T')[0]);
            frm.set_value('5th_installment_due_date', fifth_due_date.toISOString().split('T')[0]);
            frm.set_value('6th_installment_due_date', sixth_due_date.toISOString().split('T')[0]);
        },
        error: function (error) {
            console.log("An error occurred: ", error);
        }
    });
}