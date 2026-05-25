# ─── MP Handle List ───────────────────────────────────────────────────────────
# Master list of 13 Labour MPs tracked across TikTok, Instagram, Facebook and X.
#
# To add an MP: copy one block below, fill in the details, and add it to the list.
# Use None for any platform where the MP has no account.

MP_LIST = [
    {
        "name":         "Henry Tufnell",
        "party":        "Labour",
        "facebook_url": "https://www.facebook.com/HenryTufnellPembrokeshire/",
        "tiktok":       "henry.tufnell.mp",
        "x":            "TufnellHenry",
        "instagram":    "henrytufnell",
    },
    {
        "name":         "Satvir Kaur",
        "party":        "Labour",
        "facebook_url": "https://www.facebook.com/LabourSatvir/",
        "tiktok":       None,
        "x":            "LabourSatvir",
        "instagram":    "laboursatvir",
    },
    {
        "name":         "Dave Robertson",
        "party":        "Labour",
        "facebook_url": "https://www.facebook.com/DaveForLichfield/",
        "tiktok":       "dave.for.lichfield",
        "x":            "DaveR_Lichfield",
        "instagram":    "daveforlichfield",
    },
    {
        "name":         "Miatta Fahnbulleh",
        "party":        "Labour",
        "facebook_url": "https://www.facebook.com/profile.php?id=727450382",
        "tiktok":       "miattafahnbullehmp",
        "x":            "Miatsf",
        "instagram":    None,
    },
    {
        "name":         "Natalie Fleet",
        "party":        "Labour",
        "facebook_url": "https://www.facebook.com/p/Natalie-Fleet-MP-100081795262467/",
        "tiktok":       "nataliefleetmp",
        "x":            "NatalieFleetMP",
        "instagram":    "nataliefleetmp",
    },
    {
        "name":         "Joe Powell",
        "party":        "Labour",
        "facebook_url": "https://www.facebook.com/p/Joe-Powell-MP-61551120332505/",
        "tiktok":       "joe.powell.mp.ken",
        "x":            "josephpowell",
        "instagram":    "joepowelllabour",
    },
    {
        "name":         "Kevin McKenna",
        "party":        "Labour",
        "facebook_url": "https://www.facebook.com/kevinmckennamp/",
        "tiktok":       "kevin.mckenna.mp",
        "x":            "KevinMcKenna",
        "instagram":    "kevinmckennamp",
    },
    {
        "name":         "Josh Simons",
        "party":        "Labour",
        "facebook_url": "https://www.facebook.com/joshsimonsmp/",
        "tiktok":       "josh.simons.mp",
        "x":            "joshsimonsmp",
        "instagram":    "joshsimons4makerfield",
    },
    {
        "name":         "Gregor Poynton",
        "party":        "Labour",
        "facebook_url": "https://www.facebook.com/GregorPoyntonLabour/",
        "tiktok":       "gregorpoynton",
        "x":            "gregorpoynton",
        "instagram":    "gregorpoynton",
    },
    {
        "name":         "Wes Streeting",
        "party":        "Labour",
        "facebook_url": "https://www.facebook.com/wesstreetingmp/",
        "tiktok":       "wesstreetingmp",
        "x":            "wesstreeting",
        "instagram":    "wesstreeting",
    },
    {
        "name":         "Sarah Hall",
        "party":        "Labour",
        "facebook_url": "https://www.facebook.com/SarahHallLabour/",
        "tiktok":       None,
        "x":            "sarah_hall81",
        "instagram":    "sarahhall_labour",
    },
    {
        "name":         "Alex Barros-Curtis",
        "party":        "Labour",
        "facebook_url": "https://www.facebook.com/abarroscurtis/",
        "tiktok":       "abarroscurtis",
        "x":            "ABarrosCurtis",
        "instagram":    "abarroscurtis",
    },
    {
        "name":         "Claire Hughes",
        "party":        "Labour",
        "facebook_url": "https://www.facebook.com/clairehughesBA/",
        "tiktok":       "claire.hughes.mp",
        "x":            "ClairehughesBA",
        "instagram":    "clairehughesmp",
    },
]


# ─── Lookup helpers ───────────────────────────────────────────────────────────

def get_tiktok_handles():
    """Returns a list of TikTok usernames for MPs who have one."""
    return [mp["tiktok"] for mp in MP_LIST if mp["tiktok"]]

def get_facebook_urls():
    """Returns a list of Facebook URLs for all MPs."""
    return [mp["facebook_url"] for mp in MP_LIST if mp["facebook_url"]]

def get_x_handles():
    """Returns a list of X (Twitter) handles for MPs who have one."""
    return [mp["x"] for mp in MP_LIST if mp["x"]]

def get_instagram_handles():
    """Returns a list of Instagram handles for MPs who have one."""
    return [mp["instagram"] for mp in MP_LIST if mp["instagram"]]
