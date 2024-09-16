from uuid import uuid4

def request_post_email(group, request) -> str:
    email = request.POST.get('email')
    if not email:
        email = str(uuid4())

    return email

def request_data_email(group, request) -> str:
    email = request.data.get('email')
    if not email:
        email = str(uuid4())

    return email

def request_post_username(group, request) -> str:
    username = request.POST.get('username')
    if not username:
        username = str(uuid4())

    return username
