#!/usr/bin/env python3
"""
Manual test script for RAG endpoint.

This script can be used to test the /ask endpoint against a running FastAPI server.
It sends real requests and validates JSON responses.

Usage:
    python tests/test_rag_manual.py
    # Or with custom server URL:
    SERVER_URL=http://localhost:8000 python tests/test_rag_manual.py
"""

import os
import sys
import json
from typing import Dict, Any

import requests

# Default server URL
SERVER_URL = os.environ.get("SERVER_URL", "http://localhost:8000")
ASK_ENDPOINT = f"{SERVER_URL}/ask"


def test_ask_endpoint(query: str, top_n: int = 3) -> Dict[str, Any]:
    """
    Test the /ask endpoint with a given query.
    
    Args:
        query: User query string.
        top_n: Number of top attractions to use as context.
        
    Returns:
        Response JSON as dictionary.
    """
    payload = {"query": query, "top_n": top_n}
    
    print(f"\n{'='*60}")
    print(f"Testing /ask endpoint")
    print(f"{'='*60}")
    print(f"Query: {query}")
    print(f"Top N: {top_n}")
    print(f"Endpoint: {ASK_ENDPOINT}")
    print(f"\nSending request...")
    
    try:
        response = requests.post(ASK_ENDPOINT, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        print(f"\n✅ Status: {response.status_code}")
        print(f"✅ Response structure: Valid JSON")
        print(f"\n📝 Answer ({len(data.get('answer', ''))} characters):")
        print(f"{'-'*60}")
        print(data.get("answer", ""))
        print(f"{'-'*60}")
        
        # Validate response structure
        assert "answer" in data, "Response missing 'answer' field"
        assert isinstance(data["answer"], str), "Answer must be a string"
        assert len(data["answer"]) > 0, "Answer cannot be empty"
        
        print(f"\n✅ All validations passed!")
        return data
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: Could not connect to server at {SERVER_URL}")
        print(f"   Make sure the FastAPI server is running:")
        print(f"   python main.py")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"\n❌ Error: Request timed out (30s)")
        print(f"   The LLM call may be taking too long.")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ Error: HTTP {e.response.status_code}")
        try:
            error_data = e.response.json()
            print(f"   Detail: {error_data.get('detail', 'Unknown error')}")
        except:
            print(f"   Response: {e.response.text}")
        sys.exit(1)
    except AssertionError as e:
        print(f"\n❌ Validation failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Run manual tests with sample queries."""
    print(f"\n🧪 Manual RAG Endpoint Tests")
    print(f"Server: {SERVER_URL}")
    
    # Test cases
    test_cases = [
        {
            "query": "What are popular attractions in Paris?",
            "top_n": 3,
            "description": "Basic query about Paris attractions"
        },
        {
            "query": "Tell me about museums in London",
            "top_n": 2,
            "description": "Query about London museums"
        },
        {
            "query": "What can I do at the Eiffel Tower?",
            "top_n": 1,
            "description": "Specific attraction query"
        },
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n\n🔍 Test Case {i}: {test_case['description']}")
        try:
            result = test_ask_endpoint(test_case["query"], test_case["top_n"])
            results.append({"test": i, "status": "PASSED", "result": result})
        except SystemExit:
            results.append({"test": i, "status": "FAILED"})
            break
        except Exception as e:
            print(f"\n❌ Test {i} failed with error: {e}")
            results.append({"test": i, "status": "FAILED", "error": str(e)})
    
    # Summary
    print(f"\n\n{'='*60}")
    print(f"📊 Test Summary")
    print(f"{'='*60}")
    passed = sum(1 for r in results if r.get("status") == "PASSED")
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print(f"\n✅ All tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ Some tests failed")
        sys.exit(1)


if __name__ == "__main__":
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("Error: 'requests' package is required for manual testing")
        print("Install it with: pip install requests")
        sys.exit(1)
    
    main()

