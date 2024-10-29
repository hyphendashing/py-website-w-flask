import sqlite3
import click

# "import g" is a special object that is unique for each request and is used to store data that might be accessed by multiple functions during the request.
# "import current_app" is another special object that points to the Flask application handling the request. "get_db()" will be called when the application has been created and is handling a request.
from flask import current_app, g

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES) # Establish a connection to the file pointed at by the DATABASE configuration key.
        g.db.row_factory = sqlite3.Row # Tells the connection to return rows that behave like dicts which allows accessing the columns by name.
    return g.db

# Check if a connection was created by checking if g.db was set. If a connection exists, it is closed.
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    db = get_db() # Returns a database connection.

    with current_app.open_resource("schema.sql") as f: # Read the schema.sql file and execute through the database connection created on row 22.
        db.executescript(f.read().decode("utf8"))

# Define a command line command called "init-db" that calls the init_db() function and shows a success message to the user.
@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Database Initialized!")

def init_app(app):
    app.teardown_appcontext(close_db) # Calls the close_db() function when cleaning up after returning the response.
    app.cli.add_command(init_db_command) # Adds a new command that can be called with the flask command

