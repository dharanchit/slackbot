from app.constants.projects import PROJECT_NAME_LIST, PROJECT_ID_LIST

def BotChatValidator(request_obj):
    if "text" not in request_obj:
        return False, "Key is not present", (-1, -1)

    if not request_obj["text"]:
        return False, "No text input", (-1, -1)
    
    project_id_idx = -1
    project_name_idx = -1

    for i, val in enumerate(PROJECT_ID_LIST):
        if val in request_obj["text"]:
            project_id_idx = i
            break
    
    if project_id_idx == -1:
        for i, val in enumerate(PROJECT_NAME_LIST):
            if val in request_obj["text"]:
                project_name_idx = i
                break
    
    if project_id_idx == -1 and project_name_idx == -1:
        return False, "No Module Defined in Text String", (-1, -1)
    
    return True, None, (project_id_idx, project_name_idx)
