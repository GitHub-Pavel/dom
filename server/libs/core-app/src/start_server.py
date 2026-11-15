from os import getenv


def start_server():
    import uvicorn

    port = int(getenv("PORT", "3999"))
    service = getenv("SERVICE", "client")

    uvicorn.run(
        f"{service}.main:app", host="0.0.0.0", port=port, reload=True, log_config=None
    )
