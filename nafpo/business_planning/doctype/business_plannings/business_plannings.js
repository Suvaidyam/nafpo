// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt
const apply_fpo_filter_on_child_crop_name = async (table, crop_name_field) => {
    var child_table = cur_frm.fields_dict[[table]].grid;
    if (child_table) {
        try {
            child_table.get_field([crop_name_field]).get_query = function () {
                return {
                    filters: [
                        ['Crop Name', 'fpo', '=', cur_frm.doc.fpo || "Select FPO"]
                    ]
                };
            };
        } catch (error) {
            console.error(error)
        }
    }
}
frappe.ui.form.on("Business Plannings", {
    async refresh(frm) {
        filter_financial_year('financial_year_name', 'Financial Year', frm)
        apply_filter('operation_system', 'fpo', frm, frm.doc.financial_year)
        await apply_fpo_filter_on_child_crop_name('output_side', 'crop_name')
        await apply_fpo_filter_on_child_crop_name('input_side', 'crop_name')
    },
    async fpo(frm) {
        await apply_fpo_filter_on_child_crop_name('output_side', 'crop_name')
        await apply_fpo_filter_on_child_crop_name('input_side', 'crop_name')
    },
    onload: function (frm) {
        filter_financial_year('financial_year', 'start_date', frm)
    }
});
async function filter_financial_year(field_name, filter_on, frm) {
    var currentYear = new Date().getFullYear();
    var startYear = currentYear - 2;
    var endYear = currentYear + 4;

    frm.fields_dict[field_name].get_query = () => {
        return {
            filters: [
                [filter_on, 'BETWEEN', [`${startYear}-04-01`, `${endYear}-3-31`]]
            ],
            page_length: 1000
        };
    };
};

frappe.ui.form.on('Output Side Child', {
    output_side_add: async function (frm, cdt, cdn) {
        await apply_fpo_filter_on_child_crop_name('output_side', 'crop_name')
    },
    form_render: async function (frm, cdt, cdn) {
        await apply_fpo_filter_on_child_crop_name('output_side', 'crop_name')
    },
    item_code(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
    },
    quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        if (row.total_harvest_by_fpo_members_quintals < row.quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals) {
            row.quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals = ''
            frappe.throw('Quantity of produce to be bought by FPO for marketing cannot exceed the total harvest by FPO members.');
        }
    },

})

frappe.ui.form.on('Input Side Child', {
    input_side_add: async function (frm, cdt, cdn) {
        await apply_fpo_filter_on_child_crop_name('input_side', 'crop_name')
    },
    form_render: async function (frm, cdt, cdn) {
        await apply_fpo_filter_on_child_crop_name('input_side', 'crop_name')
    },
    item_code(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
    },
    percentage_of_total_cropping_area(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        if (row.percentage_of_total_cropping_area < 0 || row.percentage_of_total_cropping_area > 100) {
            row.percentage_of_total_cropping_area = ''
            frappe.throw('Percentage of Total Cropping Area for which Input Name Shall be Provided By FPO Cannot less than 0 and cannot greater than 100');
        }
    }
})

