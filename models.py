import json
import uuid
from datetime import datetime, date
from typing import List, Dict, Optional

class Recipe:
    def __init__(self, name: str, ingredients: Dict[str, str], instructions: List[str], 
                 prep_time: int, cook_time: int, servings: int, category: str = "Main Course"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.ingredients = ingredients  # {"ingredient": "amount"}
        self.instructions = instructions
        self.prep_time = prep_time  # in minutes
        self.cook_time = cook_time  # in minutes
        self.servings = servings
        self.category = category
        self.created_date = datetime.now().isoformat()
        self.rating = 0
        self.tags = []
    
    def total_time(self) -> int:
        return self.prep_time + self.cook_time
    
    def add_tag(self, tag: str):
        if tag not in self.tags:
            self.tags.append(tag)
    
    def set_rating(self, rating: int):
        if 1 <= rating <= 5:
            self.rating = rating
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'servings': self.servings,
            'category': self.category,
            'created_date': self.created_date,
            'rating': self.rating,
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        recipe = cls(
            data['name'], data['ingredients'], data['instructions'],
            data['prep_time'], data['cook_time'], data['servings'], data['category']
        )
        recipe.id = data['id']
        recipe.created_date = data['created_date']
        recipe.rating = data.get('rating', 0)
        recipe.tags = data.get('tags', [])
        return recipe

class MealPlan:
    def __init__(self):
        self.meals = {}  # {date_string: {meal_type: recipe_id}}
    
    def add_meal(self, date_obj: date, meal_type: str, recipe_id: str):
        date_str = date_obj.isoformat()
        if date_str not in self.meals:
            self.meals[date_str] = {}
        self.meals[date_str][meal_type] = recipe_id
    
    def get_meals_for_date(self, date_obj: date) -> Dict[str, str]:
        return self.meals.get(date_obj.isoformat(), {})
    
    def to_dict(self) -> dict:
        return {'meals': self.meals}
    
    @classmethod
    def from_dict(cls, data: dict):
        meal_plan = cls()
        meal_plan.meals = data.get('meals', {})
        return meal_plan
