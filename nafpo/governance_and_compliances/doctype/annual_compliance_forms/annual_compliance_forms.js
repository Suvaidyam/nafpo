// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Annual Compliance Forms", {
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
        const submitted_on_fields = ['aoc_4_submitted_on', 'mgt_7_submitted_on', 'adt_1_submitted_on', 'd_kyc_submitted_on', 'it_return_submitted_on', 'agm_submitted_on'];
        submitted_on_fields.forEach(field => {
            frm.fields_dict[field].$input.datepicker({ maxDate: new Date() });
        });
    },
    fpo(frm) {
        set_due_date(frm)
    },
    aoc_4_status(frm) {
        blank_submitted_on(frm, 'aoc_4_status', 'aoc_4_submitted_on');
    },
    mgt_7_status(frm) {
        blank_submitted_on(frm, 'mgt_7_status', 'mgt_7_submitted_on');
    },
    adt_1_status(frm) {
        blank_submitted_on(frm, 'adt_1_status', 'adt_1_submitted_on');
    },
    d_kyc_status(frm) {
        blank_submitted_on(frm, 'd_kyc_status', 'd_kyc_submitted_on');
    },
    it_return_status(frm) {
        blank_submitted_on(frm, 'it_return_status', 'it_return_submitted_on');
    },
    agm_status(frm) {
        blank_submitted_on(frm, 'agm_status', 'agm_submitted_on');
    },
    ...['aoc_4_audit_report', 'mgt_7_director_list', 'mgt_7_shareholder_list', 'adt_1_fpo_resolution', 'd_kyc_bod_aadhar', 'd_kyc_pan_card_verification', 'd_kyc_otp', 'it_return'].reduce((acc, field) => {
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
            date.setFullYear(date.getFullYear() + 1);
            let formattedDate = date.toISOString().split('T')[0];
            frm.set_value('aoc_4_due_date', formattedDate);
            frm.set_value('mgt_7_due_date', formattedDate);
            frm.set_value('adt_1_due_date', formattedDate);
            frm.set_value('d_kyc_due_date', formattedDate);
            frm.set_value('it_return_due_date', formattedDate);
            frm.set_value('agm_due_date', formattedDate);
        },
        error: function (error) {
            console.log("An error occurred: ", error);
        }
    });
}