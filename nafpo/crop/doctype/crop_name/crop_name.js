// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt
const apply_fpo_filter_on_child_crop_name = async (link_doctype_name, table, field_name) => {
    var child_table = cur_frm.fields_dict[[table]].grid;
    if (child_table) {
        try {
            child_table.get_field([field_name]).get_query = function () {
                return {
                    filters: [
                        [link_doctype_name, 'crops_name', '=', cur_frm.doc.crops_name || "Select Crop Name"]
                    ]
                };
            };
        } catch (error) {
            console.error(error)
        }
    }
}

let new_entry = false;
frappe.ui.form.on("Crop Name", {
    async refresh(frm) {
        hide_print_button(frm)
        await apply_filter('fpo', 'state', frm, frm.doc.state_name)
        await apply_filter('crops_name', 'crop_type', frm, frm.doc.crops_types)
        await apply_fpo_filter_on_child_crop_name('Crops Variety', 'crop_variety_table', 'crop_variety');
        hide_advance_search(frm, ['state_name', 'fpo',])
        extend_options_length(frm, ['state_name', 'fpo',])
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
    state_name: function (frm) {
        apply_filter('fpo', 'state', frm, frm.doc.state_name)
        truncate_multiple_fields_value(frm, ['fpo'])
    },
    crops_types: async function (frm) {
        await apply_filter('crops_name', 'crop_type', frm, frm.doc.crops_types)
        truncate_multiple_fields_value(frm, ['crops_name'])
    },
    onload(frm) {
        hide_list_view_in_useless_data(frm)
    }
});

var change_route = function () {
    frappe.set_route("List", "Crop Name");
}




frappe.ui.form.on('Crop Variety Child', {
    output_side_add: async function (frm, cdt, cdn) {
        await apply_fpo_filter_on_child_crop_name('Crops Variety', 'crop_variety_table', 'crop_variety');
    },
    form_render: async function (frm, cdt, cdn) {
        await apply_fpo_filter_on_child_crop_name('Crops Variety', 'crop_variety_table', 'crop_variety');
    }
})