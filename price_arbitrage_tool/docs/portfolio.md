# Price Arbitrage Tool

CSV-first arbitrage assistant for comparing authorized marketplace exports with AliExpress supplier data.

## Portfolio Angle

- Demonstrates practical data cleaning, product matching, scoring, and profitability modelling.
- Avoids unsafe scraping by requiring user-controlled CSV exports or authorized feeds.
- Includes manual approval and rejection files so the workflow can combine automation with human review.

## Demo Story

1. Load the included Amazon or Bol.com sample file.
2. Compare it with the AliExpress sample file.
3. Export ranked opportunities with match confidence, risk flags, net profit, and ROI.

## Next Improvements

- Add a Streamlit review UI for accepting or rejecting matches.
- Add supplier lead-time and return-rate presets per category.
- Export a separate "needs review" CSV for medium-confidence matches.
