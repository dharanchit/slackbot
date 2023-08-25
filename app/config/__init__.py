import os
def load_config():
    return {
        "DB_USER": os.getenv("MONGO_DB_USER"),
        "DB_PASSWORD": os.getenv("MONGO_DB_PASSWORD"),
        "JIRA_TOKEN":os.getenv("JIRA_TOKEN")
    }
