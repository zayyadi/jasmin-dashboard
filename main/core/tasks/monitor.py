from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.urls import reverse
import requests
from django.test import Client


@shared_task
def call_user_stat_view_manage() -> None:
    client = Client()
    response = client.get("/users_stats/manage/", {"s": "list"})
    print(response.status_code)
    # print(f"Headers: {response.headers}")
    # print(f"response: {response.content}")


@shared_task
def call_smppc_task() -> None:
    client = Client()
    response = client.get("/stats/manage/", {"s": "list"})
    print(response.status_code)
    # print(f"Headers: {response.headers}")
    # print(f"response: {response.content}")
