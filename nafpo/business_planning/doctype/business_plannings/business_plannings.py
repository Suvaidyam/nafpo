import frappe
from frappe.model.document import Document

class BusinessPlannings(Document):
    def before_save(self):
        # Field names and their corresponding rates
        fields_and_rates = {
            'gradingassying_weigning_packingbagging_at_collection_point': 'gradingassying_weigning_packingbagging_at_collection_point_rate',
            'local_transport_include_loading_unloading_collection_point': 'local_transport_include_loading_unloading_rate',
            'storing_warehousing_costs': 'storing_warehousing_costs_rate',
            'transport_to_market_include_loading__unloading': 'transport_to_market_include_loading_unloading_rate'
        }

        # Previous document states before save
        previous = self._doc_before_save if hasattr(self, '_doc_before_save') else None

        # Apply rate multiplication if either the value or the rate field has changed
        for field, rate_field in fields_and_rates.items():
            current_value = getattr(self, field, 0) or 0
            rate_value = getattr(self, rate_field, 0) or 0
            previous_value = getattr(previous, field, None) if previous else None
            previous_rate_value = getattr(previous, rate_field, None) if previous else None

            if previous is None or current_value != (previous_value or 0) or rate_value != (previous_rate_value or 0):
                setattr(self, field, current_value * rate_value)

        # Calculate total variable cost
        self.total_variable_cost = sum(getattr(self, field, 0) for field in fields_and_rates)