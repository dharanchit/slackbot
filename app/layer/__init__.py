from app.layer.routing import JiraOps

def generation_ops(body):
    #  Pass request text via NLP to identify action
    # Get Below Data from request_text
    
    act_on = "JIRA"

    # act_on, meta_data = "JIRA", {"ASSIGN_TO": "siddhant.mishra@tifin.com", "ACTION_TYPE": "CREATE", "DESCRIPTION": "TEST DESCRIPTION", "SUMMARY": "TEST TICKET"}
    if act_on == "JIRA":
        JiraOps(meta_data=body)

    return {}