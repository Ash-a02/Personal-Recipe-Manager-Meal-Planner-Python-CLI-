from datetime import date, datetime, timedelta
from recipe_manager import RecipeManager
from models import Recipe

class RecipeManagerCLI:
    def __init__(self):
        self.manager = RecipeManager()
    
    def display_menu(self):
        print("\n" + "="*50)
        print("🍳 PERSONAL RECIPE MANAGER & MEAL PLANNER")
        print("="*50)
        print("1. Add New Recipe")
        print("2. View All Recipes")
        print("3. Search Recipes")
        print("4. Filter Recipes")
        print("5. Rate Recipe")
        print("6. Plan Meals")
        print("7. Generate Shopping List")
        print("8. View Statistics")
        print("9. Exit")
        print("-"*50)
    
    def get_user_input(self, prompt: str, input_type: type = str):
        """Get validated user input"""
        while True:
            try:
                value = input(prompt)
                if input_type == int:
                    return int(value)
                elif input_type == float:
                    return float(value)
                return value
            except ValueError:
                print(f"Please enter a valid {input_type.__name__}")
    
    def add_recipe(self):
        print("\n📝 Adding New Recipe")
        print("-" * 25)
        
        name = self.get_user_input("Recipe name: ")
        category = self.get_user_input("Category (e.g., Main Course, Dessert, Appetizer): ")
        prep_time = self.get_user_input("Prep time (minutes): ", int)
        cook_time = self.get_user_input("Cook time (minutes): ", int)
        servings = self.get_user_input("Number of servings: ", int)
        
        # Get ingredients
        print("\nEnter ingredients (type 'done' when finished):")
        ingredients = {}
        while True:
            ingredient = input("Ingredient name (or 'done'): ")
            if ingredient.lower() == 'done':
                break
            amount = input(f"Amount of {ingredient}: ")
            ingredients[ingredient] = amount
        
        # Get instructions
        print("\nEnter cooking instructions (type 'done' when finished):")
        instructions = []
        step = 1
        while True:
            instruction = input(f"Step {step} (or 'done'): ")
            if instruction.lower() == 'done':
                break
            instructions.append(instruction)
            step += 1
        
        # Create and add recipe
        recipe = Recipe(name, ingredients, instructions, prep_time, cook_time, servings, category)
        
        # Add tags
        tags_input = input("Add tags (comma-separated, optional): ")
        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(',')]
            for tag in tags:
                recipe.add_tag(tag)
        
        self.manager.add_recipe(recipe)
    
    def view_recipes(self):
        print("\n📚 All Recipes")
        print("-" * 15)
        
        if not self.manager.recipes:
            print("No recipes found. Add some recipes first!")
            return
        
        for i, recipe in enumerate(self.manager.recipes.values(), 1):
            print(f"\n{i}. {recipe.name}")
            print(f"   Category: {recipe.category}")
            print(f"   Time: {recipe.total_time()} minutes ({recipe.prep_time} prep + {recipe.cook_time} cook)")
            print(f"   Servings: {recipe.servings}")
            print(f"   Rating: {'⭐' * recipe.rating if recipe.rating > 0 else 'Not rated'}")
            if recipe.tags:
                print(f"   Tags: {', '.join(recipe.tags)}")
    
    def search_recipes(self):
        print("\n🔍 Search Recipes")
        print("-" * 17)
        
        query = input("Enter search term (name, ingredient, or tag): ")
        results = self.manager.search_recipes(query)
        
        if results:
            print(f"\nFound {len(results)} recipe(s):")
            for recipe in results:
                print(f"- {recipe.name} ({recipe.category})")
        else:
            print("No recipes found matching your search.")
    
    def filter_recipes(self):
        print("\n🔧 Filter Recipes")
        print("-" * 16)
        print("1. By Category")
        print("2. By Maximum Cooking Time")
        print("3. Top Rated")
        
        choice = self.get_user_input("Choose filter option: ", int)
        
        if choice == 1:
            category = input("Enter category: ")
            results = self.manager.filter_by_category(category)
        elif choice == 2:
            max_time = self.get_user_input("Maximum cooking time (minutes): ", int)
            results = self.manager.filter_by_time(max_time)
        elif choice == 3:
            results = self.manager.get_top_rated()
        else:
            print("Invalid option")
            return
        
        if results:
            print(f"\nFound {len(results)} recipe(s):")
            for recipe in results:
                print(f"- {recipe.name} ({recipe.total_time()} min, Rating: {recipe.rating})")
        else:
            print("No recipes found with the specified criteria.")
    
    def rate_recipe(self):
        print("\n⭐ Rate Recipe")
        print("-" * 13)
        
        if not self.manager.recipes:
            print("No recipes to rate!")
            return
        
        # Show recipes
        recipes_list = list(self.manager.recipes.values())
        for i, recipe in enumerate(recipes_list, 1):
            print(f"{i}. {recipe.name} (Current rating: {recipe.rating})")
        
        try:
            choice = self.get_user_input("Select recipe number: ", int) - 1
            if 0 <= choice < len(recipes_list):
                rating = self.get_user_input("Enter rating (1-5): ", int)
                recipes_list[choice].set_rating(rating)
                self.manager.save_data()
                print(f"Rating updated for '{recipes_list[choice].name}'!")
            else:
                print("Invalid recipe selection.")
        except (ValueError, IndexError):
            print("Invalid input.")
    
    def plan_meals(self):
        print("\n📅 Meal Planning")
        print("-" * 15)
        
        if not self.manager.recipes:
            print("No recipes available for meal planning!")
            return
        
        # Show available recipes
        recipes_list = list(self.manager.recipes.values())
        print("Available recipes:")
        for i, recipe in enumerate(recipes_list, 1):
            print(f"{i}. {recipe.name}")
        
        try:
            date_str = input("Enter date (YYYY-MM-DD): ")
            meal_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            meal_type = input("Meal type (breakfast/lunch/dinner): ").lower()
            recipe_choice = self.get_user_input("Select recipe number: ", int) - 1
            
            if 0 <= recipe_choice < len(recipes_list):
                recipe_id = recipes_list[recipe_choice].id
                self.manager.meal_plan.add_meal(meal_date, meal_type, recipe_id)
                self.manager.save_data()
                print(f"Meal planned: {recipes_list[recipe_choice].name} for {meal_type} on {meal_date}")
            else:
                print("Invalid recipe selection.")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
    
    def generate_shopping_list(self):
        print("\n🛒 Shopping List Generator")
        print("-" * 26)
        
        try:
            start_date_str = input("Start date (YYYY-MM-DD): ")
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            days = self.get_user_input("Number of days: ", int)
            
            shopping_list = self.manager.generate_shopping_list(start_date, days)
            
            if shopping_list:
                print(f"\n🛒 Shopping List ({start_date} to {start_date + timedelta(days=days-1)}):")
                print("-" * 40)
                for ingredient, amounts in shopping_list.items():
                    print(f"• {ingredient}:")
                    for amount in amounts:
                        print(f"  - {amount}")
            else:
                print("No meals planned for the specified period.")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
    
    def view_statistics(self):
        print("\n📊 Recipe Statistics")
        print("-" * 19)
        
        stats = self.manager.get_recipe_stats()
        
        if "message" in stats:
            print(stats["message"])
            return
        
        print(f"Total Recipes: {stats['total_recipes']}")
        print(f"Average Cooking Time: {stats['average_cooking_time']} minutes")
        print(f"Average Rating: {stats['average_rating']}/5")
        print(f"Rated Recipes: {stats['rated_recipes']}")
        
        print("\nRecipes by Category:")
        for category, count in stats['categories'].items():
            print(f"  • {category}: {count}")
    
    def run(self):
        """Main application loop"""
        print("Welcome to Personal Recipe Manager & Meal Planner!")
        
        while True:
            self.display_menu()
            try:
                choice = self.get_user_input("Select an option (1-9): ", int)
                
                if choice == 1:
                    self.add_recipe()
                elif choice == 2:
                    self.view_recipes()
                elif choice == 3:
                    self.search_recipes()
                elif choice == 4:
                    self.filter_recipes()
                elif choice == 5:
                    self.rate_recipe()
                elif choice == 6:
                    self.plan_meals()
                elif choice == 7:
                    self.generate_shopping_list()
                elif choice == 8:
                    self.view_statistics()
                elif choice == 9:
                    print("Thanks for using Recipe Manager! Goodbye! 👋")
                    break
                else:
                    print("Invalid option. Please choose 1-9.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
