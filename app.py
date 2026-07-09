from __future__ import annotations

import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any

from flask import Flask, jsonify, render_template, request, send_from_directory
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from faq_data import APP_NAME, FAQS, FEATURES, STARTER_PROMPTS, SUBTITLE, TAGLINE


app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="/static")

WORD_RE = re.compile(r"[a-z0-9']+")
GREETING_RE = re.compile(r"^(hi|hello|hey|hiya|good morning|good afternoon|good evening)[!. ]*$", re.I)
THANKS_RE = re.compile(r"^(thanks|thank you|thx|appreciate it)[!. ]*$", re.I)

BASE_STOPWORDS = set(ENGLISH_STOP_WORDS) | {
    "please",
    "tell",
    "me",
    "about",
    "need",
    "want",
    "know",
    "help",
    "would",
    "could",
    "should",
}


@dataclass(frozen=True)
class PhraseRecord:
    faq_index: int
    text: str


def normalize_token(token: str) -> str:
    token = token.lower().strip("'")

    if len(token) > 6 and token.endswith("ies"):
        return token[:-3] + "y"
    if len(token) > 5 and token.endswith("ing"):
        return token[:-3]
    if len(token) > 5 and token.endswith("edly"):
        return token[:-4]
    if len(token) > 4 and token.endswith("ed"):
        return token[:-2]
    if len(token) > 4 and token.endswith("es"):
        return token[:-2]
    if len(token) > 4 and token.endswith("s") and not token.endswith(("ss", "us")):
        return token[:-1]
    return token


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for raw_token in WORD_RE.findall(text.lower()):
        if raw_token in BASE_STOPWORDS or raw_token.isdigit():
            continue
        token = normalize_token(raw_token)
        if token and token not in BASE_STOPWORDS:
            tokens.append(token)
    return tokens


def build_phrase_records() -> list[PhraseRecord]:
    records: list[PhraseRecord] = []
    for faq_index, faq in enumerate(FAQS):
        sources = [faq["question"], *faq["phrases"], " ".join(faq["tags"])]
        for source in sources:
            records.append(PhraseRecord(faq_index=faq_index, text=source))
    return records


PHRASE_RECORDS = build_phrase_records()
PHRASE_LOOKUP = [record.faq_index for record in PHRASE_RECORDS]
CORPUS = [record.text for record in PHRASE_RECORDS]

VECTORIZER = TfidfVectorizer(
    tokenizer=tokenize,
    preprocessor=None,
    lowercase=False,
    token_pattern=None,
    ngram_range=(1, 2),
    sublinear_tf=True,
)
MATRIX = VECTORIZER.fit_transform(CORPUS)

FAQ_TOKEN_SETS = []
for faq in FAQS:
    faq_text = " ".join([faq["question"], " ".join(faq["phrases"]), " ".join(faq["tags"])])
    FAQ_TOKEN_SETS.append(set(tokenize(faq_text)))

CATEGORY_COUNTS = Counter(faq["category"] for faq in FAQS)
TOPIC_SUMMARY = [
    {"name": category, "count": count}
    for category, count in sorted(CATEGORY_COUNTS.items(), key=lambda item: (-item[1], item[0]))
]

PAGE_CONFIG = {
    "appName": APP_NAME,
    "tagline": TAGLINE,
    "subtitle": SUBTITLE,
    "features": FEATURES,
    "starterPrompts": STARTER_PROMPTS,
    "metrics": [
        {"value": len(FAQS), "label": "Curated FAQs"},
        {"value": len(PHRASE_RECORDS), "label": "Phrase variants"},
        {"value": len(TOPIC_SUMMARY), "label": "Support categories"},
    ],
    "topics": TOPIC_SUMMARY,
}


def special_response(message: str) -> dict[str, Any] | None:
    normalized = " ".join(message.strip().lower().split())

    if not normalized:
        return None

    if GREETING_RE.fullmatch(normalized):
        return {
            "reply": (
                f"Hi, I’m {APP_NAME}. Ask me about billing, security, integrations, account access, "
                "or anything else in the FAQ library."
            ),
            "match": "Greeting intent",
            "score": 1.0,
            "confidence": 100,
            "matchedPhrase": "greeting",
            "category": "Welcome",
            "mode": "intent",
            "fallback": False,
            "suggestions": starter_suggestions(),
            "reason": "Matched a greeting intent before running FAQ similarity.",
        }

    if THANKS_RE.fullmatch(normalized):
        return {
            "reply": "Happy to help. If you want, ask another question and I’ll find the closest FAQ.",
            "match": "Thanks intent",
            "score": 1.0,
            "confidence": 100,
            "matchedPhrase": "thanks",
            "category": "Welcome",
            "mode": "intent",
            "fallback": False,
            "suggestions": starter_suggestions(),
            "reason": "Matched a gratitude intent before running FAQ similarity.",
        }

    return None


def starter_suggestions() -> list[dict[str, str]]:
    return [
        {"question": prompt, "category": "Starter prompt"}
        for prompt in STARTER_PROMPTS[:4]
    ]


def rank_faqs(message: str) -> list[dict[str, Any]]:
    if not message.strip():
        return []

    query_vector = VECTORIZER.transform([message])
    scores = cosine_similarity(query_vector, MATRIX).ravel()
    query_tokens = set(tokenize(message))

    best_by_faq: dict[int, float] = defaultdict(float)
    best_phrase: dict[int, str] = {}

    for phrase_index, phrase_score in enumerate(scores):
        faq_index = PHRASE_LOOKUP[phrase_index]
        if phrase_score >= best_by_faq[faq_index]:
            best_by_faq[faq_index] = float(phrase_score)
            best_phrase[faq_index] = PHRASE_RECORDS[phrase_index].text

    ranked: list[dict[str, Any]] = []
    for faq_index, base_score in best_by_faq.items():
        faq = FAQS[faq_index]
        faq_tokens = FAQ_TOKEN_SETS[faq_index]
        overlap = sorted(query_tokens & faq_tokens)
        bonus = min(0.15, len(overlap) * 0.03)
        score = min(1.0, base_score + bonus)

        ranked.append(
            {
                "faq_index": faq_index,
                "score": score,
                "base_score": base_score,
                "overlap": overlap,
                "matched_phrase": best_phrase.get(faq_index, faq["question"]),
                "faq": faq,
            }
        )

    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked


def format_suggestions(ranked: list[dict[str, Any]], limit: int = 3) -> list[dict[str, str]]:
    suggestions: list[dict[str, str]] = []
    for item in ranked[:limit]:
        faq = item["faq"]
        suggestions.append(
            {
                "question": faq["question"],
                "category": faq["category"],
            }
        )
    return suggestions


def build_reply(message: str) -> dict[str, Any]:
    special = special_response(message)
    if special is not None:
        return special

    ranked = rank_faqs(message)
    if not ranked:
        return {
            "reply": (
                f"Ask me about {', '.join(sorted(CATEGORY_COUNTS.keys())[:4])}, or tap one of the "
                "starter prompts to get a fast answer."
            ),
            "match": "Empty query",
            "score": 0.0,
            "confidence": 0,
            "matchedPhrase": "",
            "category": "Fallback",
            "mode": "fallback",
            "fallback": True,
            "suggestions": starter_suggestions(),
            "reason": "No text was provided.",
        }

    top = ranked[0]
    top_score = top["score"]
    faq = top["faq"]
    suggestions = format_suggestions(ranked)

    if top_score < 0.16:
        return {
            "reply": (
                "I could not find a confident match yet. Try asking about billing, integrations, "
                "security, the mobile app, or account access."
            ),
            "match": faq["question"],
            "score": round(top_score, 3),
            "confidence": max(0, min(100, int(round(top_score * 100)))),
            "matchedPhrase": top["matched_phrase"],
            "category": faq["category"],
            "mode": "fallback",
            "fallback": True,
            "suggestions": suggestions,
            "reason": "Similarity was below the confidence threshold.",
        }

    overlap_text = ", ".join(top["overlap"][:4]) if top["overlap"] else "semantic similarity"
    return {
        "reply": faq["answer"],
        "match": faq["question"],
        "score": round(top_score, 3),
        "confidence": max(0, min(100, int(round(top_score * 100)))),
        "matchedPhrase": top["matched_phrase"],
        "category": faq["category"],
        "mode": "faq",
        "fallback": False,
        "suggestions": suggestions,
        "reason": f"Matched on {overlap_text}.",
    }


@app.get("/")
def index() -> str:
    return render_template(
        "index.html",
        config=PAGE_CONFIG,
        faq_count=len(FAQS),
        category_count=len(TOPIC_SUMMARY),
        variant_count=len(PHRASE_RECORDS),
    )


@app.get("/favicon.ico")
def favicon():
    return send_from_directory(app.static_folder, "favicon.svg")


@app.post("/api/chat")
def chat() -> tuple[Any, int]:
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()

    if not message:
        return jsonify(
            {
                "reply": "Type a question and I’ll search the FAQ library for the closest answer.",
                "match": "",
                "score": 0.0,
                "confidence": 0,
                "matchedPhrase": "",
                "category": "Fallback",
                "mode": "fallback",
                "fallback": True,
                "suggestions": starter_suggestions(),
                "reason": "Empty input.",
            }
        ), 400

    response = build_reply(message)
    return jsonify(response), 200


@app.get("/api/health")
def health() -> tuple[Any, int]:
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
