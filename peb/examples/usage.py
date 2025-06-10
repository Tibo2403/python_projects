"""Example script showing how to use the peb package."""

from peb import (
    Building,
    Wall,
    Window,
    HeatingSystem,
    energy_need,
    primary_energy,
    energy_score,
    export_certificate,
)


def main() -> None:
    building = Building(
        walls=[Wall(area=100, u_value=0.3)],
        windows=[Window(area=20, u_value=1.2)],
        heating=HeatingSystem(efficiency=0.9),
    )

    region = "wallonia"
    print("Energy need:", energy_need(building, region))
    print("Primary energy:", primary_energy(building, region))
    print("Score:", energy_score(building, region))

    export_certificate(building, region, "certificate.pdf", "certificate.xml")
    print("Certificate exported.")


if __name__ == "__main__":
    main()
