// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

async function check_exists_fpo_in_mfr(frm) {
    let response = await frappe.call({
        method: "nafpo.apis.api.get_exists_event",
        args: {
            doctype_name: "FPO MFR 10K",
            filterName: "fpo",
            value: frm.doc.fpo,
        }
    });
    if (response.message) {
        // frm.set_value('fpo', '')
        return frappe.throw({ message: 'This FPO are already exists in FPO MFR 10K' });
    }
}
async function check_fpo_profile(frm) {
    let response = await frappe.call({
        method: "nafpo.apis.api.get_exists_event",
        args: {
            doctype_name: "FPO Profiling",
            filterName: "name_of_the_fpo",
            value: frm.doc.fpo,
        }
    });
    if (response.message == undefined) {
        // frm.set_value('fpo', '')
        return frappe.throw({ message: 'Please Create FPO Profiling for this FPO' });
    }
}
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

frappe.ui.form.on("FPO MFR 10K", {
    refresh: async function (frm) {
        if (frappe.user.has_role('FPO') && !frappe.user.has_role('Administrator')) {
            try {
                let fpo = await frappe.call({
                    method: "nafpo.apis.api.get_fpo_doc",
                    args: {
                        doctype_name: "NAFPO User",
                        value: frappe.session.user,
                    }
                });
                frm.set_value('fpo', fpo.message.fpo);
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
        // Replace code in Future
        // ['1st', '2nd', '3rd', '4th', '5th', '6th'].forEach(installment => {
        //     frm.set_df_property(`${installment}_installment_due_date`, 'read_only', 1);
        //     frm.set_df_property(`${installment}_installment_date`, 'read_only', 1);
        // });
    },
    async validate(frm) {
        if (frm.doc.are_you_received_1st_installment_fund !== 'Yes' &&
            frm.doc.are_you_received_2nd_installment_fund !== 'Yes' &&
            frm.doc.are_you_received_3rd_installment_fund !== 'Yes' &&
            frm.doc.are_you_received_4th_installment_fund !== 'Yes' &&
            frm.doc.are_you_received_5th_installment_fund !== 'Yes' &&
            frm.doc.are_you_received_6th_installment_fund !== 'Yes'
        ) {
            frappe.throw({ message: 'Installment Status Not Yet Updated' });
        }
        if (frm.image_uploaded) {
            frappe.validated = false;
            frm.image_uploaded = false;
        }
        await check_fpo_profile(frm)
    },

    fpo: async function (frm) {
        await check_fpo_profile(frm)
        await check_exists_fpo_in_mfr(frm)
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
    ...['1st_installment_proof_of_document', '2nd_installment_proof_of_document', '3rd_installment_proof_of_document', '4th_installment_proof_of_document', '5th_installment_proof_of_document', '6th_installment_proof_of_document'].reduce((acc, field) => {
        acc[field] = function (frm) {
            frm.image_uploaded = true;
        };
        return acc;
    }, {})
});