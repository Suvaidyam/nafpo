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
            console.log('Call apply filter')
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
    if (frm.is_new()) {
        frm.page.wrapper.find('.btn[data-original-title="Print"], .dropdown-menu [data-label="Print"]').parent().hide()
    } else {
        frm.page.wrapper.find('.btn[data-original-title="Print"], .dropdown-menu [data-label="Print"]').parent().show()
    }
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

// Validate Data field 
function validate_string(frm, field_name, field_label) {
    const field_value = frm.doc[field_name];
    if (typeof field_value === 'string' && isNaN(Number(field_value))) {
        frappe.throw({ message: `Please enter a valid ${field_label}.` });
    }
}
// Validate Mobile NUmber
function validate_mobile_number(mobileNumber, label = "Mobile Number") {
    if (mobileNumber) {
        if (!/^\+?[1-9]\d{1,14}$/.test(mobileNumber) || mobileNumber.length < 10) {
            return frappe.throw({ message: `Please enter a valid ${label}` });
        }
    }

}
// Validate IFSC Code
function validate_IFSC_Code(code) {
    if (code) {
        const ifscRegex = /^[A-Z]{4}0[A-Z0-9]{6}$/;
        if (!ifscRegex.test(code) || code.length > 11) {
            frappe.throw({ message: "Please enter a valid IFSE Code." });
            return false;
        }
        return true;
    }
}

// Validate Aadhar Number
function isValidAadhaar(aadhaarNumber) {
    if (aadhaarNumber.length !== 12 || !/^\d{12}$/.test(aadhaarNumber)) {
        return false;
    }
    var Verhoeff = {
        d: [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
            [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
            [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
            [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
            [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
            [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
            [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
            [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
            [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
        ],
        p: [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
            [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
            [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
            [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
            [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
            [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
            [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
        ],
        j: [0, 4, 3, 2, 1, 5, 6, 7, 8, 9],
        check: function (str) {
            var c = 0;
            str.replace(/\D+/g, "").split("").reverse().join("").replace(/[\d]/g, function (u, i) {
                c = Verhoeff.d[c][Verhoeff.p[i % 8][parseInt(u, 10)]];
            });
            return c === 0;
        }
    };
    return Verhoeff.check(aadhaarNumber);
}


function check_age(age) {
    if (age < 18) {
        frappe.throw({ message: "You must be at least 18 years old to enter this information." })
    } if (age > 120) {
        frappe.throw({ message: "Age cannot be greater than 120." });
    }
}