import os
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

ANIMALS_FILE = "animals.json"
ADOPTIONS_FILE = "adoptions.json"


def init_json_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("[]")

def main():
    init_json_file(ANIMALS_FILE)
    init_json_file(ADOPTIONS_FILE)

    animals = load_animals(ANIMALS_FILE)
    adoptions = load_adoptions(ADOPTIONS_FILE)

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

            if not animal:
                print(f"Nem található állat ezzel az ID-val: {animal_id}")
            elif not animal["available"]:
                print(f"Sajnáljuk, {animal['name']} már nem elérhető!")
            else:
                adopter_name = input("Add meg az örökbefogadó nevét: ").strip()
                if not adopter_name:
                    print("Hiba: Az örökbefogadó neve nem lehet üres!")
                    continue

                uj_orokbefogadas = create_adoption(animal, adopter_name)
                add_adoption(adoptions, uj_orokbefogadas)

                fake_adoption_for_update = {
                    "animal_id": animal_id,
                    "available": False,
                }
                update_animal_status(animals, fake_adoption_for_update)

                save_animals(ANIMALS_FILE, animals)
                save_adoptions(ADOPTIONS_FILE, adoptions)
                print(
                    f"Sikeres örökbefogadás! {animal['name']} új gazdája: {adopter_name}."
                )

        elif valasztas == "4":
            print("Kilépés... Szép napot!")
            break
        else:
            print("Érvénytelen választás, kérlek 1 és 4 között válassz!")


if __name__ == "__main__":
    main()
