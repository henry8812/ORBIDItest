import requests
import os
from datetime import datetime
from app.models import APICall
from app.database import SessionLocal
import json

HUBSPOT_API_BASE_URL = os.getenv("HUBSPOT_API_URL")
HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")

CLICKUP_API_BASE_URL = os.getenv("CLICKUP_API_URL")
CLICKUP_API_TOKEN = os.getenv("CLICKUP_TOKEN")
CLICKUP_LIST_ID = os.getenv("CLICKUP_LIST_ID")


def create_hubspot_contact(contact):
    headers = {
        "Authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    url = f"{HUBSPOT_API_BASE_URL}/crm/v3/objects/contacts"

    contact_data = {
        "email": contact.email,
        "firstname": contact.firstname,
        "lastname": contact.lastname,
        "phone": contact.phone,
        "website": contact.website
    }

    print("Contact data:", contact_data)  # Add this line to print the contact data before the request

    response = requests.post(url, headers=headers, json=contact_data)
    contact_data = response.json()

    print("Contact data response:", contact_data)  # Add this line to print the request response

    return contact_data


def get_hubspot_contact(contact_id):
    headers = {
        "Authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}"
    }

    url = f"{HUBSPOT_API_BASE_URL}/crm/v3/objects/contacts/{contact_id}"

    response = requests.get(url, headers=headers)
    contact_data = response.json()

    return contact_data


def get_hubspot_contacts():
    headers = {
        "Authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}"
    }

    url = f"{HUBSPOT_API_BASE_URL}/crm/v3/objects/contacts"

    response = requests.get(url, headers=headers)
    contacts_data = response.json()

    return contacts_data


def save_api_call_to_database(endpoint, params, result):
    # Convert the params dictionary to JSON
    params_json = json.dumps(params)

    # Create an instance of APICall object
    api_call = APICall(
        endpoint=endpoint,
        params=params_json,  # Save the JSON string instead of the dictionary
        result=result,
        created_at=datetime.now()
    )

    # Save the API call to the database
    db = SessionLocal()
    db.add(api_call)
    db.commit()
    db.refresh(api_call)
    db.close()
