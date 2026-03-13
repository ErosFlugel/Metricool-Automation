import requests
import json
from datetime import datetime

from src.sheet.api_connection import connected_sheet

FLAG = False

# Get Instagram Data
def get_instagram(url, headers, params, query=None):
    
    metric_type = params.get(query)

    if FLAG: 
        print(f"Attempting to connect to: {url}")
        print(f"Querying metric: {metric_type}") if metric_type else None
        
        if params.get("from") and params.get("to"):
            
            print(f"From {datetime.fromisoformat(params.get("from")).strftime("%B %d, %Y, %I:%M %p")}")
            print(f"To {datetime.fromisoformat(params.get("to")).strftime("%B %d, %Y, %I:%M %p")}")

    try:
        # Make the GET request
        response = requests.get(url, headers=headers, params=params)

        # Check for successful response status code (200-299)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        if FLAG: 
            print("\n--- API Response (Success) ---")
            print(f"Status Code: {response.status_code}")
            
            print("Response Data:")

            print(json.dumps(data, indent=4))
            
            print("------------------------------\n")

        return data

    except requests.exceptions.HTTPError as e:
        print(f"\n--- API Request Failed (HTTP Error) ---")
        print(f"Status Code: {e.response.status_code}")
        print(f"Error Message: {e}")
        try:
            print("Response Body:")
            print(e.response.json())
        except requests.exceptions.JSONDecodeError:
            print("Response Body: Could not decode JSON from error response.")
        print("---------------------------------------\n")
        print("Please check your credentials and ensure the blogId is for an Instagram profile.")

    except requests.exceptions.RequestException as e:
        print(f"\n--- API Request Failed (Connection Error) ---")
        print(f"An error occurred during the request: {e}")
        print("---------------------------------------------\n")
        
    return 

def get_charts_metadata(sheet_id):
    sh = connected_sheet(sheet_id)
    # 1. Fetch the metadata for the entire spreadsheet
    metadata = sh.fetch_sheet_metadata()

    # OPTIONAL - print the metadata of each sheet to check sheet ids
    # shpreadsheet_data = list(map(lambda sh: sh.get("properties"), metadata.get("sheets")))
    # print(json.dumps(shpreadsheet_data, indent=4))

    chart_info = []

    # 2. Loop through each sheet in the metadata
    for sheet in metadata['sheets']:
        sheet_name = sheet['properties']['title']
        
        # Check if there are any charts in this specific sheet
        if 'charts' in sheet:
            for chart in sheet['charts']:
                chart_id = chart['chartId']
                # You can also get the title of the chart if it has one
                title = chart.get('spec', {}).get('title', 'Untitled Chart')
                
                chart_info.append({
                    'sheet_name': sheet_name,
                    'chart_id': chart_id,
                    'title': title
                })

    # 3. View your results
    # for item in chart_info:
    #     print(f"Sheet: {item['sheet_name']} | Chart Title: {item['title']} | ID: {item['chart_id']}")