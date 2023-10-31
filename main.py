#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import uuid
from typing import Any, Dict, List

from fastapi import Body, FastAPI, HTTPException, APIRouter
from pydantic import BaseModel

from bardapi import BardAsync

token = '<__Secure-1PSID>'
app = FastAPI()
router = APIRouter(prefix="/v1")


def generate_chat_completion_id():
    return str(uuid.uuid4())


def get_current_timestamp():
    return int(time.time())


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Dict[str, str]]


class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    # usage: Dict[str, int]
    choices: List[Dict[str, Any]]


@router.post("/completions", response_model=ChatCompletionResponse)
async def chat_completions(completion: ChatCompletionRequest):
    """Generates a response to a prompt or a conversation."""

    # Check if the model is supported
    if completion.model != "bard":
        raise HTTPException(
            status_code=400,
            detail=f"The model `{completion.model}` does not exist")

    # Call the Bard API
    bard = BardAsync(token=token)
    answer = await bard.get_answer(completion.messages[-1]["content"])

    # Call the OpenAI API here
    # Return the response

    return {
        "id":
        generate_chat_completion_id(),
        "object":
        "chat.completion",
        "created":
        get_current_timestamp(),
        "model":
        "bard",
        "choices": [{
            "message": {
                "role": "assistant",
                "content": f"{answer['content']}",
            },
            "finish_reason": "stop",
            "index": 0
        }]
    }

@router.post("/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions_alias():
    return chat_completions(completion=ChatCompletionRequest(model="bard"))

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
