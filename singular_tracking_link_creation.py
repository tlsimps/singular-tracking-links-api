#Author: Travis Simpson
#last update 2023/01/26
#Tracking link creatiion with helper API examples - first iteration

import requests
import json

#constants
api_key = '<your-api-key>'
apps_list = ['TLS Sample Apps', 'TLS React Native']
app_subdomain = {
    'TLS Sample Apps' : 'seteam',
    'TLS React Native' : 'jospm'
}
app_platform = ['android', 'ios']
tracker_name = '_test_tracking_link_name'

#get app site ids
apps_url = "https://api.singular.net/api/v1/singular_links/apps"
apps_response = requests.get(url=apps_url, headers={'Authorization': api_key})
app_data = apps_response.json()
app_site_ids = []
app_ids = []

for app in app_data['available_apps']:
    if app['app'] in apps_list:
        app_site_ids.append(app['app_site_id'])
        app_ids.append(app['app_id'])
    if app['app'] in app_subdomain:
        app_subdomain[int(app['app_id'])] = app_subdomain.pop(app['app'])

app_site_ids_string = ",".join(str(x) for x in app_site_ids)
app_ids_string = ",".join(str(x) for x in app_ids)
print(app_ids_string)
print(app_site_ids_string)
print(app_subdomain)

#get all configured partners -- 
partners_url = "https://api.singular.net/api/v1/singular_links/configured_partners"
params = {
    # The app sites for which you want to see which partners are configured
    "app_site_id": app_site_ids_string
}

partners_response = requests.get(partners_url, params=params, headers={'Authorization': api_key})
partners_data = partners_response.json()
print(partners_data)

#get partner config detials
partner_config_url = "https://api.singular.net/api/v1/singular_links/all_partners"
params = {
    #Optional: filter to see specific partner(s)
    "partner_id": ''
}
partner_config_response = requests.get(partners_url, params=params, headers={'Authorization': api_key})
partner_config_data = partner_config_response.json()
print(partner_config_data)

#get link domains
links_url = "https://api.singular.net/api/v1/singular_links/domains"
links_response = requests.get(url=links_url, headers={'Authorization': api_key})
links_data = links_response.json()
print(links_data)


#create tracking link
create_link_url = 'https://api.singular.net/api/v1/singular_links/links'
for app_id, app_site_id in zip(app_ids, app_site_ids):
    app_site_id = int(app_site_id)
    for partner in partners_data['available_partners']:
        if partner['app_site_id'] == app_site_id:
            for app in app_data['available_apps']:
                if app['app_site_id'] == app_site_id:
                    store_url = app['store_url']
            params = {
                "app_id": app_id,
                "partner_id": partner['singular_partner_id'],
                "link_type": "partner",
                "tracking_link_name": partner['singular_partner_display_name'].replace(" ","") + tracker_name,
                "link_subdomain": app_subdomain[app_id],
                "link_dns_zone": "sng.link",
                "destination_fallback_url": "https://www.example.com/",
                "ios_redirection": {
                  "app_site_id": app_site_id,
                  "destination_url": store_url, 
                  "destination_deeplink_url": "https://www.example.com/",
                  "destination_deferred_deeplink_url": "https://www.example.com/"
                }
            }
            params = json.dumps(params)
            print(params)
            create_link_response = requests.post(create_link_url, data=params, headers={'Authorization': api_key})
            print(create_link_response.json())

