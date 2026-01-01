from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    department: str  # 'web', 'ai', 'content', 'sales'
    role: str        # 'manager', 'junior', 'senior'
    is_active: bool = True

class Client(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Issue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str
    status: str = "open"  # 'open', 'in_progress', 'resolved'
    priority: str         # 'low', 'medium', 'high'
    department: str
    
    # Relationships (Foreign Keys)
    client_id: Optional[int] = Field(default=None, foreign_key="client.id")
    assigned_to: Optional[int] = Field(default=None, foreign_key="employee.id")
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    ai_summary: Optional[str] = None
