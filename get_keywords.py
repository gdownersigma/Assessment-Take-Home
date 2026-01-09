import pandas as pd
import altair as alt
from collections import Counter
import string


STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
    'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
    'about', 'into', 'through', 'during', 'before', 'after', 'above',
    'below', 'between', 'under', 'again', 'further', 'then', 'once',
    'here', 'there', 'when', 'where', 'why', 'how', 'all', 'each',
    'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also',
    'now', 'its', 'it', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours',
    'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he',
    'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'they',
    'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who',
    'whom', 'this', 'that', 'these', 'those', 'am', 'being', 'if',
    'because', 'until', 'while', 'any', 'both', 'up', 'down', 'out',
    'off', 'over', 'yet', 'against', 'along', 'among', 'around',
    'without', 'within', 'upon', 'toward', 'towards', 'ever', 'never'
}


def load_data(file_path: str) -> pd.DataFrame:
    """Load processed data from CSV."""
    return pd.read_csv(file_path)


def extract_keywords(title: str) -> list[str]:
    """Extract keywords from a single title."""
    if pd.isna(title):
        return []
    words = title.lower().split()
    keywords = [word.strip(string.punctuation + '—–-') for word in words]
    return [word for word in keywords if word and word not in STOP_WORDS]


def get_keyword_counts(df: pd.DataFrame) -> pd.DataFrame:
    """Get keyword counts across all titles."""
    all_keywords = []
    for title in df['title']:
        all_keywords.extend(extract_keywords(title))

    counts = Counter(all_keywords)
    top_20 = counts.most_common(20)
    print(f"Top 20 keywords: {top_20}")

    return pd.DataFrame(top_20, columns=['keyword', 'count'])


def create_keywords_bar_chart(keyword_counts: pd.DataFrame) -> None:
    """Create and save the top keywords bar chart."""
    bar_chart = alt.Chart(keyword_counts).mark_bar().encode(
        x=alt.X('count', title='Count'),
        y=alt.Y('keyword', sort='-x', title='Keyword')
    ).properties(
        title='Top 20 Keywords in Book Titles'
    )

    bar_chart.save('top_keywords.png', scale_factor=2)


if __name__ == "__main__":
    df = load_data("data/PROCESSED_DATA_0.csv")
    print(f"Loaded {len(df)} records.")

    keyword_counts = get_keyword_counts(df)
    print(f"Found {len(keyword_counts)} top keywords.")

    create_keywords_bar_chart(keyword_counts)
    print("Saved top_keywords.png")
