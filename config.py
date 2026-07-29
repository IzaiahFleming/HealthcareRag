"""Central config. Adjust the CMS column names after you read the data dictionary."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent
DATA_RAW = ROOT / "data" / "raw"
INDEX_DIR = ROOT / "data" / "chroma"

# --- CMS data parsing -------------------------------------------------------
# After downloading the CMS Articles/LCDs CSVs, open the included Data Dictionary
# and set the column that holds the policy BODY TEXT (often HTML) and the id/title.
CMS_TEXT_COLUMNS = ['description'] 
CMS_ID_COLUMN = "article_id"     # e.g. "article_id" or "lcd_id"
CMS_TITLE_COLUMN = "title"   # e.g. "t itle"

# Optional narrowing so a v1 corpus stays small:
FILTER_KEYWORD = os.getenv("FILTER_KEYWORD", "")   # substring match on body text
FILTER_DOC_IDS = []                                # e.g. ["A57783"]

# --- models -----------------------------------------------------------------
EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
RERANK_MODEL = os.getenv("RERANK_MODEL", "BAAI/bge-reranker-base")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")
LLM_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-5")  # set to any current model string
EVAL_MODEL = os.getenv("EVAL_MODEL", LLM_MODEL)

# --- retrieval --------------------------------------------------------------
CHUNK_SIZE = 800        # words (simple v1; move to token-based later)
CHUNK_OVERLAP = 120
TOP_K = 8               # vector recall
RERANK_TOP_N = 4        # passages kept after reranking
