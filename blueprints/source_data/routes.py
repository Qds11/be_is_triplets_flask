from . import source_data_bp
from flask import request, request, jsonify
import requests
import base64

@source_data_bp.route('/', methods=['POST'])
def get_source_data():
    try:
        request_data = request.json
        document_url = request_data.get('url', None)

        if not document_url:
            return jsonify({'error': 'Document url(s) is required'}), 400


        # Step 1: Fetch the PDF from the database
        pdf_response   = requests.get(document_url)

        # Ensure the request was successful
        if pdf_response.status_code != 200:
            return jsonify({'error': 'Failed to download the PDF'}), 500

        # Step 2: Convert PDF to base64
        pdf_base64 = base64.b64encode(pdf_response.content).decode('utf-8')

        # Step 3: Send to OCR service
        # Step 4: Send to NLP service
        # Step 5: Store source data in the database

        # Step 6: Return the source data to the client
        data = {
            "balance_sheet": {
                "date": "December 31, 2013",
                "assets": {
                    "current_assets": {
                        "cash": 2100,
                        "petty_cash": 100,
                        "temporary_investments": 10000,
                        "accounts_receivable_net": 40500,
                        "inventory": 31000,
                        "supplies": 3800,
                        "prepaid_insurance": 1500,
                        "total_current_assets": 89000
                    },
                    "investments": 36000,
                    "property_plant_equipment": {
                        "land": 5500,
                        "land_improvements": 6500,
                        "buildings": 180000,
                        "equipment": 201000,
                        "less_accum_depreciation": -56000,
                        "net_property_plant_equipment": 337000
                    },
                    "intangible_assets": {
                        "goodwill": 105000,
                        "trade_names": 200000,
                        "total_intangible_assets": 305000
                    },
                    "other_assets": 3000,
                    "total_assets": 770000
                },
                "liabilities": {
                    "current_liabilities": {
                        "notes_payable": 5000,
                        "accounts_payable": 35900,
                        "wages_payable": 8500,
                        "interest_payable": 2900,
                        "taxes_payable": 6100,
                        "warranty_liability": 1100,
                        "unearned_revenues": 1500,
                        "total_current_liabilities": 61000
                    },
                    "long_term_liabilities": {
                        "notes_payable": 20000,
                        "bonds_payable": 400000,
                        "total_long_term_liabilities": 420000
                    },
                    "total_liabilities": 481000
                },
                "stockholders_equity": {
                    "common_stock": 110000,
                    "retained_earnings": 229000,
                    "less_treasury_stock": -50000,
                    "total_stockholders_equity": 289000
                },
                "total_liabilities_and_stockholders_equity": 770000
            },
            "income_statement": {
                "date": "For the year ended December 31, 2013",
                "sales": 500000,
                "cost_of_goods_sold": 380000,
                "gross_profit": 120000,
                "operating_expenses": {
                    "selling_expenses": 35000,
                    "administrative_expenses": 45000,
                    "total_operating_expenses": 80000
                },
                "operating_income": 40000,
                "interest_expense": 12000,
                "income_before_taxes": 28000,
                "income_tax_expense": 5000,
                "net_income_after_taxes": 23000
            },
            "cash_flow_statement": {
                "date": "For the year ended December 31, 2013",
                "cash_flow_from_operating_activities": {
                    "net_income": 23000,
                    "depreciation_expense": 4000,
                    "increase_in_accounts_receivable": -6000,
                    "decrease_in_inventory": 9000,
                    "decrease_in_accounts_payable": -5000,
                    "net_cash_provided_by_operating_activities": 25000
                },
                "cash_flow_from_investing_activities": {
                    "capital_expenditures": -28000,
                    "proceeds_from_sale_of_property": 7000,
                    "net_cash_used_by_investing_activities": -21000
                },
                "cash_flow_from_financing_activities": {
                    "borrowings_of_long_term_debt": 10000,
                    "cash_dividends_paid": -5000,
                    "purchase_of_treasury_stock": -8000,
                    "net_cash_used_by_financing_activities": -3000
                },
                "net_increase_in_cash": 1000,
                "cash_at_beginning_of_year": 1200,
                "cash_at_end_of_year": 2200
            }
        }
        return data
    except Exception as e:
        print(f"Error getting source data: {str(e)}")
        return jsonify({'error': f"Error getting source data: {str(e)}"}), 500