### Tanzim
**Accomplishments / Responsibilities**
- Main UI design
	- Landing page
	- Product details page (incl. photo listing, allergens listing, nutri-score badge, NOVA badge, etc.)
- Main Open Food Facts API function
- NOVA & Nutri-Score dictionaries
- Camera barcode scanning design & logic (incl. error handling / data validation)
	- NiceGUI-Scanner integration
- Manual barcode entry design & logic (incl. error handling / data validation)

**Resources Used:**
- https://pypi.org/project/nicegui/
	- Main GUI framework used by our application
- https://nicegui.io/documentation 
	- Comparable to FreeSimpleGUI Cookbook
	- Heavily utilized example codes & documentation on UI elements, controls, binding properties, page layout, styling & appearance, action & events, pages & routing, etc.
- https://github.com/zauberzeug/nicegui/blob/main/examples/api_requests/main.py
	- Example code for API requests - from NiceGUI website
	- Used as the reference point for developing the Open Food Facts API function
- https://pypi.org/project/nicegui-scanner/
	- Main package used for scanning barcodes within NiceGUI
- https://www.geeksforgeeks.org/python/python-async/
	- Async function for running functions asynchronously
- https://www.geeksforgeeks.org/python/response-raise_for_status-python-requests/
	- Handling URL requests (e.g., 404, network errors, etc.)
- https://realpython.com/list-comprehension-python/
	- Transforming lists / dictionaries to be more human readable
- https://www.w3schools.com/python/python_dictionaries.asp ; https://www.w3schools.com/PYTHON/python_dictionaries_nested.asp
	- Creating dictionaries & nested dictionaries for Main API function, as well as NOVA/Nutri-Score badges
- Image assets (NOVA & Nutri-Score badges) from Open Food Facts website:
	- https://static.openfoodfacts.org/images/attributes/dist/nutriscore-a.svg
	- https://static.openfoodfacts.org/images/attributes/dist/nutriscore-b.svg
	- https://static.openfoodfacts.org/images/attributes/dist/nutriscore-c.svg
	- https://static.openfoodfacts.org/images/attributes/dist/nutriscore-d.svg
	- https://static.openfoodfacts.org/images/attributes/dist/nutriscore-e.svg
	- https://static.openfoodfacts.org/images/attributes/dist/nutriscore-unknown.svg
	- https://static.openfoodfacts.org/images/attributes/dist/nova-group-1.svg
	- https://static.openfoodfacts.org/images/attributes/dist/nova-group-2.svg
	- https://static.openfoodfacts.org/images/attributes/dist/nova-group-3.svg
	- https://static.openfoodfacts.org/images/attributes/dist/nova-group-4.svg
	- https://static.openfoodfacts.org/images/attributes/dist/nova-group-unknown.svg
- Quasar Framework Documentation as reference point for modifying NiceGUI styling
	- https://quasar.dev/components
- TailwindCSS Documentation as reference point for CSS classes used for modifying NiceGUI styling
	- https://tailwindcss.com/docs

**AI Disclosure:**
- Google's built-in "AI Overview" provided various small suggestions on styling and coding logic - however it is difficult to reference these as "AI Overview" is built-in to Google Search

---
### Houston
**Accomplishments / Responsibilities**
- Profile system design & logic:
	- Profile creation, selection, deletion
	- Duplicate name validation
	- Per-session storage using app.storage.tab
- Allergen matching logic
	- String matching algorithm
	- Profile allergen warning displays
- JSON file Handling
	- Load_json() and save_profiles() functions
	- Error handling for file read/write failures

**Resources Used:**
- https://nicegui.io/documentation 
	- app.storage.tab per-session storage documentation 
	- Dialog and card syntax reference 
	- Timer pattern for delayed execution 
	- Page routing documentation
- https://nicegui.io/documentation/page#wait_for_client_connection 
	- Referenced directly for app transition errors and timeout fixes
- https://docs.python.org/3/library/json.html 
	- Referenced for json.load and json.dump
- https://www.w3schools.com/python/python_json.asp 
	- Json formatting and parsing
- https://www.w3schools.com/PYTHON/python_dictionaries_nested.asp 
	- Referenced for dictionaries when creating the Allergen API calls


