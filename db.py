from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import OperationalError



def check_database_exists(database_url: str) -> bool:
    try:
        url = make_url(database_url)
        db_name = url.database

        # Connect to default 'postgres' database to check
        admin_url = url.set(database='postgres')
        engine = create_engine(admin_url)

        with engine.connect() as conn:
            result = conn.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
            return result.scalar() is not None

    except OperationalError as e:
        raise RuntimeError(f"❌ Could not connect to PostgreSQL server: {e}")
