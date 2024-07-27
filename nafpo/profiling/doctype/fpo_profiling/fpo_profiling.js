// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt
let deleted_staff = [];
async function check_exists_fpo(frm) {
    let response = await frappe.call({
        method: "nafpo.apis.api.get_exists_event",
        args: {
            doctype_name: "FPO Profiling",
            filterName: "name_of_the_fpo",
            value: frm.doc.name_of_the_fpo,
        }
    });
    if (response.message) {
        // frm.set_value('fpo', '')
        return frappe.throw({ message: 'This FPO are already exists in FPO Profiling' });
    }
}
frappe.ui.form.on("FPO Profiling", {
    async refresh(frm) {
        await apply_filter('district_name', 'state', frm, frm.doc.state_name)
        await apply_filter('block_name', 'district', frm, frm.doc.district_name)
        await apply_filter('name_of_the_fpo', 'district', frm, frm.doc.district_name)
        await apply_filter('bod_kyc_name', 'fpo_name', frm, frm.doc.name_of_the_fpo)
        // const today = new Date();
        // frm.fields_dict.date_of_expiry_for_fertilizer.$input.datepicker({ maxDate: new Date() });
        // frm.fields_dict.date_of_incorporation.$input.datepicker({ maxDate: today });
        // frm.fields_dict.date_of_registration.$input.datepicker({ maxDate: today });
        // frm.fields_dict.ceo_date_of_joining.$input.datepicker({ maxDate: today });
        // frm.fields_dict.accountant_date_of_joining.$input.datepicker({ maxDate: today });
        // frm.fields_dict.ceo_dob.$input.datepicker({ maxDate: new Date(today.getFullYear() - 18, today.getMonth(), today.getDate()) });
        // frm.fields_dict.accountant_dob.$input.datepicker({ maxDate: new Date(today.getFullYear() - 18, today.getMonth(), today.getDate()) });
        // const expiry_fields = ['date_of_expiry_for_seeds', 'date_of_expiry_for_fertilizer', 'date_of_expiry_for_pesticide', 'date_of_expiry_for_fssai', 'date_of_expiry__for_seed_production'];
        // expiry_fields.forEach(field => {
        //     frm.fields_dict[field].$input.datepicker({ maxDate: today });
        // });
        hide_advance_search(frm, ['bod_kyc_name', 'name_of_cbbo', 'state_name',
            'block_name', 'district_name', 'name_of_the_fpo', 'type_of_organization', 'cbbo'
        ])
        extend_options_length(frm, ['district_name', 'name_of_the_fpo', 'bod_kyc_name', 'name_of_cbbo', 'cbbo'])
    },
    async validate(frm) {
        validate_string(frm, 'fpos_pincode', "FPO's Pincode");
        validate_string(frm, 'contact_detail_of_fpo', "Contact Detail of FPO");
        if (frm.image_uploaded) {
            frappe.validated = false;
            frm.image_uploaded = false;
        }
    },
    fpos_address(frm) {
        validate_string(frm, 'fpos_address', "FPO's Address");
    },
    fpos_pincode(frm) {
        validate_string(frm, 'fpos_pincode', "FPO's Pincode");
    },
    contact_detail_of_fpo(frm) {
        validate_string(frm, 'contact_detail_of_fpo', "Contact Detail of FPO");
    },
    before_save(frm) {
        frm.doc.deleted_staff_rows = deleted_staff;
    },
    state_name: async function (frm) {
        await apply_filter('district_name', 'state', frm, frm.doc.state_name)
        truncate_multiple_fields_value(frm, ['district_name', 'block_name', 'name_of_the_fpo', 'bod_kyc_name'])
    },
    district_name: async function (frm) {
        await apply_filter('block_name', 'district', frm, frm.doc.district_name)
        await apply_filter('name_of_the_fpo', 'district', frm, frm.doc.district_name)
        truncate_multiple_fields_value(frm, ['block_name', 'name_of_the_fpo'])
    },
    block_name: async function (frm) {
        truncate_multiple_fields_value(frm, ['name_of_the_fpo'])
    },
    name_of_the_fpo: async function (frm) {
        await apply_filter('bod_kyc_name', 'fpo_name', frm, frm.doc.name_of_the_fpo)
        // await apply_filter('block_name', 'fpo_name', frm, frm.doc.name_of_the_fpo);
        truncate_multiple_fields_value(frm, ['bod_kyc_name', 'fpos_address', 'fpos_pincode'])
        await check_exists_fpo(frm)
    },
    ...['gst_received_upload', 'license_doc_for_seed', 'license_doc_for_fertilizer', 'license_doc_for_pesticide', 'license_doc_for_fssai', 'licence_doc_for_seed_production', 'fpo_logo', 'supporting_document'].reduce((acc, field) => {
        acc[field] = function (frm) {
            frm.image_uploaded = true;
        };
        return acc;
    }, {})
});

frappe.ui.form.on('Supporting Agencies Child', {
    form_render(frm, cdt, cdn) {
        // $('.row-actions').remove()
    },
    from(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn)
        if (row.from > row.to) {
            row.from = ''
            frappe.show_alert({ message: "From date should be less than To date", indicator: 'red' })
        }
    },
    to(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn)
        if (row.from > row.to) {
            row.to = ''
            frappe.show_alert({ message: "From date should be less than To date", indicator: 'red' })
        }
    }
});
frappe.ui.form.on('FPO Staff Child', {
    form_render(frm, cdt, cdn) {
        $('.grid-duplicate-row').remove()
        let options = ["CEO", "Accountant", "Other Staff"]
        let existing = frm.doc.staff_details_table.map(row => {
            if (row.position_designation != "Other Staff") return row.position_designation
        })
        if (existing.length) {
            options = options.filter(option => !existing.includes(option))
        }
        frm.cur_grid.grid_form.fields_dict.position_designation.set_data(options)
    },
    staff_details_table_remove: function (frm, cdt, cdn) {
        deleted_staff.push(cdn);
    },
    aadhar_no(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        if (typeof row.aadhar_no === 'string' && isNaN(Number(row.aadhar_no))) {
            row.aadhar_no = ''
            frappe.throw({ message: `Please enter a valid Phone No` });
        }
    },
    phone_no(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn)
        if (typeof row.phone_no === 'string' && isNaN(Number(row.phone_no))) {
            row.phone_no = ''
            frappe.throw({ message: `Please enter a valid Phone No` });
        }
    }
});