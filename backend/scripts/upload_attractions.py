#!/usr/bin/env python3
"""
Upload attractions data from CSV to Supabase.

This script reads attractions data from a CSV file and uploads it to a Supabase
attractions table using the Supabase 2.0 service role key.

Environment variables required:
    SUPABASE_URL: Your Supabase project URL
    SUPABASE_SECRET_KEY: Your Supabase service role key (secret key)

Example .env file:
    SUPABASE_URL=https://your-project.supabase.co
    SUPABASE_SECRET_KEY=your-service-role-key-here
"""

import csv
import os
import sys
from typing import Any, Dict, List
from decimal import Decimal, InvalidOperation
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('BAAI/bge-small-en-v1.5')

load_dotenv()

try:
    from supabase import create_client, Client
except ImportError:
    print(
        "Error: supabase-py package not found. Install it with: pip install supabase",
        file=sys.stderr
    )
    sys.exit(1)



def get_supabase_client() -> Client:
    """
    Initialize and return a Supabase client using environment variables.
    
    Returns:
        Client: Initialized Supabase client
        
    Raises:
        SystemExit: If required environment variables are missing
    """
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SECRET_KEY")
    
    if not supabase_url:
        print(
            "Error: SUPABASE_URL environment variable is not set.",
            file=sys.stderr
        )
        print(
            "Please set it with: export SUPABASE_URL=https://your-project.supabase.co",
            file=sys.stderr
        )
        sys.exit(1)
    
    if not supabase_key:
        print(
            "Error: SUPABASE_SECRET_KEY environment variable is not set.",
            file=sys.stderr
        )
        print(
            "Please set it with: export SUPABASE_SECRET_KEY=your-key-here",
            file=sys.stderr
        )
        sys.exit(1)
    
    try:
        client = create_client(supabase_url, supabase_key)
        return client
    except Exception as e:
        print(f"Error: Failed to create Supabase client: {e}", file=sys.stderr)
        sys.exit(1)


def load_csv(path: str) -> List[Dict[str, str]]:
    """
    Read and parse the attractions CSV file.
    
    Args:
        path: Path to the CSV file
        
    Returns:
        List of dictionaries, each representing a row from the CSV
        
    Raises:
        SystemExit: If the file cannot be read or parsed
    """
    if not os.path.exists(path):
        print(f"Error: CSV file not found: {path}", file=sys.stderr)
        sys.exit(1)
    
    rows = []
    try:
        with open(path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                # Validate required fields
                required_fields = ['city_name', 'attraction_name', 'attraction_type', 'location', 'price', 'currency', 'open_hours', 'things_to_do']
                missing_fields = [field for field in required_fields if not row.get(field)]
                
                if missing_fields:
                    print(
                        f"Warning: Row {row_num} is missing fields: {', '.join(missing_fields)}. Skipping.",
                        file=sys.stderr
                    )
                    continue
                
                rows.append(row)
        
        if not rows:
            print("Error: No valid rows found in CSV file.", file=sys.stderr)
            sys.exit(1)
        
        return rows
    
    except csv.Error as e:
        print(f"Error: Failed to parse CSV file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to read CSV file: {e}", file=sys.stderr)
        sys.exit(1)


def prepare_row_for_insert(row: Dict[str, str]) -> Dict[str, Any]:
    """
    Convert a CSV row dictionary to the format expected by Supabase.
    
    Args:
        row: Dictionary from CSV row
        
    Returns:
        Dictionary with properly typed values for Supabase insertion
    """

    # Embed the attraction name
    embedding = model.encode(row['attraction_name'] + row['attraction_type'] + row['location'] + row['open_hours'])
    prepared = {
        'city_name': row['city_name'].strip(),
        'attraction_name': row['attraction_name'].strip(),
        'attraction_type': row['attraction_type'].strip(),
        'location': row['location'].strip(),
        'open_hours': row['open_hours'].strip(),
        'things_to_do': row['things_to_do'].strip(),
        'embedding': embedding.tolist(),
    }
    
    # Add optional address field if present
    if row.get('address'):
        prepared['address'] = row['address'].strip()
    
    # Add currency field (default to USD if not provided)
    prepared['currency'] = row.get('currency', 'USD').strip()
    
    # Convert price to float
    try:
        price_str = row['price'].strip()
        prepared['price'] = float(price_str)
    except (ValueError, KeyError) as e:
        raise ValueError(f"Invalid price value '{row.get('price', '')}': {e}")
    
    return prepared


def insert_attractions(client: Client, rows: List[Dict[str, str]]) -> None:
    """
    Insert attraction rows into the Supabase attractions table.
    
    Args:
        client: Supabase client instance
        rows: List of dictionaries containing attraction data from CSV
    """
    prepared_rows = []
    errors = []
    
    # Prepare all rows first
    for idx, row in enumerate(rows, start=1):
        try:
            prepared_row = prepare_row_for_insert(row)
            prepared_rows.append(prepared_row)
        except ValueError as e:
            error_msg = f"Row {idx + 1} (attraction_name: '{row.get('attraction_name', 'unknown')}'): {e}"
            errors.append(error_msg)
            print(f"Warning: {error_msg}", file=sys.stderr)
    
    if errors and not prepared_rows:
        print("Error: All rows failed validation. Cannot proceed.", file=sys.stderr)
        sys.exit(1)
    
    if not prepared_rows:
        print("Error: No valid rows to insert.", file=sys.stderr)
        sys.exit(1)
    
    # Insert all rows at once
    try:
        response = client.table('attractions').insert(prepared_rows).execute()
        
        inserted_count = len(prepared_rows)
        print(f"Success: Inserted {inserted_count} row(s) into the attractions table.")
        
        if errors:
            print(f"\nNote: {len(errors)} row(s) were skipped due to validation errors.", file=sys.stderr)
    
    except Exception as e:
        print(f"Error: Failed to insert data into Supabase: {e}", file=sys.stderr)
        
        # Try to provide more context if available
        if hasattr(e, 'message'):
            print(f"Details: {e.message}", file=sys.stderr)
        if hasattr(e, 'details'):
            print(f"Details: {e.details}", file=sys.stderr)
        
        sys.exit(1)


def main() -> None:
    """Main entry point for the script."""
    # Get CSV path from command line argument or use default
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "scripts/attractions_seed.csv"
    
    # Normalize path to handle both relative and absolute paths
    if not os.path.isabs(csv_path):
        # If relative, make it relative to the project root
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        csv_path = os.path.join(project_root, csv_path)
    
    print(f"Reading CSV from: {csv_path}")
    
    # Load CSV data
    rows = load_csv(csv_path)
    print(f"Loaded {len(rows)} row(s) from CSV.")
    
    # Initialize Supabase client
    print("Connecting to Supabase...")
    client = get_supabase_client()
    
    # Insert data
    print("Uploading data to Supabase...")
    insert_attractions(client, rows)
    
    print("Done!")


if __name__ == "__main__":
    main()

