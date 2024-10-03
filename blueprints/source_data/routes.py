from . import source_data_bp
from flask import request, request, jsonify
import requests
import base64
#from helpers.encode_file_helper import encode_file
from utils.config import OPEN_AI
import io
from PIL import Image  # For image handling
import pypdfium2 as pdfium
from helpers.error_helpers import handle_error
@source_data_bp.route('/', methods=['POST'])
def get_source_data():
    images = []
    try:
        request_data = request.json
        urls = request_data.get('urls', None)

        if not urls or not isinstance(urls, list):
            return handle_error('A list of document URLs is required', 400)
        try:
            for url in urls:
                pdf_response = requests.get(url)

                # Ensure the request was successful
                if pdf_response.status_code != 200:
                    return jsonify({'error': f'Failed to download the PDF from {url}'}), 500

                # Step 2: Convert PDF to an image (first page)
                pdf_bytes = io.BytesIO(pdf_response.content)
                pdf_document = pdfium.PdfDocument(pdf_bytes)
                page = pdf_document.get_page(0)  # Convert the first page

                # Render page as an image (using a scale for better quality)
                pil_image = page.render(scale=2).to_pil()

                # Store the image for later merging
                images.append(pil_image)

        except Exception as e:
            return jsonify({'error': 'Failed to convert PDF to image', 'details': str(e)}), 500

        # Step 3: Combine the images vertically (stack them)
        try:
            if len(images) > 1:
                # Calculate total height for the combined image
                total_height = sum(image.height for image in images)
                max_width = max(image.width for image in images)

                # Create a new blank image to hold the combined image
                combined_image = Image.new('RGB', (max_width, total_height))

                # Paste each image into the combined image
                y_offset = 0
                for image in images:
                    combined_image.paste(image, (0, y_offset))
                    y_offset += image.height
            else:
                # Only one image, no need to combine
                combined_image = images[0]

            # Step 4: Convert the combined image to base64-encoded JPEG
            buffered = io.BytesIO()
            combined_image.save(buffered, format="JPEG")
            jpeg_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            payload ={
                "model": OPEN_AI["model"],
                "messages":[
                    {
                        "role":"user",
                        "content":[
                            {
                                "type":"text",
                                "text":"Extract data from relevant financial statements (balance sheet, income statement, cash flow statement) and return in json format e.g. {'balance_sheet':'assets':{'current_asset: {'cash': 1030, 'inventory': 3432}}, 'income_statement':..., 'cash_flow_statement':...}..."
                            },
                            {
                                "type": "image_url",
                                "image_url":{
                                    "url":f"data:image/jpeg;base64,{jpeg_base64 }"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens":OPEN_AI["max_tokens"]
            }
            #response = requests.post(OPEN_AI["url"],headers=OPEN_AI["headers"], json=payload)
            #results = response.json()["choices"][0]["message"]["content"]
            #print(results)
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

            #return jpeg_base64
        except Exception as e:
            return jsonify({'error': 'Failed to combine images or convert to JPEG', 'details': str(e)}), 500

    except Exception as e:
        print(f"Error getting source data: {str(e)}")
        return jsonify({'error': f"Error getting source data: {str(e)}"}), 500