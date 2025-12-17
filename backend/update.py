from threading import Lock

update_state = {
    "status": "idle",        # idle | running | finished | cancelled | error
    "total": 0,
    "current": 0,
    "message": "",
    "cancel_requested": False,
    "error": None,
}

update_lock = Lock()