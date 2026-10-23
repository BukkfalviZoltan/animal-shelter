
import json
from pathlib import Path

from shelter.adoptions import (
    add_adoption,
    create_adoption,
    load_adoptions,
    save_adoptions,
    show_adoptions,
)

from shelter.animals import (
    find_animal_by_id,
    load_animals,
    save_animals,
    show_animals,
    update_animal_status,
)


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

ANIMALS_FILE = DATA_DIR / "animals.json"
ADOPTIONS_FILE = DATA_DIR / "adoptions.json"


def init_json_file(file_path):
    """Létrehozza a JSON-fájlt, ha még nem létezik."""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump([], file, indent=2, ensure_ascii=False)


def main():
    
    init_json_file(ANIMALS_FILE)
    init_json_file(ADOPTIONS_FILE)

    try:
        animals = load_animals(ANIMALS_FILE)
        adoptions = load_adoptions(ADOPTIONS_FILE)
    except json.JSONDecodeError:
        print("Hiba: valamelyik JSON-fájl tartalma érvénytelen.")
        return

    while True:
        print("\n=== MENEDÉKHELY REGISZTRÁCIÓ ===")
        print("1. Összes állat listázása")
        print("2. Örökbefogadások listázása")
        print("3. Állat örökbefogadása")
        print("4. Kilépés")

        valasztas = input("Válassz egy menüpontot (1-4): ").strip()

        if valasztas == "1":
            show_animals(animals)

        elif valasztas == "2":
            print("\n--- Örökbefogadások ---")
            show_adoptions(adoptions)

        elif valasztas == "3":
            print("\n--- Új örökbefogadás ---")

            try:
                animal_id = int(input("Add meg az állat ID-ját: "))
            except ValueError:
                print("Hiba: Az ID-nak számnak kell lennie!")
                continue

            animal = find_animal_by_id(animals, animal_id)

            if animal is None:
                print(f"Nem található állat ezzel az ID-val: {animal_id}")

            elif not animal["available"]:
                print(f"Sajnáljuk, {animal['name']} már nem elérhető!")

            else:
                adopter_name = input(
                    "Add meg az örökbefogadó nevét: "
                ).strip()

                if not adopter_name:
                    print("Hiba: Az örökbefogadó neve nem lehet üres!")
                    continue

                uj_orokbefogadas = create_adoption(
                    animal, adopter_name
                )
                add_adoption(adoptions, uj_orokbefogadas)

                adoption_for_update = {
                    "animal_id": animal_id,
                    "available": False,
                }

                update_animal_status(animals, adoption_for_update)

                save_animals(ANIMALS_FILE, animals)
                save_adoptions(ADOPTIONS_FILE, adoptions)

                print(
                    f"Sikeres örökbefogadás! "
                    f"{animal['name']} új gazdája: {adopter_name}."
                )

        elif valasztas == "4":
            print("Kilépés... Szép napot!")
            break

        else:
            print("Érvénytelen választás, kérlek 1 és 4 között válassz!")


if __name__ == "__main__":
    main()
