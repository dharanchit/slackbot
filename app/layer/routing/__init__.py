from app.integrations.jira import Jira

def JiraOps(meta_data):
    # Replace Hard coded thing with None
    action_type = meta_data.get("ACTION_TYPE", "CREATE")

    project_id = meta_data.get("PROJECT_ID")

    jira = Jira()
    if action_type == "CREATE" and meta_data.get("SUB_TYPE", "TICKET").upper() == "TICKET":

        data = {
            "creatorId": "62ac4659bf7afc006f3dc26d",
            "description": meta_data.get("DESCRIPTION", ""),
            "summary": meta_data.get("SUMMARY", ""),
            "project": {
                "id": project_id
            },
        }
        jira.create_ticket(data)
    elif action_type == "UPDATE":
        return "DONE"
    return "DONE"