"""A script to analyse book data."""
import pandas as pd
import altair as alt


def load_data(file_path: str) -> pd.DataFrame:
    """Load processed data from CSV."""
    return pd.read_csv(file_path)


def get_decade(year: int) -> str:
    """Convert year to decade string (e.g., 2014 -> '2010s')."""
    decade = (year // 10) * 10
    return f"{decade}s"


def create_decade_pie_chart(df: pd.DataFrame) -> None:
    """Create pie chart showing proportion of books released in each decade."""
    # Add decade column
    df['decade'] = df['year'].apply(get_decade)

    # Count books per decade
    decade_counts = df.groupby('decade').size().reset_index(name='count')

    # Create chart
    pie_chart = alt.Chart(decade_counts).mark_arc().encode(
        theta='count',
        color='decade'
    ).properties(
        title='Proportion of Books Released by Decade'
    )

    pie_chart.save('decade_releases.png', scale_factor=2)


def create_top_authors_bar_chart(df: pd.DataFrame) -> None:
    """Create sorted bar chart showing total ratings for top 10 most-rated authors."""
    # Group by author, sum ratings, get top 10
    author_ratings = df.groupby('author_name')['ratings'].sum().reset_index()
    top_authors = author_ratings.nlargest(10, 'ratings')

    # Create sorted bar chart
    bar_chart = alt.Chart(top_authors).mark_bar().encode(
        x=alt.X('ratings', title='Total Ratings'),
        y=alt.Y('author_name', sort='-x', title='Author')
    ).properties(
        title='Top 10 Most-Rated Authors'
    )

    bar_chart.save('top_authors.png', scale_factor=2)


if __name__ == "__main__":
    df = load_data("data/PROCESSED_DATA_0.csv")
    print(f"Loaded {len(df)} records.")

    print(get_decade(2005))

    create_decade_pie_chart(df)
    print("Saved decade_releases.png")

    create_top_authors_bar_chart(df)
    print("Saved top_authors.png")
