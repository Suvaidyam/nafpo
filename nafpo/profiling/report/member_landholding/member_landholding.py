import frappe

def execute(filters=None):
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

    sql_query = """
		SELECT
		CASE
			WHEN total_own_land < 1 THEN 'Marginal'
			WHEN total_own_land >= 1 AND total_own_land <= 2 THEN 'Small'
			WHEN total_own_land > 2 AND total_own_land <= 4 THEN 'Semi-Medium'
			WHEN total_own_land > 4 AND total_own_land <= 10 THEN 'Medium'
			WHEN total_own_land > 10 THEN 'Large'
			ELSE 'Other'  -- Handle any other cases if necessary
		END AS landholding_category,
		COUNT(*) AS farmer_count
	FROM
		`tabFPO member details`
	GROUP BY
		CASE
			WHEN total_own_land < 1 THEN 'Marginal'
			WHEN total_own_land >= 1 AND total_own_land <= 2 THEN 'Small'
			WHEN total_own_land > 2 AND total_own_land <= 4 THEN 'Semi-Medium'
			WHEN total_own_land > 4 AND total_own_land <= 10 THEN 'Medium'
			WHEN total_own_land > 10 THEN 'Large'
			ELSE 'Other'
		END;
    """

    data = frappe.db.sql(sql_query, as_dict=True)
    return columns, data
