from app.integrations.jira import Jira
from app.constants.projects import PROJECTS_LIST

def JiraOps(meta_data, match_tuple):
    # Replace Hard coded thing with None
    action_type = meta_data.get("ACTION_TYPE", "CREATE")

    index_match = None
    if match_tuple[0] != -1:
        index_match = match_tuple[0]
    else:
        index_match = match_tuple[1]

    project_id = PROJECTS_LIST[index_match].get("id")

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