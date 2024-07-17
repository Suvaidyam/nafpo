import frappe
from frappe.model.document import Document
from frappe.utils import today

class BusinessPlannings(Document):
    def before_save(self):
        calculate_total_quantity_available_for_sale_after_weight_loss = 0
        total_output_income = 0
        total_input_income = 0
        total_output_selling_priceincome_rs = 0
        total_input_selling_priceincome_rs = 0
        total_output_purchase_price_rs = 0
        total_input_purchase_price_rs = 0
    # Output Side Logic
        # Total harvest by FPO members (Quintals)
        output_side_row = self.output_side
        for row in output_side_row:
        # # Total harvest by FPO members (Quintals)
        #     expected_yields = frappe.db.get_value("Crop Name",row.crop_name,'expected_yields_quintal_per_acre')
        #     row.total_harvest_by_fpo_members_quintals = row.total_cropping_area_of_fpo_members_acre * expected_yields
        
        # Total Purchase Price 
            row.total_purchase_price_rs = row.quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals * row.expected_purchase_pricers
        # Quantity available for sale (default deducted X% for weight loss)
            row.quantity_available_for_sale_default_deducted_x_for_weight_loss = (1 - (self.weight_loss_percent / 100)) * row.quantity_of_produce_to_be_bought_by_fpo_for_marketing_quintals
        # Total selling price/income (Rs)
            row.total_selling_priceincome_rs = row.quantity_available_for_sale_default_deducted_x_for_weight_loss * row.expected_unit_selling_price_per_quintals
        # Total Income of FPO from Output
            row.total_income_of_fpo_from_output = row.total_selling_priceincome_rs - row.total_purchase_price_rs
        # Total  
            total_output_income += row.total_income_of_fpo_from_output
            calculate_total_quantity_available_for_sale_after_weight_loss += row.quantity_available_for_sale_default_deducted_x_for_weight_loss
            total_output_selling_priceincome_rs += row.total_selling_priceincome_rs
            total_output_purchase_price_rs += row.total_purchase_price_rs
        self.total_income_of_fpo_from_output = total_output_income
        self.quantity_available_for_sale_after_weight_loss = calculate_total_quantity_available_for_sale_after_weight_loss
        self.total_output_purchase_price_rs = total_output_purchase_price_rs
        # Total Output selling price/income (Rs)
        self.total_output_selling_priceincome_rs = total_output_selling_priceincome_rs
        
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
            total_input_selling_priceincome_rs += row.total_selling_priceincome_rs
            total_input_purchase_price_rs += row.total_purchase_price_rs
        self.total_income_of_fpo_from_input = total_input_income
        self.total_input_selling_priceincome_rs = total_input_selling_priceincome_rs
        self.total_input_purchase_price_rs = total_input_purchase_price_rs
        
    # Variable Cost Logic
        self.gradingassying_weigning_packingbagging_at_collection_point = self.quantity_available_for_sale_after_weight_loss * self.gradingassying_weigning_packingbagging_at_collection_point_rate
        self.local_transport_include_loading_unloading_collection_point = self.quantity_available_for_sale_after_weight_loss * self.local_transport_include_loading_unloading_rate
        self.storing_warehousing_costs = self.quantity_available_for_sale_after_weight_loss * self.storing_warehousing_costs_rate
        self.transport_to_market_include_loading__unloading = self.quantity_available_for_sale_after_weight_loss * self.transport_to_market_include_loading_unloading_rate
        self.total_variable_cost = (
            self.gradingassying_weigning_packingbagging_at_collection_point +
            self.local_transport_include_loading_unloading_collection_point +
            self.storing_warehousing_costs +
            self.transport_to_market_include_loading__unloading
        )
    # Fixed Cost (yearly) Logic
        get_total_value = frappe.db.get_list('FPO Fixed Capital',
                        filters={
                            'fpo': self.fpo,
                        },
                        fields=['total_value'],
                        as_list=True
                    )
        total_value = get_total_value[0][0] if get_total_value else 0
        # print('//'*40,total_value)
        self.total_work_capital = (
            self.ceo_salary + 
            self.accountant_salary + 
            self.store_keeper_salary + 
            self.staff_travel + 
            self.store_rent + 
            self.office_rent + 
            self.utilities +
            self.miscellanious +
            self.collection_centre_rent +
            self.intangible_assetspre_operating_expenses_written_off +
            self.depreciation +
            self.interest_on_loan
        )
        # Depreciation
        self.depreciation = total_value / self.depreciation_percent
        
# Net Profit (Per Year) Logic
    
    # Total Sales
        self.total_sales =  self.total_output_selling_priceincome_rs + self.total_input_selling_priceincome_rs
    # Total Expense
        self.total_expense = self.total_variable_cost + self.total_work_capital + self.total_output_purchase_price_rs + self.total_input_purchase_price_rs
    # Gross Profit /Loss (Total Sales- Total Expence)
        self.gross_profit_loss = self.total_sales - self.total_expense 
    
    # Total Income (Including Input and Output Side)
        self.total_income_including_input_and_output_side = self.total_income_of_fpo_from_output + self.total_income_of_fpo_from_input
    # Total Fixed and Variable Cost
        self.total_fixed_and_variable_cost = self.total_variable_cost + self.total_work_capital
    # Gross Profit /Loss (Total Income- Total Cost)
        self.gross_profit_loss_total_income_total_cost = self.total_income_including_input_and_output_side - self.total_fixed_and_variable_cost
        
    # Check if FPO Fixed Capital already exists for this financial year and FPO
        exists = frappe.db.exists({
            "doctype": "Business Plannings",
            "financial_year": self.financial_year,
            "fpo": self.fpo
        })
        if exists and exists != self.name:
            fpo = frappe.get_doc('FPO', self.fpo)
            fy = frappe.get_doc('Financial Year', self.financial_year)
            frappe.throw(f'Financial Year {fy.financial_year_name} already exists for the {fpo.fpo_name}')
        
        exists_fixed_capital = frappe.db.exists({
            "doctype": "FPO Fixed Capital",
            "fpo": self.fpo
        })
        if exists_fixed_capital == None:
            frappe.throw('Please create FPO Fixed Capital for this FPO')
        
        if (
            self.gradingassying_weigning_packingbagging_at_collection_point_rate == 0 or 
            self.local_transport_include_loading_unloading_rate == 0 or 
            self.weight_loss_percent == 0 or 
            self.local_transport_include_loading_unloading_rate is None or 
            self.transport_to_market_include_loading_unloading_rate == 0
        ):
            frappe.throw('Please fill Variable cost (Rate) & Weight Loss Percent Details')
