import json

def load_animals(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_animals(file_path, animals):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(animals, file, indent=2, ensure_ascii=False)

def show_animals(animals):

    if not animals:
        print("Nincsenek állatok a listában.")
        return

    print("\n--- Menedékhely Állatai ---")
    for animal in animals:
        status = "Elérhető" if animal["available"] else "Nem elérhető"
        print(f"ID: {animal['id']} | Név: {animal['name']} ({animal['type']}) | Kor: {animal['age']} év | Státusz: {status}")


def get_available_animals(animals):
    
    return [animal for animal in animals if animal["available"]]


def find_animal_by_id(animals, animal_id):
    
    for animal in animals:
        if animal["id"] == animal_id:
            return animal
    return None  


def update_animal_status(animals, adoption):
    
    target_id = adoption.get("animal_id")
    new_status = adoption.get("available")
    
    animal = find_animal_by_id(animals, target_id)
    
    if animal:
        animal["available"] = new_status
        return animal
    else:
        print(f"Hiba: Nem található állat a következő ID-val: {target_id}")
        return None
