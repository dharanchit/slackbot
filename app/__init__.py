from flask import Flask, request, Response,jsonify
from app.config import load_config
from app.config.database import connect_db, close_db_connection
from app.utils.validators import ChatTextValidator
from app.utils import ChatBotModalView, updatedChatView, chatPreview, styledResponse, get_project_id,format_response_message
from app.layer import generation_ops
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import ssl
# from app.integrations.langchain.classifier import generate_suggestions
from app.integrations.intelligence.predictions import generate_results

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


def generate_database_connection_string(config_variables):
    username, password = config_variables['DB_USER'],config_variables['DB_PASSWORD']
    # username, password = "admin", "admin"
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
        form_data = request.form.to_dict(flat=True)
        payload = form_data.get("payload", None)
        if not payload:
            triggerId = request.form.get('trigger_id')
            return trigger_modal(triggerId)
        else:
            payload = json.loads(payload)
            payload_type = payload.get("type", None)
            if payload_type == "view_submission":
                return handle_modal_callback(payload)
            else:
                return jsonify(styledResponse('*Bot not triggered!* :sad:'))
    
    def trigger_modal(trigger_id):
        try:
            response = web_client.views_open(
                trigger_id=trigger_id,
                view=ChatBotModalView()
            )
            return jsonify(styledResponse('Bot triggered successfully! :rocket:'))
        except SlackApiError as e:
            return jsonify(styledResponse(f"*Error opening modal: {e.response['error']}!*"))

    def handle_modal_callback(payload):
        try:
            block_id = payload['view']['blocks'][0]['block_id']
            submitted_value = payload['view']['state']['values'][block_id]['input-action']['value']
            app.logger.info(payload)
            app.logger.info("PayloadPayloadPayloadPayloadPayloadPayloadPayload")
            app.logger.info(submitted_value)
            app.logger.info("USER MESSAGEE+++++++")

            prediction = generate_results([submitted_value.upper()])
            app.logger.info(prediction)
            app.logger.info("Prediction")

            is_valid = ChatTextValidator(prediction)
            if not is_valid:
                return jsonify(updatedChatView(f"Failed to identify your request"))
            
            project_id = get_project_id(prediction[0]["TicketNo"], prediction[0]["Text"])
            app.logger.info(project_id)
            app.logger.info("project_id")
            if not project_id:
                return jsonify(updatedChatView("Failed to identify your project id"))


            body = {
                "ASSIGN_TO": prediction[0]["Assignee"],
                "TICKET_NO": prediction[0]["TicketNo"],
                "PROJECT_ID": project_id,
                "SUMMARY": "TEST Ticket",
                "ACTION_TYPE": "CREATE" if prediction[0]["Task"] == "Create Ticket" else "UPDATE",
                "DESCRIPTION": "",
                "SUB_TYPE": "TICKET"
            }

            # generation_ops(body)

            send_chat_message(payload['user']['id'] ,prediction)
            return jsonify(updatedChatView(submitted_value))
        except SlackApiError as e:
            return jsonify(styledResponse(f"*Error opening modal: {e.response['error']}!*"))

    def send_chat_message(user_id, prediction):
        response_message = format_response_message(prediction)
        try:
            response = web_client.chat_postMessage(
                channel=user_id,
                text=response_message
            )
            return jsonify(styledResponse('Bottt'))
        except SlackApiError as e:
            return jsonify(styledResponse("Error sending chat message:"))
    
    return app
