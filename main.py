from fastapi import FastAPI, BackgroundTasks
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.database import SessionLocal, engine, Base  
from app.models import APICall
from sqlalchemy.orm import Session
import requests
import os
from app.clickup import sync_contacts_to_clickup
from app.hubspot import create_hubspot_contact
import json
from typing import Optional
from app.hubspot import get_hubspot_contacts

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Data models
class ContactCreate(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    phone: Optional[str] = None
    website: Optional[str] = None

# Routes
@app.post("/contacts")
async def create_contact(contact: ContactCreate, background_tasks: BackgroundTasks):
    # Validate required parameters
    if not contact.phone and not contact.website:
        return {"error": "At least one of 'phone' or 'website' must be provided."}

    contact_data = contact.dict()

    print("before sending")
    # Create contact in HubSpot
    hubspot_result = create_hubspot_contact(contact)
    print("after sending")
    # Save the API call to the database
    endpoint = "/contacts"
    params = json.dumps(contact_data)
    result = json.dumps(hubspot_result)

    background_tasks.add_task(save_api_call_to_database, endpoint, params, result)

    return {"message": "Contact created"}

@app.post("/contacts/sync")
async def sync_contacts(background_tasks: BackgroundTasks):
    # Logic to synchronize contacts
    contacts = get_hubspot_contacts()

    contact_ids = [contact["id"] for contact in contacts['results']]  # Extract contact IDs

    sync_contacts_to_clickup(contact_ids)  # Call the function to sync contacts with ClickUp

    # Save the API call to the database
    endpoint = "/contacts/sync"
    params = None
    result = json.dumps({"success": True})  # If synchronization is successful, store the result as success

    background_tasks.add_task(save_api_call_to_database, endpoint, params, result)

    return {"message": "Contact synchronization initiated"}

# Function to save the API call to the database
def save_api_call_to_database(endpoint: str, params: str, result: str):
    # Create an instance of APICall object
    api_call = APICall(endpoint=endpoint, params=params, result=result)

    # Save the API call to the database
    db = SessionLocal()
    db.add(api_call)
    db.commit()
    db.refresh(api_call)
    db.close()
