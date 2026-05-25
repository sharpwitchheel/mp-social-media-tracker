# ─── MP Social Tracker ───────────────────────────────────────────────────────
# Main script. Pulls data for 13 Labour MPs from Brandwatch (Facebook, X,
# Instagram) and Exolyt (TikTok) and writes one row per MP per day into
# the MP Packages | Data Warehouse Google Sheet.
#
# How to run:
#   python3 run.py
#
# Requirements:
#   pip install requests google-auth google-auth-httplib2 google-api-python-client

import os
import datetime
import requests
from googleapiclient.discovery import build
from google.oauth2 import service_account

from config import (
    BRANDWATCH_PROJECT_ID,
    BRANDWATCH_BASE_URL,
    SPREADSHEET_ID,
    SHEET_TAB_NAME,
    SHEET_HEADERS,
    PULL_FACEBOOK,
    PULL_X,
    PULL_INSTAGRAM,
    PULL_TIKTOK,
    DAYS_TO_PULL,
    VERBOSE,
)
from mp_list import MP_LIST


# ─── Credentials ─────────────────────────────────────────────────────────────
# Tokens are read from environment variables — never hardcoded.
# Before running, set these in your terminal:
#   export BW_TOKEN="your-brandwatch-token"
#   export EXOLYT_TOKEN="your-exolyt-token"
#   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"

BW_TOKEN     = os.environ.get("BW_TOKEN")
EXOLYT_TOKEN = os.environ.get("EXOLYT_TOKEN")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


# ─── Helpers ─────────────────────────────────────────────────────────────────

def log(msg):
    """Prints a message if VERBOSE is on."""
    if VERBOSE:
        print(msg)


def get_date_range():
    """Returns (start_date, end_date) as ISO strings for the pull window."""
    end   = datetime.date.today() - datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=DAYS_TO_PULL - 1)
    return start.isoformat(), end.isoformat()


def get_sheets_service():
    """Authenticates with Google and returns a Sheets API client."""
    creds = service_account.Credentials.from_service_account_file(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"],
        scopes=SCOPES,
    )
    return build("sheets", "v4", credentials=creds)


# ─── Brandwatch ──────────────────────────────────────────────────────────────

def bw_headers():
    """Returns the auth headers for every Brandwatch API call."""
    return {"Authorization": f"Bearer {BW_TOKEN}"}


def fetch_bw_mentions(query_string, start_date, end_date, page_type=None):
    """
    Pulls mention count, total engagement, and average sentiment
    from Brandwatch for a given query string and date range.

    query_string: a Brandwatch Boolean query, e.g. a Facebook URL or X handle
    page_type:    optional filter e.g. "facebook", "twitter", "instagram"
    """
    url    = f"{BRANDWATCH_BASE_URL}/projects/{BRANDWATCH_PROJECT_ID}/data/mentions"
    params = {
        "startDate": f"{start_date}T00:00:00+0000",
        "endDate":   f"{end_date}T23:59:59+0000",
        "q":         query_string,
        "pageSize":  1,  # we only need the totals, not the full text
    }
    if page_type:
        params["pageType"] = page_type

    try:
        resp = requests.get(url, headers=bw_headers(), params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return {
            "mentions":    data.get("resultsTotal", 0),
            "engagement":  data.get("totalEngagement", 0),
            "sentiment":   data.get("sentimentSummary", {}).get("positive", 0),
        }
    except Exception as e:
        log(f"  ⚠ Brandwatch error for query '{query_string}': {e}")
        return {"mentions": None, "engagement": None, "sentiment": None}


def get_facebook_data(mp, start_date, end_date):
    """Pulls Facebook data for one MP using their page URL."""
    if not PULL_FACEBOOK or not mp.get("facebook_url"):
        return {"mentions": None, "engagement": None, "sentiment": None}
    log(f"  Facebook: {mp['facebook_url']}")
    return fetch_bw_mentions(mp["facebook_url"], start_date, end_date, page_type="facebook")


def get_x_data(mp, start_date, end_date):
    """Pulls X (Twitter) data for one MP using their handle."""
    if not PULL_X or not mp.get("x"):
        return {"mentions": None, "engagement": None, "sentiment": None}
    query = f"author:{mp['x']}"
    log(f"  X: {query}")
    return fetch_bw_mentions(query, start_date, end_date, page_type="twitter")


def get_instagram_data(mp, start_date, end_date):
    """Pulls Instagram data for one MP using their handle."""
    if not PULL_INSTAGRAM or not mp.get("instagram"):
        return {"mentions": None, "engagement": None, "sentiment": None}
    query = f"author:{mp['instagram']}"
    log(f"  Instagram: {query}")
    return fetch_bw_mentions(query, start_date, end_date, page_type="instagram")


# ─── Exolyt (TikTok) ─────────────────────────────────────────────────────────

def get_tiktok_data(mp):
    """
    Pulls TikTok account stats for one MP from Exolyt.
    Returns followers, views, likes, comments and shares.
    """
    if not PULL_TIKTOK or not mp.get("tiktok"):
        return {
            "followers": None, "views": None,
            "likes": None, "comments": None, "shares": None,
        }

    username = mp["tiktok"]
    url      = f"https://api.exolyt.com/v1/profile/{username}"
    headers  = {"Authorization": f"Bearer {EXOLYT_TOKEN}"}

    log(f"  TikTok: {username}")

    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return {
            "followers": data.get("followerCount"),
            "views":     data.get("totalVideoViews"),
            "likes":     data.get("heartCount"),
            "comments":  data.get("commentCount"),
            "shares":    data.get("shareCount"),
        }
    except Exception as e:
        log(f"  ⚠ Exolyt error for '{username}': {e}")
        return {
            "followers": None, "views": None,
            "likes": None, "comments": None, "shares": None,
        }


# ─── Google Sheets ────────────────────────────────────────────────────────────

def ensure_headers(service):
    """
    Checks if the sheet already has headers.
    If the sheet is empty, writes the header row.
    """
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_TAB_NAME}!A1:A1",
    ).execute()

    if not result.get("values"):
        log("Sheet is empty — writing headers...")
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"{SHEET_TAB_NAME}!A1",
            valueInputOption="RAW",
            body={"values": [SHEET_HEADERS]},
        ).execute()
        log("Headers written.")


def append_rows(service, rows):
    """Appends a list of rows to the bottom of the sheet."""
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_TAB_NAME}!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": rows},
    ).execute()
    log(f"  ✓ {len(rows)} row(s) written to sheet.")


# ─── Main ─────────────────────────────────────────────────────────────────────

def run():
    start_date, end_date = get_date_range()
    now = datetime.datetime.utcnow().isoformat()

    log(f"\n{'='*60}")
    log(f"MP Social Tracker — pulling data for {end_date}")
    log(f"{'='*60}\n")

    # Connect to Google Sheets
    sheets = get_sheets_service()
    ensure_headers(sheets)

    rows_to_write = []

    for mp in MP_LIST:
        log(f"\n▶ {mp['name']}")

        # Pull data from each platform
        fb  = get_facebook_data(mp,  start_date, end_date)
        x   = get_x_data(mp,         start_date, end_date)
        ig  = get_instagram_data(mp, start_date, end_date)
        tt  = get_tiktok_data(mp)

        # Build one row for this MP
        row = [
            end_date,
            mp["name"],
            mp["party"],
            # Facebook
            mp.get("facebook_url", ""),
            fb["mentions"],
            fb["engagement"],
            fb["sentiment"],
            # X
            mp.get("x", ""),
            x["mentions"],
            x["engagement"],
            x["sentiment"],
            # Instagram
            mp.get("instagram", ""),
            ig["mentions"],
            ig["engagement"],
            ig["sentiment"],
            # TikTok
            mp.get("tiktok", ""),
            tt["followers"],
            tt["views"],
            tt["likes"],
            tt["comments"],
            tt["shares"],
            # Meta
            now,
        ]

        rows_to_write.append(row)
        log(f"  ✓ {mp['name']} done")

    # Write all rows to the sheet in one batch
    log(f"\nWriting {len(rows_to_write)} rows to Google Sheet...")
    append_rows(sheets, rows_to_write)

    log(f"\n{'='*60}")
    log(f"Done. {len(rows_to_write)} MPs processed for {end_date}.")
    log(f"{'='*60}\n")


if __name__ == "__main__":
    run()
