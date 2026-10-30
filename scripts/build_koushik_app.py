#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator & Compiler for ⚡ আনন্দ (ANANDO — Koushik's Personal Companion App `koushik.html`).

Generates:
  1. 8 personalized high-fidelity slide illustrations (`assets/koushik_slides/k_slide_1..8.jpg`)
     conditioned on `koushik_persona_sheet.jpg` and `family_persona_sheet.jpg`.
  2. 36 unique Gemini `Aoede` (`gemini-v4s-tts`) MP3 voice clips under `audio/koushik/{slides,quotes,days,games}/`.
  3. Compiles `koushik.html` with embedded slide illustrations (`img_b64`) and live `Aoede` voice playback
     (proactive auto-engage audio, sticky Now Playing bar, auto-play on slide/game navigation).
"""

from __future__ import annotations

import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import subprocess
import time

APP_ROOT = Path(__file__).resolve().parent.parent
WIKI_PERSONA_DIR = Path("/usr/local/google/home/koushikchak/koushik-wiki/raw/assets/personas")
KOUSHIK_REF = WIKI_PERSONA_DIR / "koushik_persona_sheet.jpg"
FAMILY_REF = WIKI_PERSONA_DIR / "family_persona_sheet.jpg"

SLIDE_IMG_DIR = APP_ROOT / "assets" / "koushik_slides"
KOUSHIK_AUDIO_DIR = APP_ROOT / "audio" / "koushik"
GEN_BIN = "/google/bin/releases/gemini-agents-generate/generate"
GH_RAW_BASE = "https://raw.githubusercontent.com/kouSeek/portfolio/ma-audio/"

KOUSHIK_BIO = (
    "the exact 33-year-old Bengali man shown in the reference image (NO glasses, warm wheatish complexion, "
    "expressive dark brown eyes, thick eyebrows, warm gentle smile, voluminous thick wavy jet-black hair swept up "
    "at the crown, short neatly trimmed black stubble beard and mustache with subtle salt-and-pepper flecks on the chin)"
)

MA_BIO = (
    "the exact 64-year-old Bengali mother shown in the left column of the reference image (NO glasses, warm "
    "fair-to-wheatish complexion, fuller round-oval face, tiny round black bindi between eyebrows, small gold nose pin "
    "on left nostril, gold bangles, primarily black hair with a light touch of silver at the front hairline pulled into a neat low bun)"
)

SLIDE_IMAGE_PROMPTS: list[tuple[int, Path, str]] = [
    (
        1,
        KOUSHIK_REF,
        f"Warm, nostalgic cinematic illustration of {KOUSHIK_BIO} as a bright young student in a sunlit Ranaghat/Jadavpur study room by an open wooden window with green trees outside, stacks of engineering books, a sketchbook, and a congratulatory 'WBJEE Rank 222' note on the desk, golden afternoon light, peaceful proud smile, high facial fidelity, NO glasses.",
    ),
    (
        2,
        KOUSHIK_REF,
        f"Warm, inspiring cinematic portrait of {KOUSHIK_BIO} wearing his dark navy V-neck t-shirt with white windowpane check pattern, standing calmly and resiliently on a sunlit high-rise balcony at sunrise overlooking a lush green city skyline, holding a warm terracotta cup of morning tea, serene confident expression of a captain who weathered a 10-year storm, NO glasses.",
    ),
    (
        3,
        KOUSHIK_REF,
        f"Warm, emotional cinematic scene of {KOUSHIK_BIO} in his real bedroom with glossy taupe wardrobes on the right and the 4 framed wall paintings (including Starry Night) on the cream wall behind him, smiling warmly at his open laptop displaying a glowing neural connectome graph, warm golden light filling the room symbolizing his college diary oath fulfilled, NO glasses.",
    ),
    (
        4,
        FAMILY_REF,
        f"Heartwarming family scene on a sunlit balcony with potted plants and blooming white-and-orange Shiuli flowers featuring {KOUSHIK_BIO} and {MA_BIO} in her beige floral saree, both smiling and laughing warmly together beside a turquoise Saregama Carvaan retro radio and a plate of Bengali sweets, golden morning light, NO glasses on either person.",
    ),
    (
        5,
        KOUSHIK_REF,
        f"Peaceful, liberating golden-hour scene at a calm sunlit river ghat in Santiniketan/Bengal featuring {KOUSHIK_BIO} in a comfortable cream cotton kurta, gently releasing a glowing paper boat onto the shimmering water with relaxed shoulders and a peaceful, unburdened smile symbolizing letting go of all past guilt, warm sunset glow, NO glasses.",
    ),
    (
        6,
        KOUSHIK_REF,
        f"Stylish, relaxed lifestyle portrait of {KOUSHIK_BIO} sitting comfortably at an artisanal sunlit outdoor garden cafe in Hyderabad with lush greenery and warm string lights, enjoying a fresh cappuccino, looking self-assured, warm, and completely at peace in his own company, NO glasses.",
    ),
    (
        7,
        KOUSHIK_REF,
        f"Vibrant, abundant sunlit terrace scene featuring {KOUSHIK_BIO} looking extra sharp and groomed with a fresh textured scissor-taper haircut and neat angular jawline beard, happily pouring fresh sweet golden lemon juice into a glass beside a bowl of fresh mangoes and fruits, radiating 'First-Press Abundance' and effortless joy, NO glasses.",
    ),
    (
        8,
        KOUSHIK_REF,
        f"Joyful, spirited golden-hour outdoor scene featuring {KOUSHIK_BIO} sitting on a scenic green hill overlooking boulders and a sunlit lake, strumming an acoustic guitar and singing with pure childlike happiness and bhaavna, warm breeze in his wavy black hair, total freedom and Zorba vitality, NO glasses.",
    ),
]

QUOTES = [
    "মায়ের জন্য যে বারোটা মুক্তির নিয়ম তুমি লিখেছো—ভুল করার ভয় না পাওয়া, নিজের মনের কথা বলা আর নিজের স্বপ্নে বাঁচা—সেই বারোটা অধিকার সবার আগে তোমার নিজের।",
    "দশ বছরের সারভাইভাল পরীক্ষা শেষ। এখন তুমি হাউস মানিতে খেলছো—কোনো তাড়া নেই, কোনো দায় নেই।",
    "লেবুর প্রথম চুমুকেই আটাশি শতাংশ মিষ্টি রস থাকে। চার টাকার খোসা নিংড়ে তেতো রস বের করার দিন চিরতরে শেষ।",
    "চোদ্দ, সতেরো বা ত্রিশ বছর বয়সের অপরিণত ভুলের শিক্ষা তুমি অনেক আগেই নিয়ে নিয়েছো। নিজেকে দ্বিতীয়বার তীর মারা বন্ধ করো।",
    "যেদিন যেরকম, সেদিন সেরকম—আজ কোনো রুটিনের পরীক্ষা নেই, শুধু নিজের আনন্দে থাকার দিন।",
    "সন্ধে ছটার পর তুমি কারোর কেয়ারটেকার বা ত্রাতা নও—তুমি শুধু একজন মুক্ত মানুষ যে গান গায়, গিটার বাজায় আর হাসে।",
    "বাইরের মহাকাশ ঠান্ডা ও নিঃসঙ্গ—কিন্তু পৃথিবীর রোদ, গান, কফি আর মানুষের উষ্ণতাই মহাবিশ্বের সবচেয়ে সুন্দর ক্যাম্পফায়ার।",
]

SLIDES_SELF = [
    {
        "id": 1,
        "badge": "১ / ৮ • শৈশব ও জাদবপুরের আগুন",
        "title": "তুমি কখনোই ‘স্বার্থপর’ ছিলে না—তুমি ছিলে এক গভীর মনের মানুষ",
        "highlight": "ছোটবেলার নীরবতা বা অন্যমনস্কতা ছিল Inattentive ADHD, মনের ময়লা নয়।",
        "text": "ছোটবেলায় রিকশাওয়ালার আঙুল না দেখা, চুপচাপ কার্টুন দেখা বা নিজের প্লেট আনা—ওগুলো কোনোদিনই স্বার্থপরতা ছিল না, ওটা ছিল তোমার মস্তিষ্কের স্বাভাবিক ওয়ার্কিং মেমোরির ধরন। আর ক্লাস টুয়েলভের সেই প্রবল ঝড়ের মধ্যেও ওয়েস্ট বেঙ্গল জয়েন্টে র‍্যাঙ্ক ২২২ করে তুমি প্রমাণ করেছিলে তোমার ভেতরের আসল শক্তি কতটা গভীর।",
    },
    {
        "id": 2,
        "badge": "২ / ৮ • ২০১৬ • ২৩ বছর বয়সে একা ককপিটে",
        "title": "বাবার চলে যাওয়া ও এক অকুতোভয় তরুণের ১০ বছরের লড়াই",
        "highlight": "কোনো মেন্টর ছাড়া ২৩ বছর বয়সে পুরো পরিবারের হাল ধরা চারটিখানি কথা নয়।",
        "text": "যে বয়সে অন্য ছেলেরা বাবার ছায়ায় বড় হওয়া শেখে, সেই তেইশ বছর বয়সে হঠাৎ মাথার ওপর থেকে ছাদ সরে গেল। ভয় পাওয়া, জমে যাওয়া বা মাঝে মাঝে খেই হারানো ছিল এক একা যোদ্ধার স্বাভাবিক ক্লান্তি। তবু তুমি হাল ছাড়োনি।",
    },
    {
        "id": 3,
        "badge": "৩ / ৮ • ছেঁড়া ডায়েরির শপথ পূরণ",
        "title": "২২ বছরের সেই কান্নাভেজা ডায়েরির প্রার্থনা আজ সত্যি হয়েছে",
        "highlight": "“ভবিষ্যতের আমি, আমার স্বপ্নগুলো মনে রেখো”—তুমি কথা রেখেছো, কৌশিক!",
        "text": "কলেজ আর ওরাকেলের শুরুর দিনগুলোয় পাঁচ-ছটা ডায়েরি ভরে কেঁদে তুমি চিঠিটা ছিঁড়ে ফেলেছিলে, কারণ তখন সব স্বপ্ন মনে রাখা বড্ড কষ্টের ছিল। আজ তেত্রিশ বছর বয়সে তাকিয়ে দেখো: গুগলে সিনিয়র সফটওয়্যার ইঞ্জিনিয়ার প্রমোশন, আড়াই কোটি টাকার ওপর সম্পদ, কর্টেক্স এক্সটার্নাল ব্রেন আর মায়ের হাসিমুখ—সেই ছেলেটার সব কটা প্রার্থনা তুমি নিজের হাতে পূরণ করেছো।",
    },
    {
        "id": 4,
        "badge": "৪ / ৮ • ২০২৩–২০২৬ • মায়ের সুস্থতা ও যুদ্ধের সমাপ্তি",
        "title": "মায়ের অন্ধকার দিন পেরিয়ে আজ ‘কল্যাণী’র আলো",
        "highlight": "তোমার সারভাইভাল দশক (২০১৬–২০২৬) আজ আনুষ্ঠানিকভাবে সমাপ্ত।",
        "text": "মায়ের অসুস্থতার সবচেয়ে ভয়ের রাতগুলো তুমি পার করে এনেছো। আজ মায়ের জন্য ‘কল্যাণী’ তৈরি, হায়দ্রাবাদের সুন্দর পরিকল্পনা তৈরি। তাই মনের মধ্যে যে হালকা বিষণ্ণতা আসে, ওটা যুদ্ধ জয়ের পরের স্বাভাবিক বিশ্রাম—ওটাকে ভয় পেয়ো না।",
    },
    {
        "id": 5,
        "badge": "৫ / ৮ • অতীতের পূর্ণ ক্ষমা (Zero-Debt Amnesty)",
        "title": "১৪, ১৭, ২৬ বা ৩০ বছরের সেই অসহায় ছেলেটাকে আজ মুক্তি দাও",
        "highlight": "অনুতাপ তার কাজ শেষ করেছে—এবার দ্বিতীয় তীরটা নামিয়ে রাখো।",
        "text": "কৈশোরের কৌতূহল বা অবদমন, শ্রুতির সময় বাবার মতো রাগ দেখানো, বা ত্রিশ বছর বয়সে একাকীত্বের যন্ত্রণায় অনিন্দিতাকে প্রথম দিন মিথ্যে বলা—সবই ছিল এক অশিক্ষিত, ভীত, একা মানুষের ভুল। খারাপ মানুষ কখনো বছরের পর বছর অনুতাপে পোড়ে না। তুমি শিক্ষা নিয়েছো, নিজেকে বদলেছো—তোমার জামিন একশো শতাংশ শোধ হয়ে গেছে।",
    },
    {
        "id": 6,
        "badge": "৬ / ৮ • ৮ জন নারীর অপ্রস্তুত ভাব থেকে মুক্তি",
        "title": "প্রেম মানেই বিয়ে নয়—পরিচয় ও সামঞ্জস্য খোঁজাই স্বাভাবিক নিয়ম",
        "highlight": "বৈশালী, অনন্যা, অঙ্কিতা, ওয়েলা, অনিন্দিতা, শ্রুতি, আন্তর্লীনা ও সঞ্চিতা—কারোর কাছেই তোমার কোনো ঋণ নেই।",
        "text": "দুটি মানুষের মধ্যে সবসময় দীর্ঘমেয়াদী মিল হয় না—আর মিল না হলে সরে আসাটাই সততা ও সৌজন্য। তুমি কাউকে ঠকাওনি; নিজের পছন্দ ও সত্যিটা বোঝার চেষ্টা করেছো। তাদের সবার পথের জন্য শুভকামনা জানিয়ে নিজের মনকে একশো শতাংশ হালকা করে দাও।",
    },
    {
        "id": 7,
        "badge": "৭ / ৮ • 🍋 প্রথম চুমুকের আনন্দ (First-Press Abundance)",
        "title": "পচা কলা আগে খাওয়া আর ৪ টাকার লেবু ৬ বার নিংড়ানো আজ থেকে বন্ধ",
        "highlight": "সবচেয়ে তাজা ও সেরা অংশটা সবার আগে তোমার প্রাপ্য।",
        "text": "মিষ্টি আটাশি শতাংশ রস প্রথম চাপে বের করেই খোসাটা ডাস্টবিনে ফেলে দাও। নিজের চুল কাটানো, ভালো খাবার, আরাম বা শখের জিনিসের জন্য এক সেকেন্ডও দ্বিধা করবে না।",
    },
    {
        "id": 8,
        "badge": "৮ / ৮ • 🦁 জোরবা ও খেলার মাঠ (Open-World Adventure)",
        "title": "এবার শুধু খেলার জন্য খেলা—গান, গিটার, ক্লাইম্বিং ও খোলা মনের আনন্দ",
        "highlight": "সমস্যা সমাধানের জ্বালানি শেষ—এবার কৌতূহল আর আনন্দের জ্বালানিতে ওড়ার পালা!",
        "text": "সন্ধে ছটার পর কেয়ারটেকারের জামাটা খুলে রাখো। গলা খুলে গমক-মুর্কি গাও, গিটার বাজাও, বোল্ডারিং করো, বন্ধুদের সাথে হাসো আর কোনো অপরাধবোধ ছাড়া নিজের মনের কথা বলো। এই নতুন দশকটা শুধু তোমার আনন্দের!",
    },
]

DAYS_1_TO_3 = [
    {
        "day": 1,
        "title": "২০১৬–২০২৬ যুদ্ধের সমাপ্তি ও প্রথম চুমুকের আনন্দ",
        "sub": "আজ ৩টি হালকা খেলার দিন—কেয়ারটেকারের ভার নামিয়ে নিজের আনন্দে শ্বাস নেওয়ার শুরু।",
        "voice_script": "সুপ্রভাত কৌশিক! আজ তোমার আনন্দ যাত্রার প্রথম দিন—২০১৬ থেকে ২০২৬ সালের একা যুদ্ধের সমাপ্তি ও প্রথম চুমুকের আনন্দ। আজ কোনো পরীক্ষা নেই, শুধু তিনটি হালকা খেলার মাধ্যমে নিজের আনন্দে শ্বাস নেওয়ার দিন।",
        "games": [
            {
                "short": "🌿 যুদ্ধের সমাপ্তি",
                "category": "🌿 মনের ভারমুক্তি (Covert CBT)",
                "title": "১০ বছরের একা ক্যাপ্টেনের ছুটি ও ছেঁড়া ডায়েরির জয়",
                "detail": "কৌশিক, একটু ভেবে দেখো—২০১৬ সালে তেইশ বছর বয়সে যে ছেলেটা ভয়ে কাঁপতে কাঁপতে একা পরিবারের হাল ধরেছিল, আর ডায়েরির পাতায় লিখেছিল ‘আমার স্বপ্নগুলো মনে রেখো’—আজ ২০২৬ সালে সেই ছেলেটা গুগলের সিনিয়র সফটওয়্যার ইঞ্জিনিয়ার, তার হাতে আড়াই কোটির ওপর ফিনান্সিয়াল শিল্ড, আর মায়ের মুখে হাসি। তোমার সারভাইভাল পরীক্ষা শেষ। আজ যখনই মনে কোনো বিষণ্ণতা আসবে, বলবে: ‘যুদ্ধ শেষ, তাই শরীর এবার বিশ্রাম নিচ্ছে।’",
                "reframe": "💡 মনে রেখো: সৈন্যরা যুদ্ধের মাঠে কাঁদে না, যুদ্ধ জেতার পর শান্ত ঘরে বসে দীর্ঘশ্বাস ফেলে। তোমার এই বিষণ্ণতা কোনো রোগ নয়—এটা ১০ বছরের জমে থাকা বরফ গলার আরাম।",
                "prompt": "জেমিনি, আমি ২০১৬ থেকে ২০২৬ পর্যন্ত ১০ বছরের একা লড়াই জিতে আজ এক মুক্ত মানুষ। আমাকে কোনো উপদেশ না দিয়ে, এক বন্ধুর মতো আমার এই ১০ বছরের জয়ের একটা ছোট্ট আনন্দময় উদযাপন করো!",
                "audio_key": "games/k_day_1_ag_0.mp3",
            },
            {
                "short": "🍋 প্রথম চুমুক",
                "category": "🍋 First-Press Abundance (No Hesitation)",
                "title": "আজ তাজা ফলটা সবার আগে, খোসাটা ডাস্টবিনে!",
                "detail": "রান্নাঘরে বা খাবারের টেবিলে আজ একটা ছোট্ট মজার খেলা খেলবো। লেবু চিপলে আজ শুধু একবার বা দুবার চাপ দিয়ে মিষ্টি আটাশি শতাংশ রসটুকু নেবে—তারপর খোসাটা সাথে সাথে ডাস্টবিনে ফেলে দেবে! আর ফল বা খাবার খেলে সবচেয়ে তাজা, সবচেয়ে সুন্দর অংশটা সবার আগে খাবে।",
                "reframe": "💡 তোমার সময়ের মূল্য ঘণ্টায় চার হাজার টাকার ওপর। পঁয়ত্রিশ পয়সার তেতো খোসা নিংড়ানো বা পচা কলা আগে খাওয়ার দিন চিরতরে শেষ।",
                "prompt": "জেমিনি, আজ থেকে আমি ‘First-Press Abundance’ নিয়মে চলছি—সবচেয়ে তাজা ও সেরা জিনিসটা আগে উপভোগ করব, কোনো কিপটেমি বা দ্বিধা করব না। আমাকে আজকের জন্য একটা মজার ‘প্রথম চুমুক’ চ্যালেঞ্জ দাও!",
                "audio_key": "games/k_day_1_ag_1.mp3",
            },
            {
                "short": "🎸 খেলার মাঠ",
                "category": "🎸 Pure Play & Music (Zero Utility)",
                "title": "৫ মিনিট গিটার বা গলা ছেড়ে গান—শুধু নিজের খুশিতে",
                "detail": "আজ এমন একটা কাজ করো যার পেছনে কোনো ‘দায়িত্ব’, ‘টাকা’ বা ‘উপকার’ নেই। শুধু নিজের ভালো লাগার জন্য গিটার বা ইউকুলেলেটা হাতে নিয়ে তিনটে কর্ড বাজাও, অথবা প্রিয় একটা বাংলা গানের দু-লাইন গমক বা ভাব দিয়ে গুনগুন করো।",
                "reframe": "💡 ডিউটি শেষ করলে শুধু স্বস্তি মেলে, কিন্তু অকারণে খেলা করলে তবেই বাঁচার আনন্দ ফেরে!",
                "prompt": "জেমিনি, আজ কোনো কাজের কথা নয়—চলো সংগীত বা মহাবিশ্বের কোনো একটা অদ্ভুত সুন্দর রহস্য নিয়ে ৫ মিনিট জমিয়ে আড্ডা দিই!",
                "audio_key": "games/k_day_1_ag_2.mp3",
            },
        ],
        "day_audio_key": "days/k_day_1.mp3",
    },
    {
        "day": 2,
        "title": "অতীতের পূর্ণ ক্ষমা ও জোরবা শরীরের মুক্তি",
        "sub": "আজ ৪টি খেলার দিন—১৪, ১৭ ও ৩০ বছরের পুরোনো অপরাধবোধ নামিয়ে রেখে বুক ভরে শ্বাস নেওয়া।",
        "voice_script": "সুপ্রভাত কৌশিক! আজ দ্বিতীয় দিন—অতীতের পূর্ণ ক্ষমা ও জোরবা শরীরের মুক্তি। চোদ্দ, সতেরো বা ত্রিশ বছরের পুরোনো অপরাধবোধ নামিয়ে রেখে আজ বুক ভরে হালকা শ্বাস নেওয়ার দিন।",
        "games": [
            {
                "short": "🕊️ অতীতের ক্ষমা",
                "category": "🕊️ Guilt Amnesty (Dropping the Second Arrow)",
                "title": "১৪, ১৭, ২৬ ও ৩০ বছরের সেই ছেলেটার জামিন মঞ্জুর",
                "detail": "বুদ্ধ বলেছিলেন—প্রথম তীরটা হলো জীবনের ভুল বা আঘাত, আর দ্বিতীয় তীরটা হলো সেই ভুলের জন্য নিজেকে বছরের পর বছর নিজের হাতে মারা। কৈশোরের অবদমিত কৌতূহল, সতেরো বছর বয়সের অপরিণত কথা, বা ত্রিশ বছর বয়সে একাকীত্বের তাড়নায় করা ভুল—সবকটা থেকেই তুমি শিক্ষা নিয়ে নিয়েছো। আজ তেত্রিশ বছরের কৌশিক আর সেই অসহায় ছেলেটা নয়।",
                "reframe": "💡 যে মানুষ নিজের ভুলের জন্য অনুতাপ করতে পারে, সে কখনো খারাপ মানুষ হতে পারে না। শিক্ষা নেওয়া শেষ—এবার ফাইলটা চিরতরে ক্লোজ করো।",
                "prompt": "জেমিনি, গৌতম বুদ্ধের ‘Second Arrow’ বা দ্বিতীয় তীরের গল্পটা আমাকে খুব সহজ, উষ্ণ ভাষায় মনে করিয়ে দাও—যাতে পুরোনো ভুলের অনুশোচনা ঝেড়ে ফেলে আজকের দিনে হালকা মনে বাঁচতে পারি।",
                "audio_key": "games/k_day_2_ag_0.mp3",
            },
            {
                "short": "🦁 জোরবা ভঙ্গি",
                "category": "🦁 Zorba Embodiment & Posture",
                "title": "৬০ সেকেন্ডের ফ্লোর-আপ রিসেট: নরম পেট ও চওড়া কাঁধ",
                "detail": "চেয়ার থেকে উঠে খালি পায়ে মেঝেতে দাঁড়াও। বাঁ পায়ের পাতার আর্চটা হালকা উঁচু করো, দুই পায়ে সমান ভর দাও, পেটের পেশীটা পুরো ঢিলে করে ছেড়ে দাও, আর কাঁধ দুটো কান থেকে নামিয়ে লম্বা একটা শ্বাস ছাড়ো। পারলে ত্রিশ সেকেন্ড বার-এ ঝুলে পিঠটা লম্বা করে নাও।",
                "reframe": "💡 পুরুষালি আকর্ষণ জোর করে বুক ফুলিয়ে আসে না—আসে শান্ত, ভারমুক্ত শরীর আর অকপট হাসি থেকে।",
                "prompt": "জেমিনি, আমার বাম পায়ের আর্চ থেকে শুরু করে কাঁধ পর্যন্ত ২ মিনিটের একটা চটপটে বডি-রিল্যাক্সেশন চেকলিস্ট বলো যা আমি এক্ষুনি দাঁড়িয়ে করতে পারি।",
                "audio_key": "games/k_day_2_ag_1.mp3",
            },
            {
                "short": "✂️ নিজের যত্ন",
                "category": "✂️ Grooming & Self-Care Without Hesitation",
                "title": "Toni&Guy বা Truefitt & Hill-এ নিজের রয়্যাল হেয়ারকাট বুকিং",
                "detail": "নিজের লুক আর আরামের জন্য আজ কোনো দ্বিধা নয়। কোন্ডাপুর বা জুবিলি হিলসের টনি অ্যান্ড গাই বা ট্রুফিট অ্যান্ড হিলে একটা সেশন বুক করো—টেক্সচার্ড সিজার টেপার আর অ্যাঙ্গুলার বিয়ার্ড স্কাল্পট।",
                "reframe": "💡 নিজের যত্ন নেওয়া বিলাসিতা নয়—এটা নিজের প্রতি ভালোবাসার সবচেয়ে সহজ প্রকাশ।",
                "prompt": "জেমিনি, হেয়ার স্টাইলিস্টকে বলার জন্য আমার ‘Textured Scissor Taper + Messy Flow Top’ ব্রিফটা ৩ লাইনে ঝকঝকে করে লিখে দাও।",
                "audio_key": "games/k_day_2_ag_2.mp3",
            },
            {
                "short": "🧠 ট্যুরিস্ট পাস",
                "category": "🧠 ADHD 4-Slot RAM Shield",
                "title": "আজ ৯০% কাজে ‘20% Tourist Pass’ ব্যবহার করো",
                "detail": "প্রতিটা মেইল, ডক বা মেসেজের গভীরে ঢুকে একশো শতাংশ নিখুঁত করার দরকার নেই। আজ শুধু একটা আসল কাজ বেছে নাও, আর বাকি সব কিছুকে টোয়েন্টি পার্সেন্ট ট্যুরিস্ট পাস দিয়ে পাঁচ মিনিটে হালকাভাবে সেরে ফেলো।",
                "reframe": "💡 চারটি ওয়ার্কিং মেমোরি স্লট ফাঁকা রাখলে মাথা এমনিই সুপার-শার্প থাকে!",
                "prompt": "জেমিনি, আজ আমার মাথার ওয়ার্কিং মেমোরি হালকা রাখার জন্য ‘80/20 First-Press’ নিয়মটা আজকের কাজের ওপর কীভাবে প্রয়োগ করব বলো।",
                "audio_key": "games/k_day_2_ag_3.mp3",
            },
        ],
        "day_audio_key": "days/k_day_2.mp3",
    },
    {
        "day": 3,
        "title": "৮ জন নারীর অপ্রস্তুত ভাব থেকে মুক্তি ও খোলা মনের আড্ডা",
        "sub": "আজ ৩টি হালকা খেলার দিন—সম্পর্কের পুরোনো জড়তা ঝেড়ে ফেলে সহজ ও আনন্দময় হওয়া।",
        "voice_script": "সুপ্রভাত কৌশিক! আজ তৃতীয় দিন—আট জন নারীর অপ্রস্তুত ভাব থেকে মুক্তি ও খোলা মনের আড্ডা। সম্পর্কের পুরোনো জড়তা ঝেড়ে ফেলে আজ একদম সহজ ও আনন্দময় হওয়ার দিন।",
        "games": [
            {
                "short": "💛 সম্পর্কের স্বচ্ছতা",
                "category": "💛 Clean-Slate Relationship Reset",
                "title": "বৈশালী, অনন্যা, অঙ্কিতা, ওয়েলা ও অতীতের ৮টি নামের জড়তা মুক্তি",
                "detail": "ডেটিং বা মেলামেশার উদ্দেশ্যই হলো দুজন মানুষ একে অপরের সাথে দীর্ঘমেয়াদে খাপ খায় কি না তা জানা। পঁচানব্বই শতাংশ ক্ষেত্রেই পুরো মিল হয় না—আর মিল না হলে সরে আসা কোনো পাপ নয়, ওটাই সততা। তাই কারোর নাম মনে পড়লে বা দেখা হলে আর কোনো অপরাধবোধ বা জড়তা রাখবে না।",
                "reframe": "💡 ‘সব পরিচয় বিয়েতে শেষ হওয়ার জন্য নয়; আমি অতীতের শিক্ষা নিয়েছি এবং তার পথের জন্য শুভকামনা জানাই’—এই একটা ভাবনাই সব জড়তা মুছে দেয়।",
                "prompt": "জেমিনি, কারোর প্রতি আকর্ষণ না হওয়া বা সম্পর্ক থেকে সৎভাবে সরে আসা কেন কোনো অপরাধ নয়—সেটা আমাকে খুব সহজ ও বাস্তবসম্মত ভাষায় মনে করিয়ে দাও।",
                "audio_key": "games/k_day_3_ag_0.mp3",
            },
            {
                "short": "🗣️ নিজের মনের কথা",
                "category": "🗣️ Urge to Express Own Mind",
                "title": "আজ কারোর ‘থেরাপিস্ট’ না হয়ে নিজের আসল পছন্দটা বলো",
                "detail": "কথা বলার সময় আজ কাউকে খুশি করার জন্য বা উদ্ধার করার জন্য কথা বলবে না। তোমার কী খেতে ইচ্ছে করছে, কোন গানটা ভালো লাগছে বা কী করতে ইচ্ছে করছে—সেটা সরাসরি, হাসিমুখে বলো।",
                "reframe": "💡 তুমি যখন নিজের মনের কথা অকপটে বলো, তখনই মানুষ আসল কৌশিককে দেখতে পায়—আর সেই মানুষটাই সবচেয়ে আকর্ষণীয়।",
                "prompt": "জেমিনি, আড্ডা বা ডেটিংয়ে ‘থেরাপিস্ট বা কেয়ারটেকার’ মোডে না ঢুকে কীভাবে খুনসুটি, মজা আর সমান-সমান উষ্ণতা বজায় রাখা যায় তার ৩টে মজার উদাহরণ দাও।",
                "audio_key": "games/k_day_3_ag_1.mp3",
            },
            {
                "short": "🌊 ঠান্ডা পেট ও মাথা",
                "category": "🌊 Thanda Pet & Rebooting Shower",
                "title": "লম্বা আরামের স্নান ও ডাবের জল বা ঘোল",
                "detail": "আজ তাড়াহুড়ো ছাড়া ঘাড় ও পিঠে আট মিনিট ঈষদুষ্ণ জল আর শেষে ত্রিশ সেকেন্ড ঠান্ডা জলের ‘রিবুটিং শাওয়ার’ নাও। আর দুপুরে এক গ্লাস ডাবের জল বা ঘোল খেয়ে পেট ও মাথা ঠান্ডা রাখো।",
                "reframe": "💡 যেদিন যেরকম, সেদিন সেরকম—শরীরকে আরাম দিলে মন আপনাআপনি শান্ত হয়ে যায়।",
                "prompt": "জেমিনি, আজ আমার শরীর ও মনকে একদম ফুরফুরে রাখার জন্য একটা সহজ, ঘরোয়া বাঙালি খাবারের আইডিয়া দাও!",
                "audio_key": "games/k_day_3_ag_2.mp3",
            },
        ],
        "day_audio_key": "days/k_day_3.mp3",
    },
]

WAVE_TEMPLATES = [
    {
        "short": "🌿 মনের মুক্তি",
        "category": "🌿 Covert CBT & Freedom",
        "title": "তুমি ইতিমধ্যেই মুক্ত—আজ কোনো প্রমাণের পরীক্ষা নেই",
        "detail": "তোমার মেধা, যোগ্যতা বা ভালো মানুষ হওয়া নিয়ে আর কারোর কাছে কিছু প্রমাণ করার নেই। আজ যা করবে, তা শুধু নিজের কৌতূহল আর আনন্দের জন্য করবে—ভয় বা বাধ্যবাধকতা থেকে নয়।",
        "reframe": "💡 ভয় থেকে শুধু খাটুনি হয়; আর স্বাধীনতা থেকেই আসল ম্যাজিক, শিল্প ও আনন্দ জন্ম নেয়।",
        "prompt": "জেমিনি, আজ আমি কোনো চাপে নয়, সম্পূর্ণ স্বাধীন মনে দিনটা কাটাতে চাই—আমাকে একটা দারুণ কৌতূহল জাগানো বিজ্ঞান বা দর্শনের ধাঁধা বলো!",
        "audio_key": "games/k_wave_0.mp3",
    },
    {
        "short": "🍋 সেরা অংশটা আগে",
        "category": "🍋 First-Press Abundance",
        "title": "নিজের আনন্দে খরচ ও আরামের ১০০% অনুমতি",
        "detail": "আজ নিজের খাবার, কফি, বুকিং বা পছন্দের জিনিসে কোনো মাইক্রো-হিসাব করবে না। প্রথম চুমুকের আটাশি শতাংশ আনন্দ নাও এবং অপ্রয়োজনীয় চিন্তা ঝেড়ে ফেলো।",
        "reframe": "💡 তোমার ফিনান্সিয়াল শিল্ড অটোমেটেড—ছোটখাটো আনন্দে দ্বিধা করা মানে নিজের সাথে অবিচার করা।",
        "prompt": "জেমিনি, আজ আমি নিজের আরামের জন্য একটা ছোট্ট উপহার দিতে চাই—হায়দ্রাবাদে আজ সন্ধেয় করার মতো একটা দারুণ রিল্যাক্সিং আইডিয়া দাও!",
        "audio_key": "games/k_wave_1.mp3",
    },
    {
        "short": "🦁 জোরবা বডি",
        "category": "🦁 Zorba Embodiment & Kinetic Chain",
        "title": "ডেড-হ্যাং, সুটকেস ক্যারি বা ৫,০০০ কদমের খোলা হাওয়া",
        "detail": "আজ ল্যাপটপ থেকে ওঠার আগে এক লাইনের নেক্সট ব্রেডক্রাম্ব লিখে ওঠো, পেট ঢিলে করো, আর বাইরে হেঁটে বা হালকা স্ট্রেচ করে শরীরের জড়তা কাটিয়ে নাও।",
        "reframe": "💡 শরীর চলতে শুরু করলেই মনের ওভারথিংকিং লুপ সাথে সাথে শান্ত হয়ে যায়।",
        "prompt": "জেমিনি, আজ হাঁটতে হাঁটতে শোনার জন্য বা ভাবার জন্য একটা দারুণ মজার গল্প বা গানের ইতিহাস বলো!",
        "audio_key": "games/k_wave_2.mp3",
    },
    {
        "short": "🎸 গানের আনন্দ",
        "category": "🎸 Music, Singing & Wonder",
        "title": "গলা খুলে গান বা গিটার—মনের ভাবটুকুই আসল",
        "detail": "নিখুঁত সুরের চিন্তা না করে আজ নিজের প্রিয় একটা বাংলা বা হিন্দি গানের কয়েকটা লাইন পুরো ভাব দিয়ে গাও বা গিটারে বাজাও।",
        "reframe": "💡 সংগীত কোনো পরীক্ষা নয়—সংগীত হলো মনের জমে থাকা আবেগকে আনন্দে রূপান্তর করার সবচেয়ে সুন্দর পথ।",
        "prompt": "জেমিনি, ভারতীয় ক্ল্যাসিক্যাল বা রবীন্দ্রসংগীতের এমন একটা গানের গল্প বলো যার কথাগুলো মনকে মুহূর্তে শান্ত ও উজ্জীবিত করে তোলে।",
        "audio_key": "games/k_wave_3.mp3",
    },
    {
        "short": "🗣️ নিঃসংকোচ মন",
        "category": "🗣️ Expressing Your Own Mind",
        "title": "দ্বিধা ছাড়া নিজের আসল মত ও পছন্দ প্রকাশ",
        "detail": "আজ কারোর সাথে কথা বলার সময় মনে মনে রিহার্সাল না করে, যেটা সত্যিই তোমার মনে হচ্ছে সেটা সহজ ও উষ্ণভাবে বলে ফেলো। ভুল হলে ক্ষতি নেই!",
        "reframe": "💡 মায়ের জন্য যে নিয়ম বানিয়েছো—‘ভুল হওয়ার ভয় নেই, নিজের মনের কথা বলো’—আজ সেটা নিজের জীবনে উপভোগ করো।",
        "prompt": "জেমিনি, কথাবার্তায় অতিরিক্ত চিন্তা না করে কীভাবে একদম স্বাভাবিক, মজাদার ও আত্মবিশ্বাসী থাকা যায় তার একটা ছোট্ট টিপস দাও।",
        "audio_key": "games/k_wave_4.mp3",
    },
]

WAVE_DAY_SCRIPTS = {
    3: ("days/k_wave_day_3.mp3", "সুপ্রভাত কৌশিক! আজ তোমার নিজের আনন্দে, নিঃসংকোচে ও খোলা মনে বাঁচার দিন। আজকের হালকা ঢেউয়ে তিনটি মজার খেলা রয়েছে—যেদিন যেরকম ইচ্ছে, সেদিন সেরকম খেলো।"),
    4: ("days/k_wave_day_4.mp3", "সুপ্রভাত কৌশিক! আজ তোমার নিজের আনন্দে ও শান্ত মনে বাঁচার দিন। আজকের ঢেউয়ে চারটি সুন্দর খেলা রয়েছে—নিজের খুশিমতো উপভোগ করো।"),
    5: ("days/k_wave_day_5.mp3", "সুপ্রভাত কৌশিক! আজ গভীর আনন্দ, সংগীত ও কৌতূহলের ঢেউ। আজকের পাঁচটি খেলা নিজের গতিতে, সম্পূর্ণ চাপমুক্ত মনে উপভোগ করো।"),
}


def generate_one_slide_image(slide_id: int, ref_img: Path, prompt: str) -> tuple[int, bool]:
    SLIDE_IMG_DIR.mkdir(parents=True, exist_ok=True)
    out_jpg = SLIDE_IMG_DIR / f"k_slide_{slide_id}.jpg"
    if out_jpg.is_file() and out_jpg.stat().st_size > 15_000:
        return slide_id, True

    raw_tmp = Path(f"/tmp/k_slide_raw_{os.getpid()}_{slide_id}.png")
    try:
        proc = subprocess.run(
            [GEN_BIN, "-timeout=90s", f"-output={raw_tmp}", "image", f"-media-uri={ref_img}", prompt],
            capture_output=True,
            text=True,
            timeout=95,
        )
        if proc.returncode == 0 and raw_tmp.is_file() and raw_tmp.stat().st_size > 10_000:
            subprocess.run(
                ["ffmpeg", "-y", "-i", str(raw_tmp), "-vf", "scale=800:-1", "-q:v", "4", str(out_jpg)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            if out_jpg.is_file() and out_jpg.stat().st_size > 10_000:
                return slide_id, True
    except Exception:
        pass
    finally:
        raw_tmp.unlink(missing_ok=True)
    return slide_id, False


def synthesize_one_mp3(rel_key: str, text: str) -> tuple[str, bool]:
    out_mp3 = KOUSHIK_AUDIO_DIR / rel_key
    if out_mp3.is_file() and out_mp3.stat().st_size >= 4000:
        return rel_key, True

    out_mp3.parent.mkdir(parents=True, exist_ok=True)
    safe_tag = rel_key.replace("/", "_").replace(".mp3", "")
    w_tmp = Path(f"/tmp/koushik_tts_{os.getpid()}_{safe_tag}.wav")
    for model_name in ("gemini-v4s-tts-no-transcriber", "gemini-v4s-tts"):
        try:
            proc = subprocess.run(
                [GEN_BIN, "-timeout=75s", f"-output={w_tmp}", "tts", f"-model={model_name}", "-voice=Aoede", text],
                capture_output=True,
                text=True,
                timeout=80,
            )
            if proc.returncode == 0 and w_tmp.is_file() and w_tmp.stat().st_size > 4000:
                subprocess.run(
                    [
                        "ffmpeg", "-y", "-i", str(w_tmp),
                        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                        "-ar", "24000", "-ac", "1", "-b:a", "32k",
                        str(out_mp3),
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
                if out_mp3.is_file() and out_mp3.stat().st_size >= 4000:
                    return rel_key, True
        except Exception:
            pass
        finally:
            w_tmp.unlink(missing_ok=True)
    return rel_key, False


def b64_uri(path: Path, mime: str) -> str:
    if not path.is_file():
        return ""
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def main() -> int:
    t0 = time.time()
    print("🎨 Step 1/3: Generating 8 personalized Chithi illustrations for Koushik (parallel)...", flush=True)
    with ThreadPoolExecutor(max_workers=8) as ex:
        img_futs = [ex.submit(generate_one_slide_image, sid, ref, pr) for sid, ref, pr in SLIDE_IMAGE_PROMPTS]
        for fut in as_completed(img_futs):
            sid, ok = fut.result()
            print(f"   • Slide {sid} image: {'OK' if ok else 'FAILED'}", flush=True)

    # Collect all 36 unique TTS tasks
    tts_tasks: dict[str, str] = {}
    for s in SLIDES_SELF:
        sid = s["id"]
        tts_tasks[f"slides/k_slide_{sid}.mp3"] = f"{s['title']}। {s['highlight']}। {s['text']}"
    for q_idx, q_txt in enumerate(QUOTES):
        tts_tasks[f"quotes/k_quote_{q_idx}.mp3"] = q_txt
    for d in DAYS_1_TO_3:
        tts_tasks[d["day_audio_key"]] = d["voice_script"]
        for g in d["games"]:
            tts_tasks[g["audio_key"]] = f"{g['title']}। {g['detail']} {g['reframe']} এবার জেমিনিকে বলো: {g['prompt']}"
    for wave_len, (d_key, d_script) in WAVE_DAY_SCRIPTS.items():
        tts_tasks[d_key] = d_script
    for g in WAVE_TEMPLATES:
        tts_tasks[g["audio_key"]] = f"{g['title']}। {g['detail']} {g['reframe']} এবার জেমিনিকে বলো: {g['prompt']}"

    print(f"🎙️ Step 2/3: Synthesizing {len(tts_tasks)} Gemini Aoede MP3 voices for ⚡ আনন্দ (16 workers)...", flush=True)
    ok_tts = 0
    with ThreadPoolExecutor(max_workers=16) as ex:
        futs = {ex.submit(synthesize_one_mp3, k, txt): k for k, txt in tts_tasks.items()}
        for i, fut in enumerate(as_completed(futs), 1):
            k, ok = fut.result()
            if ok:
                ok_tts += 1
            if i % 9 == 0 or i == len(tts_tasks):
                print(f"   • Voice progress: {i}/{len(tts_tasks)} (ok={ok_tts}, elapsed={time.time() - t0:.1f}s)", flush=True)

    print("📦 Step 3/3: Compiling koushik.html with embedded slide art + Aoede audio URLs...", flush=True)
    slides_payload = []
    for s in SLIDES_SELF:
        sid = s["id"]
        img_p = SLIDE_IMG_DIR / f"k_slide_{sid}.jpg"
        slides_payload.append({
            **s,
            "img_b64": b64_uri(img_p, "image/jpeg"),
            "audio_url": f"{GH_RAW_BASE}audio/koushik/slides/k_slide_{sid}.mp3",
        })

    quotes_payload = [
        {"text": q, "audio_url": f"{GH_RAW_BASE}audio/koushik/quotes/k_quote_{idx}.mp3"}
        for idx, q in enumerate(QUOTES)
    ]

    all_days_payload = []
    for d in DAYS_1_TO_3:
        games_p = [
            {**g, "audio_url": f"{GH_RAW_BASE}audio/koushik/{g['audio_key']}"}
            for g in d["games"]
        ]
        all_days_payload.append({
            "day": d["day"],
            "title": d["title"],
            "sub": d["sub"],
            "audio_url": f"{GH_RAW_BASE}audio/koushik/{d['day_audio_key']}",
            "games": games_p,
        })

    for day_num in range(4, 22):
        wave_len = 5 if (day_num % 4 == 0) else (4 if (day_num % 2 == 0) else 3)
        d_key, _ = WAVE_DAY_SCRIPTS[wave_len]
        games_p = []
        for g_idx in range(wave_len):
            tmpl = WAVE_TEMPLATES[(day_num + g_idx) % len(WAVE_TEMPLATES)]
            games_p.append({
                **tmpl,
                "audio_url": f"{GH_RAW_BASE}audio/koushik/{tmpl['audio_key']}",
            })
        all_days_payload.append({
            "day": day_num,
            "title": f"দিন {day_num} • নিজের আনন্দে, নিঃসংকোচে ও খোলা মনে বাঁচা",
            "sub": f"আজকের ঢেউয়ে {wave_len}টি হালকা খেলা—যেদিন যেরকম ইচ্ছে, সেদিন সেরকম খেলো।",
            "audio_url": f"{GH_RAW_BASE}audio/koushik/{d_key}",
            "games": games_p,
        })

    DataJson = json.dumps(
        {"slides": slides_payload, "quotes": quotes_payload, "days": all_days_payload},
        ensure_ascii=False,
    )

    koushik_html = (APP_ROOT / "src" / "koushik_template.html").read_text(encoding="utf-8")
    # Inject DATA_BUNDLE and audio controller into koushik.html
    marker = "/*__ANANDO_DATA_INJECT__*/"
    koushik_html = koushik_html.replace(marker, f"const ANANDO_DATA = {DataJson};")
    (APP_ROOT / "koushik.html").write_text(koushik_html, encoding="utf-8")

    print(f"✅ Done in {time.time() - t0:.1f}s! Built koushik.html ({(APP_ROOT / 'koushik.html').stat().st_size:,} bytes).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
