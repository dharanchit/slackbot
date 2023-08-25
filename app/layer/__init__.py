from app.layer.routing import JiraOps

def handle_request(request_text):
    #  Pass request text via NLP to identify action
    # Get Below Data from request_text

    act_on, meta_data = "JIRA", {"ASSIGN_TO": "siddhant.mishra@tifin.com", "ACTION_TYPE": "CREATE"}
    if act_on == "JIRA":
        JiraOps(meta_data=meta_data)

    return {}