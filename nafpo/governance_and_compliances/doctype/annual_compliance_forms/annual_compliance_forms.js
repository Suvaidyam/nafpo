// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt
var adt_report_submitted_on_lock = false;
var adt_1_submitted_on_lock = false;
var agm_submitted_on_lock = false;
var it_return_submitted_on_lock = false;
var aoc_4_submitted_on_lock = false;
var mgt_7_submitted_on_lock = false;
var d_kyc_submitted_on_lock = false;
const submitted_on_fields = ['aoc_4_submitted_on', 'adt_report_submitted_on', 'mgt_7_submitted_on', 'adt_1_submitted_on', 'd_kyc_submitted_on', 'it_return_submitted_on', 'agm_submitted_on'];

async function blank_submitted_on(frm, status_field, date_fields) {
    if (frm.doc[status_field] == "Pending") {
        if (Array.isArray(date_fields)) {
            date_fields.forEach(date_field => frm.set_value(date_field, ''));
        } else {
            frm.set_value(date_fields, '');
        }
    }
}
async function validate_submitted_on(frm, submitted_on_felid_name, due_date_felid_name) {
    frm.fields_dict[submitted_on_felid_name].$input.datepicker({
        minDate: new Date(),
        // maxDate: new Date(frm.doc[due_date_felid_name]),
    });
}

async function set_due_date(frm) {
    let get_fpo_profiling = await callAPI({
        method: "nafpo.apis.api.get_list_event",
        args: {
            doctype_name: 'FPO Profiling',
            filter: { name_of_the_fpo: frm.doc.fpo },
            fields: ['date_of_incorporation']
        },
        freeze: true,
        freeze_message: __("Getting"),
    }).then(response => {
        return response
    });
    let financial_year_date = await callAPI({
        method: 'nafpo.apis.api.get_list_event',
        args: {
            doctype_name: 'Financial Year',
            filter: { name: frm.doc.financial_year },
            fields: ['financial_year_name', 'start_date', 'end_date']
        },
        freeze: true,
        freeze_message: __("Getting"),
    }).then(response => {
        return response
    });
    console.log('get_fpo_profiling :>> ', get_fpo_profiling[0]);
    if (get_fpo_profiling[0] == undefined) {
        frappe.throw({ message: "FPO Profile doesn't exist. Please create FPO Profiling." })
    }
    const get_next_year = financial_year_date[0].start_date.split('-')[0] - get_fpo_profiling[0].date_of_incorporation.split('-')[0]
    if (get_next_year < 0) {
        frm.set_value('financial_year', '')
        frappe.throw({ message: `The date of incorporation is earlier than the financial year.` })
    }
    const [day1, month1] = '01-01'.split('-').map(Number); console
    const [day2, month2] = '31-03'.split('-').map(Number);
    const [day, month] = `${get_fpo_profiling[0].date_of_incorporation.split('-')[2]}-${get_fpo_profiling[0].date_of_incorporation.split('-')[1]}`.split('-').map(Number);

    if ((month > month1 || (month === month1 && day >= day1)) &&
        (month < month2 || (month === month2 && day <= day2))) {
        // Audit report Due Date
        if (get_next_year >= 0) {
            let adt_report_due_date = new Date(financial_year_date[0].end_date);
            adt_report_due_date.setFullYear(adt_report_due_date.getFullYear() + get_next_year + 1);
            frm.set_value('adt_report_due_date', adt_report_due_date.toISOString().split('T')[0])

            // Calculate and set AGM Due Date
            let agm_due_date = new Date(adt_report_due_date);
            agm_due_date.setMonth(agm_due_date.getMonth() + 6);
            agm_due_date.setDate(agm_due_date.getDate() - 1);
            frm.set_value('agm_due_date', agm_due_date.toISOString().split('T')[0]);

            // Calculate and set Form ADT-1 – Auditor Appointment for Five year
            let adt_1_due_date = new Date(agm_due_date.toISOString().split('T')[0])
            adt_1_due_date.setDate(adt_1_due_date.getDate() - 21);
            frm.set_value('adt_1_due_date', adt_1_due_date.toISOString().split('T')[0])

            // Calculate and set INCOME TAX Return
            let updatedYear = parseInt(financial_year_date[0].financial_year_name.split('-')[1], 10) + get_next_year + 1;
            frm.set_value('it_return_due_date', `20${updatedYear}-10-31`)

            // DIRECTOR KYC
            frm.set_value('d_kyc_due_date', `20${financial_year_date[0].financial_year_name.split('-')[1] - 1}-09-30`)
        }

    } else {
        if (get_next_year >= 0) {
            // Audit report Due Date 
            let adt_report_due_date = new Date(financial_year_date[0].end_date);
            adt_report_due_date.setFullYear(adt_report_due_date.getFullYear() + get_next_year);
            frm.set_value('adt_report_due_date', adt_report_due_date.toISOString().split('T')[0])

            // Calculate and set AGM Due Date
            let agm_due_date = new Date(adt_report_due_date);
            agm_due_date.setMonth(agm_due_date.getMonth() + 6);
            agm_due_date.setDate(agm_due_date.getDate() - 1);
            frm.set_value('agm_due_date', agm_due_date.toISOString().split('T')[0]);

            // Calculate and set Form ADT-1 – Auditor Appointment for Five year
            let adt_1_due_date = new Date(agm_due_date.toISOString().split('T')[0])
            adt_1_due_date.setDate(adt_1_due_date.getDate() - 21);
            frm.set_value('adt_1_due_date', adt_1_due_date.toISOString().split('T')[0])

            // Calculate and set INCOME TAX Return
            let it_return_due_date = parseInt(financial_year_date[0].financial_year_name.split('-')[1], 10) + 1
            frm.set_value('it_return_due_date', `20${it_return_due_date}-10-31`)

            // DIRECTOR KYC
            let updatedYear = parseInt(financial_year_date[0].financial_year_name.split('-')[1], 10) + 1;
            frm.set_value('d_kyc_due_date', `20${updatedYear}-09-30`)
        }
    }
}
async function check_ACF(frm) {
    callAPI({
        method: 'nafpo.apis.api.get_list_event',
        args: {
            doctype_name: 'Annual Compliance Forms',
            filter: { fpo: frm.doc.fpo, financial_year: frm.doc.financial_year },
            fields: ['name', 'fpo', 'financial_year'],
            freeze: true,
            freeze_message: __("Getting"),
        },
    }).then(response => {
        if (response[0] && response[0].name !== frm.doc.name) {
            return frappe.throw({ message: `This FPO is already exist with the Financial Year ${response[0].financial_year} ` })
        }
    });
}

frappe.ui.form.on("Annual Compliance Forms", {
    refresh: async function (frm) {
        if (frappe.user.has_role('FPO') && !frappe.user.has_role('Administrator')) {
            try {
                let fpo = await frappe.call({
                    method: "nafpo.apis.api.get_fpo_doc",
                    args: {
                        doctype_name: "NAFPO User",
                        value: frappe.session.user,
                    }
                });
                frm.set_value('fpo', fpo.message.fpo);
            } catch (e) {
                console.error('User data fetch error:', e);
            }
        }
        hide_print_button(frm)
        await validate_submitted_on(frm, 'adt_report_submitted_on', 'adt_report_due_date');
        await validate_submitted_on(frm, 'aoc_4_submitted_on', 'aoc_4_due_date');
        await validate_submitted_on(frm, 'mgt_7_submitted_on', 'mgt_7_due_date');
        await validate_submitted_on(frm, 'adt_1_submitted_on', 'adt_1_due_date');
        await validate_submitted_on(frm, 'd_kyc_submitted_on', 'd_kyc_due_date');
        await validate_submitted_on(frm, 'it_return_submitted_on', 'it_return_due_date');
        await validate_submitted_on(frm, 'agm_submitted_on', 'agm_due_date');
        // submitted_on_fields.forEach(field => {
        //     frm.fields_dict[field].$input.datepicker({ maxDate: new Date() });
        // });
    },
    validate(frm) {
        if (frm.doc.aoc_4_status !== 'Completed' &&
            frm.doc.adt_report_status !== 'Completed' &&
            frm.doc.mgt_7_status !== 'Completed' &&
            frm.doc.adt_1_status !== 'Completed' &&
            frm.doc.d_kyc_status !== 'Completed' &&
            frm.doc.it_return_status !== 'Completed' &&
            frm.doc.agm_status !== 'Completed'
        ) {
            frappe.throw({ message: 'Form Status Not Yet Updated' });
        }
        // if (submitted_on_fields.some(field => new Date(frm.doc[field]).setHours(0, 0, 0, 0) > new Date().setHours(0, 0, 0, 0))) {
        //     frappe.throw({ message: "Submitted On cannot be a future date. Please select a past date" });
        // }
        if (frm.image_uploaded) {
            frappe.validated = false;
            frm.image_uploaded = false;
        }

    },
    before_save(frm) {
        // adt_report_submitted_on_lock = true;
        // adt_1_submitted_on_lock = true;
        // agm_submitted_on_lock = true;
        // it_return_submitted_on_lock = true;
        // aoc_4_submitted_on_lock = true;
        // mgt_7_submitted_on_lock = true;
        // d_kyc_submitted_on_lock = true;
        if (new Date(frm.doc.adt_report_submitted_on) < new Date(new Date().setHours(0, 0, 0, 0) && adt_report_submitted_on_lock == true)) {
            frappe.throw({ message: "Audit Report Submitted On Date can't be earlier than today's date." });
        }
        if (new Date(frm.doc.adt_1_submitted_on) < new Date(new Date().setHours(0, 0, 0, 0)) && adt_1_submitted_on_lock == true) {
            adt_1_submitted_on_lock = false
            frappe.throw({ message: "Submitted On Date can't be earlier than today's date." });
        }
        if (new Date(frm.doc.agm_submitted_on) < new Date(new Date().setHours(0, 0, 0, 0)) && agm_submitted_on_lock == true) {
            frappe.throw({ message: "Submitted On Date can't be earlier than today's date." });
        }
        if (new Date(frm.doc.it_return_submitted_on) < new Date(new Date().setHours(0, 0, 0, 0)) && it_return_submitted_on_lock == true) {
            frappe.throw({ message: "Submitted On Date can't be earlier than today's date." });
        }
        if (new Date(frm.doc.aoc_4_submitted_on) < new Date(new Date().setHours(0, 0, 0, 0)) && aoc_4_submitted_on_lock == true) {
            frappe.throw({ message: "Submitted On Date can't be earlier than today's date." });
        }
        if (new Date(frm.doc.mgt_7_submitted_on) < new Date(new Date().setHours(0, 0, 0, 0)) && mgt_7_submitted_on_lock == true) {
            frappe.throw({ message: "Submitted On Date can't be earlier than today's date." });
        }
        if (new Date(frm.doc.d_kyc_submitted_on) < new Date(new Date().setHours(0, 0, 0, 0)) && d_kyc_submitted_on_lock == true) {
            frappe.throw({ message: "Submitted On Date can't be earlier than today's date." });
        }
    },
    async fpo(frm) {
        if (frm.doc.fpo) {
            if (frm.doc.financial_year) {
                await set_due_date(frm)
                await check_ACF(frm)
            }
        }
    },
    async financial_year(frm) {
        if (frm.doc.financial_year && frm.doc.fpo) {
            await set_due_date(frm)
        }
        if (frm.doc.fpo) {
            await check_ACF(frm)
        }
    },
    agm_submitted_on(frm) {
        // FORM AOC-4 – Filing of Financial Statements
        let aoc_4_due_date = new Date(frm.doc.agm_submitted_on);
        aoc_4_due_date.setMonth(aoc_4_due_date.getMonth() + 1);
        frm.set_value('aoc_4_due_date', aoc_4_due_date.toISOString().split('T')[0]);

        // Form MGT-7 - Filing of Annual Return
        let mgt_7_due_date = new Date(frm.doc.agm_submitted_on);
        mgt_7_due_date.setMonth(mgt_7_due_date.getMonth() + 2);
        frm.set_value('mgt_7_due_date', mgt_7_due_date.toISOString().split('T')[0]);

        // Validate Manual Date Entry 
        if (new Date(frm.doc.agm_submitted_on) < new Date(new Date().setHours(0, 0, 0, 0))) {
            agm_submitted_on_lock = true
            frappe.throw({ message: "Submitted On Date can't be earlier than today's date." });
        }
    },

    async adt_report_status(frm) {
        await blank_submitted_on(frm, 'adt_report_status', ['adt_report_submitted_on', 'audit_report'], 'adt_report_submitted_on', 'adt_report_due_date');
        await validate_submitted_on(frm, 'adt_report_submitted_on', 'adt_report_due_date');
    },
    async aoc_4_status(frm) {
        await blank_submitted_on(frm, 'aoc_4_status', ['aoc_4_submitted_on', 'aoc_4_audit_report'], 'aoc_4_submitted_on', 'aoc_4_due_date');
        await validate_submitted_on(frm, 'aoc_4_submitted_on', 'aoc_4_due_date');
    },
    async mgt_7_status(frm) {
        await blank_submitted_on(frm, 'mgt_7_status', ['mgt_7_submitted_on', 'mgt_7_director_list', 'mgt_7_director_list'], 'mgt_7_submitted_on', 'mgt_7_due_date');
        await validate_submitted_on(frm, 'mgt_7_submitted_on', 'mgt_7_due_date');
    },
    async adt_1_status(frm) {
        await blank_submitted_on(frm, 'adt_1_status', ['adt_1_submitted_on', 'adt_1_fpo_resolution'], 'adt_1_submitted_on', 'adt_1_due_date');
        await validate_submitted_on(frm, 'adt_1_submitted_on', 'adt_1_due_date');
    },
    async d_kyc_status(frm) {
        await blank_submitted_on(frm, 'd_kyc_status', ['d_kyc_submitted_on', 'd_kyc_pan_card_verification', 'd_kyc_otp', 'd_kyc_bod_aadhar'], 'd_kyc_submitted_on', 'd_kyc_due_date');
        await validate_submitted_on(frm, 'd_kyc_submitted_on', 'd_kyc_due_date');
    },
    async it_return_status(frm) {
        await blank_submitted_on(frm, 'it_return_status', ['it_return_submitted_on', 'it_return'], 'it_return_submitted_on', 'it_return_due_date');
        await validate_submitted_on(frm, 'it_return_submitted_on', 'it_return_due_date');
    },
    async agm_status(frm) {
        await blank_submitted_on(frm, 'agm_status', 'agm_submitted_on', 'agm_submitted_on', 'agm_due_date');
        await validate_submitted_on(frm, 'agm_submitted_on', 'agm_due_date');
    },
    adt_report_submitted_on(frm) {
        if (new Date(frm.doc.adt_report_submitted_on) < new Date(new Date().setHours(0, 0, 0, 0))) {
            adt_report_submitted_on_lock = true
            frappe.throw({ message: "Audit Report Submitted On Date can't be earlier than today's date." });
        }
    },
    adt_1_submitted_on(frm) {
        if (new Date(frm.doc.adt_1_submitted_on) < new Date(new Date().setHours(0, 0, 0, 0))) {
            adt_1_submitted_on_lock = true
            frappe.throw({ message: "Submitted On Date can't be earlier than today's date." });
        }
    },
    // agm_submitted_on(frm) {
    //     if (new Date(frm.doc.agm_submitted_on) < new Date(new Date().setHours(0, 0, 0, 0))) {
    //         agm_submitted_on_lock = true
    //         frappe.throw({ message: "Submitted On Date can't be earlier than today's date." });
    //     }
    // },
    it_return_submitted_on(frm) {
        if (new Date(frm.doc.it_return_submitted_on) < new Date(new Date().setHours(0, 0, 0, 0))) {
            it_return_submitted_on_lock = true
            frappe.throw({ message: "Submitted On Date can't be earlier than today's date." });
        }
    },
    aoc_4_submitted_on(frm) {
        if (new Date(frm.doc.aoc_4_submitted_on) < new Date(new Date().setHours(0, 0, 0, 0))) {
            aoc_4_submitted_on_lock = true
            frappe.throw({ message: "Submitted On Date can't be earlier than today's date." });
        }
    },
    mgt_7_submitted_on(frm) {
        if (new Date(frm.doc.mgt_7_submitted_on) < new Date(new Date().setHours(0, 0, 0, 0))) {
            mgt_7_submitted_on_lock = true
            frappe.throw({ message: "Submitted On Date can't be earlier than today's date." });
        }
    },
    d_kyc_submitted_on(frm) {
        if (new Date(frm.doc.d_kyc_submitted_on) < new Date(new Date().setHours(0, 0, 0, 0))) {
            d_kyc_submitted_on_lock = true
            frappe.throw({ message: "Submitted On Date can't be earlier than today's date." });
        }
    },
    ...['aoc_4_audit_report', 'audit_report', 'mgt_7_director_list', 'mgt_7_shareholder_list', 'adt_1_fpo_resolution', 'd_kyc_bod_aadhar', 'd_kyc_pan_card_verification', 'd_kyc_otp', 'it_return'].reduce((acc, field) => {
        acc[field] = function (frm) {
            frm.image_uploaded = true;
        };
        return acc;
    }, {})
});
