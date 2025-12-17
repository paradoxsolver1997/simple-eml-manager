# backend/api.py
from fastapi import APIRouter
from backend.indexer import rebuild_index
from backend.search import search_emails
from threading import Thread
from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Query
from backend.parser import parse_eml
from pathlib import Path

from backend.update import update_lock
from backend.update import update_state

router = APIRouter(prefix="/api")

@router.post("/update")
def update_library():
    try:
        count = rebuild_index()
        return {
            "status": "ok",
            "indexed": count,
        }
    except Exception as e:
        with update_lock:
            update_state["status"] = "error"
            update_state["error"] = str(e)
        raise

@router.get("/search")
def search(q: str, field: str = "all"):
    return {
        "results": search_emails(q, field)
    }

@router.post("/update_library")
def start_update():
    with update_lock:
        if update_state["status"] == "running":
            update_state["cancel_requested"] = False
            return {"ok": False, "message": "Update already running"}

    t = Thread(target=update_library, daemon=True)
    t.start()

    return {"ok": True}

@router.get("/update_status")
def get_update_status():
    with update_lock:
        return {
            "status": update_state["status"],
            "total": update_state["total"],
            "current": update_state["current"],
            "message": update_state["message"],
            "error": update_state["error"],
        }

@router.post("/update_cancel")
def cancel_update():
    with update_lock:
        if update_state["status"] == "running":
            update_state["cancel_requested"] = True
            return {"ok": True}
    return {"ok": False}

@router.get("/email")
def get_email(
    path: str = Query(..., description="Absolute path to the .eml file")
):
    """
    Return full email content from original .eml file
    """
    print("PATH repr:", repr(path))
    print("PATH len:", len(path))
    for i, ch in enumerate(path):
        if ch == "…":
            print("FOUND ELLIPSIS AT INDEX", i)
    eml_path = Path(path)

    if not eml_path.exists():
        raise HTTPException(status_code=404, detail="EML file not found")

    if not eml_path.is_file():
        raise HTTPException(status_code=400, detail="Invalid EML path")

    try:
        mail = parse_eml(eml_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "path": mail["path"],
        "subject": mail["subject"],
        "sender": mail["sender"],
        "recipients": mail["recipients"],
        "body": mail["body"],
    }
