from flask import Flask, request, Response,jsonify
from app.config import load_config
from app.config.database import connect_db, close_db_connection
from app.utils.validators import BotChatValidator
from app.utils import chatBotModalView
from app.utils import updatedChatView
from app.utils import styledResponse
from app.layer import handle_request
import requests
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import ssl

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def generate_database_connection_string(config_variables):
    username, password = config_variables['DB_USER'],config_variables['DB_PASSWORD']
    return f"mongodb+srv://{username}:{password}@cluster0.9jgzm.mongodb.net/?retryWrites=true&w=majority"

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    config_vars = load_config()
    mongo_uri = generate_database_connection_string(config_vars)
    SLACK_BOT_TOKEN = config_vars['SLACK_BOT_TOKEN']
    web_client = WebClient(token=SLACK_BOT_TOKEN,ssl=ssl_context)
    with app.app_context():
        app.logger.info('Establishing database connection')
        connect_db(mongo_uri)

    @app.teardown_appcontext
    def teardown_db(exception):
        app.logger.warning(exception)
        close_db_connection()
        app.logger.warning("Closing Database Connection")
           
    @app.route('/bot', methods=['POST'])
    def handle_bot_interaction():
        if(request.form.to_dict(flat=True).get('payload') == None):
            triggerId = request.form.get('trigger_id')
            return trigger_modal(triggerId)
        else:
            payload = json.loads(request.form.to_dict(flat=True).get('payload'))
            if(payload['type'] == 'view_submission'):
                return handle_modal_callback(payload)
        return jsonify(styledResponse('*Bot not triggered!* :sad:'))

    def trigger_modal(trigger_id):
        try:
            response = web_client.views_open(
                trigger_id=trigger_id,
                view=chatBotModalView()
            )
            return jsonify(styledResponse('*Bot triggered successfully!* :rocket:'))
        except SlackApiError as e:
            return jsonify(styledResponse(f"*Error opening modal: {e.response['error']}!*"))
    def handle_modal_callback(payload):
        block_id = payload['view']['blocks'][0]['block_id']
        submitted_value = payload['view']['state']['values'][block_id]['input-action']['value']
        return jsonify(updatedChatView(submitted_value))
        return None

    @app.post("/v1/bot")
    def generate_results():
        body = request.data
        data = json.loads(body)

        # Validate the data
        is_valid, error_msg  = BotChatValidator(data)

        if not is_valid:
            raise Exception(error_msg)

        response = handle_request(data.get("text"))
        return Response(status=200)

    return app
