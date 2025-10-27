import uvicorn
import asyncio
from app.app import app
from app.database.database import create_tables


async def start_fastapi():
    await create_tables()
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        loop="asyncio",
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    try:
        await start_fastapi()
    except KeyboardInterrupt:
        print("Приложение остановлено по запросу пользователя")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        print("Завершение работы приложения")

if __name__ == "__main__":
    asyncio.run(main())