// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt
const apply_fpo_filter_on_child_crop_name = async (table, crop_name_field) => {
    var child_table = cur_frm.fields_dict[[table]].grid;
    if (child_table) {
        try {
            child_table.get_field([crop_name_field]).get_query = function () {
                return {
                    filters: [
                        ['Crops Name', 'crops_types', '=', cur_frm.doc.type_of_crop || "Type of Crop"]
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
        hide_advance_search(frm, ['state_name', 'fpo', 'type_of_crop'])
        extend_options_length(frm, ['state_name', 'fpo', 'type_of_crop'])
        await apply_filter('fpo', 'state', frm, frm.doc.state_name)
        await apply_filter('type_of_crop', 'single_fpo', frm, frm.doc.fpo)
        // await apply_fpo_filter_on_child_crop_name('table_crop_name_child', 'name_of_crop')
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
        truncate_multiple_fields_value(frm, ['fpo', 'type_of_crop'])
    },
    fpo: function (frm) {
        apply_filter('type_of_crop', 'single_fpo', frm, frm.doc.fpo)
        truncate_multiple_fields_value(frm, ['type_of_crop'])
    },
    onload(frm) {
        hide_list_view_in_useless_data(frm)
    }
});

var change_route = function () {
    frappe.set_route("List", "Crop Name");
}




// frappe.ui.form.on('Crop Name Child', {
//     output_side_add: async function (frm, cdt, cdn) {
//         await apply_fpo_filter_on_child_crop_name('table_crop_name_child', 'name_of_crop')
//     },
//     form_render: async function (frm, cdt, cdn) {
//         await apply_fpo_filter_on_child_crop_name('table_crop_name_child', 'name_of_crop')
//     }
// })
