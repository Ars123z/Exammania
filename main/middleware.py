# redirect_middleware.py
from django.shortcuts import redirect

class RedirectToHomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/':
            return redirect('/home/')
        return self.get_response(request)
