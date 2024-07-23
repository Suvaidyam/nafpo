import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'CBBO': ('_fpo', 'cbbo_name'), 'IA': ('_fpo', 'ia'), 'FPO': ('_fpo', 'name')},
        selected_filters=['FPO', 'CBBO', 'IA']
    )
    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""
    
    fpo = filters.get('fpo_name', None)
    financial_year = filters.get('financial_year', None)
    
    financial_year_cond = f" AND bp.financial_year = '{financial_year}'" if financial_year else ""
    fpo_cond = f" AND _fpo.name = '{fpo}'" if fpo else ""

    sql_query = f"""
        SELECT
            _fpo.fpo_name,
            bp.grant_for_fixed_capital,
            bp.grant_for_working_capital,
            bp.total_subsidy_grant_for_capex,
            bp.grant__for_salary_travel,
            bp.share_capital,
            bp.equity_grant,
            bp.credit_guarantee_fund_a_composite_loan,
            bp.total,
            bp.sales,
            bp.less_rise_in_debtor,
            bp.total_subsidy_grant_for_capex_,
            bp.grant__for_salary_travel__office_exp,
            bp.share_capital_inflow,
            bp.equity_grant_inflow,
            bp.credit_guarantee_fund_a_loan,
            bp.total_inflow,
            bp.variable_cost,
            bp.less_rise_in_current_liability,
            bp.fixed_cost_less_depreciation_and_ammortization,
            bp.rise_in_prepaid_expenses,
            bp.credit_guarantee_fund_principal_amount,
            bp.capital_costs_fixed,
            bp.tax,
            bp.profit_distributed,
            bp.total_outflow,
            bp.opening_cash_balance,
            bp.net_inflow_inflow_outflow,
            bp.closing_cash_balance_outflow,
            bp.financial_year
        FROM
            `tabBusiness Plannings` AS bp
        INNER JOIN 
            `tabFPO` AS _fpo ON bp.fpo = _fpo.name
        LEFT JOIN 
            `tabFPO Profiling` AS _fp ON _fpo.name = _fp.name_of_the_fpo
        WHERE 
            1=1 {financial_year_cond} {fpo_cond} {cond_str}
        ORDER BY 
            bp.financial_year ASC
    """
    
    columns = [
        {"fieldname": "fpo_name", "label": "FPO Name", "fieldtype": "Link", "options": "FPO", "width": 200},
        {"fieldname": "financial_year", "label": "Financial Year", "fieldtype": "Data", "width": 200},
        {"fieldname": "grant_for_fixed_capital", "label": "Grant for Fixed Capital", "fieldtype": "Currency", "width": 200},
        {"fieldname": "grant_for_working_capital", "label": "Grant for Working Capital", "fieldtype": "Currency", "width": 200},
        {"fieldname": "total_subsidy_grant_for_capex", "label": "Total Subsidy Grant for Capex", "fieldtype": "Currency", "width": 200},
        {"fieldname": "grant__for_salary_travel", "label": "Grant for Salary Travel", "fieldtype": "Currency", "width": 200},
        {"fieldname": "share_capital", "label": "Share Capital", "fieldtype": "Currency", "width": 200},
        {"fieldname": "equity_grant", "label": "Equity Grant", "fieldtype": "Currency", "width": 200},
        {"fieldname": "credit_guarantee_fund_a_composite_loan", "label": "Credit Guarantee Fund A Composite Loan", "fieldtype": "Currency", "width": 200},
        {"fieldname": "total", "label": "Total", "fieldtype": "Currency", "width": 200},
        {"fieldname": "sales", "label": "Sales", "fieldtype": "Currency", "width": 200},
        {"fieldname": "less_rise_in_debtor", "label": "Less Rise in Debtor", "fieldtype": "Currency", "width": 200},
        {"fieldname": "total_subsidy_grant_for_capex_", "label": "Total Subsidy Grant for Capex", "fieldtype": "Currency", "width": 200},
        {"fieldname": "grant__for_salary_travel__office_exp", "label": "Grant for Salary Travel Office Exp", "fieldtype": "Currency", "width": 200},
        {"fieldname": "share_capital_inflow", "label": "Share Capital Inflow", "fieldtype": "Currency", "width": 200},
        {"fieldname": "equity_grant_inflow", "label": "Equity Grant Inflow", "fieldtype": "Currency", "width": 200},
        {"fieldname": "credit_guarantee_fund_a_loan", "label": "Credit Guarantee Fund A Loan", "fieldtype": "Currency", "width": 200},
        {"fieldname": "total_inflow", "label": "Total Inflow", "fieldtype": "Currency", "width": 200},
        {"fieldname": "variable_cost", "label": "Variable Cost", "fieldtype": "Currency", "width": 200},
        {"fieldname": "less_rise_in_current_liability", "label": "Less Rise in Current Liability", "fieldtype": "Currency", "width": 200},
        {"fieldname": "fixed_cost_less_depreciation_and_ammortization", "label": "Fixed Cost Less Depreciation and Amortization", "fieldtype": "Currency", "width": 200},
        {"fieldname": "rise_in_prepaid_expenses", "label": "Rise in Prepaid Expenses", "fieldtype": "Currency", "width": 200},
        {"fieldname": "credit_guarantee_fund_principal_amount", "label": "Credit Guarantee Fund Principal Amount", "fieldtype": "Currency", "width": 200},
        {"fieldname": "capital_costs_fixed", "label": "Capital Costs Fixed", "fieldtype": "Currency", "width": 200},
        {"fieldname": "tax", "label": "Tax", "fieldtype": "Currency", "width": 200},
        {"fieldname": "profit_distributed", "label": "Profit Distributed", "fieldtype": "Currency", "width": 200},
        {"fieldname": "total_outflow", "label": "Total Outflow", "fieldtype": "Currency", "width": 200},
        {"fieldname": "opening_cash_balance", "label": "Opening Cash Balance", "fieldtype": "Currency", "width": 200},
        {"fieldname": "net_inflow_inflow_outflow", "label": "Net Inflow Inflow Outflow", "fieldtype": "Currency", "width": 200},
        {"fieldname": "closing_cash_balance_outflow", "label": "Closing Cash Balance Outflow", "fieldtype": "Currency", "width": 200},
    ]

    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
