# SnackSafe
> SnackSafe was developed by Tanzim Rashid and Houston Meyer as part of a programming class project.  
> SnackSafe is built using NiceGUI, and utilizes the Open Food Facts database to retrieve product information.

### Your Snacks, Decoded.
SnackSafe is a mobile-first, web-based barcode scanning app that is designed to identify potential allergens in packaged food products to keep users and their loved ones safe.
It relies on data collected from [Open Food Facts](https://openfoodfacts.org), a global database containing information on 4.5 million packaged food products.

Besides allergy monitoring and alerts, SnackSafe also offers insights on [NOVA Levels](https://world.openfoodfacts.org/nova) to highlight the degree of food processing, as well as the [Nutri-Score](https://world.openfoodfacts.org/nutriscore) to show the nutritional quality of food products in an easy-to-understand format.

Our goal was to develop a mobile-first, web-based solution that is easy to deploy and platform-agnostic. 

- Scan (or manually search) over [4.5 million](https://world.openfoodfacts.org/product-count) food products
- Set up profiles for allergy alerts
- Identify ultra-processed foods
- Decypher labels for nutritional quality

## Dependencies
SnackSafe requires the following Python libraries to run:
- [NiceGUI](https://github.com/zauberzeug/nicegui)
- [nicegui-scanner](https://github.com/serraict/nicegui-scanner-app)

NiceGUI converts Python into browser-compatible front-end code, enabling seamless integration of peripherals like cameras for barcode scanning.

Web browsers require secure context before they will expose the camera. To ensure proper functionality, serve SnackSafe over HTTPS (even on a local network) or use `localhost` during development.
