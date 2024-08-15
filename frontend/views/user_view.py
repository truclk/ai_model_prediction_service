from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render


def account(request):
    context = {"client_id": request.session.get("client_id"), "client_name": request.session.get("client_name")}

    return render(request, "user/account.html", context)


def user_logout(request):
    # Log out the user.
    logout(request)
    return render(request, "home.html")


def user_login(request):
    if request.method == "POST":
        # Process the request if posted data are available
        username = request.POST["username"]
        password = request.POST["password"]
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return redirect("account")
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(
                request,
                "user/login.html",
                {"error_message": "Incorrect username and / or password."},
            )
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, "user/login.html")
