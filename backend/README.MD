# Backend Side of Rupert Lim's first RAG project

Instructions to run

## Quickstart

### 1. Clone the repository




### 2. Set up a virtual environment (recommended)

```sh
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install required packages

```sh
pip install -r requirements.txt
```

### 4. Set required environment variables

You will need the following environment variables (can be set in a `.env` file in the project root):

```
SUPABASE_URL=your-supabase-url
SUPABASE_SECRET_KEY=your-supabase-secret-key
OPENAI_API_KEY=your-openai-api-key
```

Create a `.env` file if needed:

```sh
cp .env.example .env  # Edit .env with your values
```
or create your own `.env` file with the above keys.

### 5. Run the FastAPI server

```sh
uvicorn main:app --reload
```

The server will be available at: [http://localhost:8000](http://localhost:8000)

---

## Running Tests

### Automated test suite (with mocks):

```sh
pytest
```

### Manual endpoint testing:

```sh
python tests/test_rag_manual.py
```

---

## Troubleshooting

- Ensure your `.env` file has the correct values and is in the project root.
- If you add new dependencies, run `pip freeze > requirements.txt` to update the requirements file.
