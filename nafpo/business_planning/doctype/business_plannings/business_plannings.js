// Copyright (c) 2024, dhwaniris and contributors
// For license information, please see license.txt
// Filter Child Table
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
// Check FPO
async function check_capital_for_fpo(frm) {
    await callAPI({
        method: 'nafpo.apis.api.get_list_event',
        args: {
            doctype_name: "FPO Fixed Capital",
            filter: { fpo: frm.doc.fpo },
            fields: ['total_value']
        },
        freeze: true,
        freeze_message: __("Getting"),
    }).then(response => {
        if (response[0] == undefined) {
            console.log('object :>> ', 'object');
            frappe.throw({ message: 'Please create FPO Fixed Capital for this FPO' });
        }
        frm.set_value('depreciation', response[0].total_value / frm.doc.depreciation_percent)
    });
}
// Closing Cash Balance
async function get_closing_cash_balance(frm) {
    await callAPI({
        method: 'nafpo.apis.api.get_list_event',
        args: {
            doctype_name: "Business Plannings",
            filter: {
                'fpo': frm.doc.fpo,
                'financial_year': ['<', frm.doc.financial_year]
            },
            fields: ['fpo', 'financial_year', 'gross_profit_loss'],
        },
        freeze: true,
        freeze_message: __("Getting"),
    }).then(response => {
        console.log('response Data:>> ', response);
        let store_gross_profit_loss = 0;

        for (let gross_profit of response) {
            store_gross_profit_loss += gross_profit.gross_profit_loss;
        }

        let closing_cash_balance = store_gross_profit_loss + frm.doc.gross_profit_loss;
        frm.set_value('closing_cash_balance', closing_cash_balance);
    });
}

// Fixed Cost (yearly)
async function add_total_work_capital(frm) {
    const data = (
        (frm.doc.ceo_salary || 0) +
        (frm.doc.accountant_salary || 0) +
        (frm.doc.store_keeper_salary || 0) +
        (frm.doc.staff_travel || 0) +
        (frm.doc.store_rent || 0) +
        (frm.doc.office_rent || 0) +
        (frm.doc.utilities || 0) +
        (frm.doc.miscellanious || 0) +
        (frm.doc.collection_centre_rent || 0) +
        (frm.doc.intangible_assetspre_operating_expenses_written_off || 0) +
        (frm.doc.depreciation || 0) +
        (frm.doc.interest_on_loan || 0)
    );
    frm.set_value('total_work_capital', data)
}
// # Variable Cost Logic
async function variable_cost_logic(frm) {
    await frm.set_value('gradingassying_weigning_packingbagging_at_collection_point', frm.doc.quantity_available_for_sale_after_weight_loss * frm.doc.gradingassying_weigning_packingbagging_at_collection_point_rate)
    await frm.set_value('local_transport_include_loading_unloading_collection_point', frm.doc.quantity_available_for_sale_after_weight_loss * frm.doc.local_transport_include_loading_unloading_rate)
    await frm.set_value('storing_warehousing_costs', frm.doc.quantity_available_for_sale_after_weight_loss * frm.doc.storing_warehousing_costs_rate)
    await frm.set_value('transport_to_market_include_loading__unloading', frm.doc.quantity_available_for_sale_after_weight_loss * frm.doc.transport_to_market_include_loading_unloading_rate)
    frm.set_value('total_variable_cost', (
        frm.doc.gradingassying_weigning_packingbagging_at_collection_point +
        frm.doc.local_transport_include_loading_unloading_collection_point +
        frm.doc.storing_warehousing_costs +
        frm.doc.transport_to_market_include_loading__unloading
    ))
}
async function net_profit_logic(frm) {
    // # Total Sales
    frm.set_value('total_sales', frm.doc.total_output_selling_priceincome_rs + frm.doc.total_input_selling_priceincome_rs)
    // # Total Expense
    frm.set_value('total_expense', frm.doc.total_variable_cost + frm.doc.total_work_capital + frm.doc.total_output_purchase_price_rs + frm.doc.total_input_purchase_price_rs)
    // # Gross Profit / Loss(Total Sales - Total Expence)
    frm.set_value('gross_profit_loss', frm.doc.total_sales - frm.doc.total_expense)

    // # Total Income(Including Input and Output Side)
    frm.set_value('total_income_including_input_and_output_side', frm.doc.total_income_of_fpo_from_output + frm.doc.total_income_of_fpo_from_input)
    // # Total Fixed and Variable Cost
    frm.set_value('total_fixed_and_variable_cost', frm.doc.total_variable_cost + frm.doc.total_work_capital)
    // # Gross Profit / Loss(Total Income - Total Cost)
    frm.set_value('gross_profit_loss_total_income_total_cost', frm.doc.total_income_including_input_and_output_side - frm.doc.total_fixed_and_variable_cost)
}
// Financial Year
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

// ====================================== Projected Cash Flow Functions ======================================
async function calculate_mens_of_finance(frm) {
    frm.set_value('total',
        (frm.doc.total_subsidy_grant_for_capex || 0) +
        (frm.doc.grant__for_salary_travel || 0) +
        (frm.doc.share_capital || 0) +
        (frm.doc.equity_grant || 0) +
        (frm.doc.credit_guarantee_fund_a_composite_loan || 0)
    )
}
async function calculate_total_inflow(frm) {
    frm.set_value('total_inflow',
        (frm.doc.sales || 0) +
        (frm.doc.less_rise_in_debtor || 0) +
        (frm.doc.total_subsidy_grant_for_capex_ || 0) +
        (frm.doc.grant__for_salary_travel__office_exp || 0) +
        (frm.doc.share_capital_inflow || 0) +
        (frm.doc.equity_grant_inflow || 0) +
        (frm.doc.credit_guarantee_fund_a_loan || 0)
    )
}
async function calculate_total_outflow(frm) {
    frm.set_value('total_outflow',
        (frm.doc.variable_cost || 0) +
        (frm.doc.less_rise_in_current_liability || 0) +
        (frm.doc.fixed_cost_less_depreciation_and_ammortization || 0) +
        (frm.doc.rise_in_prepaid_expenses || 0) +
        (frm.doc.credit_guarantee_fund_principal_amount || 0) +
        (frm.doc.capital_costs_fixed || 0) +
        (frm.doc.tax || 0) +
        (frm.doc.profit_distributed || 0)
    )
}

frappe.ui.form.on("Business Plannings", {
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
    },
    validate(frm) {
        if (
            isEmpty(frm.doc.gradingassying_weigning_packingbagging_at_collection_point_rate) ||
            isEmpty(frm.doc.local_transport_include_loading_unloading_rate) ||
            isEmpty(frm.doc.weight_loss_percent) ||
            isEmpty(frm.doc.transport_to_market_include_loading_unloading_rate)
        ) {
            frappe.throw({ message: 'Please fill Variable cost (Rate) & Weight Loss Percent Details.', })
        }
        if (frm.doc.weight_loss_percent > 100 || frm.doc.weight_loss_percent < 0) {
            frappe.throw({ message: "Weight Loss Percent can't be greater than 100 or less than 0." });
        }
        if (frm.doc.depreciation_percent > 100 || frm.doc.depreciation_percent < 0) {
            frappe.throw({ message: "Depreciation Percent can't be greater than 100 or less than 0.", })
        }
    },
    onload: function (frm) {
        filter_financial_year('financial_year', 'start_date', frm)
    },
    async fpo(frm) {
        await apply_fpo_filter_on_child_crop_name('output_side', 'crop_name')
        await apply_fpo_filter_on_child_crop_name('input_side', 'crop_name')
        await check_capital_for_fpo(frm)
        await get_closing_cash_balance(frm)
    },
    async financial_year(frm) {
        get_closing_cash_balance(frm)
    },
    weight_loss_percent(frm) {
        if (frm.doc.weight_loss_percent > 100 || frm.doc.weight_loss_percent < 0) {
            frappe.show_alert({ message: "Weight Loss Percent can't be greater than 100 or less than 0.", indicator: 'red' })
        }
        // # Quantity available for sale (default deducted X% for weight loss)
        frm.doc.output_side.forEach(row => {
            row.quantity_available_for_sale_default_deducted_x_for_weight_loss = (1 - (frm.doc.weight_loss_percent / 100)) * row.quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals
            frm.refresh_field('output_side');
        });
        const calculate_total_quantity_available_for_sale_after_weight_loss = frm.doc.output_side.reduce((total, item) => total + item.quantity_available_for_sale_default_deducted_x_for_weight_loss, 0);
        frm.set_value('quantity_available_for_sale_after_weight_loss', calculate_total_quantity_available_for_sale_after_weight_loss);
        variable_cost_logic(frm)
    },
    async depreciation_percent(frm) {
        await check_capital_for_fpo(frm)
        if (frm.doc.depreciation_percent > 100 || frm.doc.depreciation_percent < 0) {
            frappe.show_alert({ message: "Depreciation Percent can't be greater than 100 or less than 0.", indicator: 'red' })
        }
    },
    ceo_salary(frm) {
        add_total_work_capital(frm)
    },
    accountant_salary(frm) {
        add_total_work_capital(frm)
    },
    store_keeper_salary(frm) {
        add_total_work_capital(frm)
    },
    staff_travel(frm) {
        add_total_work_capital(frm)
    },
    store_rent(frm) {
        add_total_work_capital(frm)
    },
    office_rent(frm) {
        add_total_work_capital(frm)
    },
    utilities(frm) {
        add_total_work_capital(frm)
    },
    miscellanious(frm) {
        add_total_work_capital(frm)
    },
    collection_centre_rent(frm) {
        add_total_work_capital(frm)
    },
    intangible_assetspre_operating_expenses_written_off(frm) {
        add_total_work_capital(frm)
    },
    depreciation(frm) {
        add_total_work_capital(frm)
    },
    interest_on_loan(frm) {
        add_total_work_capital(frm)
    },
    // 
    gradingassying_weigning_packingbagging_at_collection_point_rate(frm) {
        variable_cost_logic(frm)
    },
    local_transport_include_loading_unloading_rate(frm) {
        variable_cost_logic(frm)
    },
    storing_warehousing_costs_rate(frm) {
        variable_cost_logic(frm)
    },
    transport_to_market_include_loading_unloading_rate(frm) {
        variable_cost_logic(frm)
    },
    total_output_selling_priceincome_rs(frm) {
        net_profit_logic(frm)
    },
    total_input_selling_priceincome_rs(frm) {
        net_profit_logic(frm)
    },
    quantity_available_for_sale_after_weight_loss(frm) {
        variable_cost_logic(frm)
    },
    async total_variable_cost(frm) {
        await net_profit_logic(frm)
        await frm.set_value('variable_cost', frm.doc.total_variable_cost)
    },
    async total_work_capital(frm) {
        await net_profit_logic(frm)
        await frm.set_value('fixed_cost_less_depreciation_and_ammortization', frm.doc.total_work_capital - frm.doc.depreciation)
        await frm.set_value('capital_costs_fixed', frm.doc.total_work_capital)
    },
    total_output_purchase_price_rs(frm) {
        net_profit_logic(frm)
    },
    total_input_purchase_price_rs(frm) {
        net_profit_logic(frm)
    },
    total_sales(frm) {
        net_profit_logic(frm)
        frm.set_value('sales', frm.doc.total_sales)
    },
    total_expense(frm) {
        net_profit_logic(frm)
    },
    total_income_including_input_and_output_side(frm) {
        net_profit_logic(frm)
    },
    total_fixed_and_variable_cost(frm) {
        net_profit_logic(frm)
    },
    async gross_profit_loss(frm) {
        await get_closing_cash_balance(frm)
    },


    // ====================================== ================= Projected Cash Flow ================= ======================================
    async grant_for_fixed_capital(frm) {
        await frm.set_value('total_subsidy_grant_for_capex', (frm.doc.grant_for_fixed_capital || 0) + (frm.doc.grant_for_working_capital || 0))
    },
    async grant_for_working_capital(frm) {
        await frm.set_value('total_subsidy_grant_for_capex', (frm.doc.grant_for_fixed_capital || 0) + (frm.doc.grant_for_working_capital || 0))
    },
    async total_subsidy_grant_for_capex(frm) {
        await calculate_mens_of_finance(frm)
        await frm.set_value('total_subsidy_grant_for_capex_', frm.doc.total_subsidy_grant_for_capex)
    },
    async grant__for_salary_travel(frm) {
        await calculate_mens_of_finance(frm)
        await frm.set_value('grant__for_salary_travel__office_exp', frm.doc.grant__for_salary_travel)
    },
    async share_capital(frm) {
        await calculate_mens_of_finance(frm)
        await frm.set_value('share_capital_inflow', frm.doc.share_capital)
    },
    async equity_grant(frm) {
        await calculate_mens_of_finance(frm)
        await frm.set_value('equity_grant_inflow', frm.doc.equity_grant)
    },
    async credit_guarantee_fund_a_composite_loan(frm) {
        await calculate_mens_of_finance(frm)
        await frm.set_value('credit_guarantee_fund_a_loan', frm.doc.credit_guarantee_fund_a_composite_loan)
    },
    // ====================================== ================= Inflow ================= ======================================
    async grant_for_working_capital(frm) {
        await frm.set_value('total_subsidy_grant_for_capex', (frm.doc.grant_for_fixed_capital || 0) + (frm.doc.grant_for_working_capital || 0))
    },
    async sales(frm) {
        await calculate_total_inflow(frm)
    },
    async less_rise_in_debtor(frm) {
        await calculate_total_inflow(frm)
    },
    async total_subsidy_grant_for_capex_(frm) {
        await calculate_total_inflow(frm)
    },
    async grant__for_salary_travel__office_exp(frm) {
        await calculate_total_inflow(frm)
    },
    async share_capital_inflow(frm) {
        await calculate_total_inflow(frm)
    },
    async equity_grant_inflow(frm) {
        await calculate_total_inflow(frm)
    },
    async credit_guarantee_fund_a_loan(frm) {
        await calculate_total_inflow(frm)
    },
    async total_inflow(frm) {
        await frm.set_value('net_inflow_inflow_outflow', frm.doc.total_inflow - frm.doc.total_outflow)
    },
    // ====================================== ================= Outflow ================= ======================================
    async variable_cost(frm) {
        await calculate_total_outflow(frm)(frm)
    },
    async less_rise_in_current_liability(frm) {
        await calculate_total_outflow(frm)(frm)
    },
    async fixed_cost_less_depreciation_and_ammortization(frm) {
        await calculate_total_outflow(frm)(frm)
    },
    async rise_in_prepaid_expenses(frm) {
        await calculate_total_outflow(frm)(frm)
    },
    async credit_guarantee_fund_principal_amount(frm) {
        await calculate_total_outflow(frm)(frm)
    },
    async capital_costs_fixed(frm) {
        await calculate_total_outflow(frm)(frm)
    },
    async tax(frm) {
        await calculate_total_outflow(frm)(frm)
    },
    async profit_distributed(frm) {
        await calculate_total_outflow(frm)(frm)
    },
    async opening_cash_balance(frm) {
        await frm.set_value('closing_cash_balance_outflow', (frm.doc.opening_cash_balance || 0) - (frm.doc.net_inflow_inflow_outflow || 0))
    },
    async net_inflow_inflow_outflow(frm) {
        await frm.set_value('closing_cash_balance_outflow', (frm.doc.opening_cash_balance || 0) - (frm.doc.net_inflow_inflow_outflow || 0))
    },
    async total_outflow(frm) {
        await frm.set_value('net_inflow_inflow_outflow', frm.doc.total_inflow - frm.doc.total_outflow)
    },
});

// ===================================== Output Side Child =====================================

function isEmpty(value) {
    return value === 0 || value === null;
}
async function calculate_output_felids_value(frm, row) {
    // # Total harvest by FPO members(Quintals)
    callAPI({
        method: 'nafpo.apis.api.value_event',
        args: {
            doctype_name: "Crop Name",
            filter_felid_name: row.crop_name,
            felids: ['expected_yields_quintal_per_acre']
        },
        freeze: true,
        freeze_message: __("Getting"),
    }).then(response => {
        row.total_harvest_by_fpo_members_quintals = (row.total_cropping_area_of_fpo_members_acre || 0) * response;
        frm.cur_grid.refresh_field('total_harvest_by_fpo_members_quintals');
    });

    // # Total Purchase Price
    row.total_purchase_price_rs = (row.quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals || 0) * (row.expected_purchase_pricers || 0)
    frm.cur_grid.refresh_field('total_purchase_price_rs');
    //  # Quantity available for sale(default deducted X% for weight loss)
    row.quantity_available_for_sale_default_deducted_x_for_weight_loss = (1 - (frm.doc.weight_loss_percent / 100)) * row.quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals || 0
    frm.cur_grid.refresh_field('quantity_available_for_sale_default_deducted_x_for_weight_loss');
    // # Total selling price / income(Rs)
    row.total_selling_priceincome_rs = row.quantity_available_for_sale_default_deducted_x_for_weight_loss * (row.expected_unit_selling_price_per_quintals || 0)
    frm.cur_grid.refresh_field('total_selling_priceincome_rs');
    // // # Total Income of FPO from Output
    row.total_income_of_fpo_from_output = row.total_selling_priceincome_rs - row.total_purchase_price_rs
    frm.cur_grid.refresh_field('total_income_of_fpo_from_output');
    // // // ===================================== Total =====================================
    const calculate_total_output_purchase_price_rs = frm.doc.output_side.reduce((total, item) => total + item.total_purchase_price_rs, 0);
    frm.set_value('total_output_purchase_price_rs', calculate_total_output_purchase_price_rs);

    const calculate_total_output_selling_priceincome_rs = frm.doc.output_side.reduce((total, item) => total + item.total_selling_priceincome_rs, 0);
    frm.set_value('total_output_selling_priceincome_rs', calculate_total_output_selling_priceincome_rs);

    const calculate_total_income_of_fpo_from_output = frm.doc.output_side.reduce((total, item) => total + item.total_income_of_fpo_from_output, 0);
    frm.set_value('total_income_of_fpo_from_output', calculate_total_income_of_fpo_from_output);

    const calculate_total_quantity_available_for_sale_after_weight_loss = frm.doc.output_side.reduce((total, item) => total + item.quantity_available_for_sale_default_deducted_x_for_weight_loss, 0);
    frm.set_value('quantity_available_for_sale_after_weight_loss', calculate_total_quantity_available_for_sale_after_weight_loss);
}

frappe.ui.form.on('Output Side Child', {
    output_side_add: async function (frm, cdt, cdn) {
        $('.grid-duplicate-row').remove()
        await apply_fpo_filter_on_child_crop_name('output_side', 'crop_name')
    },
    form_render: async function (frm, cdt, cdn) {
        $('.grid-duplicate-row').remove()
        await apply_fpo_filter_on_child_crop_name('output_side', 'crop_name')
        if (
            isEmpty(frm.doc.gradingassying_weigning_packingbagging_at_collection_point_rate) ||
            isEmpty(frm.doc.local_transport_include_loading_unloading_rate) ||
            isEmpty(frm.doc.weight_loss_percent) ||
            isEmpty(frm.doc.transport_to_market_include_loading_unloading_rate)
        ) {
            frappe.show_alert({ message: 'Please fill Variable cost (Rate) & Weight Loss Percent Details.', indicator: 'red' })
            frm.cur_grid.remove()
        }
    },
    item_code(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
    },
    crop_name: async function (frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        calculate_output_felids_value(frm, row)
    },
    total_cropping_area_of_fpo_members_acre: async function (frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        calculate_output_felids_value(frm, row)
    },
    quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals: async function (frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        calculate_output_felids_value(frm, row)
        if (row.total_harvest_by_fpo_members_quintals < row.quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals) {
            row.quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals = ''
            frappe.throw({ message: 'Quantity of produce to be bought by FPO for marketing cannot exceed the total harvest by FPO members.' });
        }
    },
    expected_purchase_pricers: async function (frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        calculate_output_felids_value(frm, row)
    },
    expected_unit_selling_price_per_quintals: async function (frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        calculate_output_felids_value(frm, row)
    },
})

// ===================================== Input Side =====================================

async function calculate_input_felids_value(frm, row) {
    // # Total Area For Which Input Name Shall be Utilized
    row.total_area_for_which_input_name_shall_be_utilized =
        (row.total_cropping_area_of_fpo_members_acre ? row.total_cropping_area_of_fpo_members_acre : 0) *
        (row.percentage_of_total_cropping_area ? row.percentage_of_total_cropping_area : 0);
    frm.cur_grid.refresh_field('total_area_for_which_input_name_shall_be_utilized');
    // # Total Purchase price(Rs)
    row.total_purchase_price_rs =
        (row.total_area_for_which_input_name_shall_be_utilized ? row.total_area_for_which_input_name_shall_be_utilized : 0) *
        (row.expected_purchase_price_per_acre_rs ? row.expected_purchase_price_per_acre_rs : 0);
    frm.cur_grid.refresh_field('total_purchase_price_rs');
    // # Total selling price / income(Rs)
    row.total_selling_priceincome_rs =
        (row.total_area_for_which_input_name_shall_be_utilized ? row.total_area_for_which_input_name_shall_be_utilized : 0) *
        (row.expected_unit_selling_price_per_acre_rs ? row.expected_unit_selling_price_per_acre_rs : 0);
    frm.cur_grid.refresh_field('total_selling_priceincome_rs');
    // # Total Income of FPO from Input
    row.total_income_of_fpo_from_input =
        (row.total_selling_priceincome_rs ? row.total_selling_priceincome_rs : 0) -
        (row.total_purchase_price_rs ? row.total_purchase_price_rs : 0);
    frm.cur_grid.refresh_field('total_income_of_fpo_from_input');

    // ===================================== Total =====================================
    const calculate_total_input_purchase_price_rs = frm.doc.input_side.reduce((total, item) => total + item.total_purchase_price_rs, 0);
    frm.set_value('total_input_purchase_price_rs', calculate_total_input_purchase_price_rs);

    const calculate_total_input_selling_priceincome_rs = frm.doc.input_side.reduce((total, item) => total + item.total_selling_priceincome_rs, 0);
    frm.set_value('total_input_selling_priceincome_rs', calculate_total_input_selling_priceincome_rs);

    const calculate_total_income_of_fpo_from_input = frm.doc.input_side.reduce((total, item) => total + item.total_income_of_fpo_from_input, 0);
    frm.set_value('total_income_of_fpo_from_input', calculate_total_income_of_fpo_from_input);
}

frappe.ui.form.on('Input Side Child', {
    input_side_add: async function (frm, cdt, cdn) {
        $('.grid-duplicate-row').remove()
        await apply_fpo_filter_on_child_crop_name('input_side', 'crop_name')
    },
    form_render: async function (frm, cdt, cdn) {
        $('.grid-duplicate-row').remove()
        await apply_fpo_filter_on_child_crop_name('input_side', 'crop_name')
    },
    item_code(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
    },
    total_cropping_area_of_fpo_members_acre(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        calculate_input_felids_value(frm, row)
    },
    percentage_of_total_cropping_area(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        if (row.percentage_of_total_cropping_area < 0 || row.percentage_of_total_cropping_area > 100) {
            row.percentage_of_total_cropping_area = ''
            frappe.throw({ message: 'Percentage of Total Cropping Area for which Input Name Shall be Provided By FPO Cannot less than 0 and cannot greater than 100.' });
        }
        calculate_input_felids_value(frm, row)
    },
    expected_purchase_price_per_acre_rs(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        calculate_input_felids_value(frm, row)
    },
    expected_unit_selling_price_per_acre_rs(frm, cdt, cdn) {
        let row = frappe.get_doc(cdt, cdn);
        calculate_input_felids_value(frm, row)
    },
})
