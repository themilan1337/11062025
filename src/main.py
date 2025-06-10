from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os

from src.assitant import get_assistant, ASSISTANT_TYPE_GEMINI, ASSISTANT_TYPE_OPENAI, ASSISTANT_TYPE_CLAUDE
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.api import router as auth_router
from database import get_async_db
from tasks.api import router as tasks_router

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    assistant_type: Optional[str] = "openai" # Defaults to openai, can be omitted by frontend
    model_name: Optional[str] = None

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_assistant(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    try:
        # assistant_type will default to 'openai' if not provided by the client
        # or can be explicitly set to 'openai' if the client still sends it.
        # We force OpenAI usage here regardless of what client might send for assistant_type
        assistant = get_assistant("openai", model_name=request.model_name)
        
        ai_response = await assistant.get_chat_response(request.message)
        return ChatResponse(response=ai_response)
    except ValueError as e: # Should not happen if get_assistant is robust
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error in chat_with_assistant: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred.")

# Mount static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        with open("src/static/index.html") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="index.html not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading index.html: {str(e)}")


# Add routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])

@app.get("/health")
async def check_health(db: AsyncSession = Depends(get_async_db)):
    try:
        await db.execute(text("SELECT 1"))
    except OperationalError:
        raise HTTPException(
            status_code=500, detail="Database connection failed"
        )

    return {"status": "ok", "database": "connected"}
