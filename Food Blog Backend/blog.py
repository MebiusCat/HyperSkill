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

            for table_name, table_elem in self.food_data.items():
                for elem in table_elem:
                    cursor = data.cursor()
                    cursor.execute(f'''
                    INSERT OR IGNORE INTO {table_name}
                    VALUES (?,?);
                    ''', (None, elem))


my_base = RecipeDatabase()
