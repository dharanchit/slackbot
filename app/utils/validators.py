from app.constants.projects import PROJECT_NAME_LIST, PROJECT_ID_LIST

def ChatTextValidator(prediction):

    if not prediction:
        return False
    
    prediction = prediction[0]
    if "Task" in prediction and prediction["Task"] == "Update Ticket" and not prediction["TicketNo"]:
        return False
    
    return True
