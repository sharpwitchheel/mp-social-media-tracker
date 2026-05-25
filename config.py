# ─── Config ───────────────────────────────────────────────────────────────────
# All settings for the MP Social Tracker pipeline.
#
# IMPORTANT: Never paste your actual API tokens or passwords directly in here.
# We will handle credentials separately and securely in a later step.

# ─── Brandwatch ──────────────────────────────────────────────────────────────
# This is the Brandwatch project that contains the MP queries.
# Based on your existing setup, this is the UK Labour Party project.
BRANDWATCH_PROJECT_ID = "1998387529"

# The Brandwatch API base URL — this never changes.
BRANDWATCH_BASE_URL = "https://api.brandwatch.com"

# How many days of data to pull each time the script runs.
# 1 = just yesterday. Change to 7 if you want a week at a time.
DAYS_TO_PULL = 1

# ─── Exolyt (TikTok) ─────────────────────────────────────────────────────────
# Exolyt API base URL.
EXOLYT_BASE_URL = "https://api.exolyt.com"

# ─── Google Sheets ───────────────────────────────────────────────────────────
# The name of the tab inside the Google Sheet where data will be written.
SHEET_TAB_NAME = "mp_social_data"

# The columns that will appear in the Google Sheet, in order.
# One row will be written per MP per day.
SHEET_HEADERS = [
    "date",
    "mp_name",
    "party",
    # Facebook
    "facebook_url",
    "facebook_mentions",
    "facebook_engagement",
    "facebook_sentiment",
    # X (Twitter)
    "x_handle",
    "x_mentions",
    "x_engagement",
    "x_sentiment",
    # Instagram
    "instagram_handle",
    "instagram_mentions",
    "instagram_engagement",
    "instagram_sentiment",
    # TikTok (via Exolyt)
    "tiktok_handle",
    "tiktok_followers",
    "tiktok_views",
    "tiktok_likes",
    "tiktok_comments",
    "tiktok_shares",
    # Meta
    "last_updated",
]

# ─── Platforms ───────────────────────────────────────────────────────────────
# Which platforms to pull data for.
# Set any to False to skip that platform temporarily.
PULL_FACEBOOK   = True
PULL_X          = True
PULL_INSTAGRAM  = True
PULL_TIKTOK     = True

# ─── Logging ─────────────────────────────────────────────────────────────────
# If True, prints detail about every API call to the terminal as it runs.
# Useful for debugging. Set to False for cleaner output in production.
VERBOSE = True
