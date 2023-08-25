from flask import Flask, request, Response
from app.config import load_config
from app.config.database import connect_db, close_db_connection


def generate_database_connection_string(config_variables):
    # f""
    return ""

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    config_vars = load_config()
    print(config_vars, "config_varsconfig_varsconfig_vars")
    mongo_uri = generate_database_connection_string(config_vars)
    with app.app_context():
        app.logger.info('Establishing database connection')
        connect_db(mongo_uri)

    @app.teardown_appcontext
    def teardown_db(exception):
        app.logger.warning(exception)
        close_db_connection()
        app.logger.warning("Closing Database Connection")

    @app.get("/test")
    def get_request():
        query_string = request.args.get("message")
        return Response(status=200)

    return app

