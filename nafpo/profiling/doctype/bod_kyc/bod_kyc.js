// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("BOD KYC", {
    async refresh(frm) {
        await apply_filter('fpo_name', 'state', frm, frm.doc.state_name)
        hide_print_button(frm)
        hide_advance_search(frm, ['state_name', 'fpo_name'])
        extend_options_length(frm, ['state_name', 'fpo_name'])
        frm.fields_dict.date_of_joining.$input.datepicker({ maxDate: new Date() });
    },
    validate(frm) {
        validate_mobile_number(frm.doc.mobile_number)
        if (frm.image_uploaded) {
            frappe.validated = false;
            frm.image_uploaded = false;
        }
        if (new Date(frm.doc.date_of_joining) > new Date()) {
            frappe.throw({ message: "You can't select a future date" });
        }
        check_age(frm.doc.age)
        if (frm.doc.aadhar_number) {
            if (!isValidAadhaar(frm.doc.aadhar_number)) {
                frappe.throw({ message: "Please enter valid Aadhar Number." });
            }
        }
    },
    state_name: async function (frm) {
        await apply_filter('fpo_name', 'state', frm, frm.doc.state_name)
        truncate_multiple_fields_value(frm, ['fpo_name'])
    },
    aadhar_number(frm) {
        validate_string(frm, 'aadhar_number', 'Aadhar Number');
    },
    age(frm) {
        check_age(frm.doc.age)
    },
    mobile_number(frm) {
        validate_string(frm, 'mobile_number', 'Mobile Number');
    },
    date_of_joining(frm) {
        if (new Date(frm.doc.date_of_joining) > new Date()) {
            frappe.throw({ message: "You can't select a future date" });
        }
    },
    ...['din_document', 'address_proof_status', 'address_proof', 'upload_aadhar_document'].reduce((acc, field) => {
        acc[field] = function (frm) {
            frm.image_uploaded = true;
        };
        return acc;
    }, {})
});