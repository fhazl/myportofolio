from main.permissions import is_editor

def user_roles(request):
    return {"is_editor": is_editor(request.user)}