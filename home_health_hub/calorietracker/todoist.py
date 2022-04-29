from todoist_api_python.api import TodoistAPI


def add_to_todoist(item, integration_profile):

    api = TodoistAPI(integration_profile.todoist_api_key)
    try:
        task = api.add_task(
            content=item,
            project_id=integration_profile.todoist_target_project,
        )
        print(task.content)
        return True
    except Exception as error:
        print(error)
        return False
