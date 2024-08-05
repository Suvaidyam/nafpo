// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Capacity", {
    refresh: async function (frm) {
        hide_print_button(frm)
        await apply_filter('fpo_member', 'fpo', frm, frm.doc.fpo)
        await apply_filter('bod_kyc', 'fpo_name', frm, frm.doc.fpo)
        await apply_filter('operation_system', 'fpo', frm, frm.doc.fpo)
        frm.fields_dict.end_date.$input.datepicker({ minDate: new Date(frm.doc.start_date) });

        frm.image_uploaded = false;
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
            } catch (e) {
                console.error('User data fetch error:', e);
            }
        }
        hide_advance_search(frm, ['fpo_member', 'bod_kyc', 'fpo', 'operation_system'])
    },
    validate: function (frm) {
        if (frm.image_uploaded) {
            frappe.validated = false;
            frm.image_uploaded = false;
        }
        if (frm.doc.end_date < frm.doc.start_date) {
            frappe.throw({ message: "End Date Can't be grater then Start Date" })
        }
    },
    fpo(frm) {
        apply_filter('fpo_member', 'fpo', frm, frm.doc.fpo)
        apply_filter('bod_kyc', 'fpo_name', frm, frm.doc.fpo)
        apply_filter('operation_system', 'fpo', frm, frm.doc.fpo)
    },
    fpo_member(frm) {
        if (frm.doc.category == "Membership System (FPO Member)") {
            frm.set_value('no_of_participants', frm.doc.fpo_member ? frm.doc.fpo_member.length : 0);
        }
    },
    bod_kyc(frm) {
        if (frm.doc.category == "Governance System (BOD)") {
            frm.set_value('no_of_participants', frm.doc.bod_kyc ? frm.doc.bod_kyc.length : 0);
        }
    },
    operation_system(frm) {
        if (frm.doc.category == "Operation System (CEO/Account/other staff)") {
            frm.set_value('no_of_participants', frm.doc.operation_system ? frm.doc.operation_system.length : 0);
        }
    },
    other(frm) {
        if (frm.doc.category == "Other") {
            if (frm.doc.other && frm.doc.other.length > 0) {
                frm.set_value('no_of_participants', 1);
            } else {
                frm.set_value('no_of_participants', 0);
            }
        }
    },
    category(frm) {
        frm.set_value('no_of_participants', 0)
        if (frm.doc.category !== "Membership System (FPO Member)") {
            frm.set_value('fpo_member', '')
        }
        if (frm.doc.category !== "Governance System (BOD)") {
            frm.set_value('bod_kyc', '')
        }
        if (frm.doc.category !== "Operation System (CEO/Account/other staff)") {
            frm.set_value('operation_system', '')
        }
        if (frm.doc.category !== "Other") {
            frm.set_value('other', '')
        }
    },

    training_document_if_needed: function (frm) {
        frm.image_uploaded = true;
    },

    start_date(frm) {
        let total_days = Math.ceil(Math.abs(new Date(frm.doc.end_date) - new Date(frm.doc.start_date)) / (1000 * 3600 * 24));
        frm.set_value('total_days', !isNaN(total_days) && total_days >= 0 ? total_days : 0);
        frm.set_df_property('total_days', 'read_only', true);
        frm.fields_dict.end_date.$input.datepicker({ minDate: new Date(frm.doc.start_date) });
        if (frm.doc.end_date < frm.doc.start_date) {
            frm.set_value('total_days', 0);
            frappe.throw({ message: "End Date Can't be grater then Start Date" })
        }
    },
    end_date(frm) {
        let total_days = Math.ceil(Math.abs(new Date(frm.doc.end_date) - new Date(frm.doc.start_date)) / (1000 * 3600 * 24));
        frm.set_value('total_days', !isNaN(total_days) && total_days >= 0 ? total_days : 0);
        frm.set_df_property('total_days', 'read_only', true);
        if (frm.doc.end_date < frm.doc.start_date) {
            frm.set_value('total_days', 0);
            frappe.throw({ message: "End Date Can't be grater then Start Date" })
        }
    },
});



