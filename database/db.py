import sqlite3

# create database class
class DB:
    def __init__(self):
        # connect to database and create cursor to interact with database
        self.db = sqlite3.connect("database/runner.db")
        self.cur = self.db.cursor()

        notes_table = """
            CREATE TABLE IF NOT EXISTS notes(
                title TEXT NOT NULL PRIMARY KEY, 
                body TEXT NOT NULL, 
                priority TEXT NOT NULL, 
                date NUMERIC NOT NULL
                )"""

        categories_table = """CREATE TABLE IF NOT EXISTS categories(
            name TEXT NOT NULL PRIMARY KEY,
            active INT NOT NULL)"""

        files_table = """
        CREATE TABLE IF NOT EXISTS files(
            name TEXT NOT NULL,
            path TEXT NOT NULL, 
            active INT NOT NULL,
            category_name TEXT NOT NULL,
            file_id INT PRIMARY KEY,
            FOREIGN KEY(category_name) REFERENCES categories(name)
            )"""
        
        settings_table = """
            CREATE TABLE IF NOT EXISTS settings(
                old_color TEXT NOT NULL, 
                new_color TEXT NOT NULL, 
                font TEXT NOT NULL, 
                note_order TEXT NOT NULL)
        """

        # create the necessary tables
        self.create_table(notes_table)
        self.create_table(categories_table)
        self.create_table(files_table)
        self.create_table(settings_table)

    # save methode to save to database
    def save(self, table, data):

        if type(data) != list:
            data = [data]

        # determine how many fields there are based on the table passed in
        values = ""
        if table == "notes":
            values = "(?, ?, ?, ?)"
        elif table == "files":
            values = "(?, ?, ?, ?, ?)"
        elif table == "categories":
            values = "(?, ?)"

        query = f"""
            INSERT INTO {table} VALUES {values}
        """

        # execute the query to insert the data and commit the changes
        self.cur.executemany(query, data)
        self.db.commit()
        self.db.close()

    # read method to read data from the database
    def read(self, table, field=None, value=None):
        
        if field == None and value == None:
            query = ""
            if table == "notes":
                order = DB().read("settings")[0][3]
                query = f"SELECT * FROM notes ORDER BY {order}"
            elif table != "settings":
                query = f"""SELECT * FROM {table} ORDER BY name;"""
            else:
                query = f"""SELECT * FROM {table}"""
            self.cur.execute(query)
        else:
            query = f"""SELECT * FROM {table} WHERE {field} = (?) ORDER BY name"""
            self.cur.execute(query, (value,))

        # execute the query and get all the data
        data = self.cur.fetchall()

        # close the connection and return the data
        self.db.close()
        return data

    # delete method to delete data from the database
    def delete(self, table, name):
        # the label is used to find the relevant field in the table passed in
        label = "title" if table == "notes" else "name"

        # initialize the query
        query = ""

        # check if the table is files or notes because they will have a different query
        if table == "files" or table == "notes":       
            query = f"""DELETE FROM {table} WHERE {label} = (?)"""
        
        elif table == "categories":
            query = f"""DELETE FROM categories WHERE {label} = (?)"""

            # second query to delete all the files if the entire category is deleted
            query2 = f"""DELETE FROM files WHERE category_name = (?)"""
            self.cur.execute(query2, (name,))

        self.cur.execute(query, (name,))

        self.db.commit()
        self.db.close()
    
    # Get a single item
    def get_item(self, table, name):

        # identify the label depending on the table
        label = "name" if table == "categories" else "title"

        query = f"""
            SELECT * FROM {table} WHERE {label} = (?)
        """

        self.cur.execute(query, (name,))
        data = self.cur.fetchone()
        self.db.close()
        return data
    
    # name refers to the old name. the name you want to delete. the new name will be in the data object
    def update(self, table, name, data):
        # Delete the data and re upload the updated data.
        # This is different from the delete method because the user can't delete a note or category from
        # their respective windows this method will only apply when the user updates the information

        label = "category_name" if table == "files" else "name" if table == "categories" else "title"
        query = f"""DELETE FROM {table} WHERE {label} = (?)"""

        self.cur.execute(query, (name,))
        self.save(table, data)
    
    def update_category_state(self, name, state):
        query = f"UPDATE categories SET active = {state} WHERE name = (?)"
        self.cur.execute(query, (name,))
        self.db.commit()
        self.db.close()
    
    def update_settings(self, data):
        fields = ("old_color", "new_color", "font", "note_order")
        for i in range(len(fields)):
            query = f"""
                UPDATE settings SET {fields[i]} = (?);
            """
            self.cur.execute(query, (data[i],))
        self.db.commit()
        self.db.close()
        
    def first_state(self, reset=False):
        self.cur.execute("SELECT new_color FROM settings")
        data = self.cur.fetchone()
        if not data:
            self.cur.execute("INSERT INTO settings (old_color, new_color, font, note_order) VALUES ('#007EA6', '#007EA6', 'Nunito SemiBold', 'title')")
            self.db.commit()
        elif reset:
            self.cur.execute("UPDATE settings SET old_color = '#007EA6', new_color = '#007EA6', font = 'Nunito SemiBold', note_order = 'title'")
            self.db.commit()
        self.db.close()

    def create_table(self, command):
        self.cur.execute(command)

