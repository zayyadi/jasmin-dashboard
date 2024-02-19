import json
import os
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import requests

from main.core.smpp import UserStat
from main.core.models.setting import UserModel
from django.core.mail import send_mail


def user_email_notification(request, uid):
    subject = "User Status Notification"
    message = f"User with ID {uid} is in a stopped state. Please take action."
    all_query = UserModel.objects.all()
    query = all_query.filter(uid=uid)
    from_email = os.getenv("MAIL_FROM")  # Replace with your email
    url = [obj.url for obj in query]

    # Extract and clean email addresses
    admin_email_list = []
    for obj in query:
        try:
            email_addresses = json.loads(obj.email_list)
            # Ensure email_addresses is a list
            if isinstance(email_addresses, list):
                admin_email_list.extend(email_addresses)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {obj.email_list}: {e}")

    # print(f"cleaned email: {admin_email_list}")

    for urls in url:
        try:
            response = requests.get(urls)
            # Process the response as needed
            print(f"Response from {urls}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            # Handle exceptions (e.g., connection error)
            print(f"Error with {urls}: {e}")

    send_mail(subject, message, from_email, admin_email_list)

    return JsonResponse({"message": "Email notification sent successfully"})


@login_required
def user_stats_view(request):
    return render(request, "web/content/user_stats.html")


@login_required
def user_stat_view_manage(request):
    args, res_status, res_message = {}, 400, _("Sorry, Command does not matched.")
    stats = None
    if request.GET and request.is_ajax():
        s = request.GET.get("s")
        if s in ["list", "user"]:
            stats = UserStat(telnet=request.telnet)

        if stats:
            if s == "list":
                args = stats.list_u()
                res_status, res_message = 200, _("ok")

            elif s == "user":
                args = stats.list_user(uid=request.GET.get("uid"))
                res_status, res_message = 200, _("ok")

    if isinstance(args, dict):
        args["status"] = res_status
        args["message"] = str(res_message)
        # print(f"args: {args}")

    else:
        res_status = 200
        # print(f"args: {args}")
    return HttpResponse(
        json.dumps(args), status=res_status, content_type="application/json"
    )
