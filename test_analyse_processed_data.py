from analyse_processed_data import get_decade, create_decade_pie_chart, create_top_authors_bar_chart
import os
import pandas as pd


class TestGetDecade:
    def test_converts_mid_decade(self):
        assert get_decade(2014) == "2010s"

    def test_converts_start_of_decade(self):
        assert get_decade(2020) == "2020s"

    def test_converts_end_of_decade(self):
        assert get_decade(2019) == "2010s"

    def test_handles_older_decade(self):
        assert get_decade(1995) == "1990s"


class TestCreateDecadePieChart:
    def test_creates_png_file(self):
        df = pd.DataFrame({
            'year': [2010, 2015, 2020, 2021]
        })
        # Remove file if it exists
        if os.path.exists('decade_releases.png'):
            os.remove('decade_releases.png')

        create_decade_pie_chart(df)

        assert os.path.exists('decade_releases.png')

        # Clean up
        os.remove('decade_releases.png')


class TestCreateTopAuthorsBarChart:
    def test_creates_png_file(self):
        df = pd.DataFrame({
            'author_name': ['Author A', 'Author B', 'Author A', 'Author C'],
            'ratings': [1000, 2000, 500, 3000]
        })
        # Remove file if it exists
        if os.path.exists('top_authors.png'):
            os.remove('top_authors.png')

        create_top_authors_bar_chart(df)

        assert os.path.exists('top_authors.png')

        # Clean up
        os.remove('top_authors.png')
