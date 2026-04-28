from assets.constants import *

### Mount local assets directory to site ###
app.add_static_files('/assets', 'assets')

##################################################################
# Define root URL ("/") & run index function (i.e., UI elements) #
##################################################################
@ui.page("/")
def index():
    profile_label = ui.label("No profile selected")
    # shows currently selected profile

    async def update_profile_label():
        # wait for client connection before reading tab storage
        current_name = app.storage.tab.get("profile_name", None)
        if current_name:
            profile_label.set_text(f'Current profile: {current_name}')

    ui.timer(0.1, update_profile_label, once=True)
    # small delay ensures client connection is ready before accessing storage

    ##### Profile Selection / Creation Dialog #####
    with ui.dialog() as profile_dialog, ui.card():

        def choose_profile(profile):
            # store selected profile in per-tab storage
            app.storage.tab["profile_name"] = profile.get("name")
            app.storage.tab["profile_allergens"] = [
                allergen.strip().title()
                for allergen in profile.get("allergens", [])
            ]
            profile_label.set_text(f'Current profile: {app.storage.tab["profile_name"]}')
            ui.notify(f'Profile selected: {app.storage.tab["profile_name"]}', type="positive")
            profile_dialog.close()

        def create_profile():
            new_name = name_input.value.strip()
            new_allergens = allergy_select.value or []

            if not new_name:
                ui.notify("Please enter a profile name", type="warning")
                return

            # check for duplicate names
            for profile in profiles:
                if profile.get("name", "").lower() == new_name.lower():
                    ui.notify("A profile with that name already exists", type="warning")
                    return

            new_profile = {
                "name": new_name,
                "allergens": new_allergens,
                "history": []
            }

            profiles.append(new_profile)
            save_profiles()

            name_input.value = ""
            allergy_select.value = []

            # update dropdown with new profile, Little bit laggy but it works
            profile_select.options = [p.get("name", "Unnamed Profile") for p in profiles]
            profile_select.update()

            ui.notify(f"Created profile: {new_name}", type="positive")

        def delete_profile():
            selected_name = profile_select.value
            if not selected_name:
                ui.notify("Please select a profile to delete", type="warning")
                return
            for profile in profiles:
                if profile.get("name") == selected_name:
                    profiles.remove(profile)
                    save_profiles()

                    # clear active profile from storage if it was deleted, this took me forever to figure out
                    if app.storage.tab.get("profile_name") == selected_name:
                        app.storage.tab["profile_name"] = None
                        app.storage.tab["profile_allergens"] = []
                        profile_label.set_text("No profile selected")

                    profile_select.options = [p.get("name", "Unnamed Profile") for p in profiles]
                    profile_select.set_value(None)
                    profile_select.update()
                    # Refreshes profiles after deletion\

                    ui.notify(f"Deleted profile: {selected_name}", type="positive")
                    return

        ui.markdown("## Select Profile")

        profile_names = [p.get("name", "Unnamed Profile") for p in profiles]

        profile_select = ui.select(
            options=profile_names,
            label="Select a profile",
            with_input=True
        ).classes('w-full')

        def confirm_profile():
            selected_name = profile_select.value
            if not selected_name:
                ui.notify("Please select a profile first", type="warning")
                return
            for profile in profiles:
                if profile.get("name") == selected_name:
                    choose_profile(profile)
                    return
            ui.notify("Profile not found", type="negative")

        with ui.row().classes('w-full items-center gap-2'):
            ui.button("Select Profile", icon="check", color="blue", on_click=confirm_profile)
            ui.button(icon="delete", color="red", on_click=lambda: confirm_delete_dialog.open()).props('flat round').tooltip("Delete selected profile")
        # confirm and delete buttons

        # Delete confirmation dialog
        with ui.dialog() as confirm_delete_dialog, ui.card():
            ui.markdown("### Are you sure?")
            ui.label("This will permanently delete the selected profile.")
            with ui.row():
                ui.button("Cancel", icon="close", on_click=confirm_delete_dialog.close)
                ui.button("Delete", icon="delete", color="red", on_click=lambda: (confirm_delete_dialog.close(), delete_profile()))

        ui.separator()

        ui.markdown("### Create New Profile")

        name_input = ui.input(
            label="Profile Name",
            placeholder="e.g., Houston Meyer"
        )

        allergy_select = ui.select(
            options=ALLERGEN_OPTIONS,
            label="Select Allergens",
            multiple=True,
            with_input=True
        )

        ui.button("Create Profile", icon="person_add", on_click=create_profile)

    ##### Scanner Dialog Popup #####
    with ui.dialog() as scanner_dialog, ui.card():
        # Scan event function
        async def on_scan(event):
            # require profile before processing scan
            if not app.storage.tab.get("profile_name"):
                ui.notify("Please select a profile first", type="warning")
                scanner_dialog.close()
                profile_dialog.open()
                return

            barcode = event.args
            print(f"Scanned Barcode: {barcode}")
            ui.notify(f"Looking up barcode: {barcode}", type="info")
            # Stop scanning & exit dialog after successful scan (prevent multiple scans)
            if scanner:
                scanner.stop_scanning()
            scanner_dialog.close()
            # Navigate to new page with barcode as part of URL
            ui.navigate.to(f"/product/{barcode}")

        ### UI Elements ###
        ui.markdown("Place barcode in the center and keep your hands steady")
        scanner = BarcodeScanner(on_scan=on_scan)
        with ui.button_group():
            ui.button("Stop", icon="stop", color="red", on_click=lambda: (scanner.stop_scanning(), scanner_dialog.close()))
            ui.button("Settings", icon="settings", color="blue", on_click=lambda: (scanner.run_method("toggleSettings")))

    ##### Scanner Manual Input Dialog Popup #####
    with ui.dialog() as input_dialog, ui.card():
        # Text input function
        async def process_manual_input():
            # require profile selection first
            if not app.storage.tab.get("profile_name"):
                ui.notify("Please select a profile first", type="warning")
                profile_dialog.open()
                return

            barcode = manual_input.value
            # Preventing empty/blank queries
            if not barcode:
                ui.notify("Please enter a barcode", type="warning")
                return
            # Notification confirming barcode scan
            input_dialog.close()
            print(f"Typed Barcode: {barcode}")
            ui.notify(f"Looking up barcode: {barcode}", type="info")
            # Navigate to new page with barcode as part of URL
            ui.navigate.to(f"/product/{barcode}")
            # Clear input box to ensure user sees blank input when card dialog opens
            manual_input.value = ""

        ### UI Elements ###
        ui.markdown("## Enter Barcode")
        # Assign variable for manual input & introduce basic validation logic (length + numeric)
        manual_input = ui.input(label="Enter Barcode", placeholder="e.g., 0123456789",
                                 validation=lambda value:'Too short' if len(value) < 12 else None).props("type=number autofocus")
        # Trigger function on enter key
        manual_input.on('keydown.enter', process_manual_input)
        # Search button for submitting manual input
        ui.button("Search", color="green", icon="search", on_click=process_manual_input)

    # Open Scanner function (async)
    async def open_scanner():
        # require profile before scanning
        if not app.storage.tab.get("profile_name"):
            ui.notify("Please select a profile first", type="warning")
            profile_dialog.open()
            return

        scanner_dialog.open()
        # Introduced 0.3 second delay to wait for camera to load; results in blank box otherwise
        await asyncio.sleep(0.3)
        scanner.start_scanning()

    #######################
    # Main User Interface #
    #######################
    with ui.card().classes('w-full max-w-md mx-auto'):
        with ui.column().classes('justify-center items-center'):
            ui.markdown("### SnackSafe 🍽️")
            ui.separator()
            ui.markdown('''
                ##### Your Snacks, Decoded.
                SnackSafe identifies ingredients from barcodes and compares them with your allergies to help keep you and your loved ones safe.
            ''')
            ui.markdown("SnackSafe also highlights [**NOVA Levels**](https://world.openfoodfacts.org/nova) and [**Nutri-Scores**](https://world.openfoodfacts.org/nutriscore) to help you make better health-informed decisons on the food you buy.")
            ui.markdown('''
                - Scan over [4.5 million](https://world.openfoodfacts.org/product-count) food products
                - Set up profiles for allergy alerts
                - Identify ultra-processed foods
                - Decypher labels for nutritional quality
            ''')
            ui.space()
            profile_label
            ui.button("Change Profile", icon="person", on_click=profile_dialog.open)
            ui.space()
            with ui.button_group():
                ui.button("Start Scanning", color="blue", icon="barcode_reader", on_click=open_scanner)
                ui.button("Enter Barcode", color="green", icon="text_fields", on_click=input_dialog.open)
            ### Footer ###
            ui.separator()
            with ui.row().classes('justify-center items-center'):
                ui.markdown(f"Copyright © {COPYRIGHT_DATE}")
                ui.space()
                ui.markdown("Licensed under [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)")

    async def auto_open_profile():
        if not app.storage.tab.get("profile_name"):
            profile_dialog.open()

    ui.timer(0.1, auto_open_profile, once=True)
    # only open profile dialog automatically if no profile is selected


########################
# Product Details Page #
########################
@ui.page("/product/{barcode}")
async def product_page(barcode: str):
    await ui.context.client.connected(timeout=5)
    profile_name = app.storage.tab.get("profile_name")
    profile_allergens = app.storage.tab.get("profile_allergens", [])

    ### Page Header ###
    with ui.row().classes('w-full items-center mb-4'):
        ui.button(icon="arrow_back", on_click=lambda: ui.navigate.to('/')).props('flat')
        ui.label("Product Details").classes('text-xl font-bold')

    ### Grab product data from API & display errors (if any) ###
    product_data = await get_barcode_info(barcode)
    # Unknown product
    if product_data is None:
        ui.label("Unknown Product").classes('text-lg text-red-600 font-bold')
        ui.markdown(f"Barcode **{barcode}** was not found in the Open Food Facts database. Try scanning another item.")
        ui.button("Go Back", icon="arrow_back", color="blue", on_click=lambda: ui.navigate.to('/'))
        return
    # Connection error
    elif product_data == "Connection Error":
        ui.label("Network Error").classes('text-lg text-blue-600 font-bold')
        ui.markdown("Could not connect to Open Food Facts database. Try refreshing this page in a few minutes.")
        ui.button("Refresh Page", icon="refresh", color="blue", on_click=lambda: ui.navigate.reload())
        return

    # Match product allergens against selected profile allergens
    matched_allergens = []
    if profile_allergens:
        matched_allergens = [
            allergy
            for allergy in product_data.get("allergies", [])
            if any(
                profile_allergen.lower() in allergy.lower() or allergy.lower() in profile_allergen.lower()
                for profile_allergen in profile_allergens
            )
        ]
    # Profile history
    if profile_name:
        # save barcode to profile history
        for profile in profiles:
            if profile.get("name") == profile_name:
                profile.setdefault("history", []).append(barcode)
                save_profiles()
                break

    ### Main Product Dashboard ###
    with ui.card().classes('w-full max-w-md mx-auto'):
        # Product image & name
        if product_data['image']:
            ui.image(product_data['image']).classes('w-full h-48 object-contain mb-4')
        ui.markdown(f"#### {product_data['name']}")

        ui.separator()

        # Active profile label
        ui.label(f'Profile: {profile_name or "None"}').classes('text-sm text-gray-500')

        ui.separator()

        # Allergen match warning
        if matched_allergens:
            ui.label("⚠ Warning: This product contains allergens in your profile").classes(
                'text-red-600 text-lg font-bold'
            )
            with ui.row().classes('gap-2'):
                for item in matched_allergens:
                    ui.badge(item, color="red")
        else:
            ui.label("✅ No matched profile allergens found").classes(
                'text-green-600 text-lg font-bold'
            )

        ui.separator()

        # All allergens from API
        ui.markdown("##### **Allergens**")
        if product_data['allergies']:
            with ui.row():
                for allergy in product_data['allergies']:
                    ui.badge(allergy, color="red").classes('text-sm')
        else:
            ui.label("No allergens found").classes('text-green-600 text-base')

        ui.separator()

        # Nutri-Score layout
        api_nutriscore = product_data["nutriscore"]
        nutriscore_badge = nutriscore_dict.get(api_nutriscore, nutriscore_dict["N/A"])
        with ui.column().classes('items-center text-center'):
            ui.image(nutriscore_badge["img"]).classes("w-32 h-16").props("fit=contain")
            ui.markdown(f"##### {nutriscore_badge['desc']}")

        ui.separator()

        # NOVA Group layout
        api_nova = str(product_data["nova"])
        nova_badge = nova_dict.get(api_nova, nova_dict["N/A"])
        with ui.column().classes('items-center text-center'):
            ui.image(nova_badge["img"]).classes("w-12 h-16").props("fit=contain")
            ui.markdown(f"##### {nova_badge['desc']}")


###############
# Run command #
###############
# Runs locally (during demo, port 8080 is being tunneled via CloudFlare tunnel to https://demo.tanzim.ca)
# Set the show argument as 'True' (or remove it) to get the app to open a browser tab to localhost:8080
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="SnackSafe", favicon="🍽️", show=False)
