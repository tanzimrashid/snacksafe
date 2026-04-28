#################
# Deopendencies #
#################
import asyncio, httpx, json
from nicegui import app,ui
from nicegui_scanner import BarcodeScanner

#############
# Constants #
#############
COPYRIGHT_DATE = "2026"
#APP_VERSION = "0.2"
#AUTHOR = "Tanzim Rashid, Houston Meyer"
PROFILES_PATH = "./assets/json/profiles.json"
ALLERGENS_PATH = "./assets/json/allergens.json"

#############
# Functions #
#############
### Main OpenFoodFacts API Function ###
async def get_barcode_info(barcode):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            # Checks for HTTP errors (404, server down, etc)
            response.raise_for_status() 
            
            data = response.json()
            if data.get('status') == 1:
                product = data.get('product', {})
                # unformatted allergen output from Open Food Facts API
                raw_allergens = product.get('allergens_tags', [])
                # Cleaned allergen output for readability - (removes "en:" prefix & replaces instances of "-" with a space)
                allergen_output = [a.replace('en:', '').replace('-', ' ').title() for a in raw_allergens]

                # Return dictionary with relevant info required for the app
                return {
                    'name': product.get('product_name', 'Unknown Product'),
                    'image': product.get('image_front_url', ''),
                    'nutriscore': product.get('nutriscore_grade', 'N/A').upper(), # Upper func required for consistency
                    'nova': product.get('nova_group', 'N/A'),
                    'allergies': allergen_output
                }
            else:
                return None

    # Catch 404 errors (invalid product, nonfood product, etc. -- does not exist in DB)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            print(f"Barcode {barcode} not found in API (404).")
            return None
        else:
            print(f"Error: {e}")
            return "Connection Error"
    # Catch network erors
    except httpx.RequestError as e:
        print(f"Network error: {e}")
        return "Connection Error"

####################
# Load JSON Assets #
####################
# Path opens a json file at the given path adn returns its contents as a Python list or dictionary. 
# If the file doesnt exist or can't be read it returns none   
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

# Calls load_json to load the profiles file into memory. The or [] means if the file returns None
profiles = load_json(PROFILES_PATH) or []
# Same as above but for the allergens file
ALLERGEN_OPTIONS = load_json(ALLERGENS_PATH) or []
# Debugging Lines
print("Loaded profiles:", profiles)
print("Loaded allergens:", ALLERGEN_OPTIONS)

# Opens the profiles JSON file in write mode and overwrites it with the current state of the profiles list in memory
# Indent=4 makes the output human-readable in the file, and the try/except catches any file writing errors and prints them to the terminal
def save_profiles():
    try:
        with open(PROFILES_PATH, "w", encoding="utf-8") as file:
            json.dump(profiles, file, indent=4)
        print("Profiles saved successfully to:", PROFILES_PATH)
    except Exception as e:
        print("ERROR saving profiles:", e)
#Still struggling to save the info in our json. The data is there, just not physcially showing up
    
################
# Dictionaries #
################
nutriscore_dict = {
    "A": {
        "score" : "A",
        "desc"  : "Highest nutritional quality",
        "img"   : "/assets/img/nutriscore/score-a.png"
    },
    "B": {
        "score" : "B",
        "desc"  : "Favourable nutritional quality",
        "img"   : "/assets/img/nutriscore/score-b.png"
    },
    "C": {
        "score" : "C",
        "desc"  : "Moderate nutritional quality",
        "img"   : "/assets/img/nutriscore/score-c.png"
    },
    "D": {
        "score" : "D",
        "desc"  : "Lower nutritional quality",
        "img"   : "/assets/img/nutriscore/score-d.png"
    },
    "E": {
        "score" : "E",
        "desc"  : "Lowest nutritional quality",
        "img"   : "/assets/img/nutriscore/score-e.png"
    },
    "N/A": {
        "score" : "N/A",
        "desc"  : "Unknown nutritional quality",
        "img"   : "/assets/img/nutriscore/score-unknown.png"
    }
}

nova_dict = {
    "1" : {
        "group" : "Group 1",
        "desc"  : "Unprocessed or minimally processed foods",
        "img"   : "/assets/img/NOVA/group-1.png"
    },
    "2" : {
        "group" : "Group 2",
        "desc"  : "Processed culinary ingredients",
        "img"   : "/assets/img/NOVA/group-2.png"
    },
    "3" : {
        "group" : "Group 3",
        "desc"  : "Processed foods",
        "img"   : "/assets/img/NOVA/group-3.png"
    },
    "4" : {
        "group" : "Group 4",
        "desc"  : "Ultra-processed foods",
        "img"   : "/assets/img/NOVA/group-4.png"
    },
    "N/A" : {
        "group" : "N/A",
        "desc"  : "Unknown NOVA classification",
        "img"   : "/assets/img/NOVA/group-unknown.png"
    }
}
