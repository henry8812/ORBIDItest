import requests
import os
from datetime import datetime
from app.models import APICall
from app.database import SessionLocal
from app.hubspot import get_hubspot_contact

CLICKUP_API_BASE_URL = os.getenv("CLICKUP_API_URL")
CLICKUP_API_TOKEN = os.getenv("CLICKUP_TOKEN")
CLICKUP_LIST_ID = os.getenv("CLICKUP_LIST_ID")

HUBSPOT_API_BASE_URL = os.getenv("HUBSPOT_API_URL")
HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")


def sync_contacts_to_clickup(contact_ids):
    for contact_id in contact_ids:
        contact_data = get_hubspot_contact(contact_id)
        if contact_data['properties'].get('firstname') is not None and contact_data['properties'].get('lastname') is not None:
            clickup_task_data = transform_contact_data_to_clickup_task(contact_data)
            if contact_data['properties'].get('estado_clickup') is not None:
                create_clickup_task(clickup_task_data)

            print(clickup_task_data)
            # Save the API call to the database
            endpoint = "/contacts/sync"
            params = {"contact_id": contact_id}
            result = clickup_task_data["task_id"]
            #save_api_call_to_database(endpoint, params, result)


def transform_contact_data_to_clickup_task(contact_data):
    print(contact_data)

    transformed_data = {
        "name": contact_data['properties']["firstname"] + " " + contact_data['properties']["lastname"],
        "createdAt": contact_data["createdAt"],
        "email": contact_data['properties']["email"],
        "task_id" : contact_data["id"] 
        # Add here any necessary transformations for other ClickUp fields
    }
    
    return transformed_data


def create_clickup_task(task_data):
    headers = {
        "Authorization": f"Bearer {CLICKUP_API_TOKEN}",
        "Content-Type": "application/json"
    }

    url = f"{CLICKUP_API_BASE_URL}/list/{CLICKUP_LIST_ID}/task"

    response = requests.post(url, headers=headers, json=task_data)
    
    try:
        response.raise_for_status()
        result = response.json()

        # Agregar la propiedad estado_clickup a true en HubSpot para el usuario correspondiente
        if 'task_id' in task_data:
            contact_id = task_data['task_id']
            hubspot_url = f"{HUBSPOT_API_BASE_URL}/crm/v3/objects/contacts/{contact_id}"
            hubspot_headers = {
                "Authorization": f"Bearer {HUBSPOT_ACCESS_TOKEN}",
                "Content-Type": "application/json"
            }
            hubspot_payload = {
                "properties": {
                    "estado_clickup": True
                }
            }
            hubspot_response = requests.patch(hubspot_url, headers=hubspot_headers, json=hubspot_payload)
            hubspot_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

    return result


def save_api_call_to_database(endpoint, params, result):
    # Create an instance of APICall object
    api_call = APICall(
        endpoint=endpoint,
        params=params,
        result=result,
        created_at=datetime.now()
    )

    # Save the API call to the database
    db = SessionLocal()
    db.add(api_call)
    db.commit()
    db.refresh(api_call)
    db.close()
