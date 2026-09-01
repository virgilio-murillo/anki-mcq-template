#!/usr/bin/env python3
"""
Example deck showing how to use anki_mcq.

Run:
    python3 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
    ./.venv/bin/python example_deck.py
    # -> writes example_deck.apkg, then import it into Anki

Notes on writing the `answer` field:
- It is HTML (Anki renders fields as HTML). Use <b>, <code>, <ul>/<li>, <p>.
- Start with a <div class="verdict">Correct: X</div> line.
- Optional callout boxes:
    <div class="extra"><span class="h">Exam tip</span> ... </div>   (amber)
    <div class="warn"><span class="h">Heads up</span> ... </div>     (red)
    <div class="links"><span class="h">Links</span><a href="...">...</a></div>
"""
from anki_mcq import card, build_deck

cards = [
    card(
        question="Which AWS service is a fully managed NoSQL key-value and document database?",
        options=[
            "Amazon RDS",
            "Amazon DynamoDB",
            "Amazon Redshift",
            "Amazon Aurora",
        ],
        correct=1,
        key="ex-dynamodb-nosql",
        answer=(
            '<div class="verdict">Correct: {{L}} - Amazon DynamoDB.</div>'
            '<p><b>DynamoDB</b> is a fully managed <b>NoSQL</b> database with a flexible '
            'schema, single-digit-millisecond latency and horizontal scaling. RDS and Aurora '
            'are relational (rigid schema); Redshift is an OLAP data warehouse.</p>'
            '<div class="extra"><span class="h">Exam tip</span>"Global" scale is a strong '
            'DynamoDB signal via <b>Global Tables</b> (multi-region, active-active).</div>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://aws.amazon.com/dynamodb/">aws.amazon.com/dynamodb</a></div>'
        ),
    ),
    card(
        question="What is the default TTL of an Amazon API Gateway cache?",
        options=["60 seconds", "300 seconds", "3600 seconds", "It never expires"],
        correct=1,
        key="ex-apigw-cache-ttl",
        answer=(
            '<div class="verdict">Correct: {{L}} - 300 seconds.</div>'
            '<p>API Gateway cache TTL defaults to <b>300s</b>, with a max of <b>3600s</b>. '
            'Setting <code>TTL=0</code> disables caching.</p>'
            '<div class="links"><span class="h">Links</span>'
            '<a href="https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-caching.html">docs.aws apigateway caching</a></div>'
        ),
    ),
    card(
        question="Which header does a client send to invalidate its API Gateway cache entry?",
        options=[
            "<code>Cache-Control: max-age=1</code>",
            "<code>Cache-Control: max-age=0</code>",
            "<code>X-Cache: bypass</code>",
            "<code>Pragma: refresh</code>",
        ],
        correct=1,
        key="ex-apigw-invalidate-header",
        answer=(
            '<div class="verdict">Correct: {{L}} - <code>Cache-Control: max-age=0</code>.</div>'
            '<p>This tells API Gateway to bypass the cache and fetch a fresh response from the '
            'backend, replacing the stale cached entry. The documented value is exactly '
            '<code>max-age=0</code>.</p>'
            '<div class="warn"><span class="h">Gotcha</span>Only <b>authorized</b> clients can do '
            'this if you enable "Require Authorization" (IAM <code>execute-api:InvalidateCache</code>).</div>'
        ),
    ),
]

if __name__ == "__main__":
    build_deck("Example MCQ Deck", cards, "example_deck.apkg")
