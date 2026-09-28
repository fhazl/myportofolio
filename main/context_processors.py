from main.permissions import is_editor

def user_roles(request):
    if request.user.is_authenticated:
        return {"is_editor": request.user.groups.filter(name="Editor").exists()}
    return {"is_editor": False}