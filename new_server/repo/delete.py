from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import delete
from tables import Base

from .base import BaseRepo


class DeleteRepo[TableType: Base, ReadModel: BaseModel](BaseRepo[TableType, ReadModel]):

    def delete_record(self, id: int, session: Session) -> TableType:
        record = session.get(self.table_class, id)
        session.delete(record)
        session.commit()
        return record

    def delete(self, id: int, session: Session) -> ReadModel:
        record = self.delete_record(id, session)
        return self.to_read_model(record)

    def delete_by_condition(self, session: Session, **filters) -> int:
        """Удаление по условиям с поддержкой списков значений"""
        if not filters:
            raise ValueError("Не указаны условия для удаления")

        stmt = delete(self.table_class)
        for field, value in filters.items():
            if isinstance(value, list):
                # Если передан список - используем IN
                stmt = stmt.where(getattr(self.table_class, field).in_(value))
            else:
                # Если одиночное значение - используем равенство
                stmt = stmt.where(getattr(self.table_class, field) == value)

        result = session.execute(stmt)
        return result.rowcount

    def count_by_condition(self, session: Session, **filters) -> int:
        """Подсчет количества записей по условиям с поддержкой списков"""
        query = session.query(self.table_class)
        for field, value in filters.items():
            if isinstance(value, list):
                query = query.filter(getattr(self.table_class, field).in_(value))
            else:
                query = query.filter(getattr(self.table_class, field) == value)
        return query.count()