import sys
from sqlalchemy import create_engine, text
from app.database import Base, engine
from app.models import Category, Expense
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database():
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Tables created successfully")

        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM categories"))
            count = result.scalar()

            if count == 0:
                logger.info("Inserting default categories...")
                categories = [
                    "Food & Dining",
                    "Transportation",
                    "Shopping",
                    "Entertainment",
                    "Bills & Utilities",
                    "Healthcare",
                    "Travel",
                    "Education",
                    "Personal Care",
                    "Other"
                ]

                for category in categories:
                    conn.execute(
                        text("INSERT INTO categories (name) VALUES (:name)"),
                        {"name": category}
                    )
                conn.commit()
                logger.info(f"✓ Inserted {len(categories)} default categories")
            else:
                logger.info(f"✓ Categories already exist ({count} found)")

        logger.info("Database initialization completed successfully!")
        return True

    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        return False


if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)