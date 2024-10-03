import math

# Function to calculate the credit score based on financial ratios
def calculate_credit_score(rules, current_assets, current_liabilities, net_worth, total_assets, net_profit, total_liabilities, operating_cash_flow):
    # Define the financial ratios
    liquidity_ratio = current_assets / current_liabilities if current_liabilities != 0 else 0
    leverage_ratio = net_worth / total_assets if total_assets != 0 else 0
    profitability_ratio = net_profit / total_assets if total_assets != 0 else 0
    roe_ratio = net_profit / net_worth if net_worth != 0 else 0
    debt_to_asset_ratio = total_liabilities / total_assets if total_assets != 0 else 0
    ocf_to_liabilities_ratio = operating_cash_flow / total_liabilities if total_liabilities != 0 else 0

    # Accessing the weights
    w1 = rules['weights']['liquidity_ratio']
    w2 = rules['weights']['leverage_ratio']
    w3 = rules['weights']['profitability_ratio']
    w4 = rules['weights']['roe_ratio']
    w5 = rules['weights']['debt_to_asset_ratio']
    w6 = rules['weights']['ocf_to_liabilities_ratio']

    # Accessing the credit score range
    min_score = rules['score_range']['min_score']
    max_score = rules['score_range']['max_score']
    min_credit_score = rules['score_range']['min_credit_score']
    max_credit_score = rules['score_range']['max_credit_score']

    # Calculate the raw credit score
    raw_score = (w1 * liquidity_ratio +
                 w2 * leverage_ratio +
                 w3 * profitability_ratio +
                 w4 * roe_ratio +
                 w5 * debt_to_asset_ratio +
                 w6 * ocf_to_liabilities_ratio)


    credit_score = (raw_score - min_score) / (max_score - min_score) * (max_credit_score - min_credit_score) + min_credit_score
    credit_score = max(min_credit_score, min(max_credit_score, credit_score))  # Ensure it's within the range 300 to 850

    return credit_score
