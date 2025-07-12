from sqlalchemy.orm import Session
from . import models, schema

def get_todo(db: Session, todo_id: int, user_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.user_id == user_id).first()

def get_todos(db: Session, user_id:int, skip: int = 0, limit: int = 10):
    return db.query(models.Todo).filter(models.Todo.user_id == user_id).offset(skip).limit(limit).all()

def create_todo(db: Session, todo: schema.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo: schema.TodoUpdate, user_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.user_id == user_id).first()
    if db_todo:
        for key, value in todo.dict(exclude_unset=True).items():
            setattr(db_todo, key, value,)
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int, user_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.user_id == user_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo
