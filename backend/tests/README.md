# RAG Endpoint Test Suite

This directory contains comprehensive tests for the RAG (Retrieval-Augmented Generation) functionality.

## Test Files

### `test_rag_endpoint.py`
Automated unit tests using pytest with mocked dependencies. Tests include:
- Request validation
- JSON response structure validation
- Error handling (missing API keys, Supabase failures, OpenAI failures)
- Parameter validation (top_n bounds)
- Full RAG flow integration

### `test_rag_manual.py`
Manual integration test script for testing against a running server. Validates:
- Real HTTP requests to `/ask` endpoint
- JSON response structure
- Answer content validation

## Running Tests

### Automated Tests (with mocks)

```bash
# Run all RAG tests
pytest tests/test_rag_endpoint.py -v

# Run with coverage
pytest tests/test_rag_endpoint.py --cov=rag --cov=main

# Run specific test
pytest tests/test_rag_endpoint.py::test_ask_endpoint_json_response_structure -v
```

### Manual Tests (against running server)

1. Start the FastAPI server:
```bash
python main.py
# or
uvicorn main:app --reload
```

2. In another terminal, run the manual test script:
```bash
python tests/test_rag_manual.py
```

3. Or test with a custom server URL:
```bash
SERVER_URL=http://localhost:8000 python tests/test_rag_manual.py
```

## Test Coverage

The automated test suite covers:

✅ **Request Validation**
- Missing required fields
- Invalid data types
- Parameter bounds (top_n)

✅ **Response Structure**
- Valid JSON format
- Required fields present (`answer`)
- Correct data types

✅ **RAG Flow**
- Embedding computation
- Similarity retrieval
- Top-N selection
- LLM prompt building
- LLM response generation

✅ **Error Handling**
- Missing OpenAI API key
- Supabase connection failures
- OpenAI API failures
- Empty attraction results

## Expected JSON Response

The `/ask` endpoint returns:

```json
{
  "answer": "LLM-generated answer text here..."
}
```

The `answer` field:
- Must be a string
- Must not be empty
- Contains the LLM's response based on retrieved attractions

## Example Test Output

```
✅ Status: 200
✅ Response structure: Valid JSON
✅ Answer (245 characters):
------------------------------------------------------------
Based on the attractions in Paris, the Eiffel Tower and 
Louvre Museum are two of the most popular destinations...
------------------------------------------------------------
✅ All validations passed!
```

