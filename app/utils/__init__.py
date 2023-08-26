def chatBotModalView():
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
                        "text": f"your response recorded: {response}",
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