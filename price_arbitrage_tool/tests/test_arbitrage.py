from pathlib import Path

import pytest

from arbitrage import (
    ApprovedMatch,
    Product,
    find_opportunities,
    load_products,
    parse_float,
    score_match,
    similarity,
)


def make_product(source: str, sku: str, title: str, price: float, **kwargs) -> Product:
    return Product(
        source=source,
        sku=sku,
        title=title,
        price=price,
        shipping=kwargs.get("shipping", 0.0),
        url="",
        stock=kwargs.get("stock"),
        rating=kwargs.get("rating"),
        brand=kwargs.get("brand", ""),
        model=kwargs.get("model", ""),
        ean=kwargs.get("ean", ""),
        variant=kwargs.get("variant", ""),
        dimensions=kwargs.get("dimensions", ""),
        weight_grams=kwargs.get("weight_grams"),
    )


def test_parse_float_accepts_currency_and_commas():
    assert parse_float("EUR 12,50") == 12.50
    assert parse_float("") == 0.0


def test_similarity_uses_meaningful_token_overlap():
    assert similarity("Wireless Mouse Pro", "pro wireless mouse black") > 0.5
    assert similarity("Wireless Mouse", "ceramic mug") == 0.0


def test_manual_approval_overrides_low_similarity():
    seller = make_product("amazon", "A1", "Seller title", 50)
    ali = make_product("aliexpress", "X1", "Different title", 10)

    score, status, reasons, risks = score_match(
        seller,
        ali,
        {("A1", "X1"): ApprovedMatch("A1", "X1", "approved", "")},
    )

    assert score == 1.0
    assert status == "approved"
    assert reasons == ["match valide manuellement"]
    assert risks == []


def test_find_opportunities_filters_unprofitable_matches():
    seller = make_product("amazon", "A1", "Portable Charger 10000mah", 40, ean="123")
    ali = make_product("aliexpress", "X1", "Portable Charger 10000mah", 10, ean="123")

    opportunities = find_opportunities(
        [seller],
        [ali],
        min_similarity=0.1,
        auto_validate_score=0.75,
        min_profit=1,
        min_roi=0.1,
        min_rating=0,
        marketplace_fee_rate=0.15,
        payment_fee_rate=0.03,
        fixed_cost=0,
        vat_rate=0.20,
        customs_rate=0,
        return_rate=0.05,
        safety_margin_rate=0.08,
        approved_matches={},
    )

    assert len(opportunities) == 1
    assert opportunities[0].net_profit > 0
    assert opportunities[0].match_status == "auto_validated"


def test_load_products_reports_missing_required_columns(tmp_path: Path):
    csv_path = tmp_path / "bad.csv"
    csv_path.write_text("sku,title\nA1,Missing price\n", encoding="utf-8")

    with pytest.raises(ValueError, match="price"):
        load_products(csv_path, "amazon")
