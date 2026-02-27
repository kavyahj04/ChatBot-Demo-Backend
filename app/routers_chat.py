from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from .response_picker import get_bot_response_a, get_bot_response_b
from .db import get_db
from . import schemas

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=schemas.ChatResponse)
async def chat(
    payload: schemas.ChatRequest,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    print("Received:", payload)
    print("Looking for chat_session_id:", payload.chat_session_id)

    participant = await db.participants_demo.find_one(
        {"sessions.chat_session_id": payload.chat_session_id}
    )

    if not participant:
        print("Session not found:", payload.chat_session_id)
        raise HTTPException(status_code=404, detail=f"Chat session not found")

    condition = participant.get("condition", "A")
    if condition == "B":
        bot_response = get_bot_response_b(payload.user_message)
    else:
        bot_response = get_bot_response_a(payload.user_message)

    print(f"Condition: {condition}, Response: {bot_response}")

    session_index = None
    for i, session in enumerate(participant.get("sessions", [])):
        if session.get("chat_session_id") == payload.chat_session_id:
            session_index = i
            break

    if session_index is None:
        raise HTTPException(status_code=404, detail="Session index not found")

    result = await db.participants_demo.update_one(
        {"pid": participant["pid"]},
        {
            "$push": {
                f"sessions.{session_index}.messages": {
                    "$each": [
                        {
                            "sender": "user",
                            "text": payload.user_message,
                            "timestamp": datetime.utcnow().isoformat()
                        },
                        {
                            "sender": "bot",
                            "text": bot_response,
                            "timestamp": datetime.utcnow().isoformat()
                        }
                    ]
                }
            }
        }
    )

    print(f"Update result: matched={result.matched_count}, modified={result.modified_count}")

    return schemas.ChatResponse(
        assistant_message=bot_response,
        condition_id=condition,
        model="demo",
        usage={}
    )