import frappe
from frappe.model.document import Document

class BusinessPlannings(Document):
    def before_save(self):
        total_output_income = 0
        total_input_income = 0
    # Output Side Logic
        # Total harvest by FPO members (Quintals)
        output_side_row = self.output_side
        for row in output_side_row:
        # Total harvest by FPO members (Quintals)
            expected_yields = frappe.db.get_value("Crop Name",row.crop_name,'expected_yields_quintal_per_acre')
            row.total_harvest_by_fpo_members_quintals = row.total_cropping_area_of_fpo_members_acre * expected_yields
        # Total Purchase Price 
            row.total_purchase_price_rs = row.quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals * row.expected_purchase_pricers
        # Quantity available for sale (default deducted X% for weight loss)
            row.quantity_available_for_sale_default_deducted_x_for_weight_loss = (1 - (self.weight_loss_percent / 100)) * row.quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals
        # Total selling price/income (Rs)
            row.total_selling_priceincome_rs = row.quantity_available_for_sale_default_deducted_x_for_weight_loss * row.expected_unit_selling_price_per_quintals
        # Total Income of FPO from Output
            row.total_income_of_fpo_from_output = row.total_selling_priceincome_rs * row.total_purchase_price_rs
        # Total  
            total_output_income += row.total_income_of_fpo_from_output
        self.total_income_of_fpo_from_output = total_output_income
        
    # Input Side Logic
        input_side_row = self.input_side
        for row in input_side_row:
        # Total Area For Which Input Name Shall be Utilized
            row.total_area_for_which_input_name_shall_be_utilized = row.total_cropping_area_of_fpo_members_acre * row.percentage_of_total_cropping_area
        # Total Purchase price (Rs)
            row.total_purchase_price_rs = row.total_area_for_which_input_name_shall_be_utilized * row.expected_purchase_price_per_acre_rs
        # Total selling price/income (Rs)
            row.total_selling_priceincome_rs = row.total_area_for_which_input_name_shall_be_utilized * row.expected_unit_selling_price_per_acre_rs
        # Total Income of FPO from Input
            row.total_income_of_fpo_from_input = row.total_selling_priceincome_rs - row.total_purchase_price_rs
        
            total_input_income += row.total_income_of_fpo_from_input
        self.total_income_of_fpo_from_input = total_input_income
        
    # Variable Cost Logic
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