from datetime import datetime
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from .db import get_db
from . import schemas

router = APIRouter(prefix="/session", tags=["session"])


@router.post("/start", response_model=schemas.SessionStartResponse)
async def start_session(
    payload: schemas.SessionStartRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    print("Received-Session-Info", payload)

    chat_session_id = f"session_{payload.pid}_{datetime.utcnow().timestamp()}"
    new_session = {
        "chat_session_id": chat_session_id,
        "status": "active",
        "created_at": datetime.utcnow().isoformat(),
        "messages": []
    }

    existing = await db.participants_demo.find_one({"pid": payload.pid})

    if existing:
        condition = existing.get("condition", "A")
        print(f"Existing participant - reusing condition: {condition}")

        await db.participants_demo.update_one(
            {"pid": payload.pid},
            {"$push": {"sessions": new_session}}
        )

    else:
        pid_sum = sum(ord(c) for c in payload.pid)
        condition = "A" if pid_sum % 2 == 0 else "B"
        print(f"New participant - assigned condition: {condition}")

        await db.participants_demo.insert_one({
            "pid": payload.pid,
            "session_id": payload.prolific_session_id,
            "study_id": payload.study_id,
            "qr_pre": payload.qr_pre,
            "condition": condition,
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "sessions": [new_session]
        })

    return schemas.SessionStartResponse(
        chat_session_id=chat_session_id,
        condition_id=condition,
        condition_name=f"Condition {condition}"
    )