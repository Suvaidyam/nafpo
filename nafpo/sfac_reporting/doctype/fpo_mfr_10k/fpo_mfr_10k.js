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
        return frappe.throw({ message: 'This FPO are already exists in FPO MFR 10K' });
    }
}
function set_due_date(frm) {
    frappe.call({
        method: "nafpo.apis.api.get_list_event",
        args: {
            doctype_name: 'FPO Profiling',
            filter: { 'name': frm.doc.fpo },
            fields: ['date_of_registration']
        },
        callback: function (response) {
            console.log('date_of_registration :>> ', response.message[0].date_of_registration);
            let registration_date = new Date(response.message[0].date_of_registration);
            // Define due dates as an array with the corresponding month increments
            const due_dates = [0, 6, 12, 18, 24, 30].map(months => {
                let due_date = new Date(registration_date);
                due_date.setMonth(registration_date.getMonth() + months);
                return due_date.toISOString().split('T')[0];
            });
            // Set values in the form
            ['1st_installment_due_date', '2nd_installment_due_date', '3rd_installment_due_date', '4th_installment_due_date', '5th_installment_due_date', '6th_installment_due_date'].forEach((field, index) => {
                frm.set_value(field, due_dates[index]);
            });
        },
        error: function (error) {
            console.log("An error occurred: ", error);
        }
    });
}

frappe.ui.form.on("FPO MFR 10K", {
    refresh: async function (frm) {
        if (frappe.user.has_role('FPO') && !frappe.user.has_role('Administrator') && frm.is_new()) {
            try {
                let fpo = await frappe.call({
                    method: "nafpo.apis.api.get_fpo_doc",
                    args: {
                        doctype_name: "NAFPO User",
                        value: frappe.session.user,
                    }
                });
                frm.set_value('fpo', fpo.message.fpo);
                // set_due_date(frm);
            } catch (e) {
                console.error('User data fetch error:', e);
            }
        }
        hide_print_button(frm)
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
    },

    fpo: async function (frm) {
        if (frm.is_new() && frm.doc.fpo) {
            await check_exists_fpo_in_mfr(frm)
        }
        if (frm.doc.fpo) { set_due_date(frm) }
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