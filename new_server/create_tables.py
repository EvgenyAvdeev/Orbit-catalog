from tables import Base
from database import db_echo
from sqlalchemy import text

def main():
    engine = db_echo.get_engine()
    with engine.begin() as conn:
        Base.metadata.reflect(engine)
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(text(f'DROP TABLE IF EXISTS "{table.name}" CASCADE'))
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    main()
