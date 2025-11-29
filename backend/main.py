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
    allow_origins=["http://localhost:3000", "http://localhost:3001", "https://my-first-rag-drab.vercel.app/"],  # Next.js default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class SearchRequest(BaseModel):
    """Request model for search endpoint."""
    query_embedding: List[float] = Field(
        ...,
        description="The embedding vector of the query"
    )
    match_count: Optional[int] = Field(
        default=2,
        ge=1,
        le=10,
        description="Number of similar items to fetch (1-10, default: 2)"
    )


class MatchItem(BaseModel):
    """Model for a single match result."""
    id: int
    content: str
    similarity: Optional[float] = None


class SearchResponse(BaseModel):
    """Response model for search endpoint."""
    matches: List[MatchItem]


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
            "search": "/search (POST)"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}




@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Search for similar documents using vector embeddings.
    
    Args:
        request: SearchRequest containing query_embedding and optional match_count
        
    Returns:
        SearchResponse with list of matching documents
        
    Raises:
        HTTPException: If Supabase query fails or returns an error
    """
    # Ensure match_count is within bounds (default 2, max 10)
    match_count = request.match_count if request.match_count is not None else 2
    match_count = min(max(match_count, 1), 10)  # Clamp between 1 and 10
    
    logger.info(f"Search request received: match_count={match_count}, embedding_dim={len(request.query_embedding)}")
    
    try:
        # Call Supabase RPC function
        response = supabase.rpc(
            "match_documents",
            {
                "query_embedding": request.query_embedding,
                "match_count": match_count
            }
        ).execute()
        
        # Check if response has data
        if not hasattr(response, 'data') or response.data is None:
            logger.warning("Supabase RPC returned no data")
            return SearchResponse(matches=[])
        
        # Process the response data
        matches = []
        for item in response.data:
            # Convert item to dict if it's not already
            if not isinstance(item, dict):
                item = dict(item) if hasattr(item, '__dict__') else {}
            
            # Extract similarity if present (could be 'similarity', 'distance', etc.)
            similarity = item.get('similarity')
            if similarity is None:
                # Try alternative field names
                similarity = item.get('distance')
            
            # Build match item - handle missing fields gracefully
            match_data = {
                'id': item.get('id'),
                'content': item.get('content', ''),
            }
            if similarity is not None:
                match_data['similarity'] = float(similarity)
            
            match_item = MatchItem(**match_data)
            matches.append(match_item)
        
        logger.info(f"Search completed: found {len(matches)} matches")
        return SearchResponse(matches=matches)
    
    except Exception as e:
        error_msg = f"Error querying Supabase: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )


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

