// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("One Time Organization Registration Forms", {
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
        const submitted_on_fields = ['inc_20_submitted_on', 'inc_22_submitted_on', 'adt_1_submitted_on'];
        submitted_on_fields.forEach(field => {
            frm.fields_dict[field].$input.datepicker({ maxDate: new Date() });
        });
    },
    validate(frm) {
        if (frm.doc.inc_20_status !== 'Completed' &&
            frm.doc.inc_22_status !== 'Completed' &&
            frm.doc.adt_1_due_date !== 'Completed'
        ) {
            frappe.throw('At least one of the Status Conditions must be met.');
        }
    },
    // financial_year: async function (frm) {
    //     check_fpo(frm)
    // },
    inc_20_status: function (frm) {
        blank_submitted_on(frm, 'inc_20_status', 'inc_20_submitted_on');
    },

    inc_22_status: function (frm) {
        blank_submitted_on(frm, 'inc_22_status', 'inc_22_submitted_on');
    },

    adt_1_status: function (frm) {
        blank_submitted_on(frm, 'adt_1_status', 'adt_1_submitted_on');
    },
    fpo(frm) {
        set_due_date(frm)
    },
    ...['inc_20_bank_statement', 'inc_20_bank_statement', 'inc_22_noc', 'inc_22_rent_agreement', 'inc_22_electricity_bill', 'adt_1_fpo_resolution'].reduce((acc, field) => {
        acc[field] = function (frm) {
            disable_Attachment_autosave(frm);
        };
        return acc;
    }, {})
});

function blank_submitted_on(frm, status_field, date_field) {
    if (frm.doc[status_field] == "Pending") {
        frm.set_value(date_field, '');
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
            if (response.message == undefined) {
                frappe.throw("FPO Profile doesn't exist. Please create FPO Profiling.")
            }
            let date = new Date(response.message.date_of_registration);
            date.setDate(date.getDate() + 180);
            frm.set_value('inc_20_due_date', date.toISOString().split('T')[0]);
            date.setDate(date.getDate() + 30);
            frm.set_value('inc_22_due_date', date.toISOString().split('T')[0]);
            frm.set_value('adt_1_due_date', date.toISOString().split('T')[0]);
        },
        error: function (error) {
            console.log("An error occurred: ", error);
        }
    });
}