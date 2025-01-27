
def get_workspace_slug(workspace_name):
    return workspace_name.replace(" ", "-")


def upload_books(txt_file_list):
    return []


def workspace_update_embeddings(work_space_name, txt_file_list):
    slug = get_workspace_slug(work_space_name)
    pass


def do_feed_books(work_space_name, txt_file_list):
    file_location_list = upload_books(txt_file_list)

