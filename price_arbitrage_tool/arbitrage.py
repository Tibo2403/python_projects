#!/usr/bin/env python3
"""
Outil simple d'arbitrage de prix entre une marketplace et AliExpress.

Le script compare deux fichiers CSV exportes depuis des sources de prix
legitimes, puis classe les produits selon marge nette et ROI.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_MARKETPLACE_FEE_RATE = 0.15
DEFAULT_BOL_FEE_RATE = 0.15
DEFAULT_PAYMENT_FEE_RATE = 0.03
DEFAULT_FIXED_COST = 0.0
DEFAULT_VAT_RATE = 0.20
DEFAULT_CUSTOMS_RATE = 0.0
DEFAULT_RETURN_RATE = 0.05
DEFAULT_SAFETY_MARGIN_RATE = 0.08


@dataclass(frozen=True)
class Product:
    source: str
    sku: str
    title: str
    price: float
    shipping: float
    url: str
    stock: int | None
    rating: float | None
    brand: str
    model: str
    ean: str
    variant: str
    dimensions: str
    weight_grams: float | None

    @property
    def landed_cost(self) -> float:
        return self.price + self.shipping


@dataclass(frozen=True)
class Opportunity:
    seller: Product
    aliexpress: Product
    match_score: float
    match_status: str
    match_reasons: list[str]
    risk_flags: list[str]
    sell_price: float
    buy_cost: float
    fees: float
    extra_costs: float
    net_profit: float
    roi: float


@dataclass(frozen=True)
class ApprovedMatch:
    seller_sku: str
    aliexpress_sku: str
    status: str
    note: str


def normalize_text(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def token_set(value: str) -> set[str]:
    ignored = {"the", "and", "with", "for", "de", "la", "le", "les", "un", "une", "et", "avec", "pour"}
    return {token for token in normalize_text(value).split() if token not in ignored}


def similarity(left: str, right: str) -> float:
    left_tokens = token_set(left)
    right_tokens = token_set(right)
    if not left_tokens or not right_tokens:
        return 0.0
    overlap = len(left_tokens & right_tokens)
    union = len(left_tokens | right_tokens)
    return overlap / union


def same_normalized(left: str, right: str) -> bool:
    return bool(left and right and normalize_text(left) == normalize_text(right))


def parse_float(value: str | None, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    cleaned = value.strip().replace(",", ".")
    cleaned = re.sub(r"[^0-9.\-]", "", cleaned)
    if cleaned in {"", ".", "-"}:
        return default
    return float(cleaned)


def parse_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    cleaned = re.sub(r"[^0-9\-]", "", value.strip())
    if cleaned in {"", "-"}:
        return None
    return int(cleaned)


def optional_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    return parse_float(value)


def load_products(path: Path, source: str) -> list[Product]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"sku", "title", "price"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path} manque les colonnes obligatoires: {', '.join(sorted(missing))}")

        products: list[Product] = []
        for row_number, row in enumerate(reader, start=2):
            title = (row.get("title") or "").strip()
            sku = (row.get("sku") or "").strip()
            if not title:
                print(f"Ignore ligne {row_number} de {path}: titre vide")
                continue
            products.append(
                Product(
                    source=source,
                    sku=sku,
                    title=title,
                    price=parse_float(row.get("price")),
                    shipping=parse_float(row.get("shipping")),
                    url=(row.get("url") or "").strip(),
                    stock=parse_int(row.get("stock")),
                    rating=parse_float(row.get("rating"), default=math.nan),
                    brand=(row.get("brand") or "").strip(),
                    model=(row.get("model") or "").strip(),
                    ean=(row.get("ean") or row.get("gtin") or row.get("upc") or "").strip(),
                    variant=(row.get("variant") or "").strip(),
                    dimensions=(row.get("dimensions") or "").strip(),
                    weight_grams=optional_float(row.get("weight_grams") or row.get("weight")),
                )
            )
        return products


def first_value(row: dict[str, str], names: Iterable[str]) -> str:
    for name in names:
        value = row.get(name)
        if value:
            return value.strip()
    return ""


def load_approved_matches(path: Path | None) -> dict[tuple[str, str], ApprovedMatch]:
    if path is None or not path.exists():
        return {}

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        has_seller_key = bool({"seller_sku", "marketplace_sku", "amazon_sku", "bol_sku"} & fieldnames)
        required = {"aliexpress_sku", "status"}
        missing = required - fieldnames
        if not has_seller_key:
            missing.add("seller_sku")
        if missing:
            raise ValueError(f"{path} manque les colonnes obligatoires: {', '.join(sorted(missing))}")

        matches: dict[tuple[str, str], ApprovedMatch] = {}
        for row in reader:
            seller_sku = first_value(row, ("seller_sku", "marketplace_sku", "amazon_sku", "bol_sku"))
            aliexpress_sku = (row.get("aliexpress_sku") or "").strip()
            status = normalize_text(row.get("status") or "")
            if not seller_sku or not aliexpress_sku:
                continue
            matches[(seller_sku, aliexpress_sku)] = ApprovedMatch(
                seller_sku=seller_sku,
                aliexpress_sku=aliexpress_sku,
                status=status,
                note=(row.get("note") or "").strip(),
            )
        return matches


def score_match(seller: Product, ali: Product, approved_matches: dict[tuple[str, str], ApprovedMatch]) -> tuple[float, str, list[str], list[str]]:
    approved = approved_matches.get((seller.sku, ali.sku))
    if approved and approved.status in {"approved", "valide", "valid", "ok"}:
        return 1.0, "approved", ["match valide manuellement"], []
    if approved and approved.status in {"rejected", "rejete", "reject", "no", "non"}:
        return 0.0, "rejected", ["match rejete manuellement"], ["rejected_match"]

    score = 0.0
    reasons: list[str] = []
    risks: list[str] = []

    title_score = similarity(seller.title, ali.title)
    score += title_score * 0.35
    if title_score >= 0.50:
        reasons.append(f"titre proche {title_score:.2f}")

    if same_normalized(seller.ean, ali.ean):
        score += 0.45
        reasons.append("ean identique")
    elif seller.ean or ali.ean:
        risks.append("ean_different_ou_manquant")

    if same_normalized(seller.brand, ali.brand):
        score += 0.10
        reasons.append("marque identique")
    elif seller.brand or ali.brand:
        risks.append("marque_differente_ou_manquante")

    if same_normalized(seller.model, ali.model):
        score += 0.20
        reasons.append("modele identique")
    elif seller.model or ali.model:
        risks.append("modele_different_ou_manquant")

    if same_normalized(seller.variant, ali.variant):
        score += 0.05
        reasons.append("variante identique")
    elif seller.variant or ali.variant:
        risks.append("variante_a_verifier")

    if same_normalized(seller.dimensions, ali.dimensions):
        score += 0.05
        reasons.append("dimensions identiques")
    elif seller.dimensions or ali.dimensions:
        risks.append("dimensions_a_verifier")

    if seller.weight_grams and ali.weight_grams:
        heavier = max(seller.weight_grams, ali.weight_grams)
        lighter = min(seller.weight_grams, ali.weight_grams)
        if heavier > 0 and lighter / heavier >= 0.85:
            score += 0.05
            reasons.append("poids proche")
        else:
            risks.append("poids_different")

    if not seller.ean and not seller.model:
        risks.append(f"{seller.source}_sans_identifiant_fort")
    if not ali.ean and not ali.model:
        risks.append("aliexpress_sans_identifiant_fort")

    score = min(score, 1.0)
    status = "auto_validated" if score >= 0.85 and "ean_different_ou_manquant" not in risks else "manual_review"
    return score, status, reasons or ["similarite faible"], risks


def product_is_available(product: Product, min_rating: float) -> bool:
    if product.stock is not None and product.stock <= 0:
        return False
    if product.rating is not None and not math.isnan(product.rating) and product.rating < min_rating:
        return False
    return True


def find_opportunities(
    seller_products: Iterable[Product],
    aliexpress_products: Iterable[Product],
    *,
    min_similarity: float,
    auto_validate_score: float,
    min_profit: float,
    min_roi: float,
    min_rating: float,
    marketplace_fee_rate: float,
    payment_fee_rate: float,
    fixed_cost: float,
    vat_rate: float,
    customs_rate: float,
    return_rate: float,
    safety_margin_rate: float,
    approved_matches: dict[tuple[str, str], ApprovedMatch],
) -> list[Opportunity]:
    opportunities: list[Opportunity] = []
    ali_available = [p for p in aliexpress_products if product_is_available(p, min_rating)]

    for seller in seller_products:
        if not product_is_available(seller, min_rating):
            continue

        for ali in ali_available:
            match_score, match_status, match_reasons, risk_flags = score_match(seller, ali, approved_matches)
            if match_score < min_similarity:
                continue

            sell_price = seller.price
            buy_cost = ali.landed_cost
            fees = sell_price * (marketplace_fee_rate + payment_fee_rate) + fixed_cost
            extra_costs = buy_cost * (vat_rate + customs_rate) + sell_price * (return_rate + safety_margin_rate)
            net_profit = sell_price - buy_cost - fees - extra_costs
            roi = net_profit / buy_cost if buy_cost > 0 else 0.0

            if net_profit >= min_profit and roi >= min_roi:
                if match_status == "manual_review" and match_score >= auto_validate_score:
                    match_status = "auto_validated"
                opportunities.append(
                    Opportunity(
                        seller=seller,
                        aliexpress=ali,
                        match_score=match_score,
                        match_status=match_status,
                        match_reasons=match_reasons,
                        risk_flags=risk_flags,
                        sell_price=sell_price,
                        buy_cost=buy_cost,
                        fees=fees,
                        extra_costs=extra_costs,
                        net_profit=net_profit,
                        roi=roi,
                    )
                )

    return sorted(opportunities, key=lambda item: (item.net_profit, item.roi), reverse=True)


def write_opportunities(path: Path, opportunities: list[Opportunity]) -> None:
    fieldnames = [
        "marketplace",
        "seller_sku",
        "seller_title",
        "seller_price",
        "seller_url",
        "aliexpress_sku",
        "aliexpress_title",
        "aliexpress_cost",
        "aliexpress_url",
        "match_score",
        "match_status",
        "match_reasons",
        "risk_flags",
        "fees",
        "extra_costs",
        "net_profit",
        "roi_percent",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in opportunities:
            writer.writerow(
                {
                    "marketplace": item.seller.source,
                    "seller_sku": item.seller.sku,
                    "seller_title": item.seller.title,
                    "seller_price": f"{item.sell_price:.2f}",
                    "seller_url": item.seller.url,
                    "aliexpress_sku": item.aliexpress.sku,
                    "aliexpress_title": item.aliexpress.title,
                    "aliexpress_cost": f"{item.buy_cost:.2f}",
                    "aliexpress_url": item.aliexpress.url,
                    "match_score": f"{item.match_score:.2f}",
                    "match_status": item.match_status,
                    "match_reasons": " | ".join(item.match_reasons),
                    "risk_flags": " | ".join(item.risk_flags),
                    "fees": f"{item.fees:.2f}",
                    "extra_costs": f"{item.extra_costs:.2f}",
                    "net_profit": f"{item.net_profit:.2f}",
                    "roi_percent": f"{item.roi * 100:.1f}",
                }
            )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compare Amazon ou Bol.com avec AliExpress pour trouver des opportunites d'arbitrage.")
    parser.add_argument("--amazon", type=Path, help="CSV Amazon avec colonnes: sku,title,price,shipping,url,stock,rating")
    parser.add_argument("--bol", type=Path, help="CSV Bol.com avec colonnes: sku,title,price,shipping,url,stock,rating")
    parser.add_argument("--marketplace", choices=("auto", "amazon", "bol"), default="auto", help="Marketplace de vente utilisee")
    parser.add_argument("--aliexpress", required=True, type=Path, help="CSV AliExpress avec colonnes: sku,title,price,shipping,url,stock,rating")
    parser.add_argument("--output", default=Path("opportunities.csv"), type=Path, help="Fichier CSV de sortie")
    parser.add_argument("--approved-matches", type=Path, help="CSV de couples valides/rejetes: seller_sku,aliexpress_sku,status,note")
    parser.add_argument("--min-similarity", default=0.45, type=float, help="Score minimum de correspondance produit, de 0 a 1")
    parser.add_argument("--auto-validate-score", default=0.85, type=float, help="Score a partir duquel un match peut etre considere valide automatiquement")
    parser.add_argument("--min-profit", default=5.0, type=float, help="Marge nette minimum par vente")
    parser.add_argument("--min-roi", default=0.25, type=float, help="ROI minimum, 0.25 = 25%%")
    parser.add_argument("--min-rating", default=0.0, type=float, help="Note minimale si la colonne rating est presente")
    parser.add_argument("--marketplace-fee-rate", type=float, help="Frais marketplace estimes. Par defaut: Amazon 15%%, Bol.com 15%%")
    parser.add_argument("--payment-fee-rate", default=DEFAULT_PAYMENT_FEE_RATE, type=float, help="Frais de paiement estimes")
    parser.add_argument("--fixed-cost", default=DEFAULT_FIXED_COST, type=float, help="Cout fixe par vente: emballage, retour, prep, etc.")
    parser.add_argument("--vat-rate", default=DEFAULT_VAT_RATE, type=float, help="TVA estimee sur le cout d'achat, 0.20 = 20%%")
    parser.add_argument("--customs-rate", default=DEFAULT_CUSTOMS_RATE, type=float, help="Droits de douane estimes sur le cout d'achat")
    parser.add_argument("--return-rate", default=DEFAULT_RETURN_RATE, type=float, help="Provision retours/SAV sur le prix de vente")
    parser.add_argument("--safety-margin-rate", default=DEFAULT_SAFETY_MARGIN_RATE, type=float, help="Marge de securite sur le prix de vente")
    parser.add_argument("--top", default=20, type=int, help="Nombre d'opportunites affichees dans le terminal")
    return parser


def resolve_seller_source(args: argparse.Namespace) -> tuple[Path, str, float]:
    selected = args.marketplace
    if selected == "auto":
        if args.bol and args.amazon:
            raise ValueError("Utilise --marketplace amazon ou --marketplace bol si --amazon et --bol sont fournis.")
        if args.bol:
            selected = "bol"
        elif args.amazon:
            selected = "amazon"
        else:
            raise ValueError("Fournis un fichier --amazon ou --bol.")

    if selected == "bol":
        if not args.bol:
            raise ValueError("--marketplace bol necessite --bol.")
        return args.bol, "bol", args.marketplace_fee_rate if args.marketplace_fee_rate is not None else DEFAULT_BOL_FEE_RATE

    if not args.amazon:
        raise ValueError("--marketplace amazon necessite --amazon.")
    return args.amazon, "amazon", args.marketplace_fee_rate if args.marketplace_fee_rate is not None else DEFAULT_MARKETPLACE_FEE_RATE


def main() -> int:
    args = build_parser().parse_args()

    seller_path, seller_source, marketplace_fee_rate = resolve_seller_source(args)
    seller_products = load_products(seller_path, seller_source)
    aliexpress_products = load_products(args.aliexpress, "aliexpress")
    approved_matches = load_approved_matches(args.approved_matches)
    opportunities = find_opportunities(
        seller_products,
        aliexpress_products,
        min_similarity=args.min_similarity,
        auto_validate_score=args.auto_validate_score,
        min_profit=args.min_profit,
        min_roi=args.min_roi,
        min_rating=args.min_rating,
        marketplace_fee_rate=marketplace_fee_rate,
        payment_fee_rate=args.payment_fee_rate,
        fixed_cost=args.fixed_cost,
        vat_rate=args.vat_rate,
        customs_rate=args.customs_rate,
        return_rate=args.return_rate,
        safety_margin_rate=args.safety_margin_rate,
        approved_matches=approved_matches,
    )

    write_opportunities(args.output, opportunities)

    print(f"{len(opportunities)} opportunite(s) trouvee(s). Export: {args.output}")
    for item in opportunities[: args.top]:
        print(
            f"- {item.net_profit:.2f} EUR | ROI {item.roi * 100:.1f}% | "
            f"{item.match_status} score {item.match_score:.2f} | "
            f"{item.seller.source} {item.sell_price:.2f} EUR -> AliExpress {item.buy_cost:.2f} EUR | "
            f"{item.seller.title[:80]}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
