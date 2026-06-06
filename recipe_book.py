import json
import os
import time
import datetime

FILE_NAME = "recipes.json"

# Load recipes from file
def load_recipes():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

# Save recipes to file
def save_recipes(recipes):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(recipes, f, indent=4, ensure_ascii=False)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    clear_screen()
    print("="*70)
    print(f"          {title.center(60)}")
    print("="*70)

def add_recipe():
    print_header("ADD NEW RECIPE")
    name = input("   Recipe Name          : ").strip()
    if not name:
        print("❌ Recipe name is required!")
        time.sleep(1.5)
        return
    
    ingredients = []
    print("   Ingredients (type 'done' when finished):")
    while True:
        ing = input("     • ").strip()
        if ing.lower() == 'done':
            break
        if ing:
            ingredients.append(ing)
    
    instructions = input("\n   Instructions (one line): ").strip()
    try:
        prep_time = int(input("   Prep Time (minutes)  : "))
    except:
        prep_time = 0
    try:
        servings = int(input("   Servings             : "))
    except:
        servings = 1
    
    category = input("   Category (Breakfast, Lunch, Dinner, Dessert, etc.): ").strip() or "General"
    
    recipe = {
        "id": len(load_recipes()) + 1,
        "name": name,
        "category": category,
        "ingredients": ingredients,
        "instructions": instructions,
        "prep_time": prep_time,
        "servings": servings,
        "date_added": datetime.date.today().strftime("%Y-%m-%d")
    }
    
    recipes = load_recipes()
    recipes.append(recipe)
    save_recipes(recipes)
    
    print(f"\n✅ Recipe '{name}' added successfully!")
    time.sleep(2)

def view_all_recipes():
    print_header("ALL RECIPES")
    recipes = load_recipes()
    if not recipes:
        print("   No recipes yet. Add some delicious ones!")
    else:
        for r in recipes:
            print(f"[{r['id']:02d}] {r['name']:<35} | {r['category']:<15} | {r['prep_time']} mins")
    input("\nPress Enter to continue...")

def view_recipe():
    print_header("VIEW RECIPE")
    recipes = load_recipes()
    if not recipes:
        print("No recipes available.")
        input("\nPress Enter...")
        return
    
    try:
        rid = int(input("Enter Recipe ID: "))
        recipe = next((r for r in recipes if r["id"] == rid), None)
        
        if recipe:
            print(f"\n🍳 {recipe['name'].upper()}")
            print(f"Category     : {recipe['category']}")
            print(f"Prep Time    : {recipe['prep_time']} minutes")
            print(f"Servings     : {recipe['servings']}")
            print(f"Date Added   : {recipe['date_added']}")
            print("\nIngredients:")
            for ing in recipe['ingredients']:
                print(f"   • {ing}")
            print("\nInstructions:")
            print(f"   {recipe['instructions']}")
        else:
            print("❌ Recipe not found!")
    except:
        print("Invalid ID!")
    input("\nPress Enter to continue...")

def search_recipe():
    print_header("SEARCH RECIPES")
    query = input("Search by name or ingredient: ").strip().lower()
    recipes = load_recipes()
    found = [r for r in recipes if query in r['name'].lower() or 
             any(query in ing.lower() for ing in r['ingredients'])]
    
    if found:
        print(f"\nFound {len(found)} recipe(s):\n")
        for r in found:
            print(f"[{r['id']:02d}] {r['name']}")
    else:
        print("No matching recipes found.")
    input("\nPress Enter to continue...")

def main():
    while True:
        print_header("🍳 RECIPE BOOK APP")
        print("   1. Add New Recipe")
        print("   2. View All Recipes")
        print("   3. View Recipe Details")
        print("   4. Search Recipes")
        print("   5. Exit")
        print("="*70)
        
        choice = input("\n   Enter your choice (1-5): ").strip()
        
        if choice == "1":
            add_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            view_recipe()
        elif choice == "4":
            search_recipe()
        elif choice == "5":
            print_header("GOODBYE!")
            print("   Happy Cooking! 👨‍🍳👩‍🍳")
            time.sleep(2)
            break
        else:
            print("   ❌ Invalid choice!")
            time.sleep(1)

if __name__ == "__main__":
    main()