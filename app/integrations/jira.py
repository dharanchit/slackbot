from app.config import load_config
from requests.auth import HTTPBasicAuth
import requests
import json


class Jira:
    def __init__(self):
        config = load_config()
        token = config.get("JIRA_TOKEN")
        jira_email = config.get("JIRA_EMAIL")
        self.auth = HTTPBasicAuth(jira_email, token)
        # Project URL in env
        self.project_url = "https://magnifi-dev.atlassian.net"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def get_list_of_user(self):
        response = requests.get(f"{self.project_url}/rest/api/3/users/search", headers=self.headers, auth=self.auth)
        data =response.text if response and response.text else None
        if not data:
            return None, "Unable to fetch users"
        
        users_list = json.loads(data)
        # With this get user id and Push users list to redis

        return users_list
    
    def get_all_projects_list(self):
        response = requests.get(f"{self.project_url}/rest/api/3/project/search", headers=self.headers, auth=self.auth)
        data =response.text if response and response.text else None
        if not data:
            return None, "Unable to fetch users"
        
        projects_list = json.loads(data)
        # With this get user id and Push users list to redis
        
        return projects_list

    def create_ticket(self, info):
        # API To create issue
        payload = {
            "fields": {
                "assignee": {
                    "id": info.creatorId,
                },
                "description": {
                    "content": [
                        {
                            "text": info.description,
                            "type": "text"
                        }
                    ]
                },
                "labels": info.labels,
                "project": info.project,
                "reporter": info.creatorId,
            },
        }
        response = requests.get(f"{self.project_url}/rest/api/3/issue", headers=self.headers, auth=self.auth, payload=json.dumps(payload))
        if response.status_code == 201:
            return True, 200, "Created Issue"
        
        return False, 500, response.text
