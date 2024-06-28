// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

// async function set_bod_kyc_name(frm) {
//     if (frm.doc.category === "Governance System (BOD)") {
//         try {
//             let response = await callAPI({
//                 method: "nafpo.apis.api.get_fpo_profile",
//                 args: {
//                     name: frm.doc.fpo,
//                 }
//             });
//             if (Array.isArray(response)) {
//                 let extractedValue = response[0];
//                 if (extractedValue) {
//                     frm.set_value('bod_kyc_name', extractedValue);
//                 } else {
//                     console.warn('No valid data found in the response.');
//                 }
//             } else {
//                 frm.set_value('bod_kyc_name', response);
//             }
//         } catch (error) {
//             console.error('Error fetching data:', error);
//         }
//     }
// }

frappe.ui.form.on("Capacity", {
    refresh: async function (frm) {
        if (frappe.user.has_role('FPO') && !frappe.user.has_role('Administrator')) {
            try {
                let { message: { fpo } } = await frappe.call({
                    method: "frappe.client.get",
                    args: { doctype: "Nafpo User", name: frappe.session.user }
                });
                frm.set_value('fpo', fpo)
            } catch (e) {
                console.error('User data fetch error:', e);
            }
        }
        hide_advance_search(frm, ['fpo_member', 'bod_kyc', 'fpo', 'operation_system'])
    },
    category(frm) {
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
    start_date(frm) {
        let total_days = Math.ceil(Math.abs(new Date(frm.doc.end_date) - new Date(frm.doc.start_date)) / (1000 * 3600 * 24));
        console.log('total_days', total_days)
        frm.set_value('total_days', !isNaN(total_days) && total_days >= 0 ? total_days : 0);
        frm.set_df_property('total_days', 'read_only', true);
    },
    end_date(frm) {
        frm.fields_dict.end_date.$input.datepicker({ minDate: new Date(frm.doc.start_date) });
        let total_days = Math.ceil(Math.abs(new Date(frm.doc.end_date) - new Date(frm.doc.start_date)) / (1000 * 3600 * 24));
        frm.set_value('total_days', !isNaN(total_days) && total_days >= 0 ? total_days : 0);
        frm.set_df_property('total_days', 'read_only', true);
    },
    onload: function (frm) {
        hide_list_view_in_useless_data(frm)
    },
    ...['training_document_if_needed'].reduce((acc, field) => {
        acc[field] = function (frm) {
            disable_Attachment_autosave(frm);
        };
        return acc;
    }, {})
});