# -*- encoding: utf-8 -*-
import os
import requests

from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

import json

from main.core.smpp import SMPPCCM
from main.core.models.setting import Settings
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
def smppccm_view(request):
    return render(request, "web/content/smppccm.html")


@login_required
def smppccm_view_manage(request):
    args, res_status, res_message = {}, 400, _("Sorry, Command does not matched.")
    smppccm = None
    if request.POST and request.is_ajax():
        s = request.POST.get("s")
        if s in ["list", "add", "edit", "delete", "start", "stop", "restart"]:
            smppccm = SMPPCCM(telnet=request.telnet)
        if smppccm:
            if s == "list":
                args = smppccm.list()
                for connector in args["connectors"]:
                    if connector["status"] == "stopped":
                        print(f"Danger!!! : smppccm {connector['cid']} stopped!!!")
                res_status, res_message = 200, _("OK")
            elif s == "add":
                smppccm.create(
                    data=dict(
                        cid=request.POST.get("cid"),
                        host=request.POST.get("host"),
                        port=request.POST.get("port"),
                        username=request.POST.get("username"),
                        password=request.POST.get("password"),
                    )
                )
                res_status, res_message = 200, _("SMPPCCM added successfully!")
            elif s == "edit":
                smppccm.partial_update(
                    data=dict(
                        cid=request.POST.get("cid"),
                        logfile=request.POST.get("logfile"),
                        logrotate=request.POST.get("logrotate"),
                        loglevel=request.POST.get("loglevel"),
                        host=request.POST.get("host"),
                        port=request.POST.get("port"),
                        ssl=request.POST.get("ssl"),
                        username=request.POST.get("username"),
                        password=request.POST.get("password"),
                        bind=request.POST.get("bind"),
                        bind_to=request.POST.get("bind_to"),
                        trx_to=request.POST.get("trx_to"),
                        res_to=request.POST.get("res_to"),
                        pdu_red_to=request.POST.get("pdu_red_to"),
                        con_loss_retry=request.POST.get("con_loss_retry"),
                        con_loss_delay=request.POST.get("con_loss_delay"),
                        con_fail_retry=request.POST.get("con_fail_retry"),
                        con_fail_delay=request.POST.get("con_fail_delay"),
                        src_addr=request.POST.get("src_addr"),
                        src_ton=request.POST.get("src_ton"),
                        src_npi=request.POST.get("src_npi"),
                        dst_ton=request.POST.get("dst_ton"),
                        dst_npi=request.POST.get("dst_npi"),
                        bind_ton=request.POST.get("bind_ton"),
                        bind_npi=request.POST.get("bind_npi"),
                        validity=request.POST.get("validity"),
                        priority=request.POST.get("priority"),
                        requeue_delay=request.POST.get("requeue_delay"),
                        addr_range=request.POST.get("addr_range"),
                        systype=request.POST.get("systype"),
                        dlr_expiry=request.POST.get("dlr_expiry"),
                        submit_throughput=request.POST.get("submit_throughput"),
                        proto_id=request.POST.get("proto_id"),
                        coding=request.POST.get("coding"),
                        elink_interval=request.POST.get("elink_interval"),
                        def_msg_id=request.POST.get("def_msg_id"),
                        ripf=request.POST.get("ripf"),
                        dlr_msgid=request.POST.get("dlr_msgid"),
                    ),
                    cid=request.POST.get("cid"),
                )
                res_status, res_message = 200, _("SMPPCCM updated successfully!")
            elif s == "delete":
                args = smppccm.destroy(cid=request.POST.get("cid"))
                res_status, res_message = 200, _("SMPPCCM deleted successfully!")
            elif s == "start":
                args = smppccm.start(cid=request.POST.get("cid"))
                res_status, res_message = 200, _("SMPPCCM started successfully!")
            elif s == "stop":
                args = smppccm.stop(cid=request.POST.get("cid"))
                res_status, res_message = 200, _("SMPPCCM stoped successfully!")
            elif s == "restart":
                args = smppccm.stop(cid=request.POST.get("cid"))
                args = smppccm.start(cid=request.POST.get("cid"))
                res_status, res_message = 200, _("SMPPCCM restarted successfully!")
    if isinstance(args, dict):
        args["status"] = res_status
        args["message"] = str(res_message)
        # print(f"args {args}")
    else:
        res_status = 200
        # print(f"args {args}")
    return HttpResponse(
        json.dumps(args), status=res_status, content_type="application/json"
    )
