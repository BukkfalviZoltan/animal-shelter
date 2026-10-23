import json


def load_adoptions(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_adoptions(file_path, adoptions):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(adoptions, file, indent=2, ensure_ascii=False)


def create_adoption(animal, adopter_name):
    return {
        "animal_id": animal["id"],
        "animal_name": animal["name"],
        "adopter": adopter_name,
    }


def add_adoption(adoptions, adoption):
    adoptions.append(adoption)


def show_adoptions(adoptions):
    if not adoptions:
        print("Még nincs orökbefogadás.")
        return

    for adoption in adoptions:
        print(
            f"#{adoption['animal_id']} {adoption['animal_name']} "
            f"- örökbefogadó: {adoption['adopter']}"
        )
