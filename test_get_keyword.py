from get_keywords import extract_keywords, get_keyword_counts, create_keywords_bar_chart
import pandas as pd
import os


class TestExtractKeywords:
    def test_extracts_basic_keywords(self):
        assert extract_keywords("Love Story") == ['love', 'story']

    def test_removes_stop_words(self):
        assert extract_keywords("The Queen of Hearts") == ['queen', 'hearts']

    def test_converts_to_lowercase(self):
        assert extract_keywords("SUMMER LOVE") == ['summer', 'love']

    def test_strips_punctuation(self):
        assert extract_keywords("Love, Actually!") == ['love', 'actually']

    def test_handles_empty_string(self):
        assert extract_keywords("") == []

    def test_handles_nan(self):
        assert extract_keywords(pd.NA) == []

    def test_filters_empty_strings_from_punctuation(self):
        assert extract_keywords("Love — Life") == ['love', 'life']


class TestGetKeywordCounts:
    def test_returns_dataframe_with_correct_columns(self):
        df = pd.DataFrame({'title': ['Love Story', 'Summer Love']})
        result = get_keyword_counts(df)
        assert list(result.columns) == ['keyword', 'count']

    def test_counts_keywords_correctly(self):
        df = pd.DataFrame(
            {'title': ['Love Story', 'Love Song', 'Summer Days']})
        result = get_keyword_counts(df)
        love_count = result[result['keyword'] == 'love']['count'].values[0]
        assert love_count == 2

    def test_returns_top_20_only(self):
        titles = [f"Word{i} Extra" for i in range(30)]
        df = pd.DataFrame({'title': titles})
        result = get_keyword_counts(df)
        assert len(result) <= 20

    def test_sorts_by_most_common(self):
        df = pd.DataFrame(
            {'title': ['Love', 'Love', 'Love', 'Summer', 'Summer', 'Fire']})
        result = get_keyword_counts(df)
        assert result.iloc[0]['keyword'] == 'love'
        assert result.iloc[1]['keyword'] == 'summer'


class TestCreateKeywordsBarChart:
    def test_creates_png_file(self):
        keyword_counts = pd.DataFrame({
            'keyword': ['love', 'summer', 'fire'],
            'count': [10, 5, 3]
        })
        # Remove file if it exists
        if os.path.exists('top_keywords.png'):
            os.remove('top_keywords.png')

        create_keywords_bar_chart(keyword_counts)

        assert os.path.exists('top_keywords.png')

        # Clean up
        os.remove('top_keywords.png')
