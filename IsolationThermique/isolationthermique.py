# -*- coding: utf-8 -*-
"""Calculs de déperdition thermique simplifiés."""
from typing import Dict


def pertes_parois(coeffs_u: Dict[str, float], surfaces: Dict[str, float]) -> Dict[str, float]:
    """Calcule les déperditions pour chaque paroi: U * A."""
    return {name: coeffs_u[name] * surfaces.get(name, 0.0) for name in coeffs_u}


def pertes_totales_parois(coeffs_u: Dict[str, float], surfaces: Dict[str, float]) -> float:
    """Somme des déperditions pour toutes les parois."""
    return sum(pertes_parois(coeffs_u, surfaces).values())


def pertes_ponts_thermiques(psi: Dict[str, float], longueurs: Dict[str, float]) -> Dict[str, float]:
    """Calcule les déperditions liées aux ponts thermiques: ψ * l."""
    return {name: psi[name] * longueurs.get(name, 0.0) for name in psi}


def pertes_totales_ponts_thermiques(psi: Dict[str, float], longueurs: Dict[str, float]) -> float:
    """Somme des pertes par ponts thermiques."""
    return sum(pertes_ponts_thermiques(psi, longueurs).values())


def coefficient_global(coeffs_u: Dict[str, float], surfaces: Dict[str, float],
                       psi: Dict[str, float], longueurs: Dict[str, float]) -> float:
    """Calcule le coefficient global de déperdition thermique."""
    return (
        pertes_totales_parois(coeffs_u, surfaces)
        + pertes_totales_ponts_thermiques(psi, longueurs)
    )


if __name__ == "__main__":
    # Exemple d'utilisation
    u = {
        "mur_nord": 0.4,
        "mur_sud": 0.35,
        "toit": 0.25,
        "plancher": 0.3,
    }

    a = {
        "mur_nord": 20.0,
        "mur_sud": 20.0,
        "toit": 30.0,
        "plancher": 30.0,
    }

    psi = {
        "plancher_mur": 0.1,
        "toit_mur": 0.08,
    }

    l = {
        "plancher_mur": 15.0,
        "toit_mur": 20.0,
    }

    pertes_paroi = pertes_parois(u, a)
    pertes_ponts = pertes_ponts_thermiques(psi, l)

    print("Pertes par paroi (U*A) :", pertes_paroi)
    print("Σ(U*A) =", pertes_totales_parois(u, a), "W/K")
    print("Pertes ponts thermiques (ψ*l) :", pertes_ponts)
    print("Σ(ψ*l) =", pertes_totales_ponts_thermiques(psi, l), "W/K")
    print("Coefficient global :", coefficient_global(u, a, psi, l), "W/K")
