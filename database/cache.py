import time

cache_store = {}

def get_cache(key: str):
    item = cache_store.get(key)

    if not item:
        return None

    # ⏰ Check expiry
    if item["expiry"] < time.time():
        del cache_store[key]
        return None

    return item["data"]


def set_cache(key: str, value, ttl: int = 60):
    cache_store[key] = {
        "data": value,
        "expiry": time.time() + ttl
    }