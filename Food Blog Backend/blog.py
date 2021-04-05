import sys
import sqlite3


class RecipeDatabase:
    food_data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
                 "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
                 "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}
    
    def __init__(self):
        if len(sys.argv) > 1:
            self.__database__ = sys.argv[1]
        else:
            self.__database__ = 'food_blog.db'
        self.database()

    def database(self):
        with sqlite3.connect(self.__database__) as data:
            data.executescript('''
            CREATE TABLE IF NOT EXISTS meals (
            meal_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            meal_name TEXT NOT NULL UNIQUE        
            );            
            CREATE TABLE IF NOT EXISTS ingredients (
            ingredient_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            ingredient_name TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS measures (
            measure_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            measure_name TEXT UNIQUE
            );   
            ''')

            for meal in self.food_data['meals']:
                cursor = data.cursor()
                cursor.execute('''
                INSERT OR IGNORE INTO meals (meal_name)
                VALUES (?);
                ''', (meal,))

            for ingredient in self.food_data['ingredients']:
                cursor = data.cursor()
                cursor.execute('''
                INSERT OR IGNORE INTO ingredients (ingredient_name)
                VALUES (?);
                ''', (ingredient,))

            for measure in self.food_data['measures']:
                cursor = data.cursor()
                cursor.execute('''
                INSERT OR IGNORE INTO measures (measure_name)
                VALUES (?);
                ''', (measure,))


my_base = RecipeDatabase()
