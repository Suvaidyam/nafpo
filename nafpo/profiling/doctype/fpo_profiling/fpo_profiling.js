// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt
let deleted_staff = [];
const expiry_fields = ['date_of_expiry_for_seeds', 'date_of_expiry_for_fertilizer', 'date_of_expiry_for_pesticide', 'date_of_expiry_for_fssai', 'date_of_expiry__for_seed_production'];
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
        return frappe.throw({ message: 'This FPO are already exists in FPO Profiling' });
    }
}
function validate_expiry_felids(frm) {
    if (expiry_fields.some(field => new Date(frm.doc[field]).setHours(0, 0, 0, 0) < new Date().setHours(0, 0, 0, 0))) {
        frappe.throw({ message: "Date of expiry cannot be a past date. Please select a future date" });
    }
}

async function frize_date(frm) {
    await callAPI({
        method: "nafpo.apis.api.get_exists_event",
        args: {
            doctype_name: 'Annual Compliance Forms',
            filterName: 'fpo',
            value: frm.doc.name_of_the_fpo
        },
        freeze: true,
        freeze_message: __("Getting"),
    }).then(response => {
        if (response) {
            frm.set_df_property('date_of_incorporation', 'read_only', true);
        } else {
            frm.set_df_property('date_of_incorporation', 'read_only', false);
        }
    });
    await callAPI({
        method: "nafpo.apis.api.get_exists_event",
        args: {
            doctype_name: 'FPO MFR 10K',
            filterName: 'fpo',
            value: frm.doc.name
        },
        freeze: true,
        freeze_message: __("Getting"),
    }).then(response => {
        if (response) {
            frm.set_df_property('date_of_registration', 'read_only', true);
        }
    });
}


frappe.ui.form.on("FPO Profiling", {
    async refresh(frm) {
        await apply_filter('district_name', 'state', frm, frm.doc.state_name)
        await apply_filter('block_name', 'district', frm, frm.doc.district_name)
        await apply_filter('name_of_the_fpo', 'district', frm, frm.doc.district_name)
        await apply_filter('bod_kyc_name', 'fpo_name', frm, frm.doc.name_of_the_fpo)
        hide_print_button(frm)
        expiry_fields.forEach(field => {
            frm.fields_dict[field].$input.datepicker({ minDate: new Date() });
        });
        frm.fields_dict.date_of_registration.$input.datepicker({ maxDate: new Date() });
        hide_advance_search(frm, ['bod_kyc_name', 'name_of_cbbo', 'state_name',
            'block_name', 'district_name', 'name_of_the_fpo', 'type_of_organization', 'cbbo'
        ])
        extend_options_length(frm, ['district_name', 'name_of_the_fpo', 'bod_kyc_name', 'name_of_cbbo', 'cbbo'])
        await frize_date(frm)
    },
    async validate(frm) {
        validate_mobile_number(frm.doc.contact_detail_of_fpo, "Contact Detail of FPO")
        if (frm.doc.fpos_pincode) {
            if (frm.doc.fpos_pincode.length < 6) {
                frappe.throw({ message: "Please enter a valid FPO's Pincode." })
            }
        }
        validate_string(frm, 'fpos_pincode', "FPO's Pincode");
        if (frm.image_uploaded) {
            frappe.validated = false;
            frm.image_uploaded = false;
        }
        // if (expiry_fields.some(field => new Date(frm.doc[field]).setHours(0, 0, 0, 0) < new Date().setHours(0, 0, 0, 0))) {
        //     frappe.throw({ message: "Date of expiry cannot be a past date. Please select a future date" });
        // }
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
    date_of_expiry_for_seeds(frm) {
        validate_expiry_felids(frm)
    },
    // date_of_expiry_for_fertilizer(frm) {
    //     validate_expiry_felids(frm)
    // },
    // date_of_expiry_for_pesticide(frm) {
    //     validate_expiry_felids(frm)
    // },
    // date_of_expiry_for_fssai(frm) {
    //     validate_expiry_felids(frm)
    // },
    // date_of_expiry__for_seed_production(frm) {
    //     validate_expiry_felids(frm)
    // },
    name_of_the_fpo: async function (frm) {
        await apply_filter('bod_kyc_name', 'fpo_name', frm, frm.doc.name_of_the_fpo)
        truncate_multiple_fields_value(frm, ['bod_kyc_name', 'fpos_address', 'fpos_pincode'])
        await check_exists_fpo(frm)
        await frize_date(frm)
    },
    ...['gst_received_upload', 'license_doc_for_seed', 'license_doc_for_fertilizer', 'license_doc_for_pesticide', 'license_doc_for_fssai', 'licence_doc_for_seed_production', 'fpo_logo', 'supporting_document'].reduce((acc, field) => {
        acc[field] = function (frm) {
            frm.image_uploaded = true;
        };
        return acc;
    }, {})
});

frappe.ui.form.on('Supporting Agencies Child', {
    from(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn)
        if (row.from > row.to) {
            row.from = ''
            frappe.show_alert({ message: "The 'From' date must be earlier than the 'To' date.", indicator: 'red' })
        }
    },
    to(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn)
        if (row.from > row.to) {
            row.to = ''
            frappe.show_alert({ message: "The 'From' date must be earlier than the 'To' date.", indicator: 'red' })
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
            frappe.throw({ message: `Please enter a valid Aadhar No` });
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