// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

async function apply_filter(field_name, filter_on, frm, filter_value, multiSelectParent = false) {
    frm.fields_dict[field_name].get_query = () => {
        if (multiSelectParent) {
            let values = filter_value.map(val => val[filter_on]) || frm.doc[filter_on].map(val => val[filter_on]);
            return {
                filters: [
                    [filter_on, 'IN', values],
                ],
                page_length: 1000
            };
        } else {
            let filter = filter_value || frm.doc[filter_on] || `please select ${filter_on}`;
            return {
                filters: {
                    [filter_on]: filter,
                },
                page_length: 1000
            };
        }
    };
};

let new_entry = false;
frappe.ui.form.on("Crop Type", {
    refresh(frm) {
        hide_advance_search(frm, ['state', 'fpo', 'single_state', 'single_fpo'])
        extend_options_length(frm, ['state', 'fpo', 'single_state', 'single_fpo'])
        apply_filter('fpo', 'state', frm, frm.doc.state, multiSelectParent = true)
        apply_filter('single_fpo', 'state', frm, frm.doc.single_state)
    },
    before_save: function (frm) {
        if (frm.doc.__islocal) {
            new_entry = true;
        } else {
            new_entry = false;
        }
    },
    after_save: function () {
        if (new_entry) {
            change_route();
        }
    },
    state: function (frm) {
        apply_filter('fpo', 'state', frm, frm.doc.state, multiSelectParent = true)
        truncate_multiple_fields_value(frm, ['fpo'])
    },
    single_state: function (frm) {
        apply_filter('single_fpo', 'state', frm, frm.doc.single_state)
        truncate_multiple_fields_value(frm, ['single_fpo'])
    },
});

var change_route = function () {
    frappe.set_route("List", "Crop Type");
}