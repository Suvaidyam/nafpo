import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
        mappings={'CBBO': ('_fpo', 'cbbo_name'), 'IA': ('_fpo', 'ia'), 'FPO': ('_fpo', 'name')},
        selected_filters=['FPO', 'CBBO', 'IA']
    )
    cond_str = f" AND {user_filter_conditions}" if user_filter_conditions else ""
    
    fpo = filters.get('fpo_name', None)
    financial_years = filters.get('financial_year', [])
    
    fpo_cond = f" AND _fpo.name = '{fpo}'" if fpo else ""
    financial_year_cond = ""
    if financial_years:
        financial_year_list = "', '".join(financial_years)
        financial_year_cond = f" AND bp.financial_year IN ('{financial_year_list}')"

    sql_query = f"""
        SELECT
            _fpo.fpo_name,
            bp.financial_year,
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
            bp.closing_cash_balance_outflow
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
    
    data = frappe.db.sql(sql_query, as_dict=True)
    
    # Collect all unique financial years to create dynamic columns
    financial_years = sorted({d['financial_year'] for d in data})
    
    # Prepare columns for financial years
    columns = [
        {"fieldname": "detail", "label": "Projected Cash Flow Detail", "fieldtype": "Data", "width": 400}
    ]
    for year in financial_years:
        columns.append({"fieldname": f"financial_year_{year}", "label": year, "fieldtype": "Data", "width": 200})
    
    # Define detail labels
    detail_labels = {
        'grant_for_fixed_capital': 'Grant for Fixed Capital', 
        'grant_for_working_capital': 'Grant for Working Capital', 
        'total_subsidy_grant_for_capex': 'Total Subsidy Grant for Capex', 
        'grant__for_salary_travel': 'Grant for Salary Travel', 
        'share_capital': 'Share Capital', 
        'equity_grant': 'Equity Grant', 
        'credit_guarantee_fund_a_composite_loan': 'Credit Guarantee Fund A Composite Loan', 
        'total': 'Total', 
        'sales': 'Sales', 
        'less_rise_in_debtor': 'Less Rise in Debtor', 
        'total_subsidy_grant_for_capex_': 'Total Subsidy Grant for Capex', 
        'grant__for_salary_travel__office_exp': 'Grant for Salary Travel Office Exp', 
        'share_capital_inflow': 'Share Capital Inflow', 
        'equity_grant_inflow': 'Equity Grant Inflow', 
        'credit_guarantee_fund_a_loan': 'Credit Guarantee Fund A Loan', 
        'total_inflow': 'Total Inflow', 
        'variable_cost': 'Variable Cost', 
        'less_rise_in_current_liability': 'Less Rise in Current Liability', 
        'fixed_cost_less_depreciation_and_ammortization': 'Fixed Cost Less Depreciation and Amortization', 
        'rise_in_prepaid_expenses': 'Rise in Prepaid Expenses', 
        'credit_guarantee_fund_principal_amount': 'Credit Guarantee Fund Principal Amount', 
        'capital_costs_fixed': 'Capital Costs Fixed', 
        'tax': 'Tax', 
        'profit_distributed': 'Profit Distributed', 
        'total_outflow': 'Total Outflow', 
        'opening_cash_balance': 'Opening Cash Balance', 
        'net_inflow_inflow_outflow': 'Net Inflow Inflow Outflow', 
        'closing_cash_balance_outflow': 'Closing Cash Balance Outflow'
    }
    
    # Initialize pivot data structure
    pivot_data = {label: {year: 0 for year in financial_years} for label in detail_labels.values()}
    
    for row in data:
        for key, label in detail_labels.items():
            pivot_data[label][row['financial_year']] = row.get(key, 0)

    # Flatten the pivot data into a list
    formatted_data = []
    for label, years in pivot_data.items():
        detail_row = {"detail": label}
        for year in financial_years:
            detail_row[f"financial_year_{year}"] = years.get(year, 0)
        formatted_data.append(detail_row)

    return columns, formatted_data
