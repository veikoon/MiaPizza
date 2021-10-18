import sqlite3
connection = sqlite3.connect("data.sql")
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE Pizzas (
        Pizzaid INTEGER PRIMARY KEY,
        PizzaName TEXT
        )
""")
cursor.execute("""
    CREATE TABLE Ingredients (
        Ingredientid INTEGER PRIMARY KEY,
        IngredientName TEXT,
        IngredientQuantity INTEGER
        )
""")
cursor.execute("""
    CREATE TABLE IngredientsList (
        Pizzaid INTEGER,
        Ingredientid INTEGER,
        Quantity INTGER
        )
""")
cursor.execute("""
    INSERT INTO Pizzas VALUES 
    (1, 'Reine')
""")
cursor.execute("""
    INSERT INTO Ingredients VALUES 
    (1, 'Tomate', 0),
    (2, 'Jambon', 0),
    (3, 'Emmental', 0),
    (4, 'Mozza', 0)
""")
cursor.execute("""
    INSERT INTO IngredientsList VALUES 
    (1, 1, 1),
    (1, 2, 70),
    (1, 3, 45),
    (1, 4, 70)
""")
connection.commit()