import json
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from main.core.models.setting import Settings
from django.views import View


@login_required
def settings(request):
    return render(request, "web/content/settings.html")


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
                    # updates.id = (request.POST.get("id"),)
                    updates.cid = (request.POST.get("cid"),)
                    updates.url = (request.POST.get("url"),)
                    updates.email_list = (request.POST.get("email_list"),)
                    updates.save()

                    dicts = model_to_dict(updates)
                    args = json.dumps(dicts)

                    res_status, res_message = 200, _("entry Deleted successfully!")

                elif s == "delete":
                    args = get_object_or_404(Settings, id=request.POST.get("id"))
                    args.delete()
                    return JsonResponse(
                        {
                            "status": "success",
                            "message": _("SMPPCCM stopped successfully!"),
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


# def settings_list(request):
#     settings = Settings.objects.all()
#     data = [
#         {"cid": setting.cid, "url": setting.url, "email_list": setting.email_list}
#         for setting in settings
#     ]
#     return JsonResponse(data, safe=False)


# class SettingsEditView(View):
#     def post(self, request, cid):
#         setting = get_object_or_404(Settings, cid=cid)
#         data = json.loads(request.body)
#         setting.cid = data.get("cid", setting.cid)
#         setting.url = data.get("url", setting.url)
#         setting.email_list = data.get("email_list", setting.email_list)
#         setting.save()
#         return JsonResponse(
#             {"status": "success", "message": "Settings updated successfully"}
#         )


# class SettingsAddView(View):
#     def post(self, request):
#         data = json.loads(request.body)
#         cid = data.get("cid")
#         url = data.get("url")
#         email_list = data.get("email_list")
#         Settings.objects.create(cid=cid, url=url, email_list=email_list)
#         return JsonResponse(
#             {"status": "success", "message": "Settings added successfully"}
#         )


# class SettingsDeleteView(View):
#     def post(self, request, cid: str):
#         setting = get_object_or_404(Settings, cid=cid)
#         setting.delete()
#         return JsonResponse(
#             {"status": "success", "message": "Settings deleted successfully"}
#         )
