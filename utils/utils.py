from django.http import Http404, HttpRequest


def check_user(func):
    def wrapper(*args, **kwargs):
        req: HttpRequest = args[1]
        if req.user.username == "":
            raise Http404()
        return func(*args, **kwargs)
    return wrapper
