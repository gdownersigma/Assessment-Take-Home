import pandas as pd
from process_raw_data import clean_title, clean_rating, clean_ratings_count, process_data


class TestCleanTitle:
    def test_removes_single_parentheses(self):
        assert clean_title("Never Let Me Go (Paperback)") == "Never Let Me Go"

    def test_removes_series_info(self):
        assert clean_title(
            "Siege and Storm (The Shadow and Bone Trilogy, #2)") == "Siege and Storm"

    def test_removes_multiple_parentheses(self):
        assert clean_title("Some Book (Series, #1) (Hardcover)") == "Some Book"

    def test_handles_no_parentheses(self):
        assert clean_title("Just a Normal Title") == "Just a Normal Title"

    def test_handles_empty_string(self):
        assert clean_title("") == ""

    def test_handles_nan(self):
        assert clean_title(pd.NA) is None
        assert clean_title(float('nan')) is None

    def test_strips_whitespace(self):
        assert clean_title("  Spaced Title (Info)  ") == "Spaced Title"


class TestCleanRating:
    def test_converts_comma_to_float(self):
        assert clean_rating("3,84") == 3.84

    def test_handles_whole_number(self):
        assert clean_rating("4,00") == 4.0

    def test_handles_nan(self):
        assert clean_rating(pd.NA) is None


class TestCleanRatingsCount:
    def test_removes_backticks(self):
        assert clean_ratings_count("`593231`") == 593231

    def test_handles_no_backticks(self):
        assert clean_ratings_count("12345") == 12345

    def test_handles_nan(self):
        assert clean_ratings_count(pd.NA) is None


class TestProcessData:
    def test_merges_author_names(self):
        raw_df = pd.DataFrame({
            'book_title': ['Test Book (Hardcover)'],
            'author_id': [1],
            'Rating': '4,50',
            'ratings': '`1000`',
            'Year released': 2020
        })
        authors_df = pd.DataFrame({
            'author_id': [1],
            'author_name': ['Test Author']
        })
        result = process_data(raw_df, authors_df)
        assert result.iloc[0]['author_name'] == 'Test Author'

    def test_drops_missing_author(self):
        raw_df = pd.DataFrame({
            'book_title': ['Book One', 'Book Two'],
            'author_id': [1, 999],
            'Rating': ['4,00', '3,50'],
            'ratings': ['`100`', '`200`'],
            'Year released': [2010, 2011]
        })
        authors_df = pd.DataFrame({
            'author_id': [1],
            'author_name': ['Only Author']
        })
        result = process_data(raw_df, authors_df)
        assert len(result) == 1

    def test_sorts_by_rating_descending(self):
        raw_df = pd.DataFrame({
            'book_title': ['Low Book', 'High Book'],
            'author_id': [1, 1],
            'Rating': ['3,00', '5,00'],
            'ratings': ['`100`', '`200`'],
            'Year released': [2010, 2011]
        })
        authors_df = pd.DataFrame({
            'author_id': [1],
            'author_name': ['Author']
        })
        result = process_data(raw_df, authors_df)
        assert result.iloc[0]['title'] == 'High Book'

    def test_output_has_correct_columns(self):
        raw_df = pd.DataFrame({
            'book_title': ['Test Book'],
            'author_id': [1],
            'Rating': '4,00',
            'ratings': '`100`',
            'Year released': 2020
        })
        authors_df = pd.DataFrame({
            'author_id': [1],
            'author_name': ['Author']
        })
        result = process_data(raw_df, authors_df)
        assert list(result.columns) == [
            'title', 'author_name', 'rating', 'ratings', 'year']
