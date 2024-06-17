// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("FPO Profiling", {
    async refresh(frm) {
        const today = new Date();
        frm.fields_dict.date_of_incorporation.$input.datepicker({ maxDate: today });
        frm.fields_dict.ceo_date_of_joining.$input.datepicker({ maxDate: today });
        frm.fields_dict.accountant_date_of_joining.$input.datepicker({ maxDate: today });
        frm.fields_dict.ceo_dob.$input.datepicker({ maxDate: new Date(today.getFullYear() - 18, today.getMonth(), today.getDate()) });
        frm.fields_dict.accountant_dob.$input.datepicker({ maxDate: new Date(today.getFullYear() - 18, today.getMonth(), today.getDate()) });
        const expiry_fields = ['date_of_expiry_for_seeds', 'date_of_expiry_for_fertilizer', 'date_of_expiry_for_pesticide', 'date_of_expiry_for_fssai', 'date_of_expiry__for_seed_production'];
        expiry_fields.forEach(field => {
            frm.fields_dict[field].$input.datepicker({ maxDate: today });
        });
        hide_advance_search(frm, ['bod_kyc_name', 'name_of_cbbo', 'state_name',
            'block_name', 'district_name', 'name_of_the_fpo', 'type_of_organization'
        ])
        extend_options_length(frm, ['fpo_name', 'fpo_name', 'district_name', 'name_of_the_fpo', 'bod_kyc_name', 'name_of_cbbo', 'cbbo'])
        await apply_filter('district_name', 'state', frm, frm.doc.state_name)
        await apply_filter('block_name', 'district', frm, frm.doc.district_name)
        await apply_filter('name_of_the_fpo', 'block', frm, frm.doc.block_name, true)
        await apply_filter('bod_kyc_name', 'fpo_name', frm, frm.doc.name_of_the_fpo)
    },
    validate(frm) {
        integer_length_validator(frm.doc.accountant_contact_number, 10, 'Accountant Contact Number');
        integer_length_validator(frm.doc.ceo_contact_number, 10, 'CEO Contact Number');
    },
    state_name: async function (frm) {
        await apply_filter('district_name', 'state', frm, frm.doc.state_name)
        truncate_multiple_fields_value(frm, ['district_name', 'block_name', 'name_of_the_fpo', 'bod_kyc_name'])
    },
    district_name: async function (frm) {
        await apply_filter('block_name', 'district', frm, frm.doc.district_name)
        truncate_multiple_fields_value(frm, ['block_name', 'name_of_the_fpo'])
    },
    block_name: async function (frm) {
        await apply_filter('name_of_the_fpo', 'block', frm, frm.doc.block_name, true)
        truncate_multiple_fields_value(frm, ['name_of_the_fpo'])
    },
    name_of_the_fpo: async function (frm) {
        await apply_filter('bod_kyc_name', 'fpo_name', frm, frm.doc.name_of_the_fpo)
        truncate_multiple_fields_value(frm, ['bod_kyc_name', 'fpos_address', 'fpos_pincode'])
    },
    ceo_contact_number(frm) {
        integer_length_validator(frm.doc.ceo_contact_number, 10, 'CEO Contact Number');
    },
    accountant_contact_number(frm) {
        integer_length_validator(frm.doc.accountant_contact_number, 10, 'Accountant Contact Number');
    },
    onload(frm) {
        hide_list_view_in_useless_data(frm)
    },
    ...['gst_received_upload', 'license_doc_for_seed', 'license_doc_for_fertilizer', 'license_doc_for_pesticide', 'license_doc_for_fssai', 'licence_doc_for_seed_production', 'fpo_logo', 'supporting_document'].reduce((acc, field) => {
        acc[field] = function (frm) {
            disable_Attachment_autosave(frm);
        };
        return acc;
    }, {})
});
