#!/usr/bin/env python3
"""
RAG (Retrieval-Augmented Generation) module for question answering.

This module provides functions for:
1. Computing query embeddings
2. Retrieving similar attractions from Supabase
3. Building LLM prompts with context
4. Calling LLM to generate answers

All RAG-related logic is isolated here for clarity and maintainability.
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional

import numpy as np
from huggingface_hub import InferenceClient
from openai import OpenAI
from supabase import Client

# Configure logging
logger = logging.getLogger(__name__)

# Hugging Face Inference API configuration
HF_EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# Lazy-loaded Hugging Face Inference client
hf_client: Optional[InferenceClient] = None


def get_hf_client() -> InferenceClient:
    """
    Return a shared InferenceClient instance for computing query embeddings.
    
    The client is initialized lazily on first use and reused for subsequent calls.
    
    Raises:
        RuntimeError: If HF_TOKEN is not set.
    """
    global hf_client
    if hf_client is None:
        hf_token = os.environ.get("HF_TOKEN")
        if not hf_token:
            msg = "HF_TOKEN environment variable is not set"
            logger.error(msg)
            raise RuntimeError(msg)
        try:
            hf_client = InferenceClient(
                provider="hf-inference",
                api_key=hf_token,
            )
            logger.info("Initialized Hugging Face InferenceClient for embeddings")
        except Exception as exc:
            logger.error(f"Failed to initialize Hugging Face InferenceClient: {exc}")
            raise
    return hf_client


def get_openai_client() -> OpenAI:
    """
    Create an OpenAI client using the OPENAI_API_KEY environment variable.
    
    Raises:
        RuntimeError: If OPENAI_API_KEY is not set.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        msg = "OPENAI_API_KEY environment variable is not set"
        logger.error(msg)
        raise RuntimeError(msg)
    return OpenAI(api_key=api_key)


def get_query_embedding(user_query: str) -> List[float]:
    """
    Compute an embedding vector for the given user query text using Hugging Face Inference API.
    
    Args:
        user_query: Raw text query from the user.
        
    Returns:
        List of floats representing the embedding vector.
        
    Raises:
        RuntimeError: If HF_TOKEN is not set or API call fails.
    """
    client = get_hf_client()
    
    try:
        result = client.feature_extraction(
            user_query,
            model=HF_EMBEDDING_MODEL,
        )
        
        # Handle different response formats
        # Convert numpy array to list if needed
        if isinstance(result, np.ndarray):
            result = result.tolist()
        
        if isinstance(result, list):
            # If it's a list of lists (batch), take the first one
            if len(result) > 0 and isinstance(result[0], list):
                result = result[0]
            return [float(x) for x in result]
        elif isinstance(result, (int, float)):
            # Single value (unlikely but handle it)
            return [float(result)]
        else:
            logger.error(f"Unexpected embedding response format: {type(result)}")
            raise ValueError(f"Unexpected embedding response format: {type(result)}")
            
    except Exception as exc:
        logger.error(f"Error getting embedding from Hugging Face API: {exc}", exc_info=True)
        raise RuntimeError(f"Failed to get embedding: {str(exc)}")


def get_similarities(supabase: Client, user_query: str, max_matches: int = 10) -> List[Dict]:
    """
    Use Supabase similarity logic to get sorted attraction matches.
    
    Args:
        supabase: Supabase client instance.
        user_query: Raw user query text.
        max_matches: Maximum number of similar attractions to retrieve from Supabase.
        
    Returns:
        List of attraction records from RPC, already sorted by similarity (descending).
        Each dict contains: id, city_name, attraction_name, attraction_type, address,
        price, currency, open_hours, things_to_do, and similarity score.
    """
    query_embedding = get_query_embedding(user_query)

    try:
        response = supabase.rpc(
            "match_documents",
            {
                "query_embedding": query_embedding,
                "match_count": max_matches,
            },
        ).execute()
    except Exception as exc:
        logger.error(f"Error querying Supabase for similarities: {exc}", exc_info=True)
        raise

    if not hasattr(response, "data") or response.data is None:
        logger.warning("Supabase RPC match_documents returned no data for similarities")
        return []

    # RPC already returns sorted results, so we just return them as-is
    results = []
    for item in response.data:
        if not isinstance(item, dict):
            item = dict(item) if hasattr(item, "__dict__") else {}

        # Extract similarity score if present
        similarity = item.get("similarity")
        if similarity is None:
            similarity = item.get("distance")

        # Add similarity to the item dict if we found it
        if similarity is not None:
            try:
                item["similarity"] = float(similarity)
            except (TypeError, ValueError):
                pass

        results.append(item)

    return results


def get_top_n_docs(attractions: List[Dict], n: int = 3) -> List[Dict]:
    """
    Return the top-N attractions from the already-sorted list.
    
    Args:
        attractions: List of attraction dicts from RPC (already sorted by similarity).
        n: Number of top attractions to return.
        
    Returns:
        List of top-N attraction dicts.
    """
    if n <= 0:
        return []
    # RPC already sorts by similarity, so just take first N
    return attractions[:n]


def build_attraction_text(attraction: Dict) -> str:
    """
    Build a formatted text representation of an attraction for LLM context.
    
    Args:
        attraction: Dict containing attraction fields from RPC (id, city_name, 
                   attraction_name, attraction_type, address, price, currency, 
                   open_hours, things_to_do).
        
    Returns:
        Formatted string combining relevant attraction information.
    """
    parts = []
    
    # Add attraction name and location
    attraction_name = attraction.get("attraction_name", "")
    city_name = attraction.get("city_name", "")
    if attraction_name:
        if city_name:
            parts.append(f"Attraction: {attraction_name} in {city_name}")
        else:
            parts.append(f"Attraction: {attraction_name}")
    
    # Add attraction type
    attraction_type = attraction.get("attraction_type", "")
    if attraction_type:
        parts.append(f"Type: {attraction_type}")
    
    # Add address if available
    address = attraction.get("address", "")
    if address:
        parts.append(f"Address: {address}")
    
    # Add price information
    price = attraction.get("price")
    currency = attraction.get("currency", "USD")
    if price is not None:
        parts.append(f"Price: {price} {currency}")
    
    # Add opening hours
    open_hours = attraction.get("open_hours", "")
    if open_hours:
        parts.append(f"Opening Hours: {open_hours}")
    
    # Add things to do (main content)
    things_to_do = attraction.get("things_to_do", "")
    if things_to_do:
        parts.append(f"Description: {things_to_do}")
    
    return "\n".join(parts) if parts else ""


def _load_prompt_template() -> str:
    """
    Load the prompt template from rag_prompt.txt file.
    
    Returns:
        Prompt template string with {user_query} and {context_intro} placeholders.
        Falls back to default template if file not found.
    """
    # Try to find rag_prompt.txt in the same directory as this file
    current_dir = Path(__file__).parent
    prompt_file = current_dir / "rag_prompt.txt"
    
    if prompt_file.exists():
        try:
            with open(prompt_file, "r", encoding="utf-8") as f:
                template = f.read()
            logger.info(f"Loaded prompt template from {prompt_file}")
            return template
        except Exception as exc:
            logger.warning(f"Failed to load prompt template from {prompt_file}: {exc}. Using default.")
    else:
        logger.warning(f"Prompt template file not found at {prompt_file}. Using default.")
    
    # Fallback to default template
    return """You are a helpful assistant specializing in travel and attractions. The user has asked the following question:

User query:
\"\"\"{user_query}\"\"\"

{context_intro}

IMPORTANT: Use ONLY the attractions provided in the database information above to answer the user's query. Do not add additional attractions, locations, or destinations that are not listed in the database. 

If the database contains relevant attractions, focus your answer exclusively on those. You may provide helpful context about the attractions (such as general travel tips or cultural information), but do not introduce new destinations or attractions that are not in the database.

If no relevant attractions were found in the database, you may provide a brief general answer, but clearly state that no specific attractions were found in the database.
"""


def build_llm_prompt(user_query: str, attractions_text: List[Tuple[str, str]]) -> str:
    """
    Build a structured prompt for the LLM including the user query and context attractions.
    
    The prompt template is loaded from rag_prompt.txt file, with placeholders for
    {user_query} and {context_intro} that are replaced with actual values.
    
    Args:
        user_query: The original user question.
        attractions_text: List of (attraction_id, formatted_text) tuples.
        
    Returns:
        Complete prompt string ready to send to the LLM.
    """
    # Build context introduction
    if attractions_text:
        context_parts: List[str] = []
        for attraction_id, text in attractions_text:
            context_parts.append(f"Attraction ID: {attraction_id}\n{text}\n---")
        context_block = "\n\n".join(context_parts)
        context_intro = (
            "Here are some relevant attractions from the database, "
            "ranked by similarity:\n\n"
            f"{context_block}"
        )
    else:
        context_intro = (
            "No relevant attractions were retrieved from the database. "
            "Please answer based only on the user's query and your general knowledge about travel and attractions."
        )
    
    # Load template and replace placeholders
    template = _load_prompt_template()
    prompt = template.format(user_query=user_query, context_intro=context_intro)
    
    return prompt.strip()


def call_llm(prompt: str) -> str:
    """
    Call the LLM (OpenAI) with the given prompt and return the assistant's message.
    
    Args:
        prompt: Complete prompt string to send to the LLM.
        
    Returns:
        LLM-generated answer text.
    """
    client = get_openai_client()
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
    except Exception as exc:
        logger.error(f"Error calling OpenAI chat completion: {exc}", exc_info=True)
        raise

    try:
        return response.choices[0].message.content or ""
    except (AttributeError, IndexError, KeyError) as exc:
        logger.error(f"Unexpected OpenAI response structure: {exc}", exc_info=True)
        return ""


def answer_user_query(supabase: Client, user_query: str, top_n: int = 3) -> str:
    """
    Full RAG flow orchestrator:
      1. Compute query embedding and get sorted attractions from Supabase.
      2. Take top-N attractions (already sorted by RPC).
      3. Build formatted text for each attraction.
      4. Build a prompt for the LLM with query + attractions.
      5. Call the LLM and return the answer as a string.
    
    Args:
        supabase: Supabase client instance.
        user_query: Raw text query from the user.
        top_n: Number of top similar attractions to use as context (default: 3).
        
    Returns:
        LLM-generated answer string.
    """
    # Step 1: get sorted attractions from Supabase RPC
    attractions = get_similarities(supabase, user_query, max_matches=max(top_n, 10))

    # Step 2: take top-N attractions (RPC already sorted by similarity)
    top_attractions = get_top_n_docs(attractions, n=top_n)

    # Step 3: build formatted text for each attraction
    attractions_with_text: List[Tuple[str, str]] = []
    for attraction in top_attractions:
        attraction_id = str(attraction.get("id", ""))
        if not attraction_id:
            continue
        
        text = build_attraction_text(attraction)
        if text:
            attractions_with_text.append((attraction_id, text))

    # Step 4: build prompt and call LLM
    prompt = build_llm_prompt(user_query, attractions_with_text)
    return call_llm(prompt)

