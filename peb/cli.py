"""Command line interface for peb calculations."""

import argparse
from typing import List

from .models import Building, Wall, Window, HeatingSystem
from .config import REGIONAL_CONFIG
from .calculations import energy_need, primary_energy, energy_score


def _prompt_float(message: str) -> float:
    return float(input(message))


def _prompt_walls(name: str) -> List[Wall]:
    nb = int(input(f"Nombre de {name} : "))
    items = []
    for i in range(nb):
        area = _prompt_float(f"Surface du {name[:-1]} {i + 1} (m²) : ")
        u_value = _prompt_float(f"Valeur U du {name[:-1]} {i + 1} : ")
        items.append(Wall(area=area, u_value=u_value))
    return items


def _prompt_windows() -> List[Window]:
    nb = int(input("Nombre de fenêtres : "))
    windows = []
    for i in range(nb):
        area = _prompt_float(f"Surface de la fenêtre {i + 1} (m²) : ")
        u_value = _prompt_float(f"Valeur U de la fenêtre {i + 1} : ")
        windows.append(Window(area=area, u_value=u_value))
    return windows


def _build_from_excel(path: str) -> Building:
    import pandas as pd

    df_build = pd.read_excel(path, sheet_name="building")
    floor_area = float(df_build.loc[0, "floor_area"])
    infiltration_rate = float(df_build.loc[0, "infiltration_rate"])
    heating_eff = float(df_build.loc[0, "heating_efficiency"])

    df_walls = pd.read_excel(path, sheet_name="walls")
    walls = [Wall(area=row["area"], u_value=row["u_value"]) for _, row in df_walls.iterrows()]

    df_windows = pd.read_excel(path, sheet_name="windows")
    windows = [Window(area=row["area"], u_value=row["u_value"]) for _, row in df_windows.iterrows()]

    return Building(
        floor_area=floor_area,
        infiltration_rate=infiltration_rate,
        walls=walls,
        windows=windows,
        heating=HeatingSystem(efficiency=heating_eff),
    )


def _build_interactive() -> Building:
    floor_area = _prompt_float("Surface chauffée (m²) : ")
    infiltration = _prompt_float("Taux d'infiltration (1/h) : ")
    heating_eff = _prompt_float("Rendement du chauffage (0-1) : ")
    walls = _prompt_walls("murs")
    windows = _prompt_windows()
    return Building(
        floor_area=floor_area,
        infiltration_rate=infiltration,
        walls=walls,
        windows=windows,
        heating=HeatingSystem(efficiency=heating_eff),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Calcul de performance énergétique")
    parser.add_argument(
        "--excel",
        help="Classeur Excel contenant les données du bâtiment",
    )
    parser.add_argument(
        "--region",
        default="wallonia",
        choices=list(REGIONAL_CONFIG.keys()),
        help="Région pour les calculs",
    )
    args = parser.parse_args()

    if args.excel:
        building = _build_from_excel(args.excel)
    else:
        building = _build_interactive()

    print("Besoin en énergie :", energy_need(building, args.region))
    print("Énergie primaire :", primary_energy(building, args.region))
    print("Score énergétique :", energy_score(building, args.region))


if __name__ == "__main__":
    main()
