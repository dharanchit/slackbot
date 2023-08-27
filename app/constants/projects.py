PROJECTS_LIST = [
  {
    "id": "10348",
    "project_name": "magnifi",
    "key": "MC"
  },
  {
    "id": "10337",
    "project_name": "wealth",
    "key": "WC"
  }
]

PROJECT_NAME_LIST = [i["project_name"].upper() for i in PROJECTS_LIST]
PROJECT_ID_LIST = [i["key"].upper() for i in PROJECTS_LIST]
PROJECT_NAME_ID_MAPPING = {i["key"]: i["id"] for i in PROJECTS_LIST}
