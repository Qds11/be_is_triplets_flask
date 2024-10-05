# financial_ratio_service.py

def calculate_financial_ratios(source_data):
    income_statement = source_data["income_statement"]
    balance_sheet = source_data["balance_sheet"]
    cash_flow_statement = source_data["cash_flow_statement"]

    try:
        liquidity_ratio = balance_sheet["current_assets"] / balance_sheet["current_liabilities"] if balance_sheet["current_liabilities"] != 0 else 0
        leverage_ratio = balance_sheet["net_worth"] / balance_sheet["total_assets"] if balance_sheet["total_assets"] != 0 else 0
        profitability_ratio = income_statement["net_profit"] / balance_sheet["total_assets"] if balance_sheet["total_assets"] != 0 else 0
        roe_ratio = income_statement["net_profit"] / balance_sheet["net_worth"] if balance_sheet["net_worth"] != 0 else 0
        debt_to_asset_ratio = balance_sheet["total_liabilities"] / balance_sheet["total_assets"] if balance_sheet["total_assets"] != 0 else 0
        ocf_to_liabilities_ratio = cash_flow_statement["operating_cash_flow"] / balance_sheet["total_liabilities"] if balance_sheet["total_liabilities"] != 0 else 0

        return {
            "liquidity_ratio": liquidity_ratio,
            "leverage_ratio": leverage_ratio,
            "profitability_ratio": profitability_ratio,
            "roe_ratio": roe_ratio,
            "debt_to_asset_ratio": debt_to_asset_ratio,
            "ocf_to_liabilities_ratio": ocf_to_liabilities_ratio
        }

    except Exception as e:
        raise Exception(f"Error calculating financial ratios: {str(e)}")
