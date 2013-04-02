#-*- coding: utf-8 -*-
from models import MyHttpRequest


class SaveRequestMiddleware(object):
    """
    Doc strings will be here
    """
    def process_request(self, request):
        MyHttpRequest.objects.create_from_request(request)
        return None
