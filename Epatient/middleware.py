import re
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout

class LoginRequiredMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        path = request.path_info.lstrip('/')
        print(path)
        if path.find("admin/") != -1:
            return None
        if path == 'sign-out':
            return None

        flag1 = True
        try:
            email = request.session['useremail']
            phone_number = request.session['phone_number']
        except KeyError:
            flag1 = False

        flag2 = False
        if path in settings.LOGIN_EXEMPT_URLS:
            flag2 = True

        if flag1 and flag2:
            return redirect('main:dashboard')
        elif flag1 or flag2:
            return None
        return redirect(settings.LOGIN_URL)
class UserTypeRequiredMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
    
    def __call__(self,request):
        response = self.get_response(request)
        return response
    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path_info.lstrip('/')
        