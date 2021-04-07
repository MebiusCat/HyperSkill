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
        self.populate_book()

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
            CREATE TABLE IF NOT EXISTS recipes (
            recipe_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            recipe_name TEXT NOT NULL,
            recipe_description TEXT
            );             
            ''')

            for table_name, table_elem in self.food_data.items():
                for elem in table_elem:
                    cursor = data.cursor()
                    cursor.execute(f'''
                    INSERT OR IGNORE INTO {table_name}
                    VALUES (?,?);
                    ''', (None, elem))

    def add_recipe(self, name, description):
        with sqlite3.connect(self.__database__) as data:
            cursor = data.cursor()
            cursor.execute('''
            INSERT OR IGNORE INTO recipes (recipe_name, recipe_description)
            VALUES (?, ?);
            ''', (name, description))

    def populate_book(self):
        print('Pass the empty recipe name to exit.')
        while True:
            name = input('Recipe name: ')
            if not name:
                exit()
            desc = input('Recipe description: ')
            self.add_recipe(name, desc)


my_base = RecipeDatabase()
