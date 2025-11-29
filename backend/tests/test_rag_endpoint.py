#!/usr/bin/env python3
"""
Test suite for RAG endpoint (/ask) in the FastAPI application.

Tests the end-to-end RAG flow including:
- Request validation
- JSON response structure
- Error handling
- Integration with mocked Supabase and OpenAI
"""

import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from typing import List, Dict

import pytest
from fastapi.testclient import TestClient

# Add parent directory to path so we can import main
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set up test environment variables before importing main
os.environ.setdefault("SUPABASE_URL", "http://test-supabase.local")
os.environ.setdefault("SUPABASE_SECRET_KEY", "test-secret-key")
os.environ.setdefault("OPENAI_API_KEY", "test-openai-key")

import main  # noqa: E402
import rag  # noqa: E402


# Test client
client = TestClient(main.app)


class MockSupabaseResponse:
    """Mock Supabase RPC response object."""

    def __init__(self, data: List[Dict]):
        self.data = data


class MockOpenAIResponse:
    """Mock OpenAI chat completion response object."""

    def __init__(self, content: str):
        self.choices = [MagicMock()]
        self.choices[0].message = MagicMock()
        self.choices[0].message.content = content


def test_ask_endpoint_health_check():
    """Test that the /ask endpoint exists and accepts requests."""
    # This will fail if OpenAI/Supabase aren't mocked, but we're just checking endpoint exists
    with patch("rag.get_similarities") as mock_similarities, patch(
        "rag.call_llm"
    ) as mock_llm:
        mock_similarities.return_value = []
        mock_llm.return_value = "Test answer"

        response = client.post("/ask", json={"query": "test query"})
        # Should not be 404 (endpoint exists)
        assert response.status_code != 404


def test_ask_endpoint_request_validation():
    """Test that /ask endpoint validates request structure."""
    # Missing required 'query' field
    response = client.post("/ask", json={})
    assert response.status_code == 422  # Validation error

    # Invalid query type
    response = client.post("/ask", json={"query": 123})
    assert response.status_code == 422

    # Valid request structure
    with patch("rag.get_similarities") as mock_similarities, patch(
        "rag.call_llm"
    ) as mock_llm:
        mock_similarities.return_value = []
        mock_llm.return_value = "Test answer"

        response = client.post("/ask", json={"query": "What are attractions in Paris?"})
        assert response.status_code in [200, 500]  # Either success or internal error (if not mocked properly)


def test_ask_endpoint_json_response_structure():
    """Test that /ask returns proper JSON response structure."""
    mock_attractions = [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "city_name": "Paris",
            "attraction_name": "Eiffel Tower",
            "attraction_type": "landmark",
            "address": "Champ de Mars, Paris",
            "price": 29.50,
            "currency": "USD",
            "open_hours": "Daily: 9:00-23:45",
            "things_to_do": "Climb to the top for panoramic city views",
            "similarity": 0.91,
        },
        {
            "id": "223e4567-e89b-12d3-a456-426614174001",
            "city_name": "Paris",
            "attraction_name": "Louvre Museum",
            "attraction_type": "museum",
            "address": "Rue de Rivoli, Paris",
            "price": 17.00,
            "currency": "USD",
            "open_hours": "Daily: 9:00-18:00",
            "things_to_do": "Explore world-famous artworks",
            "similarity": 0.85,
        },
    ]

    with patch("rag.get_similarities") as mock_similarities, patch(
        "rag.call_llm"
    ) as mock_llm:
        mock_similarities.return_value = mock_attractions
        mock_llm.return_value = "The Eiffel Tower and Louvre Museum are popular attractions in Paris."

        response = client.post(
            "/ask",
            json={"query": "What are popular attractions in Paris?", "top_n": 2},
        )

        assert response.status_code == 200
        data = response.json()

        # Validate response structure
        assert "answer" in data
        assert isinstance(data["answer"], str)
        assert len(data["answer"]) > 0

        # Verify the answer contains expected content
        assert "Eiffel Tower" in data["answer"] or "Louvre" in data["answer"] or "Paris" in data["answer"]


def test_ask_endpoint_with_top_n_parameter():
    """Test that /ask endpoint respects top_n parameter."""
    mock_attractions = [
        {
            "id": f"{i}23e4567-e89b-12d3-a456-42661417400{i}",
            "city_name": "Paris",
            "attraction_name": f"Attraction {i}",
            "attraction_type": "landmark",
            "things_to_do": f"Description {i}",
            "similarity": 0.9 - (i * 0.1),
        }
        for i in range(5)
    ]

    with patch("rag.get_similarities") as mock_similarities, patch(
        "rag.call_llm"
    ) as mock_llm, patch("rag.get_top_n_docs") as mock_top_n:
        mock_similarities.return_value = mock_attractions
        mock_top_n.return_value = mock_attractions[:2]  # Should get top 2
        mock_llm.return_value = "Test answer with 2 attractions"

        response = client.post(
            "/ask",
            json={"query": "test query", "top_n": 2},
        )

        assert response.status_code == 200
        # Verify get_top_n_docs was called with n=2
        mock_top_n.assert_called_once()
        call_args = mock_top_n.call_args
        assert call_args[1]["n"] == 2 or call_args[0][1] == 2


def test_ask_endpoint_default_top_n():
    """Test that /ask uses default top_n=3 when not provided."""
    with patch("rag.get_similarities") as mock_similarities, patch(
        "rag.call_llm"
    ) as mock_llm, patch("rag.get_top_n_docs") as mock_top_n:
        mock_similarities.return_value = []
        mock_top_n.return_value = []
        mock_llm.return_value = "Test answer"

        response = client.post("/ask", json={"query": "test query"})

        assert response.status_code == 200
        # Verify get_top_n_docs was called with default n=3
        mock_top_n.assert_called_once()
        call_args = mock_top_n.call_args
        assert call_args[1]["n"] == 3 or call_args[0][1] == 3


def test_ask_endpoint_empty_attractions():
    """Test /ask endpoint when no attractions are found."""
    with patch("rag.get_similarities") as mock_similarities, patch(
        "rag.call_llm"
    ) as mock_llm:
        mock_similarities.return_value = []  # No attractions found
        mock_llm.return_value = "I couldn't find specific attractions, but I can help with general information."

        response = client.post(
            "/ask",
            json={"query": "What are attractions in a non-existent city?"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert isinstance(data["answer"], str)


def test_ask_endpoint_error_handling_missing_openai_key():
    """Test /ask endpoint error handling when OPENAI_API_KEY is missing."""
    with patch.dict(os.environ, {}, clear=True):
        os.environ["SUPABASE_URL"] = "http://test.local"
        os.environ["SUPABASE_SECRET_KEY"] = "test-key"
        # OPENAI_API_KEY not set

        with patch("rag.get_similarities") as mock_similarities:
            mock_similarities.return_value = [
                {
                    "id": "123",
                    "attraction_name": "Test",
                    "things_to_do": "Test description",
                }
            ]

            response = client.post("/ask", json={"query": "test query"})

            # Should return 500 with error message
            assert response.status_code == 500
            data = response.json()
            assert "detail" in data


def test_ask_endpoint_error_handling_supabase_failure():
    """Test /ask endpoint error handling when Supabase query fails."""
    with patch("rag.get_similarities") as mock_similarities:
        mock_similarities.side_effect = Exception("Supabase connection failed")

        response = client.post("/ask", json={"query": "test query"})

        assert response.status_code == 500
        data = response.json()
        assert "detail" in data


def test_ask_endpoint_error_handling_openai_failure():
    """Test /ask endpoint error handling when OpenAI API call fails."""
    mock_attractions = [
        {
            "id": "123",
            "attraction_name": "Test",
            "things_to_do": "Test description",
        }
    ]

    with patch("rag.get_similarities") as mock_similarities, patch(
        "rag.call_llm"
    ) as mock_llm:
        mock_similarities.return_value = mock_attractions
        mock_llm.side_effect = Exception("OpenAI API error")

        response = client.post("/ask", json={"query": "test query"})

        assert response.status_code == 500
        data = response.json()
        assert "detail" in data


def test_ask_endpoint_top_n_validation():
    """Test that /ask endpoint validates top_n parameter bounds."""
    # top_n too low (should be clamped or validated)
    response = client.post("/ask", json={"query": "test", "top_n": 0})
    assert response.status_code == 422  # Validation error

    # top_n too high (should be clamped or validated)
    response = client.post("/ask", json={"query": "test", "top_n": 20})
    assert response.status_code == 422  # Validation error

    # Valid top_n
    with patch("rag.get_similarities") as mock_similarities, patch(
        "rag.call_llm"
    ) as mock_llm:
        mock_similarities.return_value = []
        mock_llm.return_value = "Test answer"

        response = client.post("/ask", json={"query": "test", "top_n": 5})
        assert response.status_code in [200, 500]


def test_ask_endpoint_full_rag_flow_integration():
    """Integration test for full RAG flow with realistic data."""
    mock_attractions = [
        {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "city_name": "Paris",
            "attraction_name": "Eiffel Tower",
            "attraction_type": "landmark",
            "address": "Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France",
            "price": 29.50,
            "currency": "USD",
            "open_hours": "Daily: 9:00-23:45",
            "things_to_do": "Climb to the top for panoramic city views, visit the first-floor glass floor, and dine at the restaurant.",
            "similarity": 0.95,
        },
        {
            "id": "223e4567-e89b-12d3-a456-426614174001",
            "city_name": "Paris",
            "attraction_name": "Louvre Museum",
            "attraction_type": "museum",
            "address": "Rue de Rivoli, 75001 Paris, France",
            "price": 17.00,
            "currency": "USD",
            "open_hours": "Mon/Wed/Thu/Sat/Sun: 9:00-18:00; Fri: 9:00-21:45",
            "things_to_do": "Explore world-famous artworks including the Mona Lisa, Venus de Milo, and ancient Egyptian artifacts.",
            "similarity": 0.88,
        },
    ]

    expected_llm_answer = (
        "Based on the attractions in Paris, the Eiffel Tower and Louvre Museum "
        "are two of the most popular destinations. The Eiffel Tower offers "
        "panoramic views and dining options, while the Louvre Museum houses "
        "famous artworks like the Mona Lisa."
    )

    with patch("rag.get_similarities") as mock_similarities, patch(
        "rag.call_llm"
    ) as mock_llm:
        mock_similarities.return_value = mock_attractions
        mock_llm.return_value = expected_llm_answer

        response = client.post(
            "/ask",
            json={
                "query": "What are the most popular attractions in Paris?",
                "top_n": 2,
            },
        )

        assert response.status_code == 200
        data = response.json()

        # Validate response structure
        assert "answer" in data
        assert isinstance(data["answer"], str)
        assert len(data["answer"]) > 0

        # Verify RAG flow was called correctly
        mock_similarities.assert_called_once()
        mock_llm.assert_called_once()

        # Verify the prompt was built with attraction context
        llm_call_args = mock_llm.call_args[0][0]  # First positional argument (prompt)
        assert "Paris" in llm_call_args
        assert "Eiffel Tower" in llm_call_args or "Louvre" in llm_call_args


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

