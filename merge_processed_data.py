import pandas as pd


def merge_csv_files(output_file: str = 'PROCESSED_DATA.csv') -> None:
    """Merge multiple processed CSV files into one."""
    dfs = []

    for i in range(5):
        file_name = f'data/PROCESSED_DATA_{i}.csv'
        try:
            df = pd.read_csv(file_name)
            dfs.append(df)
            print(f"Loaded {len(df)} records from {file_name}")
        except FileNotFoundError:
            print(f"Warning: {file_name} not found, skipping.")

    if not dfs:
        print("No files found to merge.")
        return

    merged = pd.concat(dfs, ignore_index=True)
    merged = merged.drop_duplicates()
    merged = merged.sort_values('rating', ascending=False)

    merged.to_csv(output_file, index=False)
    print(f"Saved {len(merged)} records to {output_file}")


if __name__ == "__main__":
    merge_csv_files()
