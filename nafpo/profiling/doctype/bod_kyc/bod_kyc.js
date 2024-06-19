// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("BOD KYC", {
    async refresh(frm) {
        await hide_advance_search(frm, ['state_name', 'fpo_name'])
        await extend_options_length(frm, ['state_name', 'fpo_name'])
        await apply_filter('fpo_name', 'state', frm, frm.doc.state_name)
    },
    validate(frm) {
        validate_numeric_field(frm, 'mobile_number', 'Mobile Number');
        validate_numeric_field(frm, 'aadhar_number', 'Aadhar Number');
    },
    state_name: async function (frm) {
        await apply_filter('fpo_name', 'state', frm, frm.doc.state_name)
        truncate_multiple_fields_value(frm, ['fpo_name'])
    },
    mobile_number(frm) {
        validate_numeric_field(frm, 'mobile_number', 'Mobile Number');
    },
    aadhar_number(frm) {
        validate_numeric_field(frm, 'aadhar_number', 'Aadhar Number');
    },
    onload(frm) {
        hide_list_view_in_useless_data(frm)
    },
    ...['din_document', 'address_proof_status', 'address_proof', 'upload_aadhar_document'].reduce((acc, field) => {
        acc[field] = function (frm) {
            disable_Attachment_autosave(frm);
        };
        return acc;
    }, {})
});

function validate_numeric_field(frm, field_name, field_label) {
    const field_value = frm.doc[field_name];
    if (typeof field_value === 'string' && isNaN(Number(field_value))) {
        frappe.throw(__(`Please enter a valid ${field_label}.`));
        frm.set_value(field_name, '');
    }
}
