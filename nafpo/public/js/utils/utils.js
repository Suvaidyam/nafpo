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
// Show Print Button
const show_print_button = (frm) => {
    frm.page.wrapper.find('.btn[data-original-title="Print"], .dropdown-menu [data-label="Print"]').parent().show()
}
// Disable autosave on doctype to attach image
function disable_Attachment_autosave(frm) {
    if (this.frm) {
        this.parse_validate_and_set_in_model(frm.file_url)
            .then(function () {
                this.frm.attachments.update_attachment(frm);
            });
    }
    this.set_value(frm.file_url);
}

// Disable autosave on doctype to attach image
function hide_list_view_in_useless_data(frm) {
    const comments_section = frm.wrapper.querySelector('.comment-input-wrapper');
    if (comments_section) {
        comments_section.style.display = 'none';
    }
    const side_section = frm.wrapper.querySelector('.layout-side-section');
    if (side_section) {
        side_section.style.display = 'none';
    }
    const side_section_content = frm.wrapper.querySelector('.form-sidebar');
    if (side_section_content) {
        side_section_content.style.display = 'none';
    }
    const hide_activity = frm.wrapper.querySelector('.timeline-item');
    if (hide_activity) {
        hide_activity.style.display = 'none';
    }
    const hide_activity_timeline = frm.wrapper.querySelector('.new-timeline');
    if (hide_activity_timeline) {
        hide_activity_timeline.style.display = 'none';
    }
    const hide_up_scroll_icon = frm.wrapper.querySelector('.scroll-to-top');
    if (hide_up_scroll_icon) {
        hide_up_scroll_icon.style.display = 'none';
    }
}

// Validate Data field 
function validate_string(frm, field_name, field_label) {
    const field_value = frm.doc[field_name];
    if (typeof field_value === 'string' && isNaN(Number(field_value))) {
        frappe.throw(__(`Please enter a valid ${field_label}.`));
    }
}