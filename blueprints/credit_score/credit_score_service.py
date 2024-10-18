
# Function to calculate the credit score based on financial ratios
def calculate_credit_score(rules_content, financial_ratios):

    rules = rules_content["scoring_weights"]

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
    raw_score = (w1 * financial_ratios["liquidity_ratio"] +
                 w2 * financial_ratios["leverage_ratio"] +
                 w3 * financial_ratios["profitability_ratio"] +
                 w4 * financial_ratios["roe_ratio"] +
                 w5 * financial_ratios["debt_to_asset_ratio"] +
                 w6 * financial_ratios["ocf_to_liabilities_ratio"])


    credit_score = (raw_score - min_score) / (max_score - min_score) * (max_credit_score - min_credit_score) + min_credit_score
    credit_score = max(min_credit_score, min(max_credit_score, credit_score))  # Ensure it's within the range 300 to 850

    return credit_score
