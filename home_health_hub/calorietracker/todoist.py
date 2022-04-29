from todoist_api_python.api import TodoistAPI


def add_to_todoist(item, integration_profile):

    api = TodoistAPI(integration_profile.todoist_api_key)
    try:
        task = api.add_task(
            content=item,
            project_id=integration_profile.todoist_target_project,
        )
        print(task)
        return True
    except Exception as error:
        print(error)
        return False


def bulk_add_to_todoist(item_list, integration_profile):
    api = TodoistAPI(integration_profile.todoist_api_key)
    try:
        for item in item_list:
            task = api.add_task(
                content=item,
                project_id=integration_profile.todoist_target_project,
            )
            print(task)
        return True
    except Exception as error:
        print(error)
        return False
