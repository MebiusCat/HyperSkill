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
            PRAGMA foreign_keys = ON;
            CREATE TABLE IF NOT EXISTS serve (
            serve_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER NOT NULL,
            meal_id INTEGER NOT NULL,
            FOREIGN KEY(recipe_id) 
               REFERENCES recipes(recipe_id),
            FOREIGN KEY(meal_id) 
               REFERENCES meals(meal_id) 
            );               
            CREATE TABLE IF NOT EXISTS quantity (
            quantity_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            measure_id INTEGER NOT NULL,
            ingredient_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            recipe_id INTEGER NOT NULL,
            FOREIGN KEY(measure_id) 
               REFERENCES measures(measure_id),
            FOREIGN KEY(ingredient_id) 
               REFERENCES ingredients(ingredient_id),              
            FOREIGN KEY(recipe_id) 
               REFERENCES recipes(recipe_id)              
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
            return cursor.lastrowid

    def add_serve(self, recipe_id, meals):
        with sqlite3.connect(self.__database__) as data:
            for meal_id in meals:
                cursor = data.cursor()
                cursor.execute('''
                INSERT OR IGNORE INTO serve (recipe_id, meal_id)
                VALUES (?, ?);
                ''', (recipe_id, meal_id))

    def add_quantity(self, value, measure_id, ingredient_id, recipe_id):
        with sqlite3.connect(self.__database__) as data:
            cursor = data.cursor()
            cursor.execute('''
            INSERT OR IGNORE INTO quantity (recipe_id, ingredient_id, measure_id, quantity)
            VALUES (?, ?, ?, ?);
            ''', (recipe_id, ingredient_id, measure_id, value))

    def get_meals(self):
        with sqlite3.connect(self.__database__) as data:
            cursor = data.cursor()
            cursor.execute('''
            SELECT meal_id, meal_name
            FROM meals;
            ''')
            return cursor.fetchall()

    def get_ingredient(self, mask):
        with sqlite3.connect(self.__database__) as data:
            cursor = data.cursor()
            cursor.execute(f'''
            SELECT ingredient_id, ingredient_name
            FROM ingredients
            WHERE ingredient_name LIKE ?;
            ''', (f'%{mask}%',))
            result = cursor.fetchall()
            if len(result) == 1:
                return result[0][0]
        return None

    def get_measure(self, mask):
        with sqlite3.connect(self.__database__) as data:
            cursor = data.cursor()
            cursor.execute(f'''
            SELECT measure_id
            FROM measures
            WHERE measure_name LIKE ?;
            ''', (f'{mask}%',))
            result = cursor.fetchall()
            if len(result) == 1:
                return result[0][0]
        return None

    def get_empty_measure(self):
        with sqlite3.connect(self.__database__) as data:
            cursor = data.cursor()
            cursor.execute(f'''
            SELECT measure_id
            FROM measures
            WHERE measure_name LIKE ?;
            ''', ('',))
            result = cursor.fetchall()
            if len(result) == 1:
                return result[0][0]
        return None

    def populate_book(self):
        print('Pass the empty recipe name to exit.')
        while True:
            name = input('Recipe name: ')
            if not name:
                exit()
            desc = input('Recipe description: ')
            recipe_id = self.add_recipe(name, desc)

            meals_db = self.get_meals()
            for id_, meal in meals_db:
                print(f'{id_}) {meal}  ', end='')
            prompt_ = '\nEnter proposed meals separated by a space:'
            result = list(map(int, input(prompt_).split()))
            self.add_serve(recipe_id, result)
            ingredients_prompt = 'Input quantity of ingredient <press enter to stop>'
            while True:
                row_ = input(ingredients_prompt).split()
                if not row_:
                    break

                if len(row_) == 2:
                    value = int(row_[0])
                    measure = self.get_empty_measure()
                    ingredient = self.get_ingredient(row_[1])
                else:
                    value = int(row_[0])
                    measure = self.get_measure(row_[1])
                    ingredient = self.get_ingredient(row_[2])
                if not measure:
                    print('The measure is not conclusive!')
                    continue
                elif not ingredient:
                    print('The ingredient is not conclusive!')
                    continue
                self.add_quantity(value, measure, ingredient, recipe_id)


my_base = RecipeDatabase()
