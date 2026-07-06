# Outil d'arbitrage Amazon / Bol.com / AliExpress

Ce projet compare des prix Amazon ou Bol.com avec AliExpress a partir de fichiers CSV, puis calcule les opportunites avec marge nette et ROI.

Il ne scrape pas Amazon ou AliExpress directement. C'est volontaire: ces sites ont des protections et des conditions d'utilisation strictes. Utilise plutot des exports, des APIs autorisees, des flux fournisseurs, ou des donnees que tu as le droit d'exploiter.

## Format CSV

Colonnes obligatoires:

- `sku`
- `title`
- `price`

Colonnes optionnelles:

- `shipping`
- `url`
- `stock`
- `rating`
- `brand`
- `model`
- `ean`
- `variant`
- `dimensions`
- `weight_grams`

## Lancer l'exemple

Depuis ce dossier:

```powershell
python .\arbitrage.py --amazon .\examples\amazon.csv --aliexpress .\examples\aliexpress.csv --output .\opportunities.csv
```

Pour Bol.com:

```powershell
python .\arbitrage.py --bol .\examples\bol.csv --aliexpress .\examples\aliexpress.csv --output .\opportunities_bol.csv
```

Avec des correspondances validees manuellement:

```powershell
python .\arbitrage.py `
  --amazon .\examples\amazon.csv `
  --aliexpress .\examples\aliexpress.csv `
  --approved-matches .\examples\matches_valides.csv `
  --output .\opportunities.csv
```

Pour Bol.com avec correspondances validees:

```powershell
python .\arbitrage.py `
  --bol .\examples\bol.csv `
  --aliexpress .\examples\aliexpress.csv `
  --approved-matches .\examples\matches_bol_valides.csv `
  --output .\opportunities_bol.csv
```

## Options utiles

```powershell
python .\arbitrage.py `
  --amazon .\examples\amazon.csv `
  --aliexpress .\examples\aliexpress.csv `
  --min-profit 8 `
  --min-roi 0.35 `
  --min-similarity 0.45 `
  --auto-validate-score 0.85 `
  --marketplace-fee-rate 0.15 `
  --payment-fee-rate 0.03 `
  --fixed-cost 1.20 `
  --vat-rate 0.20 `
  --customs-rate 0.00 `
  --return-rate 0.05 `
  --safety-margin-rate 0.08 `
  --output .\opportunities.csv
```

Si tu fournis `--amazon` et `--bol` dans la meme commande, precise aussi `--marketplace amazon` ou `--marketplace bol`.

## Validation des produits

Le fichier `matches_valides.csv` permet de verrouiller les bons couples marketplace/AliExpress:

```csv
seller_sku,aliexpress_sku,status,note
AMZ-001,ALI-900,approved,Produit verifie manuellement
AMZ-999,ALI-999,rejected,Pas la meme variante
```

Les anciens noms `amazon_sku` et `bol_sku` sont aussi acceptes pour compatibilite.

Statuts acceptes:

- `approved`, `valid`, `valide`, `ok`
- `rejected`, `reject`, `rejete`, `no`, `non`

Sans ce fichier, l'outil utilise un score automatique base sur:

- titre
- EAN/UPC/GTIN
- marque
- modele
- variante
- dimensions
- poids

Les opportunites incertaines sortent avec `match_status = manual_review`.

## Interpretrer le resultat

Le fichier `opportunities.csv` contient:

- marketplace de vente: Amazon ou Bol.com
- prix de vente marketplace estime
- cout d'achat AliExpress, livraison incluse
- frais estimes
- couts additionnels estimes: TVA, douane, retours, marge de securite
- marge nette
- ROI
- score de correspondance produit
- statut de validation
- raisons du match
- flags de risque

Verifie toujours manuellement:

- que les produits sont vraiment identiques
- les delais de livraison
- la TVA, les droits de douane et les obligations locales
- les restrictions de marque, brevets, securite produit et conformite CE
- les regles Amazon/Bol.com concernant dropshipping, fulfillment, retours et factures

## Brancher de vraies sources

Le point d'entree est `load_products()` dans `arbitrage.py`. Tu peux remplacer la lecture CSV par:

- Amazon Product Advertising API
- Bol.com Retailer API ou exports vendeur Bol.com
- API partenaire ou outil de veille prix
- export AliExpress / fournisseur
- base interne de produits
