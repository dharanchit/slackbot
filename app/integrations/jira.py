from app.config import load_config
from requests.auth import HTTPBasicAuth
import requests
import json
import logging

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

    def create_ticket(self, info):
        # API To create issue
        payload = {
            "fields": {
                "assignee": {
                    "id": info["assignee_id"]
                },
                "description": {
                    "content": [
                        {
                        "content": [
                            {
                            "text": info["description"],
                            "type": "text"
                            }
                        ],
                        "type": "paragraph"
                        }
                    ],
                    "type": "doc",
                    "version": 1
                },
                "issuetype": {
                    "name": "Task"
                },
                "project": info["project"],
                "summary": info["summary"]
            },
        }
        response = requests.post(f"{self.project_url}/rest/api/3/issue", headers=self.headers, auth=self.auth, data=json.dumps(payload))

        if response.status_code == 201:
            return True, 200, "Created Issue"
        
        return False, 500, response.text
    
