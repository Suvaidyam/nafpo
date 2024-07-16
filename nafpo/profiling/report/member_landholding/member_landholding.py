import frappe
from nafpo.utils.rport_filter import ReportFilter

def execute(filters=None):
    user_filter_conditions = ReportFilter.rport_filter_by_user_permissions(
    mappings={'CBBO': ('_fpo', 'cbbo_name'), 'IA': ('_fpo', 'ia'), 'FPO': ('_fpo', 'name')},
    selected_filters=['CBBO', 'IA', 'FPO'],
)
    cond_str = f" WHERE {user_filter_conditions}" if user_filter_conditions else ""
    columns = [
        {
            "fieldname": "farmer_count",
            "label": "Farmer Count",
            "fieldtype": "Int",
            "width": 300
        },
        {
            "fieldname": "landholding_category",
            "label": "Landholding Category",
            "fieldtype": "Data",
            "width": 300
        },
    ]

    sql_query = f"""
		SELECT
    CASE
        WHEN fmd.total_owned_in_hectare < 1 THEN 'Marginal'
        WHEN fmd.total_owned_in_hectare >= 1 AND fmd.total_owned_in_hectare <= 2 THEN 'Small'
        WHEN fmd.total_owned_in_hectare > 2 AND fmd.total_owned_in_hectare <= 4 THEN 'Semi-Medium'
        WHEN fmd.total_owned_in_hectare > 4 AND fmd.total_owned_in_hectare <= 10 THEN 'Medium'
        WHEN fmd.total_owned_in_hectare > 10 THEN 'Large'
    END AS landholding_category,
    COUNT(*) AS farmer_count
FROM
    `tabFPO member details` AS fmd
INNER JOIN `tabFPO` AS _fpo ON fmd.fpo = _fpo.name
{cond_str}
GROUP BY
    CASE
        WHEN fmd.total_owned_in_hectare < 1 THEN 'Marginal'
        WHEN fmd.total_owned_in_hectare >= 1 AND fmd.total_owned_in_hectare <= 2 THEN 'Small'
        WHEN fmd.total_owned_in_hectare > 2 AND fmd.total_owned_in_hectare <= 4 THEN 'Semi-Medium'
        WHEN fmd.total_owned_in_hectare > 4 AND fmd.total_owned_in_hectare <= 10 THEN 'Medium'
        WHEN fmd.total_owned_in_hectare > 10 THEN 'Large'
    END;
    """

    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
