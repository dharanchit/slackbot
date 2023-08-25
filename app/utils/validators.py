def BotChatValidator(request_obj):
    if "text" not in request_obj:
        return False, "Key is not present"
    if not request_obj["text"]:
        return False, "No text input"
    
    return True, None
