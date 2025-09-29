import json
import os
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict
from models import Recipe, MealPlan

class RecipeManager:
    def __init__(self, data_file: str = "recipes_data.json"):
        self.data_file = data_file
        self.recipes = {}  # {recipe_id: Recipe}
        self.meal_plan = MealPlan()
        self.load_data()
    
    def load_data(self):
        """Load recipes and meal plans from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                
                # Load recipes
                for recipe_data in data.get('recipes', []):
                    recipe = Recipe.from_dict(recipe_data)
                    self.recipes[recipe.id] = recipe
                
                # Load meal plan
                meal_plan_data = data.get('meal_plan', {})
                self.meal_plan = MealPlan.from_dict(meal_plan_data)
                
                print(f"Loaded {len(self.recipes)} recipes from {self.data_file}")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def save_data(self):
        """Save recipes and meal plans to JSON file"""
        try:
            data = {
                'recipes': [recipe.to_dict() for recipe in self.recipes.values()],
                'meal_plan': self.meal_plan.to_dict()
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Data saved to {self.data_file}")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def add_recipe(self, recipe: Recipe):
        """Add a new recipe"""
        self.recipes[recipe.id] = recipe
        self.save_data()
        print(f"Recipe '{recipe.name}' added successfully!")
    
    def search_recipes(self, query: str) -> List[Recipe]:
        """Search recipes by name, ingredients, or tags"""
        query = query.lower()
        results = []
        
        for recipe in self.recipes.values():
            # Search in name
            if query in recipe.name.lower():
                results.append(recipe)
                continue
            
            # Search in ingredients
            if any(query in ingredient.lower() for ingredient in recipe.ingredients.keys()):
                results.append(recipe)
                continue
            
            # Search in tags
            if any(query in tag.lower() for tag in recipe.tags):
                results.append(recipe)
        
        return results
    
    def filter_by_category(self, category: str) -> List[Recipe]:
        """Filter recipes by category"""
        return [recipe for recipe in self.recipes.values() 
                if recipe.category.lower() == category.lower()]
    
    def filter_by_time(self, max_time: int) -> List[Recipe]:
        """Filter recipes by maximum total cooking time"""
        return [recipe for recipe in self.recipes.values() 
                if recipe.total_time() <= max_time]
    
    def get_top_rated(self, limit: int = 5) -> List[Recipe]:
        """Get top rated recipes"""
        rated_recipes = [recipe for recipe in self.recipes.values() if recipe.rating > 0]
        return sorted(rated_recipes, key=lambda x: x.rating, reverse=True)[:limit]
    
    def generate_shopping_list(self, start_date: date, days: int = 7) -> Dict[str, List[str]]:
        """Generate shopping list for meal plan"""
        shopping_list = defaultdict(list)
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            meals = self.meal_plan.get_meals_for_date(current_date)
            
            for meal_type, recipe_id in meals.items():
                if recipe_id in self.recipes:
                    recipe = self.recipes[recipe_id]
                    for ingredient, amount in recipe.ingredients.items():
                        shopping_list[ingredient].append(f"{amount} (for {recipe.name})")
        
        return dict(shopping_list)
    
    def get_recipe_stats(self) -> Dict[str, any]:
        """Get statistics about recipes"""
        if not self.recipes:
            return {"message": "No recipes found"}
        
        total_recipes = len(self.recipes)
        categories = defaultdict(int)
        total_time = 0
        rated_count = 0
        total_rating = 0
        
        for recipe in self.recipes.values():
            categories[recipe.category] += 1
            total_time += recipe.total_time()
            if recipe.rating > 0:
                rated_count += 1
                total_rating += recipe.rating
        
        avg_time = total_time / total_recipes
        avg_rating = total_rating / rated_count if rated_count > 0 else 0
        
        return {
            "total_recipes": total_recipes,
            "categories": dict(categories),
            "average_cooking_time": round(avg_time, 1),
            "average_rating": round(avg_rating, 1),
            "rated_recipes": rated_count
        }
