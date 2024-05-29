// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Crop POP", {
    refresh(frm) {
        hide_advance_search(frm, ['state', 'district', 'block', 'fpo', 'crop_type', 'crop_name'])
        extend_options_length(frm, ['state', 'district', 'block', 'fpo', 'crop_type', 'crop_name'])
        apply_filter('district', 'state', frm, frm.doc.state)
        apply_filter('block', 'district', frm, frm.doc.district)
        apply_filter('fpo', 'block', frm, frm.doc.block)
        apply_filter('crop_type', 'fpo', frm, frm.doc.fpo)
        apply_filter('crop_name', 'type_of_crop', frm, frm.doc.crop_type)
        frm.set_df_property('crop_practice_table', 'cannot_delete_rows', true);
        frm.set_df_property('crop_practice_table', 'cannot_add_rows', true);
        frm.set_df_property('pest_diagnostic_management_table', 'cannot_delete_rows', true);
        frm.set_df_property('pest_diagnostic_management_table', 'cannot_add_rows', true);
    },
    validate(frm) {
        if (frm.doc.duration_of_the_crop_in_days > 365) {
            frappe.throw(`Duration of the Crop (In Days) must be no greater than 365.`)
        }
    },
    state: function (frm) {
        apply_filter('district', 'state', frm, frm.doc.state)
        truncate_multiple_fields_value(frm, ['district', 'block', 'fpo', 'crop_type', 'crop_name'])
    },
    district: function (frm) {
        apply_filter('block', 'district', frm, frm.doc.district)
        truncate_multiple_fields_value(frm, ['block', 'fpo', 'crop_type', 'crop_name'])
    },
    block: function (frm) {
        apply_filter('fpo', 'block', frm, frm.doc.block)
        truncate_multiple_fields_value(frm, ['fpo', 'crop_type', 'crop_name'])
    },
    fpo: function (frm) {
        apply_filter('crop_type', 'fpo', frm, frm.doc.fpo)
        truncate_multiple_fields_value(frm, ['crop_type', 'crop_name'])
    },
    crop_type: function (frm) {
        apply_filter('crop_name', 'type_of_crop', frm, frm.doc.crop_type)
        truncate_multiple_fields_value(frm, ['crop_name'])
    },
    duration_of_the_crop_in_days(frm) {
        if (frm.doc.duration_of_the_crop_in_days > 365) {
            return frappe.throw(`Duration of the Crop (In Days) must be no greater than 365.`)
        }
    },
    no_of_practise(frm) {
        console.log(frappe.session.user);
        let doc = {
            docstatus: 0,
            doctype: "Crop Best Practice Child",
            idx: 1,
            name: "new-crop-best-practice-child-dovdaejply",
            owner: frappe.session.user,
            parent: "new-crop-pop-naxzairvoz",
            parentfield: "crop_practice_table",
            parenttype: "Crop POP",
            __islocal: 1,
            __unedited: true,
            __unsaved: 1
        };
        if (frm.doc.no_of_practise && !isNaN(frm.doc.no_of_practise) && frm.doc.no_of_practise <= 20) {
            let items = new Array(frm.doc.no_of_practise).fill('doc')
            let docs = []
            for (item in items) {
                doc.idx = item + 1
                docs.push(doc)
            }
            frm.set_value('crop_practice_table', docs)
        } else if (frm.doc.no_of_practise) {
            frm.set_value('no_of_practise', 20)
        } else {
            frm.set_value('crop_practice_table', [])
        }
    },
    number_of_damages_to_be_posted(frm) {
        let doc = {
            docstatus: 0,
            doctype: "Pest Diagnostic and Management Child",
            idx: 1,
            name: "new-pest-diagnostic-and-management-child-bvflyqreis",
            owner: "Administrator",
            parent: "new-crop-pop-pgtpntcexc",
            parentfield: "pest_diagnostic_management_table",
            parenttype: "Crop POP",
            __islocal: 1,
            __unedited: true,
            __unsaved: 1
        };
        if (frm.doc.number_of_damages_to_be_posted && !isNaN(frm.doc.number_of_damages_to_be_posted) && frm.doc.number_of_damages_to_be_posted <= 20) {
            let items = new Array(frm.doc.number_of_damages_to_be_posted).fill('doc')
            let docs = []
            for (item in items) {
                doc.idx = item + 1
                docs.push(doc)
            }
            frm.set_value('pest_diagnostic_management_table', docs)
        } else if (frm.doc.number_of_damages_to_be_posted) {
            frm.set_value('number_of_damages_to_be_posted', 20)
        } else {
            frm.set_value('pest_diagnostic_management_table', [])
        }
    }
});

// frappe.ui.form.on('Crop Best Practice Child', {
//     crop_practice_table_add: function (frm) {
//         console.log('frm.doc.crop_practice_table :>> ', frm.doc.crop_practice_table);
//     }
// })

// frappe.ui.form.on('Pest Diagnostic and Management Child', {
//     pest_diagnostic_management_table_add: function (frm) {
//         console.log('frm.doc.pest_diagnostic_management_table :>> ', frm.doc.pest_diagnostic_management_table);
//     }
// })
