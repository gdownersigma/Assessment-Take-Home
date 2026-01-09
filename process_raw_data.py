"""A script to process book data."""

import argparse
import pandas as pd
import sqlite3
import re


def load_csv(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file."""
    return pd.read_csv(file_path)


def get_authors(db_path: str) -> pd.DataFrame:
    """Retrieve authors from the SQLite database."""
    conn = sqlite3.connect(db_path)
    query = "SELECT id as author_id, name as author_name FROM author"
    authors = pd.read_sql_query(query, conn)
    conn.close()
    return authors


def clean_title(title: str) -> str:
    """remove series/format info in parentheses from title."""
    if pd.isna(title):
        return None
    return re.sub(r'\s*\(.*?\)', '', title).strip()


def clean_rating(rating: str) -> float:
    """Convert rating from '3,84' to 3.84 float."""
    if pd.isna(rating):
        return None
    return float(rating.replace(',', '.'))


def clean_ratings_count(ratings: str) -> int:
    """Remove backticks and convert to integer."""
    if pd.isna(ratings):
        return None
    return int(str(ratings).replace('`', ''))


def process_data(df: pd.DataFrame, authors: pd.DataFrame) -> pd.DataFrame:
    """Process the raw data and return a cleaned DataFrame."""
    df = df.merge(authors, on='author_id', how='left')

    # Cleaning columns
    df['title'] = df['book_title'].apply(clean_title)
    df['rating'] = df['Rating'].apply(clean_rating)
    df['ratings'] = df['ratings'].apply(clean_ratings_count)
    df['year'] = df['Year released']

    # Replace empty strings/whitespace with NaN, then drop
    df['title'] = df['title'].replace(r'^\s*$', None, regex=True)
    df['author_name'] = df['author_name'].replace(r'^\s*$', None, regex=True)
    df = df.dropna(subset=['title', 'author_name'])

    df = df[['title', 'author_name', 'rating', 'ratings', 'year']]

    df = df.sort_values('rating', ascending=False)

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process book data from a CSV file.")
    parser.add_argument("input", type=str,
                        help="Path to the input CSV file.")
    args = parser.parse_args()

    # Load raw data
    data = load_csv(args.input)
    print(f"Loaded {len(data)} records from {args.input}")

    # Load authors from SQLite
    authors = get_authors("data/authors.db")
    print(f"Loaded {len(authors)} authors from database")

    # Process data
    processed_data = process_data(data, authors)
    print(f"Processed data contains {len(processed_data)} records")

    # OUTPUT
    raw_data_number = re.search(r'(\d+)', args.input).group(1)
    processed_data.to_csv(
        f"data/PROCESSED_DATA_{raw_data_number}.csv", index=False)
