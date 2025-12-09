#!/usr/bin/env python3
"""
FastAPI server for vector similarity search using Supabase.

This server provides a POST endpoint to search for similar documents
using vector embeddings stored in Supabase.
"""

import os
import logging
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from supabase import create_client, Client
from dotenv import load_dotenv

# Import RAG functionality
import rag


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file (if present)
# This makes SUPABASE_URL and SUPABASE_SECRET_KEY available via os.environ
load_dotenv()

# Read environment variables (from real env or .env)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.environ.get("SUPABASE_SECRET_KEY")

# Validate environment variables
if not SUPABASE_URL:
    error_msg = "SUPABASE_URL environment variable is not set"
    logger.error(error_msg)
    raise ValueError(error_msg)

if not SUPABASE_SECRET_KEY:
    error_msg = "SUPABASE_SECRET_KEY environment variable is not set"
    logger.error(error_msg)
    raise ValueError(error_msg)

# Initialize Supabase client
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)
    logger.info("Supabase client initialized successfully")
except Exception as e:
    error_msg = f"Failed to initialize Supabase client: {e}"
    logger.error(error_msg)
    raise


# Initialize FastAPI app
app = FastAPI(
    title="Vector Similarity Search API",
    description="Search for similar documents using vector embeddings",
    version="1.0.0"
)

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://firstragapp.rupertlim.com",
        "http://localhost:3000",
        "http://localhost:3001",
        "https://my-first-rag-drab.vercel.app",
        "https://frontend-my-first-rag.vercel.app",
        "https://frontend-my-first-mqe864ctf-rupert-ls-projects.vercel.app",
        "https://frontend-my-first-rag-git-main-rupert-ls-projects.vercel.app",
        "https://frontend-my-first-j7n9igmcq-rupert-ls-projects.vercel.app",
        "https://frontend-my-first-rag-rupert-ls-projects.vercel.app",
        "https://frontend-my-first-o8rfc4795-rupert-ls-projects.vercel.app",
        "https://frontend-my-first-txt5rym8b-rupert-ls-projects.vercel.app",
    ],  # Next.js default ports and Vercel deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class QueryRequest(BaseModel):
    """Request model for free-text question answering."""
    query: str
    top_n: Optional[int] = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of top similar documents to use as context (1-10, default: 3)",
    )


class AnswerResponse(BaseModel):
    """Response model for LLM-generated answers."""
    answer: str


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {
        "message": "Vector Similarity Search API",
        "status": "running",
        "endpoints": {
            "ask": "/ask (POST)"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/ask", response_model=AnswerResponse)
async def ask(request: QueryRequest):
    """
    Endpoint for end-to-end question answering using RAG:
      - Accepts a free-text query.
      - Uses embeddings and Supabase to retrieve similar documents.
      - Calls an LLM with the query and retrieved context.
      - Returns the LLM's answer.
    """
    top_n = request.top_n if request.top_n is not None else 3
    try:
        answer = rag.answer_user_query(supabase, request.query, top_n=top_n)
        return AnswerResponse(answer=answer)
    except RuntimeError as runtime_error:
        # Typically missing OPENAI_API_KEY or similar configuration issue
        logger.error(f"Configuration error in /ask: {runtime_error}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(runtime_error))
    except Exception as exc:
        logger.error(f"Error in /ask endpoint: {exc}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating an answer. Please try again later.",
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

