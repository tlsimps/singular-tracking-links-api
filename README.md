# singular-tracking-links-api
Call the singular create links and helper apis to generate singular tracking links

**NOT FOR USE IN PROD** - shows example calls only. Intentionally making a call for an Android app site with ios_redirection only to show validation error example. See the custom source link generation example for dynamic handling of ios / android redirections - https://github.com/tlsimps/singular_custom_source_link_google_sheet 

1. Change the api_key to your singular reporting api key
2. Edit with your own Apps list
3. Update the app_subomain mapping - find your subdomain in the Manage Links page
4. change the tracker_name
5. Will create ios links for all partners configured for ios app sites in your specified apps list
6. Intentionally not calling the android redirection to show a validation error example response from the singular links api
