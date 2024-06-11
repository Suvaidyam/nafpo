// This Function Hide Advance search option in Link Fields
const hide_advance_search = (frm, list) => {
    for (item of list) {
        frm.set_df_property(item, 'only_select', true);
    }
};
//  This Function extend limit of Link field in dropdowns
const extend_options_length = (frm, fields) => {
    fields?.forEach((field) => {
        frm.set_query(field, () => {
            return { page_length: 1000 };
        });
    })
};

// this function apply filter
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

//  This Fields delete fields values
async function truncate_multiple_fields_value(_frm, fields) {
    for (field of fields) {
        _frm.set_value(field, '')
    }
}
// Calling APIs Common function
function callAPI(options) {
    return new Promise((resolve, reject) => {
        frappe.call({
            ...options,
            callback: async function (response) {
                resolve(response?.message || response?.value)
            }
        });
    })
}

// Integer length validator
const integer_length_validator = (value, reqd_length, label) => {
    if (value && String(value).length > reqd_length) {
        frappe.throw(`${label} can't be more than ${reqd_length} digits!`)
    }
}

// Hide Print Button
const hide_print_button = (frm) => {
    frm.page.wrapper.find('.btn[data-original-title="Print"], .dropdown-menu [data-label="Print"]').parent().hide()
}
// Hide Print Button
const show_print_button = (frm) => {
    frm.page.wrapper.find('.btn[data-original-title="Print"], .dropdown-menu [data-label="Print"]').parent().show()
}