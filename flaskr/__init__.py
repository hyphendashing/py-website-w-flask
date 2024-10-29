import os
from flask import Flask

# Create and configure the app.
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),)

    # Load instance config (if it exists).
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    # Load test config (if instance config doesn't exist).
    else:
        app.config.from_mapping(test_config)

    # Check for isntance folder.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Test page with a "Hello World" message.
    # URL: http://127.0.0.1:5000/hello
    @app.route("/hello")
    def hello():
        return "Hello World!"
    
    from . import database 
    database.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    return app