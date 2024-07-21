from backend_api.models import Client
from backend_api.models import ClientUser
from django.shortcuts import redirect
from django.urls import resolve

PUBLIC_URLS = [
    "fe/home/",  # Add all your public URLs here
    "fe/login/",
]


def client_require_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        request_path = resolve(request.path_info).route
        if request_path not in PUBLIC_URLS:
            if not request.user.is_authenticated:
                return redirect("/fe/login/")

        # Code to be executed for each request before
        # the view (and later middleware) are called.
        client_id = request.session.get("client_id", None)

        # Client hasn't pass in, check if user has any clients.
        if not client_id and request.user.is_authenticated:
            userclients = Client.objects.filter(clientuser__user=request.user)
            if len(userclients):
                client_id = userclients[0].pk
                request.session["client_id"] = client_id
        request.session["client_id"] = client_id
        response = get_response(request)
        return response

    return middleware
