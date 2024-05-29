// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

frappe.ui.form.on("Training Material", {
    refresh(frm) {
        hide_advance_search(frm, ['state', 'district', 'block', 'fpo', 'category', 'language_of_training_material', 'language_of_module'])
        extend_options_length(frm, ['state', 'district', 'block', 'fpo', 'category', 'language_of_training_material', 'language_of_module'])
        apply_filter('district', 'state', frm, frm.doc.state)
        apply_filter('block', 'district', frm, frm.doc.district)
        apply_filter('fpo', 'block', frm, frm.doc.block)
        frm.trigger('category')
        frm.set_df_property('training_content_table', 'cannot_delete_rows', true);
        frm.set_df_property('training_content_table', 'cannot_add_rows', true);
    },
    validate(frm) {
        if (frm.doc.duration_of_training_in_days > 30) {
            frappe.throw(`Count of Duration of Training (In days) can't be more than 30 digits!`)
        }
    },
    state: function (frm) {
        apply_filter('district', 'state', frm, frm.doc.state)
        truncate_multiple_fields_value(frm, ['district', 'block', 'fpo'])
    },
    district: function (frm) {
        apply_filter('block', 'district', frm, frm.doc.district)
        truncate_multiple_fields_value(frm, ['block', 'fpo'])
    },
    block: function (frm) {
        apply_filter('fpo', 'block', frm, frm.doc.block)
        truncate_multiple_fields_value(frm, ['fpo'])
    },
    category(frm) {
        if (frm.doc.category.length > 0 && frm.doc.category.map(e => { return e.category }).includes("Other")) {
            frm.set_df_property('other_category', 'hidden', 0)
            frm.set_df_property('other_category', 'reqd', 1)
        } else {
            frm.set_df_property('other_category', 'hidden', 1)
            frm.set_df_property('other_category', 'reqd', 0)
        }
    },
    duration_of_training_in_days(frm) {
        if (frm.doc.duration_of_training_in_days > 30) {
            frappe.throw(`Count of Duration of Training (In days) can't be more than 30`)
        }
    },
    no_of_sessions(frm) {
        let doc = {
            doctype: "Training Content Child",
            owner: frappe.session.user,
            parent: "new-training-material-kxkjpffbso",
            parentfield: "training_content_table",
            parenttype: "Training Material",
            __islocal: 1,
            __unedited: true,
            __unsaved: 1
        };
        if (frm.doc.no_of_sessions && !isNaN(frm.doc.no_of_sessions) && frm.doc.no_of_sessions <= 20) {
            let items = new Array(frm.doc.no_of_sessions).fill('doc')
            let docs = []
            for (item in items) {
                doc.idx = item + 1
                docs.push(doc)
            }
            frm.set_value('training_content_table', docs)
        } else if (frm.doc.no_of_sessions) {
            frm.set_value('no_of_sessions', 20)
        } else {
            frm.set_value('training_content_table', [])
        }
    }
});
// frappe.ui.form.on('Training Content Child', {
//     training_content_table_add: function (frm) {
//     }
// })
