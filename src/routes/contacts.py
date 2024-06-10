from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.database.db import get_db
from src.schemas import ContactCreate, ContactUpdate, ContactResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])

@router.post("/", response_model=ContactResponse)
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(contact, db)

@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return await repository_contacts.get_contacts(skip, limit, db)

@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(
    first_name: Optional[str] = Query(None, alias="first_name"),
    last_name: Optional[str] = Query(None, alias="last_name"),
    email: Optional[str] = Query(None, alias="email"),
    db: Session = Depends(get_db)
):
    return await repository_contacts.search_contacts(first_name, last_name, email, db)

@router.get("/upcoming_birthdays", response_model=List[ContactResponse])
async def upcoming_birthdays(db: Session = Depends(get_db)):
    today = datetime.today()
    next_week = today + timedelta(days=7)
    contacts = await repository_contacts.get_contacts_with_upcoming_birthdays(today, next_week, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    return await repository_contacts.update_contact(contact_id, contact, db)

@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.delete_contact(contact_id, db)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact



