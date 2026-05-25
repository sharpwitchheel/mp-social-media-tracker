# MP Social Tracker

Tracks 13 Labour MPs across TikTok, Instagram, Facebook and X.

Pulls data daily from Brandwatch (Facebook, Instagram, X) and Exolyt (TikTok)
and writes one row per MP per day into the MP Packages | Data Warehouse Google Sheet.

---

## What this does

Every time the script runs it:
1. Loops through all 13 MPs in `mp_list.py`
2. Pulls their mentions, engagement and sentiment from Brandwatch for Facebook, X and Instagram
3. Pulls their TikTok follower count, views, likes, comments and shares from Exolyt
4. Writes one row per MP into the Google Sheet

---

## Files

| File | What it does |
|---|---|
| `mp_list.py` | The master list of 13 MPs and all their social media handles |
| `config.py` | Settings — Sheet ID, folder ID, which platforms to pull, how many days |
| `run.py` | The main script — run this to pull data and write to the sheet |
| `README.md` | This file |

---

## The 13 MPs tracked

- Henry Tufnell
- Satvir Kaur
- Dave Robertson
- Miatta Fahnbulleh
- Natalie Fleet
- Joe Powell
- Kevin McKenna
- Josh Simons
- Gregor Poynton
- Wes Streeting
- Sarah Hall
- Alex Barros-Curtis
- Claire Hughes

---

## Output

Data is written to this Google Sheet:
**MP Packages | Data Warehouse**
`https://docs.google.com/spreadsheets/d/1APRohBUSuuKnOF4q1G7soSePR2cViOGji4nLFIkoSbo`

One row per MP per day. Columns:

| Column | Source |
|---|---|
| date | Date the script ran |
| mp_name | MP full name |
| party | Political party |
| facebook_url | Their Facebook page URL |
| facebook_mentions | How many times they were mentioned |
| facebook_engagement | Total engagement on those mentions |
| facebook_sentiment | Positive sentiment score |
| x_handle | Their X username |
| x_mentions | Mention count on X |
| x_engagement | Engagement on X |
| x_sentiment | Sentiment on X |
| instagram_handle | Their Instagram username |
| instagram_mentions | Mention count on Instagram |
| instagram_engagement | Engagement on Instagram |
| instagram_sentiment | Sentiment on Instagram |
| tiktok_handle | Their TikTok username |
| tiktok_followers | Follower count |
| tiktok_views | Total video views |
| tiktok_likes | Total likes |
| tiktok_comments | Total comments |
| tiktok_shares | Total shares |
| last_updated | Timestamp the row was written |

---

## To add a new MP

Open `mp_list.py` and copy one of the existing blocks. Fill in their details
and add it to the list. Use `None` for any platform they don't have.

---

## Requirements

- Python 3.8+
- A Brandwatch API token (stored as environment variable `BW_TOKEN`)
- An Exolyt API token (stored as environment variable `EXOLYT_TOKEN`)
- A Google service account JSON file with access to the warehouse sheet
