import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_latest_app_version(package_name, credentials):
    service = build('androidpublisher', 'v3', credentials=credentials)
    app_info = service.edits().insert(body={}, packageName=package_name).execute()
    app_edit_id = app_info['id']

    listings = service.edits().listings().list(
        packageName=package_name,
        editId=app_edit_id).execute()
    
    print("Listings:", listings)

    latest_app_version = listings['listings'][0]['version']
    return latest_app_version

def update_version_json(version):
    with open("version.json", "r") as f:
        version_data = json.load(f)

    version_data["latest_app_version"] = version

    with open("version.json", "w") as f:
        json.dump(version_data, f, indent=2)

if __name__ == "__main__":
    package_name = os.environ["PACKAGE_NAME"]
    service_account_json = os.environ["SERVICE_ACCOUNT_JSON"]

    credentials = service_account.Credentials.from_service_account_info(
        json.loads(service_account_json),
        scopes=["https://www.googleapis.com/auth/androidpublisher"]
    )

    latest_app_version = get_latest_app_version(package_name, credentials)
    update_version_json(latest_app_version)
