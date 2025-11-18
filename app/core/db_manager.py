from app.core.database import engine


class DatabaseManager:
    async def connect(self):
        pass

    async def close(self):
        await engine.dispose()


db_manager = DatabaseManager()
