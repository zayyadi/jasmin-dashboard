import os
import requests
import json

from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from main.core.models.setting import Settings
from main.core.smpp import Stats

from django.core.mail import send_mail


def send_email_notification(request, cid):
    subject = "Connector Status Notification"
    message = f"Connector with ID {cid} is in a stopped state. Please take action."
    all_query = Settings.objects.all()
    query = all_query.filter(cid=cid)
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

    print(f"cleaned email: {admin_email_list}")

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
def settings(request):
    return render(request, "web/content/settings.html")


@login_required
def smppc_status_setting(request):
    return render(request, "web/content/smppc_status.html")


def smppc_status_view_manage(request):
    args, res_status, res_message = {}, 400, _("Sorry, Command does not matched.")
    stats = None
    if request.GET and request.is_ajax():
        s = request.GET.get("s")
        if s in ["list", "smppc"]:
            stats = Stats(telnet=request.telnet)

            if stats:
                if s == "list":
                    args = stats.list_s()
                    res_status, res_message = 200, _("ok")
                    for conn in args.get("stats", []):
                        disconnected_at = conn.get("disconnected_at", "ND")
                        bound_at = conn.get("bound_at", "ND")

                        if disconnected_at != "ND" and bound_at != "ND":
                            if disconnected_at > bound_at:
                                conn["status"] = "DOWN"
                            else:
                                conn["status"] = "BOUND"
                        elif disconnected_at == "ND" and bound_at != "ND":
                            conn["status"] = "BOUND"
                        elif disconnected_at != "ND" and bound_at == "ND":
                            conn["status"] = "DOWN"
                        else:
                            conn["status"] = "UNBOUND"

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


@login_required
def monitor_settings(request):
    return render(request, "web/content/monitor_settings.html")


@login_required
def settings_manage(request):
    try:
        args, res_status, res_message = {}, 400, _("Sorry, Command does not matched.")
        if request.POST and request.is_ajax():
            s = request.POST.get("s")
            if s in ["list", "add", "edit", "delete"]:
                if s == "list":
                    settings = Settings.objects.all()
                    args = [
                        {
                            "id": setting.id,
                            "cid": setting.cid,
                            "url": setting.url,
                            "email_list": [
                                email.strip("['']")
                                for email in setting.email_list.split(",")
                            ],
                        }
                        for setting in settings
                    ]
                    res_status, res_message = 200, _("OK")
                elif s == "add":
                    settings_instance = Settings.objects.create(
                        cid=request.POST.get("cid"),
                        url=request.POST.get("url"),
                        email_list=request.POST.get("email_list"),
                    )

                    # Convert the Settings instance to a dictionary
                    settings_dict = model_to_dict(settings_instance)

                    # Serialize the dictionary to JSON
                    args = json.dumps(settings_dict)

                    res_status, res_message = 200, _("Settings added successfully!")

                elif s == "edit":

                    updates = get_object_or_404(Settings, id=request.POST.get("id"))

                    updates.cid = request.POST.get("cid", "")
                    updates.url = request.POST.get("url", "")
                    updates.email_list = request.POST.get("email_list", "")

                    updates.save()

                    dicts = model_to_dict(updates)
                    args = json.dumps(dicts)

                    res_status, res_message = 200, _("entry Updated successfully!")

                elif s == "delete":
                    args = get_object_or_404(Settings, id=request.POST.get("id"))
                    args.delete()
                    return JsonResponse(
                        {
                            "status": "success",
                            "message": _("Entry Deleted successfully!"),
                        }
                    )

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
    except Exception as e:
        raise e
