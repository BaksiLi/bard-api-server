#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel

from bardapi import BardAsync

# API Endpoint
app = FastAPI()
router = APIRouter(prefix="/v1")

# Authentication
bearer = HTTPBearer()
auth_key = 'xxxx'

# Reverse Bard API
bard_token = '<__Secure-1PSID>'
bard = BardAsync(token=bard_token)


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
async def chat_completions(completion: ChatCompletionRequest,
                           auth_key: str = Depends(bearer)):
    """Generates a response to a prompt or a conversation."""

    # Validate the token
    if auth_key.credentials != "****abc":
        raise HTTPException(status_code=401, detail="Invalid token")

    # Check if the model is supported
    if completion.model != "bard":
        raise HTTPException(
            status_code=400,
            detail=f"The model `{completion.model}` does not exist")

    # Call the Bard API
    answer = await bard.get_answer(completion.messages[-1]["content"])
    # answer = bard.get_answer(completion.messages[-1]["content"])

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
async def chat_completions_alias(completion: ChatCompletionRequest,
                                 auth_key: str = Depends(bearer)):
    return await chat_completions(completion=completion, auth_key=auth_key)


app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
