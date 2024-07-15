// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("BOD KYC", {
    async refresh(frm) {
        await hide_advance_search(frm, ['state_name', 'fpo_name'])
        await extend_options_length(frm, ['state_name', 'fpo_name'])
        await apply_filter('fpo_name', 'state', frm, frm.doc.state_name)
    },
    validate(frm) {
        validate_string(frm, 'mobile_number', 'Mobile Number');
        validate_string(frm, 'aadhar_number', 'Aadhar Number');
    },
    state_name: async function (frm) {
        await apply_filter('fpo_name', 'state', frm, frm.doc.state_name)
        truncate_multiple_fields_value(frm, ['fpo_name'])
    },
    director_identification_number(frm) {
        validate_string(frm, 'director_identification_number', 'Director Identification Number');
    },
    ...['din_document', 'address_proof_status', 'address_proof', 'upload_aadhar_document'].reduce((acc, field) => {
        acc[field] = function (frm) {
            disable_Attachment_autosave(frm);
        };
        return acc;
    }, {})
});