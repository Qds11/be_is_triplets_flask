from . import financial_ratio_bp
from flask import jsonify, request

@financial_ratio_bp.route('/', methods=['POST'])
def get_financial_ratio():

    request_data = request.json

    source_data = request_data.get('source_data', None)

    income_statement = source_data["income_statement"]
    balance_sheet = source_data["balance_sheet"]
    cash_flow_statement = source_data["cash_flow_statement"]

    try:
        liquidity_ratio = balance_sheet["current_assets"]/ balance_sheet["current_liabilities"] if balance_sheet["current_liabilities"]!= 0 else 0
        leverage_ratio = balance_sheet["net_worth"] / balance_sheet["total_assets"] if balance_sheet["total_assets"] != 0 else 0
        profitability_ratio = income_statement["net_profit"] /  balance_sheet["total_assets"]  if  balance_sheet["total_assets"]  != 0 else 0
        roe_ratio = income_statement["net_profit"] / balance_sheet["net_worth"] if balance_sheet["net_worth"] != 0 else 0
        debt_to_asset_ratio= balance_sheet["total_liabilities"] / balance_sheet["total_assets"] if balance_sheet["total_assets"] != 0 else 0
        ocf_to_liabilities_ratio = cash_flow_statement["operating_cash_flow"] / balance_sheet["total_liabilities"] if balance_sheet["total_liabilities"] != 0 else 0
        #liquidity_activity_ratios = calculate_liquidity_activity_ratios(balance_sheet, income_statement)

    except Exception as e:
        print(f"Error calculating lquidity activity ratio: {str(e)}")
        return jsonify({'error': f"Error calculating lquidity activity ratios: {str(e)}"}), 500

    return jsonify({"liquidity_ratio":liquidity_ratio,
                    "leverage_ratio":leverage_ratio,
                    "profitability_ratio":profitability_ratio,
                    "roe_ratio":roe_ratio,
                    "debt_to_asset_ratio":debt_to_asset_ratio,
                    "ocf_to_liabilities_ratio":ocf_to_liabilities_ratio}),201



# Function to calculate Liquidity & Activity Ratios
# def calculate_liquidity_activity_ratios(balance_sheet, income_statement):
#     assets =  balance_sheet["assets"]
#     current_assets = assets["current_assets"]
#     # Extract relevant data from the JSON structure
#     total_current_assets = current_assets["total_current_assets"]
#     current_liabilities = balance_sheet["liabilities"]["current_liabilities"]["total_current_liabilities"]

#     cash = current_assets["cash"]
#     petty_cash = current_assets["petty_cash"]
#     temporary_investments = current_assets["temporary_investments"]
#     accounts_receivable_net = current_assets["accounts_receivable_net"]

#     net_credit_sales = income_statement["sales"]
#     average_accounts_receivable = accounts_receivable_net  # Assuming the net accounts receivable represents the average

#     cost_of_goods_sold = income_statement["cost_of_goods_sold"]
#     average_inventory = current_assets["inventory"]  # Assuming inventory represents the average

#     # Calculate Liquidity Ratios
#     working_capital = total_current_assets - current_liabilities
#     current_ratio = total_current_assets / current_liabilities
#     quick_ratio = (cash + petty_cash + temporary_investments + accounts_receivable_net) / current_liabilities

#     # Calculate Activity Ratios
#     accounts_receivable_turnover = net_credit_sales / average_accounts_receivable
#     days_sales_in_accounts_receivable = 365 / accounts_receivable_turnover
#     inventory_turnover = cost_of_goods_sold / average_inventory
#     days_sales_in_inventory = 365 / inventory_turnover

#     # Return the calculated ratios
#     return {
#         "working_capital": working_capital,
#         "current_ratio": round(current_ratio, 2),
#         "quick_ratio": round(quick_ratio, 2),
#         "accounts_receivable_turnover": round(accounts_receivable_turnover, 2),
#         "days_sales_in_accounts_receivable": round(days_sales_in_accounts_receivable, 2),
#         "inventory_turnover": round(inventory_turnover, 2),
#         "days_sales_in_inventory": round(days_sales_in_inventory, 2)
#     }
