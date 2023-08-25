from flask import Flask, request, Response
from app.config import load_config
from app.config.database import connect_db, close_db_connection
import json
from app.utils.validators import BotChatValidator

def generate_database_connection_string(config_variables):
    username,password = config_variables['DB_USER'],config_variables['DB_PASSWORD']
    return f"mongodb+srv://{username}:{password}@cluster0.9jgzm.mongodb.net/?retryWrites=true&w=majority"

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    config_vars = load_config()
    mongo_uri = generate_database_connection_string(config_vars)
    with app.app_context():
        app.logger.info('Establishing database connection')
        connect_db(mongo_uri)

    @app.teardown_appcontext
    def teardown_db(exception):
        app.logger.warning(exception)
        close_db_connection()
        app.logger.warning("Closing Database Connection")

    @app.post("/v1/bot")
    def generate_results():
        body = request.data
        data = json.loads(body)

        # Validate the data
        is_valid, error_msg  = BotChatValidator(data)

        if not is_valid:
            raise Exception(error_msg)
        # Pass through NLP to understand text

        return Response(status=200)

    return app

