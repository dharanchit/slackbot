from app.constants.projects import *

def ChatBotModalView():
    payload = {
        "type": "modal",
        "callback_id": "modal-identifier",
        "title": {
            "type": "plain_text",
            "text": "Hitman"
        },
        "blocks": [{
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "input-action",
                "multiline":True
            },
            "label": {
                "type": "plain_text",
                "text": "Hello im Hitman, specify your commands"
                    }
            }],
            "submit": {
            "type": "plain_text",
            "text": "Submit"
            }
    }

    return payload

def updatedChatView(response):
    payload =  {
        "response_action": "update",
        "view": {
            "type": "modal",
            "title": {"type": "plain_text", "text": "Command executed"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": f"Response: {response}",
                        },
                    }
                ],
            },
        }
    return payload

def styledResponse(response):
    payload={
        "response_type": "ephemeral",  # Display the message only to the user who triggered the command
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": response
                }
            }
        ]
    }
    return payload

def chatPreview(response):
    payload={
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": response,
                    "emoji": True
                }
            }
        ]
    }
    return payload

def identify_project_from_message(message):
    project_id_idx, project_name_idx  = -1, -1
    for i, val in enumerate(PROJECT_ID_LIST):
        if val in message.upper():
            project_id_idx = i
            break

    if project_id_idx == -1:
        for i, val in enumerate(PROJECT_NAME_LIST):
            if val in message.upper():
                project_name_idx = i
                break
    
    if project_id_idx != -1:
        return PROJECTS_LIST[project_id_idx]["id"]
    if project_name_idx != -1:
        return PROJECTS_LIST[project_name_idx]["id"]

    return None

def get_project_id(ticker_number, message):
    if not ticker_number:
        project_id = identify_project_from_message(message)
        return project_id
    project_id = ticker_number.split("-")[0].upper()
    return PROJECT_NAME_ID_MAPPING.get(project_id, None)
