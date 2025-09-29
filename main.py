from cli_interface import RecipeManagerCLI
from recipe_manager import RecipeManager
from models import Recipe

def add_sample_recipes(manager: RecipeManager):
    """Add some sample recipes for demonstration"""
    
    # Sample Recipe 1: Spaghetti Carbonara
    carbonara = Recipe(
        name="Spaghetti Carbonara",
        ingredients={
            "spaghetti": "400g",
            "eggs": "4 large",
            "parmesan cheese": "100g grated",
            "pancetta": "150g diced",
            "black pepper": "to taste",
            "salt": "to taste"
        },
        instructions=[
            "Cook spaghetti in salted boiling water until al dente",
            "Fry pancetta until crispy",
            "Beat eggs with grated parmesan and black pepper",
            "Drain pasta, reserving some pasta water",
            "Mix hot pasta with pancetta and egg mixture",
            "Add pasta water if needed for creaminess",
            "Serve immediately with extra parmesan"
        ],
        prep_time=10,
        cook_time=15,
        servings=4,
        category="Main Course"
    )
    carbonara.add_tag("italian")
    carbonara.add_tag("pasta")
    carbonara.add_tag("quick")
    carbonara.set_rating(5)
    
    # Sample Recipe 2: Chocolate Chip Cookies
    cookies = Recipe(
        name="Chocolate Chip Cookies",
        ingredients={
            "flour": "2 1/4 cups",
            "butter": "1 cup softened",
            "brown sugar": "3/4 cup",
            "white sugar": "3/4 cup",
            "eggs": "2 large",
            "vanilla extract": "2 tsp",
            "baking soda": "1 tsp",
            "salt": "1 tsp",
            "chocolate chips": "2 cups"
        },
        instructions=[
            "Preheat oven to 375°F (190°C)",
            "Cream butter and sugars together",
            "Beat in eggs and vanilla",
            "Mix in flour, baking soda, and salt",
            "Stir in chocolate chips",
            "Drop spoonfuls on baking sheet",
            "Bake for 9-11 minutes until golden brown",
            "Cool on baking sheet for 5 minutes"
        ],
        prep_time=15,
        cook_time=11,
        servings=24,
        category="Dessert"
    )
    cookies.add_tag("baking")
    cookies.add_tag("sweet")
    cookies.add_tag("family-friendly")
    cookies.set_rating(4)
    
    # Sample Recipe 3: Greek Salad
    greek_salad = Recipe(
        name="Greek Salad",
        ingredients={
            "tomatoes": "4 large, chopped",
            "cucumber": "1 large, sliced",
            "red onion": "1/2 medium, sliced",
            "feta cheese": "200g cubed",
            "olives": "1/2 cup kalamata",
            "olive oil": "1/4 cup",
            "lemon juice": "2 tbsp",
            "oregano": "1 tsp dried",
            "salt": "to taste",
            "pepper": "to taste"
        },
        instructions=[
            "Chop tomatoes and place in large bowl",
            "Add sliced cucumber and red onion",
            "Add feta cheese cubes and olives",
            "Whisk together olive oil, lemon juice, and oregano",
            "Pour dressing over salad",
            "Season with salt and pepper",
            "Toss gently and serve immediately"
        ],
        prep_time=15,
        cook_time=0,
        servings=4,
        category="Salad"
    )
    greek_salad.add_tag("healthy")
    greek_salad.add_tag("vegetarian")
    greek_salad.add_tag("mediterranean")
    greek_salad.set_rating(4)
    
    # Add recipes to manager
    manager.add_recipe(carbonara)
    manager.add_recipe(cookies)
    manager.add_recipe(greek_salad)
    
    print("✅ Sample recipes added successfully!")

def main():
    """Main function to run the Recipe Manager application"""
    print("🍳 Initializing Personal Recipe Manager...")
    
    # Create CLI interface
    app = RecipeManagerCLI()
    
    # Check if this is first run (no existing data)
    if not app.manager.recipes:
        print("\n🎉 Welcome! It looks like this is your first time using the Recipe Manager.")
        add_samples = input("Would you like to add some sample recipes to get started? (y/n): ")
        
        if add_samples.lower() in ['y', 'yes']:
            add_sample_recipes(app.manager)
    
    # Run the main application
    app.run()

if __name__ == "__main__":
    main()
