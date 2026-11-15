from datetime import datetime, timezone

from core_app import bootstrap, start_server

app = bootstrap()


@app.get("/")
async def read_root():
    return {
        "message": "Hello, World!",
        "dateiso": datetime.now(timezone.utc).isoformat(),
        "status": "UPDATED",
    }


if __name__ == "__main__":
    start_server()
