// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt

async function check_fpo(frm) {
    await callAPI({
        method: 'nafpo.apis.api.get_exists_event',
        args: {
            doctype_name: 'FPO Fixed Capital',
            filterName: 'fpo',
            value: frm.doc.fpo,
        },
        freeze: true,
        freeze_message: __("Getting"),
    }).then(response => {
        if (response && response != frm.doc.name) {
            // frm.set_value('fpo', '')
            frappe.throw({ message: 'This FPO already exists for the Fixed Capital' })
        }
    });
}

async function frize_date(frm) {
    await callAPI({
        method: "nafpo.apis.api.get_exists_event",
        args: {
            doctype_name: 'Business Plannings',
            filterName: 'fpo',
            value: frm.doc.fpo
        },
        freeze: true,
        freeze_message: __("Getting"),
    }).then(response => {
        if (response) {
            frm.set_df_property('fixed_capital_details_table', 'read_only', true);
        } else {
            frm.set_df_property('fixed_capital_details_table', 'read_only', false);
        }
    });
}

frappe.ui.form.on("FPO Fixed Capital", {
    async refresh(frm) {
        hide_print_button(frm)
        if (frm.doc.fpo) {
            await frize_date(frm)
        }
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
    async fpo(frm) {
        if (frm.doc.fpo) {
            await check_fpo(frm)
            await frize_date(frm)
        }
    }
});


frappe.ui.form.on('FPO Fixed Capital Child', {
    value(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        // Initialize data to store the sum
        let data = 0;
        // Loop through the child table and sum the values
        frm.doc.fixed_capital_details_table.forEach(item => {
            data += (item.value || 0);
        });
        // Set the total value and refresh the field
        frm.set_value('total_value', data);
        frm.refresh_field('total_value');
    }
})