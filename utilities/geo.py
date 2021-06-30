# Variables providing information for towns in the dataset.
towns = {
    "west_plains": {
        "formatted": "West Plains",
        "abbreviation": "WP",
        "population": 24554,
        "latitude": 36.728152,
        "longitude": -91.852589,
        "zip_code": "65775"
    },
    "willow_springs": {
        "formatted": "Willow Springs",
        "abbreviation": "WS",
        "population": 5414,
        "latitude": 36.991905,
        "longitude": -91.969294,
        "zip_code": "65793"
    },
    "mountain_view": {
        "formatted": "Mountain View",
        "abbreviation": "MV",
        "population": 5382,
        "latitude": 36.995735,
        "longitude": -91.702704,
        "zip_code": "65548"
    },
    "bakersfield": {
        "formatted": "Bakersfield",
        "abbreviation": "Bk",
        "population": 191,
        "latitude": 36.523025,
        "longitude": -92.142095,
        "zip_code": "65609"
    },
    "brandsville": {
        "formatted": "Brandsville",
        "abbreviation": "Br",
        "population": None,
        "latitude": 36.650903,
        "longitude": -91.695846,
        "zip_code": "65688"
    },
    "cabool": {
        "formatted": "Cabool",
        "abbreviation": "Cb",
        "population": 83,
        "latitude": 37.123558,
        "longitude": -92.103918,
        "zip_code": "65689"
    },
    "caulfield": {
        "formatted": "Caulfield",
        "abbreviation": "Cf",
        "population": 844,
        "latitude": 36.614380,
        "longitude": -92.104774,
        "zip_code": "65626"
    },
    "dora": {
        "formatted": "Dora",
        "abbreviation": "D",
        "population": 213,
        "latitude": 36.777159,
        "longitude": -92.217051,
        "zip_code": "65637"
    },
    "koshkonong": {
        "formatted": "Koshkonong",
        "abbreviation": "K",
        "population": 349,
        "latitude": 36.598067,
        "longitude": -91.643898,
        "zip_code": "65692"
    },
    "moody": {
        "formatted": "Moody",
        "abbreviation": "M",
        "population": 326,
        "latitude": 36.529258,
        "longitude": -91.989273,
        "zip_code": "65777"
    },
    "peace_valley": {
        "formatted": "Peace Valley",
        "abbreviation": "PV",
        "population": 406,
        "latitude": 36.839671,
        "longitude": -91.746286,
        "zip_code": "65788"
    },
    "pomona": {
        "formatted": "Pomona",
        "abbreviation": "Pm",
        "population": 2030,
        "latitude": 36.866780,
        "longitude": -91.916741,
        "zip_code": "65789"
    },
    "pottersville": {
        "formatted": "Pottersville",
        "abbreviation": "Pt",
        "population": 608,
        "latitude": 36.695834,
        "longitude": -92.031255,
        "zip_code": "65790"
    },
    "summersville": {
        "formatted": "Summersville",
        "abbreviation": "S",
        "population": None,
        "latitude": 37.179627,
        "longitude": -91.656329,
        "zip_code": "65571"
    },
    "unknown": {
        "formatted": "Unknown",
        "abbreviation": "?",
        "population": None,
        "latitude": None,
        "longitude": None,
        "zip_code": None
    }
}

# Variables providing information for groups of towns in the dataset.
groups = {
    "howell_county": {
        "formatted": "Howell County",
        "abbreviation": "Total",
        "towns": ["west_plains", "willow_springs", "mountain_view", "bakersfield", "brandsville", "cabool", "caulfield", "dora", "koshkonong", "moody", "peace_valley", "pomona", "pottersville", "summersville", "unknown"]
    },
    "cities": {
        "formatted": "Cities",
        "abbreviation": "Cities",
        "towns": ["west_plains", "willow_springs", "mountain_view"]
    },
    "other": {
        "formatted": "Other",
        "abbreviation": "Other",
        "towns": ["bakersfield", "brandsville", "cabool", "caulfield", "dora", "koshkonong", "moody", "peace_valley", "pomona", "pottersville", "summersville", "unknown"]
    }
}