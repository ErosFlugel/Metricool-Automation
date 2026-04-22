# Work when imported by main.py

from src.sheet.api_connection import connected_sheet
from src.sheet.sheet_data import profile_specs, spanish_months
from src.metricool.api_data_mimesa import get_gender, get_age, get_detalles_ig, get_followers, get_metrics_st, get_competitors, get_detalles_st, get_totals

from src.utils.data_handlers import get_base_graphic_compare_table

import json

def generate_details_IG(month, blog_id, worksheets):
    # Table Base
    current_worksheet = list(filter(lambda item: item.get("title") == "Detalles IG", worksheets))[0]
    worksheet_id = current_worksheet.get("id")

    # api_data
    combo_details_ig_data = get_detalles_ig(month, blog_id, worksheets)

    # Code guard
    if (not combo_details_ig_data.get("success")) and (combo_details_ig_data.get("status") == "empty_metricool"):

        requests = [
            {
                "updateCells": {
                    "rows": combo_details_ig_data.get("data").get("details_ig"),
                    "fields": "userEnteredValue",
                    "range": {
                        "sheetId": worksheet_id,
                        "startRowIndex": 0,
                        "startColumnIndex": 0,
                        "endColumnIndex": 1,
                        "endRowIndex": 1,
                    }
                }
            }
        ]
        return requests

    if combo_details_ig_data.get("success") == True:
        details_ig_data = combo_details_ig_data.get("data").get("details_ig")

    # table limits
    posts_and_reels_without_ads_starting_row = current_worksheet.get("tables_data")[0].get("row_starting_position")
    starting_column_index = current_worksheet.get("tables_data")[0].get("column_starting_position") - 1
    data_column_amount = len(details_ig_data[0].get("values"))
    # data_row_amount = len(details_ig_data)

    requests = [
        {
            # CLEANING table
            "repeatCell": {
                "range": {
                    "sheetId": worksheet_id,  # Place the worksheet ID
                    "startRowIndex": posts_and_reels_without_ads_starting_row - 1,  # Clear from the very top
                    "startColumnIndex": starting_column_index,
                    # "endRowIndex": data_row_amount,
                    "endColumnIndex": data_column_amount
                },
                "cell": {
                    "userEnteredValue": {} # This "empties" the cell
                },
                "fields": "userEnteredValue"
            },
        },
        { #Cleaning Status
            "updateCells": {
                "rows": [
                    {
                        "values": [
                            {"userEnteredValue": {"stringValue": ""}}
                        ]
                    }
                ],
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": 0,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1,
                    "endRowIndex": 1,
                }
            }
        },
        { #MONTH TITLE
            "updateCells": {
                "rows": [
                    {
                        "values": [
                            {"userEnteredValue": {"stringValue": month.get("name")}}
                        ]
                    }
                ],
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1,
                    "endRowIndex": 2,
                }
            }
        },
        {
            "updateCells": {
                "rows": details_ig_data,
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": posts_and_reels_without_ads_starting_row - 1,
                    "startColumnIndex": starting_column_index,
                    "endColumnIndex": starting_column_index + data_column_amount,
                    # "endRowIndex": data_row_amount,
                }
            }
        }
    ]

    #######################################################################################################
    # Interacciones without ads:
    requests += generate_interactions_without_ads(combo_details_ig_data.get("data").get("interactions_without_ads"), month, worksheets)
    #######################################################################################################
    # Metrics without ads:
    requests += generate_metrics_without_ads(combo_details_ig_data.get("data").get("metrics_without_ads"), month, worksheets)

    # # Table Base
    # current_worksheet = list(filter(lambda item: item.get("title") == "Interacciones SIN ADS", worksheets))[0]
    # worksheet_id = current_worksheet.get("id")

    return requests

def generate_totals(month, follower_monthly_position, worksheets):
    # Table Base
    current_worksheet = list(filter(lambda item: item.get("title") == "Totales", worksheets))[0]
    worksheet_id = current_worksheet.get("id")

    # api_data
    columns_data = current_worksheet.get("tables_data")[0].get("columns_data")
    totals_data = get_totals(columns_data, follower_monthly_position)

    starting_column_index = current_worksheet.get("tables_data")[0].get("column_starting_position") - 1
    starting_row_index = current_worksheet.get("tables_data")[0].get("row_starting_position") - 1
    end_column_index = starting_column_index + len(columns_data)

    requests = [
        {
            "updateCells": {
                "rows": totals_data.get("data"),
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": starting_row_index,
                    "startColumnIndex": starting_column_index,
                    "endColumnIndex": end_column_index,
                    "endRowIndex": starting_row_index + 1,
                }
            }
        },
        {
            "updateCells": {
                "rows": [{"values": [{"userEnteredValue": {"stringValue": month.get("name")}}]}],
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": 19,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1,
                    "endRowIndex": 20,
                }
            }
        }
    ]
    return requests

def generate_followers(month, blog_id, worksheets):
    # Table Base
    current_worksheet = list(filter(lambda item: item.get("title") == "Seguidores", worksheets))[0]
    worksheet_id = current_worksheet.get("id")

    # api_data
    followers_data = get_followers(month, blog_id, current_worksheet)

    # Code guard
    if (not followers_data.get("success")) and (followers_data.get("status") == "empty_metricool"):

        requests = [
            {
                "updateCells": {
                    "rows": followers_data.get("data"),
                    "fields": "userEnteredValue",
                    "range": {
                        "sheetId": worksheet_id,
                        "startRowIndex": 0,
                        "startColumnIndex": 0,
                        "endColumnIndex": 1,
                        "endRowIndex": 1,
                    }
                }
            }
        ]
        return requests
    
    if followers_data.get("success") == True:
        followers_data = followers_data.get("data")

    # table limits
    current_monthly_position = (current_worksheet.get("tables_data")[0].get("row_starting_position") - 1) + (month.get("number") - 1)
    starting_column_index = current_worksheet.get("tables_data")[0].get("column_starting_position") - 1
    data_column_amount = len(followers_data[0].get("values"))
    data_row_amount = len(followers_data)
    
    # Main Table
    requests = [
        # Cleaning status error cell
        {
            "updateCells": {
                "rows": [{"values": [{"userEnteredValue": {"stringValue": ""}}]}],
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": 0,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1,
                    "endRowIndex": 1,
                }
            }
        },
        {
            "updateCells": {
                "rows": followers_data,
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": current_monthly_position,
                    "startColumnIndex": starting_column_index,
                    "endColumnIndex": starting_column_index + data_column_amount,
                    "endRowIndex": current_monthly_position + 1,
                }
            }
        }
    ]

    # Base data for graphics
    compare_months = [
        {
            "name": spanish_months[month.get("number") - 3],
            "row_number": spanish_months.index(spanish_months[month.get("number") - 3]) + current_worksheet.get("tables_data")[0].get("row_starting_position")
        },
        {
            "name": spanish_months[month.get("number") - 2],
            "row_number": spanish_months.index(spanish_months[month.get("number") - 2]) + current_worksheet.get("tables_data")[0].get("row_starting_position")
        },
        {
            "name": month.get("name"),
            "row_number": current_monthly_position + 1
        },
    ]

    charts_data = current_worksheet.get("charts")

    for chart in charts_data:
        # sheet_data for graph tables
        table_source = chart.get("table_source")
        comparing_graphic_rows = get_base_graphic_compare_table(compare_months, table_source.get("formula_letter_index"))

        # table limits
        data_graphic_column_amount = len(comparing_graphic_rows[0].get("values"))
        data_graphic_row_amount = len(comparing_graphic_rows)

        requests.append({
        "updateCells": {
            "rows": comparing_graphic_rows,
            "fields": "userEnteredValue",
            "range": {
                "sheetId": worksheet_id,
                "startRowIndex": table_source.get("row_starting_position") - 1,
                "startColumnIndex": table_source.get("column_starting_position") - 1,
                "endColumnIndex": (table_source.get("column_starting_position") - 1) + data_graphic_column_amount,
                "endRowIndex": (table_source.get("row_starting_position") - 1) + data_graphic_row_amount,
            }
        }
    })

    #######################################################################################################
    # Totals:
    requests.append(generate_totals(month, current_monthly_position + 1, worksheets))

    return requests


def generate_demographics(month, blog_id, worksheets):
    # Table Base
    current_worksheet = list(filter(lambda item: item.get("title") == "Sexo y edad", worksheets))[0]
    worksheet_id = current_worksheet.get("id")

    # api_data
    gender_data = get_gender(month, blog_id)
    age_data = get_age(month, blog_id)

    # Code guard
    if (not gender_data.get("success")) or (not age_data.get("success")):
        
        feedback_message = gender_data.get("data") if not gender_data.get("success") else age_data.get("data")

        requests = [
            {
                "updateCells": {
                    "rows": feedback_message,
                    "fields": "userEnteredValue",
                    "range": {
                        "sheetId": worksheet_id,
                        "startRowIndex": 0,
                        "startColumnIndex": 0,
                        "endColumnIndex": 1,
                        "endRowIndex": 1,
                    }
                }
            }
        ]
        return requests
    
    if gender_data.get("success") == True:
        gender_data = gender_data.get("data")

    if age_data.get("success") == True:
        age_data = age_data.get("data")

    # gender table limits
    gender_index_starting_row = current_worksheet.get("tables_data")[1].get("row_starting_position") - 1
    gender_starting_column_index = current_worksheet.get("tables_data")[1].get("column_starting_position") - 1
    gender_data_column_amount = len(gender_data[0].get("values"))
    gender_data_row_amount = len(gender_data)

    # Age table limits
    age_index_starting_row = current_worksheet.get("tables_data")[0].get("row_starting_position") - 1
    age_starting_column_index = current_worksheet.get("tables_data")[0].get("column_starting_position") - 1
    age_data_column_amount = len(age_data[0].get("values"))
    age_data_row_amount = len(age_data)

    requests = [
        # Cleaning status error cell
        {
            "updateCells": {
                "rows": [{"values": [{"userEnteredValue": {"stringValue": ""}}]}],
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": 0,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1,
                    "endRowIndex": 1,
                }
            }
        },
        # Writes the month name
        {
            "updateCells": {
                "rows": [
                    {
                        "values": [
                            {"userEnteredValue": {"stringValue": month.get("name")}}, 
                        ]
                    }
                ],
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1,
                    "endRowIndex": 2,
                }
            }
        },
        {
            "updateCells": {
                "rows": gender_data,
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": gender_index_starting_row,
                    "startColumnIndex": gender_starting_column_index,
                    "endColumnIndex": gender_starting_column_index + gender_data_column_amount,
                    "endRowIndex": gender_index_starting_row + gender_data_row_amount,
                }
            }
        },
        {
            "updateCells": {
                "rows": age_data,
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": age_index_starting_row,
                    "startColumnIndex": age_starting_column_index,
                    "endColumnIndex": age_starting_column_index + age_data_column_amount,
                    "endRowIndex": age_index_starting_row + age_data_row_amount,
                }
            }
        },
    ]

    return requests

def generate_interactions_without_ads(rows_data, month, worksheets):
    # Table Base
    current_worksheet = list(filter(lambda item: item.get("title") == "Interacciones SIN ADS", worksheets))[0]
    worksheet_id = current_worksheet.get("id")

    # Code guard
    if not rows_data:
        return

    # table limits
    current_monthly_position = (current_worksheet.get("tables_data")[0].get("row_starting_position") - 1) + (month.get("number") - 1)
    starting_column_index = current_worksheet.get("tables_data")[0].get("column_starting_position") - 1
    data_column_amount = len(rows_data[0].get("values"))
    # data_row_amount = len(rows_data)

     # Main Table
    requests = [
        {
            "updateCells": {
                "rows": rows_data,
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": current_monthly_position,
                    "startColumnIndex": starting_column_index,
                    "endColumnIndex": starting_column_index + data_column_amount,
                    "endRowIndex": current_monthly_position + 1,
                }
            }
        }
    ]

    # Base data for graphics
    compare_months = [
        {
            "name": spanish_months[month.get("number") - 3],
            "row_number": spanish_months.index(spanish_months[month.get("number") - 3]) + current_worksheet.get("tables_data")[0].get("row_starting_position")
        },
        {
            "name": spanish_months[month.get("number") - 2],
            "row_number": spanish_months.index(spanish_months[month.get("number") - 2]) + current_worksheet.get("tables_data")[0].get("row_starting_position")
        },
        {
            "name": month.get("name"),
            "row_number": current_monthly_position + 1
        },
    ]

    charts_data = current_worksheet.get("charts")

    for chart in charts_data:
        # sheet_data for graph tables
        table_source = chart.get("table_source")
        comparing_graphic_rows = get_base_graphic_compare_table(compare_months, table_source.get("formula_letter_index"))

        # table limits
        data_graphic_column_amount = len(comparing_graphic_rows[0].get("values"))
        data_graphic_row_amount = len(comparing_graphic_rows)

        requests.append({
        "updateCells": {
            "rows": comparing_graphic_rows,
            "fields": "userEnteredValue",
            "range": {
                "sheetId": worksheet_id,
                "startRowIndex": table_source.get("row_starting_position") - 1,
                "startColumnIndex": table_source.get("column_starting_position") - 1,
                "endColumnIndex": (table_source.get("column_starting_position") - 1) + data_graphic_column_amount,
                "endRowIndex": (table_source.get("row_starting_position") - 1) + data_graphic_row_amount,
            }
        }
    })

    return requests

def generate_metrics_without_ads(rows_data, month, worksheets):
    # Table Base
    current_worksheet = list(filter(lambda item: item.get("title") == "Métricas SIN ADS", worksheets))[0]
    worksheet_id = current_worksheet.get("id")

    # Code guard
    if not (rows_data[0] and rows_data[1]):
        return
    
    requests = []
    # print(json.dumps(rows_data, indent=4))
    
    for i, table_rows_data in enumerate(rows_data):
        
        # table limits
        current_monthly_position = (current_worksheet.get("tables_data")[i].get("row_starting_position") - 1) + (month.get("number") - 1)
        starting_column_index = current_worksheet.get("tables_data")[i].get("column_starting_position") - 1
        data_column_amount = len(table_rows_data[0].get("values"))
        # data_row_amount = len(table_rows_data)

        # Main Table
        requests.append([
            {
                "updateCells": {
                    "rows": table_rows_data,
                    "fields": "userEnteredValue",
                    "range": {
                        "sheetId": worksheet_id,
                        "startRowIndex": current_monthly_position,
                        "startColumnIndex": starting_column_index,
                        "endColumnIndex": starting_column_index + data_column_amount,
                        "endRowIndex": current_monthly_position + 1,
                    }
                }
            }
        ])

        # Base data for graphics
        compare_months = [
            {
                "name": spanish_months[month.get("number") - 3],
                "row_number": spanish_months.index(spanish_months[month.get("number") - 3]) + current_worksheet.get("tables_data")[0].get("row_starting_position")
            },
            {
                "name": spanish_months[month.get("number") - 2],
                "row_number": spanish_months.index(spanish_months[month.get("number") - 2]) + current_worksheet.get("tables_data")[0].get("row_starting_position")
            },
            {
                "name": month.get("name"),
                "row_number": current_monthly_position + 1
            },
        ]

        charts_data = current_worksheet.get("charts")

        for chart in charts_data:
            # sheet_data for graph tables
            table_source = chart.get("table_source")
            comparing_graphic_rows = get_base_graphic_compare_table(compare_months, table_source.get("formula_letter_index"))

            # table limits
            data_graphic_column_amount = len(comparing_graphic_rows[0].get("values"))
            data_graphic_row_amount = len(comparing_graphic_rows)

            requests.append({
            "updateCells": {
                "rows": comparing_graphic_rows,
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": table_source.get("row_starting_position") - 1,
                    "startColumnIndex": table_source.get("column_starting_position") - 1,
                    "endColumnIndex": (table_source.get("column_starting_position") - 1) + data_graphic_column_amount,
                    "endRowIndex": (table_source.get("row_starting_position") - 1) + data_graphic_row_amount,
                }
            }
        })

    return requests

def generate_details_st(month, blog_id, worksheets):
    # Table Base
    current_worksheet = list(filter(lambda item: item.get("title") == "Detalles ST", worksheets))[0]
    worksheet_id = current_worksheet.get("id")

    # api_data
    stories_details_data = get_detalles_st(month, blog_id)
    
    # Code guard
    if (not stories_details_data.get("success")) and (stories_details_data.get("status") == "empty_metricool"):

        requests = [
            {
                "updateCells": {
                    "rows": stories_details_data.get("data"),
                    "fields": "userEnteredValue",
                    "range": {
                        "sheetId": worksheet_id,
                        "startRowIndex": 0,
                        "startColumnIndex": 0,
                        "endColumnIndex": 1,
                        "endRowIndex": 1,
                    }
                }
            }
        ]
        return requests
    
    if stories_details_data.get("success") == True:
        stories_details_data = stories_details_data.get("data")
    
    # table limits
    row_starting_position_index = current_worksheet.get("tables_data")[0].get("row_starting_position") - 1
    starting_column_index = current_worksheet.get("tables_data")[0].get("column_starting_position") - 1
    data_column_amount = len(stories_details_data[0].get("values"))
    data_row_amount = len(stories_details_data)

    requests = [
        {
            # CLEANING table
            "repeatCell": {
                "range": {
                    "sheetId": worksheet_id,  # Place the worksheet ID
                    "startRowIndex": row_starting_position_index,  # Clear from the very top
                    "startColumnIndex": starting_column_index,
                    # "endRowIndex": data_row_amount,
                    "endColumnIndex": data_column_amount + 1
                },
                "cell": {
                    "userEnteredValue": {} # This "empties" the cell
                },
                "fields": "userEnteredValue"
            },
        },
        { #CLEANING status error cell
            "updateCells": {
                "rows": [
                    {
                        "values": [
                            {"userEnteredValue": {"stringValue": ""}}
                        ]
                    }
                ],
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": 0,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1,
                    "endRowIndex": 1,
                }
            }
        },
        { #MONTH TITLE
            "updateCells": {
                "rows": [
                    {
                        "values": [
                            {"userEnteredValue": {"stringValue": month.get("name")}}
                        ]
                    }
                ],
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": 1,
                    "startColumnIndex": 1,
                    "endColumnIndex": 2,
                    "endRowIndex": 2,
                }
            }
        },
        {
            "updateCells": {
                "rows": stories_details_data,
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": row_starting_position_index,
                    "startColumnIndex": starting_column_index,
                    "endColumnIndex": starting_column_index + data_column_amount,
                    "endRowIndex": data_row_amount + row_starting_position_index,
                }
            }
        }
    ]

    #######################################################################################################
    # Metrics ST:
    requests += generate_metrics_st(month, worksheets)

    return requests
    

def generate_metrics_st(month, worksheets):
    # Table Base
    current_worksheet = list(filter(lambda item: item.get("title") == "Métricas ST", worksheets))[0]
    worksheet_id = current_worksheet.get("id")

    # api_data
    metrics_data = get_metrics_st(month, current_worksheet)

    # Code Guard
    if not metrics_data:
        return 
    
    # table limits
    row_starting_position = current_worksheet.get("tables_data")[0].get("row_starting_position")
    current_monthly_position = (row_starting_position - 1) + (month.get("number") - 1)
    starting_column_index = current_worksheet.get("tables_data")[0].get("column_starting_position") - 1
    data_column_amount = len(metrics_data[0].get("values"))
    data_row_amount = len(metrics_data)

    requests = [
        {
            "updateCells": {
                "rows": metrics_data,
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": current_monthly_position,
                    "startColumnIndex": starting_column_index,
                    "endColumnIndex": starting_column_index + data_column_amount,
                    "endRowIndex": current_monthly_position + 1,
                }
            }
        }
    ]

    # Base data for graphics
    compare_months = [
        {
            "name": spanish_months[month.get("number") - 3],
            "row_number": spanish_months.index(spanish_months[month.get("number") - 3]) + row_starting_position
        },
        {
            "name": spanish_months[month.get("number") - 2],
            "row_number": spanish_months.index(spanish_months[month.get("number") - 2]) + row_starting_position
        },
        {
            "name": month.get("name"),
            "row_number": current_monthly_position + 2
        },
    ]

    # Graphics data
    charts_data = current_worksheet.get("charts")
    table_source = charts_data[0].get("table_source")
    chart_rows_data = get_base_graphic_compare_table(compare_months, table_source.get("formula_letter_index"))

    starting_column_index = table_source.get("column_starting_position") - 1
    starting_row_index = table_source.get("row_starting_position") - 1
    chart_data_column_amount = len(chart_rows_data[0].get("values"))
    chart_data_row_amount = len(chart_rows_data)

    # Stories Graphic
    requests.append({
        "updateCells": {
            "rows": chart_rows_data,
            "fields": "userEnteredValue",
            "range": {
                "sheetId": worksheet_id,
                "startRowIndex": starting_row_index,
                "startColumnIndex": starting_column_index,
                "endColumnIndex": starting_column_index + chart_data_column_amount,
                "endRowIndex": starting_row_index + chart_data_row_amount,
            }
        }
    })

    return requests

def generate_competitors(month, blog_id, worksheets):
    # Table Base
    current_worksheet = list(filter(lambda item: item.get("title") == "Competidores", worksheets))[0]
    worksheet_id = current_worksheet.get("id")

    # api_data
    data = get_competitors(month, blog_id, current_worksheet)

    # Code guard
    if (not data.get("success")) and (data.get("status") == "empty_metricool"):

        requests = [
            {
                "updateCells": {
                    "rows": data.get("data"),
                    "fields": "userEnteredValue",
                    "range": {
                        "sheetId": worksheet_id,
                        "startRowIndex": 0,
                        "startColumnIndex": 0,
                        "endColumnIndex": 1,
                        "endRowIndex": 1,
                    }
                }
            }
        ]
        return requests
    
    
    if data.get("success"):
        data = data.get("data")
    
    # Main table limits
    competitors_tables_data = current_worksheet.get("tables_data")

    requests = [
        # CLEANING status error cell
        {
            "updateCells": {
                "rows": [{"values": [{"userEnteredValue": {"stringValue": ""}}]}],
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": 0,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1,
                    "endRowIndex": 1,
                }
            }
        }
    ]

    for i, row in enumerate(competitors_tables_data): 

        # Main table limits
        row_starting_position = row.get("row_starting_position")
        current_monthly_position = month.get("number") + row_starting_position - 1
        starting_column_index = row.get("column_starting_position") - 1
        data_column_amount = len(data.get("titles")[0].get("values"))

        # Titles
        requests.append({
            "updateCells": {
                "rows": data.get("titles"),
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": row_starting_position - 1,
                    "startColumnIndex": starting_column_index + 1,
                    "endColumnIndex": (data_column_amount) + 1,
                    "endRowIndex": row_starting_position,
                }
            }
        })

        # Competitors data
        requests.append({
            "updateCells": {
                "rows": data.get("data").get(row.get("name")),
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": current_monthly_position,
                    "startColumnIndex": starting_column_index,
                    "endColumnIndex": (data_column_amount + 1),
                    "endRowIndex": current_monthly_position + 1,
                }
            }
        })

        # GRAPHICS

        chart_data = current_worksheet.get("charts")[i].get("table_source")

        # Titles
        clean_titles = [{"values": [title for title in data.get("titles")[0].get("values") if title.get("userEnteredValue").get("stringValue") != "%"]}]
        data_column_amount = len(clean_titles[0].get("values"))

        requests.append({
            "updateCells": {
                "rows": clean_titles,
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": chart_data.get("row_starting_position") - 1,
                    "startColumnIndex": chart_data.get("column_starting_position"),
                    "endColumnIndex": (chart_data.get("column_starting_position") + data_column_amount),
                    "endRowIndex": chart_data.get("row_starting_position"),
                }
            }
        })

        # Base data for graphics
        compare_months = [
            {
                "name": spanish_months[month.get("number") - 3],
                "row_number": spanish_months.index(spanish_months[month.get("number") - 3]) + row.get("row_starting_position") + 1
            },
            {
                "name": spanish_months[month.get("number") - 2],
                "row_number": spanish_months.index(spanish_months[month.get("number") - 2]) + row.get("row_starting_position") + 1
            },
            {
                "name": month.get("name"),
                "row_number": current_monthly_position + 1
            },
        ]

        # Competitors data
        competitors_data = [competidores_sheet for competidores_sheet in worksheets if competidores_sheet.get("title") == "Competidores"][0].get("data")

        formula_index_competitors = list(map(lambda comp: comp.get("formula_index"), competitors_data))

        requests.append({
            "updateCells": {
                "rows": get_base_graphic_compare_table(compare_months, formula_index_competitors),
                "fields": "userEnteredValue",
                "range": {
                    "sheetId": worksheet_id,
                    "startRowIndex": chart_data.get("row_starting_position"),
                    "startColumnIndex": chart_data.get("column_starting_position") - 1,
                    "endColumnIndex": ((chart_data.get("column_starting_position") - 1) + data_column_amount + 1),
                    "endRowIndex": chart_data.get("row_starting_position") + len(compare_months),
                }
            }
        })

    return requests
    

def create_report(month, blog_id):
    
    worksheets = [comp.get("worksheets") for comp in profile_specs if comp.get("name") == blog_id.get("name")][0]
    
    requests = [
        generate_details_IG(month, blog_id, worksheets),
        generate_followers(month, blog_id, worksheets),
        generate_demographics(month, blog_id, worksheets),
        generate_details_st(month, blog_id, worksheets),
        generate_competitors(month, blog_id, worksheets),
    ]

    if len(requests) > 0:
        
        sheet = connected_sheet(blog_id.get("sheet-id"))
        sheet.batch_update({"requests": requests})

    print("---BUILD COMPLETE---")