from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from src.database.models import Contact
from src.schemas import ContactCreate, ContactUpdate

async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()

async def get_contact(contact_id: int, db: Session) -> Optional[Contact]:
    return db.query(Contact).filter(Contact.id == contact_id).first()

async def create_contact(contact: ContactCreate, db: Session) -> Contact:
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

async def update_contact(contact_id: int, contact: ContactUpdate, db: Session) -> Optional[Contact]:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    return None

async def delete_contact(contact_id: int, db: Session) -> Optional[Contact]:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return db_contact
    return None

async def search_contacts(first_name: Optional[str], last_name: Optional[str], email: Optional[str], db: Session) -> List[Contact]:
    query = db.query(Contact)
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))
    return query.all()

async def get_contacts_with_upcoming_birthdays(today: datetime, next_week: datetime, db: Session):
    today_str = today.strftime('%m-%d')
    next_week_str = next_week.strftime('%m-%d')
    
    contacts = db.query(Contact).all()
    upcoming_birthdays = []
    
    for contact in contacts:
        birthday_str = contact.birthday.strftime('%m-%d')
        if today_str <= birthday_str <= next_week_str:
            upcoming_birthdays.append(contact)
    
    return upcoming_birthdays