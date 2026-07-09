# LumiFlow FAQ Chatbot

This project is a polished FAQ chatbot website built with Flask, a cosine-similarity matcher, and a custom animated UI.

## What it does

- Collects a curated FAQ set for a product-style support experience.
- Preprocesses user text with lightweight NLP-style normalization:
  - tokenization
  - cleaning
  - stop-word removal
  - simple word-form normalization
- Matches the user question against the most similar FAQ using TF-IDF cosine similarity.
- Falls back to the nearest suggestions when the match is low-confidence.
- Renders everything in a refined chat interface with hover states, transitions, and motion.

## Run it

```bash
python3 app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Customize the FAQs

Edit [`faq_data.py`](./faq_data.py) to change:

- the product name
- the FAQ questions and answers
- the starter prompts
- the feature callouts on the left side of the page

## API

- `POST /api/chat`
  - body: `{ "message": "your question" }`
  - returns the best matching FAQ answer, confidence score, and suggested follow-up questions

