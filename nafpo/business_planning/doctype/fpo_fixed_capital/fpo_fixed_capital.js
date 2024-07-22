// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

async function check_fpo(frm) {
    callAPI({
        method: 'nafpo.apis.api.get_exists_event',
        args: {
            doctype_name: 'FPO Fixed Capital',
            filterName: 'fpo',
            value: frm.doc.fpo,
        },
        freeze: true,
        freeze_message: __("Getting"),
    }).then(response => {
        if (response) {
            // frm.set_value('fpo', '')
            return frappe.throw('This FPO already exists for the Fixed Capital')
        }
    });
}

frappe.ui.form.on("FPO Fixed Capital", {
    async refresh(frm) {
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
        const fixedCapitalItems = [
            "Preoperative Expenses-Registration fee",
            "Hardware & software",
            "Weighing scale & moisture meter",
            "Office Furniture",
            "Computer & accessories"
        ];
        if (frm.is_new()) {
            if (!frm.doc.fixed_capital_details_table || frm.doc.fixed_capital_details_table.length === 0) {
                for (const item of fixedCapitalItems) {
                    frm.add_child('fixed_capital_details_table', { 'item': item });
                }
                frm.refresh_field('fixed_capital_details_table');
            }
        }
    },
    before_save(frm) {
        // check_fpo(frm)
    },
    fpo(frm) {
        check_fpo(frm)
    }
});


frappe.ui.form.on('FPO Fixed Capital Child', {
    value(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        // Initialize data to store the sum
        let data = 0;
        // Loop through the child table and sum the values
        frm.doc.fixed_capital_details_table.forEach(item => {
            data += item.value;
        });
        // Set the total value and refresh the field
        frm.set_value('total_value', data);
        frm.refresh_field('total_value');
    }
})