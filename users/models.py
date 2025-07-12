import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from core.database import Base

class Role(enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(Enum(Role), default=Role.user, nullable=False)

    todos = relationship("Todo", back_populates="user", cascade="all, delete")

