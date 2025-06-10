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

# Mount static files directory (for index.html and any other static assets)
# Get the absolute path to the 'static' directory
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class ChatRequest(BaseModel):
    message: str
    assistant_type: str = ASSISTANT_TYPE_GEMINI # Default to Gemini
    # session_id: Optional[str] = None # For session management if needed

class ChatResponse(BaseModel):
    response: str

app.include_router(auth_router, tags=["auth"])
app.include_router(tasks_router, tags=["tasks"])


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    # Serve the index.html file
    index_html_path = os.path.join(static_dir, "index.html")
    try:
        with open(index_html_path, "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="index.html not found")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_assistant(chat_request: ChatRequest):
    try:
        assistant = get_assistant(chat_request.assistant_type)
        # For simplicity, using generate_response. For actual chat, use generate_chat_response with history.
        # This example is stateless for now.
        ai_response = await assistant.generate_response(chat_request.message)
        return ChatResponse(response=ai_response)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log the exception for debugging
        print(f"Error in /api/chat: {e}")
        raise HTTPException(status_code=500, detail="An error occurred with the AI assistant.")

@app.get("/health")
async def check_health(db: AsyncSession = Depends(get_async_db)):
    try:
        await db.execute(text("SELECT 1"))
    except OperationalError:
        raise HTTPException(
            status_code=500, detail="Database connection failed"
        )

    return {"status": "ok", "database": "connected"}
