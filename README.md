# 🍳 Personal Recipe Manager & Meal Planner (Python CLI)

A command-line application built with Python to help users manage personal recipes, plan meals, generate shopping lists, and track cooking statistics. Ideal for home cooks and meal preppers looking to stay organized.

---

## 📌 Features

- ✅ Add, view, search, and filter recipes
- ⭐ Rate recipes and assign custom tags
- 📅 Plan meals for any date and meal type (breakfast/lunch/dinner)
- 🛒 Auto-generate shopping lists based on planned meals
- 📊 View recipe analytics: average cooking time, ratings, and category distribution
- 💾 Data persistence using JSON (recipes and meal plans saved across sessions)

---

## 🛠 Tech Stack

- **Language:** Python 3
- **Design:** Object-Oriented Programming (OOP)
- **Storage:** JSON (file-based persistence)
- **Interface:** Command-Line Interface (CLI)

---

## 📂 Project Structure

├── main.py # Entry point, loads samples, starts CLI
├── cli_interface.py # Handles all user interactions and menu options
├── recipe_manager.py # Core logic for managing recipes and meal plans
├── models.py # Data models: Recipe and MealPlan
└── recipes_data.json # (Auto-generated) stores user data persistently


---

## ▶️ How to Run

Make sure you have Python 3 installed.

```bash
# Step 1: Clone the repository
git clone https://github.com/yourusername/recipe-manager-cli.git
cd recipe-manager-cli

# Step 2: Run the application
python main.py
