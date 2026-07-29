"""Load CMS MCD CSVs, strip HTML, return a list of document dicts."""
import pandas as pd
from bs4 import BeautifulSoup
import config


def _clean_html(text):
    if not isinstance(text, str):
        return ""
    return BeautifulSoup(text, "lxml").get_text(" ", strip=True)


def load_documents():
    docs = []
    csvs = sorted(config.DATA_RAW.glob("*.csv"))
    if not csvs:
        raise FileNotFoundError(
            f"No CSVs in {config.DATA_RAW}. Download CMS data first (see PHASE0.md)."
        )
    for path in csvs:
        df = pd.read_csv(path, dtype=str, encoding="latin-1", on_bad_lines="skip")
        print(f"{path.name}: columns = {list(df.columns)}")
        text_col = next((c for c in config.CMS_TEXT_COLUMNS if c in df.columns), None)
        if text_col is None:
            print("  !! no known text column; edit config.CMS_TEXT_COLUMNS to match the data dictionary")
            continue
        if config.FILTER_KEYWORD:
            df = df[df[text_col].str.contains(config.FILTER_KEYWORD, case=False, na=False)]
        if config.FILTER_DOC_IDS and config.CMS_ID_COLUMN in df.columns:
            df = df[df[config.CMS_ID_COLUMN].isin(config.FILTER_DOC_IDS)]
        for _, row in df.iterrows():
            body = _clean_html(row[text_col])
            if len(body) < 200:          # skip stubs
                continue
            docs.append({
                "id": row.get(config.CMS_ID_COLUMN) if config.CMS_ID_COLUMN else None,
                "title": row.get(config.CMS_TITLE_COLUMN) if config.CMS_TITLE_COLUMN else path.stem,
                "source": path.name,
                "text": body,
            })
    print(f"Loaded {len(docs)} documents.")
    return docs


if __name__ == "__main__":
    load_documents()
