from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Table, select, insert, update, delete
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy.orm import Session

from app.dependencies.mysql import get_mysql_db, metadata

router = APIRouter(
    prefix="/mysql",
    tags=["MySQL Generic CRUD"]
)


@router.get("/{table_name}")
def read_all_rows(table_name: str, db: Session = Depends(get_mysql_db)):
    """
    Retrieve all rows from the given table using SQLAlchemy 2.0 best practices.
    The 'mappings().all()' call returns a list of dictionaries, avoiding the ValueError
    from 'dict(row)' on complex row objects.
    """
    try:
        table = Table(table_name, metadata, autoload_with=db.bind)
    except NoSuchTableError:
        raise HTTPException(status_code=404, detail="Table not found")

    # Use `.mappings().all()` to get a list of dictionary-like rows
    results = db.execute(select(table)).mappings().all()
    return results


@router.post("/{table_name}")
def create_row(table_name: str, data: dict, db: Session = Depends(get_mysql_db)):
    try:
        table = Table(table_name, metadata, autoload_with=db.bind)
    except NoSuchTableError:
        raise HTTPException(status_code=404, detail="Table not found")

    stmt = insert(table).values(**data)
    result = db.execute(stmt)
    db.commit()

    return {"inserted_id": result.lastrowid, "data": data}


@router.put("/{table_name}/{row_id}")
def update_row(table_name: str, row_id: str, data: dict, db: Session = Depends(get_mysql_db)):
    try:
        table = Table(table_name, metadata, autoload_with=db.bind)
    except NoSuchTableError:
        raise HTTPException(status_code=404, detail="Table not found")

    # Assume the table uses a primary key column named "id".
    # Adjust if needed for your schema (or read PK dynamically).
    stmt = update(table).where(table.c.id == row_id).values(**data)
    result = db.execute(stmt)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Row not found")
    return {"updated_id": row_id, "new_data": data}


@router.delete("/{table_name}/{row_id}")
def delete_row(table_name: str, row_id: str, db: Session = Depends(get_mysql_db)):
    try:
        table = Table(table_name, metadata, autoload_with=db.bind)
    except NoSuchTableError:
        raise HTTPException(status_code=404, detail="Table not found")

    stmt = delete(table).where(table.c.id == row_id)
    result = db.execute(stmt)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Row not found")
    return {"deleted_id": row_id}
