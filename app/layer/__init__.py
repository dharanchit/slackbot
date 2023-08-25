from app.layer.routing import JiraOps

def handle_request(request_text, index_match):
    #  Pass request text via NLP to identify action
    # Get Below Data from request_text

    act_on, meta_data = "JIRA", {"ASSIGN_TO": "siddhant.mishra@tifin.com", "ACTION_TYPE": "CREATE", "DESCRIPTION": "TEST DESCRIPTION", "SUMMARY": "TEST TICKET"}
    if act_on == "JIRA":
        JiraOps(meta_data=meta_data, match_tuple=index_match)

    return {}