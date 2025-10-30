import uvicorn
import asyncio
from app.fastapi_app import app

async def start_fastapi():
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