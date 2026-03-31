import os
from dotenv import load_dotenv
from datetime import datetime
from functools import reduce

from src.metricool.api_requests import get_instagram
from src.sheet.sheet_data import spanish_months
from src.utils.date_handlers import get_monthly_range_date
from src.utils.data_handlers import change_keys_dict_list
from src.utils.config_handlers import get_application_path
    # ----------------------------------------------

# Load environment variables from .env file
root_dir = get_application_path(__file__)
env_path = os.path.join(root_dir, ".env")
load_dotenv(dotenv_path=env_path)

# --- Configuration ---
BASE_URL = "https://app.metricool.com/api"

# Get credentials from environment variables
USER_TOKEN = os.getenv("USER_TOKEN")
USER_ID = os.getenv("USER_ID")

# Check if all required credentials are set
if not all([USER_TOKEN, USER_ID]):
    print("Error: USER_TOKEN or USER_ID not set in .env file.")
    print("Please replace the placeholder values with your actual Metricool credentials.")
    # Exit gracefully if credentials are not set
    exit()

headers = {
    "X-Mc-Auth": USER_TOKEN,
    "Content-Type": "application/json"
}

# Persistent Data to be used in multiple calls
stored_data = {}


def get_formula(letter, current_row, row_to_compare):
    return f"=IFERROR(({letter}{current_row}-{letter}{row_to_compare})/{letter}{row_to_compare}*100, {""})"
# -----------------------------------------------------
# Instagram demographic distribution

# Distribución por SEXO de toda la cuenta durante un período de tiempo (start_date y end_date) provenientes de range_date

def get_gender(month, blog_id):
    
    date_ranges = get_monthly_range_date(month.get("number"))

    endpoint = f"/v2/analytics/distribution"
    url = f"{BASE_URL}{endpoint}"

    params = {
        "userId": USER_ID,
        "blogId": blog_id.get("code"),
        "timezone": "America/Caracas",
        "network": "instagram",
        "metric": "gender", #age, gender, city, country
        "subject": "account",
        "from": date_ranges[0],
        "to": date_ranges[1],
    }

    try: 

        demographic_gender = get_instagram(url, headers, params)

        demographic_gender = [{item["key"]: item["value"]} for item in demographic_gender["data"]]

        key_changes = {
            "M": "Masculino",
            "F": "Femenino",
            "U": "Desconocido",
        }

        demographic_gender = change_keys_dict_list(demographic_gender, key_changes)

        demographic_gender = list(map(lambda gend: {"values": [
            {"userEnteredValue": {"stringValue": list(gend.keys())[0]}},
            {"userEnteredValue": {"numberValue": list(gend.values())[0]}}
        ]}, demographic_gender))
        
        return demographic_gender
    
    except Exception as error:
        print("===============================")
        print("Something bad happend getting gender data:")
        print(error)

# # Distribución por EDAD de toda la cuenta durante un período de tiempo (start_date y end_date) provenientes de range_date

def get_age(month, blog_id):
    
    date_ranges = get_monthly_range_date(month.get("number"))

    endpoint = f"/v2/analytics/distribution"
    url = f"{BASE_URL}{endpoint}"

    params = {
        "userId": USER_ID,
        "blogId": blog_id.get("code"),
        "timezone": "America/Caracas",
        "network": "instagram",
        "metric": "age", #age, gender, city, country
        "subject": "account",
        "from": date_ranges[0],
        "to": date_ranges[1],
    }

    try:

        demographic_age = get_instagram(url, headers, params)

        demographic_age = [{item["key"]: item["value"]} for item in demographic_age["data"]]

        demographic_age = sorted(demographic_age, key=lambda d: int(list(d.keys())[0].split('-')[0].split('+')[0]))

        demographic_age = list(map(lambda age: {"values": [
            {"userEnteredValue": {"stringValue": list(age.keys())[0]}},
            {"userEnteredValue": {"numberValue": list(age.values())[0]}}
        ]}, demographic_age))

        return demographic_age
    
    except Exception as error:
        print("===============================")
        print("Something bad happend getting age data:")
        print(error)

# ----------------------------------------------------
# Get Basic data from posts and reels of instagram

def get_detalles_ig(month, blog_id, worksheets):
    
    date_ranges = get_monthly_range_date(month.get("number"))

    endpoint = "/v2/analytics/posts/instagram" #stories, reels or posts
    url = f"{BASE_URL}{endpoint}"

    params = {
        "userId": USER_ID,
        "blogId": blog_id.get("code"),
        "timezone": "America/Caracas",
        "from": date_ranges[0],
        "to": date_ranges[1],
    }

    try:

        instagram_posts = get_instagram(url, headers, params)

        endpoint = "/v2/analytics/reels/instagram"
        url = f"{BASE_URL}{endpoint}"

        instagram_reels = get_instagram(url, headers, params)

        detalles_ig_data = []

        # cleaning the data to be used
        for post in instagram_posts.get("data"):
            detalles_ig_data.append({
                "meta":{
                    "type": "post",
                    "publishedAt": datetime.fromisoformat(post.get("publishedAt").get("dateTime")),
                },

                "data": [
                    {"type": "numberValue", "content": post.get("likes")}, #ME GUSTAS
                    {"type": "numberValue", "content": post.get("comments")}, #COMENTARIOS
                    {"type": "numberValue", "content": post.get("shares")}, #COMPARTIDOS
                    {"type": "numberValue", "content": post.get("saved")}, #GUARDADOS
                    {"type": "stringValue", "content": post.get("")}, #REPOSTEOS
                    {"type": "numberValue", "content": post.get("reach")}, #ALCANCE POSTS
                    {"type": "stringValue", "content": ""}, #ALCANCE REELS
                    {"type": "numberValue", "content": post.get("views")}, #VISUALIZACIONES POSTS
                    {"type": "stringValue", "content": ""}, #VISUALIZACIONES REELS
                    {"type": "formulaValue", "content": "INSERT FÓRMULA"}, #VISUALIZACIONES TOTALES
                    {"type": "stringValue", "content": ""}, #VISTAS AL PERFIL
                    {"type": "formulaValue", "content": "INSERT FÓRMULA"}, #INTERACCIONES
                    {"type": "formulaValue", "content": "INSERT FÓRMULA"}, #ALCANCE TOTAL
                    {"type": "numberValue", "content": post.get("engagement")}, #ENGAGEMENT
                ]

            })

        for reel in instagram_reels.get("data"):
            detalles_ig_data.append({
                "meta":{
                    "type": "reel",
                    "publishedAt": datetime.fromisoformat(reel.get("publishedAt").get("dateTime")),
                },
                "data":[

                    {"type": "numberValue", "content": reel.get("likes")}, #ME GUSTAS
                    {"type": "numberValue", "content": reel.get("comments")}, #COMENTARIOS
                    {"type": "numberValue", "content": reel.get("shares")}, #COMPARTIDOS
                    {"type": "numberValue", "content": reel.get("saved")}, #GUARDADOS
                    {"type": "numberValue", "content": reel.get("reposts")}, #REPOSTEOS
                    {"type": "stringValue", "content": ""}, #ALCANCE POSTS
                    {"type": "numberValue", "content": reel.get("reach")}, #ALCANCE REELS
                    {"type": "stringValue", "content": ""}, #VISUALIZACIONES POSTS
                    {"type": "numberValue", "content": reel.get("views")}, #VISUALIZACIONES REELS
                    {"type": "formulaValue", "content": "INSERT FÓRMULA"}, #VISUALIZACIONES TOTALES
                    {"type": "stringValue", "content": ""}, #VISTAS AL PERFIL
                    {"type": "formulaValue", "content": "INSERT FÓRMULA"}, #INTERACCIONES
                    {"type": "formulaValue", "content": "INSERT FÓRMULA"}, #ALCANCE TOTAL
                    {"type": "numberValue", "content": reel.get("engagement")}, #ENGAGEMENT
                ]

            })

        # Ordering the publications by published date (newest to oldest)
        detalles_ig_data.sort(key=lambda pub: pub.get("meta").get("publishedAt"), reverse=False) #Reverse for the order

        # Setting Formulas
        for i, pub in enumerate(detalles_ig_data):
            # Sum Visualizaciones_Totales
            pub.get("data")[9]["content"] = f"=IFERROR(SUM(I{8 + i}:J{8 + i}), \"\")"

            # Sum Interacciones_Totales
            pub.get("data")[11]["content"] = f"=IFERROR(SUM(B{8 + i}:F{8 + i}), \"\")"

            # Sum Alcance_Total
            pub.get("data")[12]["content"] = f"=IFERROR(SUM(G{8 + i}:H{8 + i}), \"\")"
            
        # Building API Request
        detalles_ig_data_rows = list(map(lambda media: {"values": [
            {"userEnteredValue": {metric.get("type"): metric.get("content")}} for metric in media.get("data")
        ]}, detalles_ig_data))

        # Adding column row number to each row
        list(map(lambda media: media[1].get("values").insert(0,{"userEnteredValue": {"numberValue": (media[0] + 1)}}), enumerate(detalles_ig_data_rows)))

        # Storing Persisting data
        stored_data["publications"] = len(detalles_ig_data_rows)
        stored_data["total_views"] = reduce(lambda acc, row: acc + (row.get("data")[7].get("content") if row.get("meta").get("type") == 'post' else row.get("data")[8].get("content")), detalles_ig_data, 0)
        stored_data["interactions"] = reduce(lambda acc, row: acc + row.get("data")[0].get("content") + row.get("data")[1].get("content") + row.get("data")[2].get("content") + row.get("data")[3].get("content") + (row.get("data")[4].get("content") if isinstance(row.get("data")[4].get("content"), int) else 0), detalles_ig_data, 0)
        stored_data["profile_views"] = 0
        stored_data["engagement"] = reduce(lambda acc, row: acc + (row.get("data")[13].get("content")), detalles_ig_data, 0) / len(detalles_ig_data_rows)

        #######################################################################################################
        # Interations without ads:
        interactions_without_ads = get_interactions_without_ads(detalles_ig_data, month, worksheets)
        #######################################################################################################
        # Metrics without ads:
        metrics_without_ads = get_metrics_without_ads(stored_data, detalles_ig_data, month, worksheets)

        all_data = {
            "detalles_ig": detalles_ig_data_rows,
            "interactions_without_ads": interactions_without_ads,
            "metrics_without_ads": metrics_without_ads
        }

        return all_data
    
    except Exception as error:
        print("===============================")
        print("Something bad happend getting details_ig data:")
        print(error)

# -----------------------------------------------------
# 
def get_interactions_without_ads(base_data, month, worksheets):
    # Table Base
    current_worksheet = list(filter(lambda item: item.get("title") == "Interacciones SIN ADS", worksheets))[0]

    # Formula data
    row_starting_position = current_worksheet.get("tables_data")[0].get("row_starting_position")
    current_month_row = row_starting_position + (month.get("number") - 1)
    row_to_compare = spanish_months.index(spanish_months[month.get("number") - 2]) + row_starting_position

    # data for each column in the table
    columns_data = current_worksheet.get("tables_data")[0].get("columns_data")

    interactions_without_ads = [{"userEnteredValue": {"stringValue": month.get("name")}}]
    
    for i, column in enumerate(columns_data):
        # main column data
        interactions_without_ads.append(
            {"userEnteredValue": {"numberValue": reduce(lambda acc, curr: acc + (curr.get("data")[column.get("base_data_index")].get("content") if isinstance(curr.get("data")[column.get("base_data_index")].get("content"), int) else 0), base_data, 0)}}
        )
        # formula column
        interactions_without_ads.append({"userEnteredValue": {"formulaValue": get_formula(column.get("formula_letter"), current_month_row, row_to_compare)}})
        
        # empty space intersection column
        if i < (len(columns_data) - 1):
            interactions_without_ads.append({"userEnteredValue": {"stringValue": ""}})

    interactions_without_ads = [{"values": interactions_without_ads}]

    return interactions_without_ads
# -----------------------------------------------------
# 
def get_metrics_without_ads(posts_and_reels_base_data, reels_base_data, month, worksheets):
    # Table Base
    current_worksheet = list(filter(lambda item: item.get("title") == "Métricas SIN ADS", worksheets))[0]

    ################################################################################################
    # (POST AND REELS) Table
    # Formula
    row_starting_position = current_worksheet.get("tables_data")[0].get("row_starting_position")
    current_month_row = row_starting_position + (month.get("number") - 1)
    row_to_compare = spanish_months.index(spanish_months[month.get("number") - 2]) + row_starting_position

    # data for each column in the table
    columns_data = current_worksheet.get("tables_data")[0].get("columns_data")

    posts_and_reels_without_ads = [{"userEnteredValue": {"stringValue": month.get("name")}}]
    
    for i, column in enumerate(columns_data):
        # main column data
        posts_and_reels_without_ads.append(
            {"userEnteredValue": {"numberValue": posts_and_reels_base_data.get(column.get("stored_data_key"))}}
        )
        # formula column
        posts_and_reels_without_ads.append({"userEnteredValue": {"formulaValue": get_formula(column.get("formula_letter"), current_month_row, row_to_compare)}})

        # empty space intersection column
        if i < (len(columns_data) - 1):
            posts_and_reels_without_ads.append({"userEnteredValue": {"stringValue": ""}})

    posts_and_reels_without_ads = [{"values": posts_and_reels_without_ads}]

    ################################################################################################
    # REELS Table
    # Formula
    row_starting_position = current_worksheet.get("tables_data")[1].get("row_starting_position")
    current_month_row = row_starting_position + (month.get("number") - 1)
    row_to_compare = spanish_months.index(spanish_months[month.get("number") - 2]) + row_starting_position

    # data for each column in the table
    columns_data = current_worksheet.get("tables_data")[1].get("columns_data")

    reels_without_ads = [{"userEnteredValue": {"stringValue": month.get("name")}}]

    for i, column in enumerate(columns_data):
        # main column data
        reels_without_ads.append(
            {"userEnteredValue": {"numberValue": reduce(lambda acc, curr: acc + (curr.get("data")[column.get("base_data_index")].get("content") if isinstance(curr.get("data")[column.get("base_data_index")].get("content"), int) else 0), reels_base_data, 0)}}
        )
        # formula column
        reels_without_ads.append({"userEnteredValue": {"formulaValue": get_formula(column.get("formula_letter"), current_month_row, row_to_compare)}})
        
        # empty space intersection column
        if i < (len(columns_data) - 1):
            reels_without_ads.append({"userEnteredValue": {"stringValue": ""}})

    reels_without_ads = [{"values": reels_without_ads}]
    
    metrics_without_ads = [
        posts_and_reels_without_ads,
        reels_without_ads
    ]

    return metrics_without_ads
# -----------------------------------------------------
# 
def get_followers(month, blog_id, worksheet):
    
    date_ranges = get_monthly_range_date(month.get("number"))
    
    endpoint = f"/v2/analytics/timelines"
    url = f"{BASE_URL}{endpoint}"

    params = {
        "userId": USER_ID,
        "blogId": blog_id.get("code"),
        "timezone": "America/Caracas",
        "network": "instagram",
        "metric": "followers",  # The specific metric -> followers, friends, delta_followers, saved, interactions, count, views, likes, comments, reach, engagement, shares
        "from": date_ranges[0],
        "to": date_ranges[1],
        "subject": "account" #account for metrics: followers, friends, delta_followers, views, reach    #reels for metrics: saved, interactions, count, views, comments, reach, engagement, shares    #posts for metrics: saved, interactions, count, views, likes, comments, reach, engagement, shares
    }
    try:
        
        total_followers = get_instagram(url, headers, params, "metric")

        if len(total_followers.get("data")[0].get("values")) == 0:
            raise ValueError("The API response does not contain the expected 'values' data for followers.")
        
        total_followers = total_followers.get("data")[0].get("values")[0].get("value")

        total_publications = stored_data.get("publications")

        current_row = (month.get("number") - 1) + worksheet.get("tables_data")[0].get("row_starting_position")
        row_to_compare = spanish_months.index(spanish_months[month.get("number") - 2]) + worksheet.get("tables_data")[0].get("row_starting_position")

        followers_data = [{"values": [
            {"userEnteredValue": {"stringValue": month.get("name")}},
            {"userEnteredValue": {"numberValue": total_followers}},
            {"userEnteredValue": {"formulaValue": f"=IFERROR(B{current_row}-B{row_to_compare}, {""})"}},
            {"userEnteredValue": {"formulaValue": get_formula("B", current_row, row_to_compare)}},
            {"userEnteredValue": {"stringValue": ""}},
            {"userEnteredValue": {"numberValue": total_publications}},
        ]}]

        return followers_data

    except Exception as error:
        print("===============================")
        print("Something bad happend getting followers data:")
        print(error)

# -----------------------------------------------------
# Get Basic data from posts and reels of instagram

def get_detalles_st(month, blog_id):
    
    date_ranges = get_monthly_range_date(month.get("number"))

    endpoint = "/v2/analytics/stories/instagram" #stories, reels or posts
    url = f"{BASE_URL}{endpoint}"

    params = {
        "userId": USER_ID,
        "blogId": blog_id.get("code"),
        "timezone": "America/Caracas",
        "from": date_ranges[0],
        "to": date_ranges[1],
    }

    try: 

        instagram_stories = get_instagram(url, headers, params)

        stories_data = list(map(lambda storie: {"reach": storie.get("reach") if isinstance(storie.get("reach"), int) else 0, "impressions": storie.get("impressions") if isinstance(storie.get("impressions"), int) else 0, "publishedAt": storie.get("publishedAt").get("dateTime")}, instagram_stories.get("data")))

        # Ordering the stories by published date (newest to oldest)
        stories_data.sort(key=lambda pub: pub.get("publishedAt"), reverse=False) #Reverse for the order

        # Storing Persisting data
        stored_data["stories"] = {
            "total": len(stories_data),
            "impressions": reduce(lambda acc, storie: acc + storie.get("impressions"), stories_data, 0),
            "reach": reduce(lambda acc, storie: acc + storie.get("reach"), stories_data, 0)
        }

        stories_data = [{
            "values": [
                {"userEnteredValue": {"numberValue": index + 1}},
                {"userEnteredValue": {"numberValue": storie.get("impressions") if isinstance(storie.get("impressions"), int) else 0}},
                {"userEnteredValue": {"numberValue": storie.get("reach") if isinstance(storie.get("reach"), int) else 0}},
            ]
        } for index, storie in enumerate(stories_data)]

        return stories_data
    
    except Exception as error:
        print("===============================")
        print("Something bad happend getting stories metrics data:")
        print(error)

# -----------------------------------------------------
# 
def get_metrics_st(month, blog_id, worksheet):

    try: 

        stories_data = stored_data.get("stories")

        all_impressions = stories_data.get("impressions")
        all_reach = stories_data.get("reach")

        stories_data = [month.get("name"), all_impressions, "INSERT FÓRMULA", "", all_reach, "INSERT FÓRMULA", "", stories_data.get("total"), "INSERT FÓRMULA"]

        # Apply Fórmulas
        current_row = (month.get("number") - 1) + worksheet.get("tables_data")[0].get("row_starting_position")
        row_to_compare = spanish_months.index(spanish_months[month.get("number") - 2]) + worksheet.get("tables_data")[0].get("row_starting_position")

        stories_data[2] = get_formula("B", current_row, row_to_compare)
        stories_data[5] = get_formula("E", current_row, row_to_compare)
        stories_data[8] = get_formula("H", current_row, row_to_compare)

        stories_data = [{"values": [
            {"userEnteredValue": {"stringValue": stories_data[0]}},
            {"userEnteredValue": {"numberValue": stories_data[1]}},
            {"userEnteredValue": {"formulaValue": stories_data[2]}},
            {"userEnteredValue": {"stringValue": stories_data[3]}},
            {"userEnteredValue": {"numberValue": stories_data[4]}},
            {"userEnteredValue": {"formulaValue": stories_data[5]}},
            {"userEnteredValue": {"stringValue": stories_data[6]}},
            {"userEnteredValue": {"numberValue": stories_data[7]}},
            {"userEnteredValue": {"formulaValue": stories_data[8]}},
        ]}]

        return stories_data
    
    except Exception as error:
        print("===============================")
        print("Something bad happend getting stories metrics data:")
        print(error)

# -----------------------------------------------------
def get_competitors(month, blog_id, current_worksheet):
    
    date_ranges = get_monthly_range_date(month.get("number"))

    endpoint = "/v2/analytics/competitors/instagram" #stories, reels or posts
    url = f"{BASE_URL}{endpoint}"

    params = {
        "userId": USER_ID,
        "blogId": blog_id.get("code"),
        "timezone": "America/Caracas",
        "limit": 1000, #I have no idea why but this is necessary...  
        "from": date_ranges[0],
        "to": date_ranges[1],
    }

    try:
        
        instagram_competitors = get_instagram(url, headers, params)

        # getting the data from sheet_data.py
        competitors_order = list(map(lambda comp: comp.get("providerId"), current_worksheet.get("data")))

        # Cleaning and filtering data
        competitors_data = [
            {
                "providerId": comp.get("providerId"), 
                "followers": comp.get("followers") or 0, 
                "posts": (comp.get("posts") or 0) + (comp.get("reels") or 0), 
                "likes": comp.get("likes") or 0, 
                "comments": comp.get("comments") or 0, 
                "engagement": comp.get("engagement") or 0
            } for comp in instagram_competitors.get("data") if comp.get("providerId") in competitors_order]

        # Ordering competitors
        competitors_data = sorted(competitors_data, key=lambda comp: competitors_order.index(comp.get("providerId")))

        formula_columns = list(map(lambda comp: comp.get("formula_index"), current_worksheet.get("data")))

        column_titles = list(map(lambda comp: comp.get("name"), current_worksheet.get("data")))

        column_titles = [sub_item for title in column_titles for sub_item in (title, "%")]

        competitors_tables_data = {
            "titles": [
                {
                    "values": list(map(lambda name: {"userEnteredValue": {"stringValue": name}}, column_titles))
                }
            ],
            "data": {
                category["name"]: [
                    {"values": [
                        {"userEnteredValue": {"stringValue": month.get("name")}}
                    ]}
                ] for category in current_worksheet.get("tables_data") 
            }
        }

        for key, table in competitors_tables_data.get("data").items():
            
            for comp in competitors_data:
                # Value
                table[0].get("values").append({"userEnteredValue": {"numberValue": comp.get(key)}})

                # Formula
                formula_letter = [brand.get("formula_index") for brand in current_worksheet.get("data") if comp.get("providerId") == brand.get("providerId")][0]
                current_row = month.get("number") + [metric.get("row_starting_position") for metric in current_worksheet.get("tables_data") if metric.get("name") == key][0]
                row_to_compare = spanish_months.index(spanish_months[month.get("number") - 2]) + [metric.get("row_starting_position") for metric in current_worksheet.get("tables_data") if metric.get("name") == key][0] + 1

                formula = get_formula(formula_letter, current_row, row_to_compare)

                table[0].get("values").append({"userEnteredValue": {"formulaValue": formula}}) 
            
        
        return competitors_tables_data
    
    except Exception as error:
        print("===============================")
        print("Something bad happend getting competitors data:")
        print(error)

# -------------------------------------------------
