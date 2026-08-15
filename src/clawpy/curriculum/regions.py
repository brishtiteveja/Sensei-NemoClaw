"""Region-based education system configurations.

Each region defines tracks, subjects, exams, and universities.
Adding a new country = adding a new dict entry.
"""

from __future__ import annotations

LANGUAGES = {
    "bn": {"name": "Bangla", "name_local": "বাংলা", "flag": "🇧🇩"},
    "hi": {"name": "Hindi", "name_local": "हिन्दी", "flag": "🇮🇳"},
    "zh": {"name": "Chinese", "name_local": "中文", "flag": "🇨🇳"},
    "es": {"name": "Spanish", "name_local": "Español", "flag": "🇪🇸"},
    "en": {"name": "English", "name_local": "English", "flag": "🇬🇧"},
    "id": {"name": "Indonesian", "name_local": "Bahasa Indonesia", "flag": "🇮🇩"},
    "ms": {"name": "Malay", "name_local": "Bahasa Melayu", "flag": "🇲🇾"},
    "ha": {"name": "Hausa", "name_local": "Hausa", "flag": "🇳🇬"},
}

REGIONS: dict[str, dict] = {
    "bd": {
        "id": "bd",
        "name": "Bangladesh",
        "name_local": "বাংলাদেশ",
        "grade_level": "HSC (Grade 11-12)",
        "grade_level_local": "এইচএসসি (একাদশ-দ্বাদশ)",
        "language": "bn",
        "tracks": {
            "engineering": {
                "title": "Engineering",
                "title_local": "ইঞ্জিনিয়ারিং",
                "description": "BUET, KUET, RUET, CUET, IUT",
                "icon": "⚙️",
                "subjects": ["physics", "chemistry", "higher_math"],
                "weights": {"physics": 0.35, "higher_math": 0.35, "chemistry": 0.30},
                "exams": ["buet", "cuet", "kuet", "ruet", "iut", "sust"],
            },
            "medical": {
                "title": "Medical",
                "title_local": "মেডিকেল",
                "description": "MBBS admission",
                "icon": "🏥",
                "subjects": ["biology", "chemistry", "physics", "general_math"],
                "weights": {"biology": 0.40, "chemistry": 0.30, "physics": 0.20, "general_math": 0.10},
                "exams": ["medical"],
            },
            "university": {
                "title": "University Science",
                "title_local": "বিশ্ববিদ্যালয়",
                "description": "DU, RU, CU, JU, GST",
                "icon": "🏛️",
                "subjects": ["physics", "chemistry", "higher_math", "biology", "general_math"],
                "weights": {"physics": 0.20, "chemistry": 0.20, "higher_math": 0.20, "biology": 0.20, "general_math": 0.20},
                "exams": ["du", "ru", "cu", "ju", "gst"],
            },
        },
        "universities": {
            "buet": {"name": "BUET", "name_local": "বুয়েট", "track": "engineering", "city": "Dhaka"},
            "cuet": {"name": "CUET", "name_local": "চুয়েট", "track": "engineering", "city": "Chittagong"},
            "kuet": {"name": "KUET", "name_local": "কুয়েট", "track": "engineering", "city": "Khulna"},
            "ruet": {"name": "RUET", "name_local": "রুয়েট", "track": "engineering", "city": "Rajshahi"},
            "iut": {"name": "IUT", "name_local": "আইইউটি", "track": "engineering", "city": "Gazipur"},
            "sust": {"name": "SUST", "name_local": "শাবিপ্রবি", "track": "engineering", "city": "Sylhet"},
            "du": {"name": "Dhaka University", "name_local": "ঢাকা বিশ্ববিদ্যালয়", "track": "university", "city": "Dhaka"},
            "ru": {"name": "Rajshahi University", "name_local": "রাজশাহী বিশ্ববিদ্যালয়", "track": "university", "city": "Rajshahi"},
            "cu": {"name": "Chittagong University", "name_local": "চট্টগ্রাম বিশ্ববিদ্যালয়", "track": "university", "city": "Chittagong"},
            "ju": {"name": "Jahangirnagar University", "name_local": "জাহাঙ্গীরনগর বিশ্ববিদ্যালয়", "track": "university", "city": "Dhaka"},
            "gst": {"name": "GST Cluster", "name_local": "জিএসটি ক্লাস্টার", "track": "university", "city": "Nationwide"},
            "medical": {"name": "Medical Colleges", "name_local": "মেডিকেল কলেজ", "track": "medical", "city": "Nationwide"},
        },
        "subjects": {
            "physics": {"title": "Physics", "title_local": "পদার্থবিজ্ঞান", "icon": "⚛️"},
            "chemistry": {"title": "Chemistry", "title_local": "রসায়ন", "icon": "⚗️"},
            "higher_math": {"title": "Higher Mathematics", "title_local": "উচ্চতর গণিত", "icon": "📐"},
            "general_math": {"title": "General Mathematics", "title_local": "সাধারণ গণিত", "icon": "➕"},
            "biology": {"title": "Biology", "title_local": "জীববিজ্ঞান", "icon": "🧬"},
        },
    },
    "in": {
        "id": "in",
        "name": "India",
        "name_local": "भारत",
        "grade_level": "Class 11-12",
        "grade_level_local": "कक्षा 11-12",
        "language": "hi",
        "tracks": {
            "engineering": {
                "title": "Engineering", "title_local": "इंजीनियरिंग",
                "description": "JEE Main + Advanced, BITSAT", "icon": "⚙️",
                "subjects": ["physics", "chemistry", "mathematics"],
                "weights": {"physics": 0.33, "chemistry": 0.33, "mathematics": 0.34},
                "exams": ["jee_main", "jee_advanced", "bitsat"],
            },
            "medical": {
                "title": "Medical", "title_local": "मेडिकल",
                "description": "NEET UG", "icon": "🏥",
                "subjects": ["biology", "chemistry", "physics"],
                "weights": {"biology": 0.40, "chemistry": 0.30, "physics": 0.30},
                "exams": ["neet"],
            },
        },
        "universities": {
            "jee_main": {"name": "JEE Main (NITs)", "name_local": "JEE Main", "track": "engineering", "city": "Nationwide"},
            "jee_advanced": {"name": "JEE Advanced (IITs)", "name_local": "JEE Advanced", "track": "engineering", "city": "Nationwide"},
            "bitsat": {"name": "BITS Pilani", "name_local": "BITS पिलानी", "track": "engineering", "city": "Pilani"},
            "neet": {"name": "NEET UG", "name_local": "NEET", "track": "medical", "city": "Nationwide"},
        },
        "subjects": {
            "physics": {"title": "Physics", "title_local": "भौतिक विज्ञान", "icon": "⚛️"},
            "chemistry": {"title": "Chemistry", "title_local": "रसायन विज्ञान", "icon": "⚗️"},
            "mathematics": {"title": "Mathematics", "title_local": "गणित", "icon": "📐"},
            "biology": {"title": "Biology", "title_local": "जीव विज्ञान", "icon": "🧬"},
        },
    },
    "cn": {
        "id": "cn",
        "name": "China",
        "name_local": "中国",
        "grade_level": "Senior High (Grade 10-12)",
        "grade_level_local": "高中",
        "language": "zh",
        "tracks": {
            "science": {
                "title": "Science Track", "title_local": "理科",
                "description": "Gaokao Science", "icon": "🔬",
                "subjects": ["physics", "chemistry", "biology", "mathematics"],
                "weights": {"mathematics": 0.30, "physics": 0.25, "chemistry": 0.25, "biology": 0.20},
                "exams": ["gaokao_science"],
            },
            "liberal_arts": {
                "title": "Liberal Arts", "title_local": "文科",
                "description": "Gaokao Liberal Arts", "icon": "📚",
                "subjects": ["history", "geography", "politics", "mathematics"],
                "weights": {"history": 0.30, "geography": 0.25, "politics": 0.25, "mathematics": 0.20},
                "exams": ["gaokao_arts"],
            },
        },
        "universities": {
            "gaokao_science": {"name": "Gaokao (Science)", "name_local": "高考理科", "track": "science", "city": "Nationwide"},
            "gaokao_arts": {"name": "Gaokao (Arts)", "name_local": "高考文科", "track": "liberal_arts", "city": "Nationwide"},
        },
        "subjects": {
            "physics": {"title": "Physics", "title_local": "物理", "icon": "⚛️"},
            "chemistry": {"title": "Chemistry", "title_local": "化学", "icon": "⚗️"},
            "biology": {"title": "Biology", "title_local": "生物", "icon": "🧬"},
            "mathematics": {"title": "Mathematics", "title_local": "数学", "icon": "📐"},
            "history": {"title": "History", "title_local": "历史", "icon": "📜"},
            "geography": {"title": "Geography", "title_local": "地理", "icon": "🌍"},
            "politics": {"title": "Politics", "title_local": "政治", "icon": "⚖️"},
        },
    },
    "es": {
        "id": "es",
        "name": "Spain / Latin America",
        "name_local": "España / Latinoamérica",
        "grade_level": "Bachillerato (Grade 11-12)",
        "grade_level_local": "Bachillerato",
        "language": "es",
        "tracks": {
            "science": {
                "title": "Science & Technology", "title_local": "Ciencias y Tecnología",
                "description": "Selectividad / EBAU", "icon": "🔬",
                "subjects": ["physics", "chemistry", "mathematics", "biology"],
                "weights": {"mathematics": 0.30, "physics": 0.25, "chemistry": 0.25, "biology": 0.20},
                "exams": ["selectividad_science"],
            },
            "health": {
                "title": "Health Sciences", "title_local": "Ciencias de la Salud",
                "description": "Medicine / Nursing", "icon": "🏥",
                "subjects": ["biology", "chemistry", "mathematics"],
                "weights": {"biology": 0.40, "chemistry": 0.35, "mathematics": 0.25},
                "exams": ["selectividad_health"],
            },
        },
        "universities": {
            "selectividad_science": {"name": "Selectividad (Science)", "name_local": "Selectividad Ciencias", "track": "science", "city": "Nationwide"},
            "selectividad_health": {"name": "Selectividad (Health)", "name_local": "Selectividad Salud", "track": "health", "city": "Nationwide"},
        },
        "subjects": {
            "physics": {"title": "Physics", "title_local": "Física", "icon": "⚛️"},
            "chemistry": {"title": "Chemistry", "title_local": "Química", "icon": "⚗️"},
            "biology": {"title": "Biology", "title_local": "Biología", "icon": "🧬"},
            "mathematics": {"title": "Mathematics", "title_local": "Matemáticas", "icon": "📐"},
        },
    },
    "gb": {
        "id": "gb",
        "name": "United Kingdom",
        "name_local": "United Kingdom",
        "grade_level": "A-Levels / Year 12-13",
        "grade_level_local": "A-Levels",
        "language": "en",
        "tracks": {
            "stem": {
                "title": "STEM", "title_local": "STEM",
                "description": "Engineering, Medicine, Sciences", "icon": "🔬",
                "subjects": ["physics", "chemistry", "mathematics", "biology"],
                "weights": {"mathematics": 0.25, "physics": 0.25, "chemistry": 0.25, "biology": 0.25},
                "exams": ["a_levels"],
            },
            "medical": {
                "title": "Medicine", "title_local": "Medicine",
                "description": "UCAT / BMAT", "icon": "🏥",
                "subjects": ["biology", "chemistry", "mathematics"],
                "weights": {"biology": 0.40, "chemistry": 0.35, "mathematics": 0.25},
                "exams": ["ucat", "bmat"],
            },
        },
        "universities": {
            "a_levels": {"name": "A-Level Exams", "name_local": "A-Levels", "track": "stem", "city": "Nationwide"},
            "ucat": {"name": "UCAT", "name_local": "UCAT", "track": "medical", "city": "Nationwide"},
            "bmat": {"name": "BMAT", "name_local": "BMAT", "track": "medical", "city": "Nationwide"},
        },
        "subjects": {
            "physics": {"title": "Physics", "title_local": "Physics", "icon": "⚛️"},
            "chemistry": {"title": "Chemistry", "title_local": "Chemistry", "icon": "⚗️"},
            "biology": {"title": "Biology", "title_local": "Biology", "icon": "🧬"},
            "mathematics": {"title": "Mathematics", "title_local": "Mathematics", "icon": "📐"},
        },
    },
    "idn": {
        "id": "idn",
        "name": "Indonesia",
        "name_local": "Indonesia",
        "grade_level": "SMA (Kelas 10-12)",
        "grade_level_local": "SMA Kelas 10-12",
        "language": "id",
        "tracks": {
            "science": {
                "title": "Science", "title_local": "IPA (Ilmu Pengetahuan Alam)",
                "description": "SNBT / UTBK", "icon": "🔬",
                "subjects": ["physics", "chemistry", "biology", "mathematics"],
                "weights": {"mathematics": 0.30, "physics": 0.25, "chemistry": 0.25, "biology": 0.20},
                "exams": ["snbt_saintek"],
            },
            "medical": {
                "title": "Medical", "title_local": "Kedokteran",
                "description": "FK / FKG admission", "icon": "🏥",
                "subjects": ["biology", "chemistry", "physics"],
                "weights": {"biology": 0.40, "chemistry": 0.35, "physics": 0.25},
                "exams": ["snbt_medical"],
            },
        },
        "universities": {
            "snbt_saintek": {"name": "SNBT Saintek", "name_local": "SNBT Saintek", "track": "science", "city": "Nationwide"},
            "snbt_medical": {"name": "Medical Faculty", "name_local": "FK / FKG", "track": "medical", "city": "Nationwide"},
        },
        "subjects": {
            "physics": {"title": "Physics", "title_local": "Fisika", "icon": "⚛️"},
            "chemistry": {"title": "Chemistry", "title_local": "Kimia", "icon": "⚗️"},
            "biology": {"title": "Biology", "title_local": "Biologi", "icon": "🧬"},
            "mathematics": {"title": "Mathematics", "title_local": "Matematika", "icon": "📐"},
        },
    },
    "my": {
        "id": "my",
        "name": "Malaysia",
        "name_local": "Malaysia",
        "grade_level": "STPM / Matriculation",
        "grade_level_local": "STPM / Matrikulasi",
        "language": "ms",
        "tracks": {
            "science": {
                "title": "Science Stream", "title_local": "Aliran Sains",
                "description": "STPM / Matrikulasi Science", "icon": "🔬",
                "subjects": ["physics", "chemistry", "biology", "mathematics"],
                "weights": {"mathematics": 0.25, "physics": 0.25, "chemistry": 0.25, "biology": 0.25},
                "exams": ["stpm_science"],
            },
            "engineering": {
                "title": "Engineering", "title_local": "Kejuruteraan",
                "description": "UTM, USM, UKM Engineering", "icon": "⚙️",
                "subjects": ["physics", "chemistry", "mathematics"],
                "weights": {"mathematics": 0.35, "physics": 0.35, "chemistry": 0.30},
                "exams": ["stpm_engineering"],
            },
        },
        "universities": {
            "stpm_science": {"name": "STPM (Science)", "name_local": "STPM Sains", "track": "science", "city": "Nationwide"},
            "stpm_engineering": {"name": "STPM (Engineering)", "name_local": "STPM Kejuruteraan", "track": "engineering", "city": "Nationwide"},
        },
        "subjects": {
            "physics": {"title": "Physics", "title_local": "Fizik", "icon": "⚛️"},
            "chemistry": {"title": "Chemistry", "title_local": "Kimia", "icon": "⚗️"},
            "biology": {"title": "Biology", "title_local": "Biologi", "icon": "🧬"},
            "mathematics": {"title": "Mathematics", "title_local": "Matematik", "icon": "📐"},
        },
    },
    "ng": {
        "id": "ng",
        "name": "Nigeria",
        "name_local": "Nigeria",
        "grade_level": "Senior Secondary (SS1-SS3)",
        "grade_level_local": "Senior Secondary",
        "language": "en",
        "tracks": {
            "science": {
                "title": "Science", "title_local": "Science",
                "description": "JAMB / WAEC / NECO", "icon": "🔬",
                "subjects": ["physics", "chemistry", "biology", "mathematics"],
                "weights": {"mathematics": 0.25, "physics": 0.25, "chemistry": 0.25, "biology": 0.25},
                "exams": ["jamb_science"],
            },
            "engineering": {
                "title": "Engineering", "title_local": "Engineering",
                "description": "UNILAG, UI, OAU Engineering", "icon": "⚙️",
                "subjects": ["physics", "chemistry", "mathematics"],
                "weights": {"physics": 0.35, "mathematics": 0.35, "chemistry": 0.30},
                "exams": ["jamb_engineering"],
            },
            "medical": {
                "title": "Medical", "title_local": "Medicine",
                "description": "MBBS / BDS admission", "icon": "🏥",
                "subjects": ["biology", "chemistry", "physics"],
                "weights": {"biology": 0.40, "chemistry": 0.35, "physics": 0.25},
                "exams": ["jamb_medical"],
            },
        },
        "universities": {
            "jamb_science": {"name": "JAMB (Sciences)", "name_local": "JAMB Sciences", "track": "science", "city": "Nationwide"},
            "jamb_engineering": {"name": "JAMB (Engineering)", "name_local": "JAMB Engineering", "track": "engineering", "city": "Nationwide"},
            "jamb_medical": {"name": "JAMB (Medical)", "name_local": "JAMB Medical", "track": "medical", "city": "Nationwide"},
        },
        "subjects": {
            "physics": {"title": "Physics", "title_local": "Physics", "icon": "⚛️"},
            "chemistry": {"title": "Chemistry", "title_local": "Chemistry", "icon": "⚗️"},
            "biology": {"title": "Biology", "title_local": "Biology", "icon": "🧬"},
            "mathematics": {"title": "Mathematics", "title_local": "Mathematics", "icon": "📐"},
        },
    },
}

DEFAULT_REGION = "bd"


def get_region(region_id: str | None = None) -> dict:
    return REGIONS.get(region_id or DEFAULT_REGION, REGIONS[DEFAULT_REGION])


def get_all_regions() -> dict[str, dict]:
    return {
        rid: {"id": r["id"], "name": r["name"], "name_local": r["name_local"], "language": r["language"]}
        for rid, r in REGIONS.items()
    }


def get_languages() -> dict:
    return LANGUAGES
