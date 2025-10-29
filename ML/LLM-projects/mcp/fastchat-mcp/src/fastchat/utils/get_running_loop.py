import asyncio


def get_running_loop():
    try:
        loop = asyncio.get_running_loop()
        return loop
    except RuntimeError:
        return None
