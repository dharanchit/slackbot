from app.integrations.jira import Jira

def JiraOps(meta_data):
    # Replace Hard coded thing with None
    action_type = meta_data.get("ACTION_TYPE", "CREATE")
    jira = Jira()
    if action_type == "CREATE" and meta_data.get("SUB_TYPE", "TICKET").upper() == "TICKET":
        project_id = meta_data.get("PROJECT_ID")
        # if not project_id:
        #     raise Exception("No Project Id Found")
        data = {
            "creatorId": "62ac4659bf7afc006f3dc26d",
            "description": meta_data.get("DESCRIPTION", ""),
            "labels": meta_data.get("LABELS", []),
            "project": {
                "id": project_id
            },
        }
        # jira.create_ticket(data)
        jira.get_all_projects_list()
    return "DONE"