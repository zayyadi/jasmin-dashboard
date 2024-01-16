from django.conf import settings
from main.core.exceptions import ObjectNotFoundError

# from django.conf import settings
from main.core.tools import split_cols

from main.core.smpp.smppccm import SMPPCCM

import logging


STANDARD_PROMPT = settings.STANDARD_PROMPT
INTERACTIVE_PROMPT = settings.INTERACTIVE_PROMPT

logger = logging.getLogger(__name__)


class Stats:
    lookup_field = "cid"

    def __init__(self, telnet):
        self.telnet = telnet

    def get_smppccm(self, cid, silent=False):
        # Some of this could be abstracted out - similar pattern in users.py
        self.telnet.sendline("smppccm -s " + cid)
        matched_index = self.telnet.expect(
            [
                r".+Unknown connector:.*" + STANDARD_PROMPT,
                r".+Usage:.*" + STANDARD_PROMPT,
                r"(.+)\n" + STANDARD_PROMPT,
            ]
        )
        if matched_index != 2:
            if silent:
                return
            else:
                raise ObjectNotFoundError("Unknown connector: %s" % cid)
        result = self.telnet.match.group(1)
        smppccm = {}
        for line in result.splitlines():
            d = [x for x in line.split() if x]
            if len(d) == 2:
                smppccm[str(d[0], "utf-8")] = str(d[1], "utf-8")
        return smppccm

    def list_smpp(self):
        self.telnet.sendline("stats --smppcs")
        self.telnet.expect([r"(.+)\n" + STANDARD_PROMPT])
        res = str(self.telnet.match.group(0)).strip().replace("\\r", "").split("\\n")
        # print(res)
        if len(res) < 3:
            return []
        return split_cols(res[2:-2])

    def list_s(self):
        connector_list = self.list_smpp()
        # print(f"connector: {connector_list}")
        return {
            "stats": [
                {
                    "cid": r[0].strip().lstrip("#"),
                    "connected_at": [c.strip() for c in " ".join(r[1:2]).split(",")],
                    "bound_at": r[3].strip(),
                    "disconnected_at": [c.strip() for c in " ".join(r[4:5]).split(",")],
                    "submits": r[6].strip(),
                    "delivers": r[7].strip(),
                    "qos_err": r[8].strip(),
                    "other_err": r[9].strip(),
                }
                for r in connector_list
            ]
        }

    def list_smppc(self, cid):
        self.telnet.sendline(f"stats --smppc {cid}")
        self.telnet.expect([r"(.+)\n" + STANDARD_PROMPT])
        res = str(self.telnet.match.group(0)).strip().replace("\\r", "").split("\\n")
        # print(f"resuls: {res}")
        if len(res) < 3:
            return []
        connector_detail = split_cols(res[2:-2])
        # print(f"connector details: {connector_detail}")

        return {
            "smppc": [
                {
                    "item": r[0].strip().lstrip("#"),
                    "value": r[1],
                }
                for r in connector_detail
            ]
        }


class SMPPSERVERStat(object):
    lookup_field = "cid"

    def __init__(self, telnet):
        self.telnet = telnet

    def list_smpp_server(self):
        self.telnet.sendline("stats --smppsapi")
        self.telnet.expect([r"(.+)\n" + STANDARD_PROMPT])
        res = str(self.telnet.match.group(0)).strip().replace("\\r", "").split("\\n")
        # print(f"resuls: {res}")
        if len(res) < 3:
            return []
        connector_detail = split_cols(res[2:-2])
        print(f"connector details: {connector_detail}")

        return {
            "smppsapi": [
                {
                    "item": r[0].strip().lstrip("#"),
                    "value": r[1],
                }
                for r in connector_detail
            ]
        }


class HTTPStat(object):
    def __init__(self, telnet):
        self.telnet = telnet

    def list_http_server(self):
        self.telnet.sendline("stats --httpapi")
        self.telnet.expect([r"(.+)\n" + STANDARD_PROMPT])
        res = str(self.telnet.match.group(0)).strip().replace("\\r", "").split("\\n")
        # print(f"resuls: {res}")
        if len(res) < 3:
            return []
        connector_detail = split_cols(res[2:-2])
        # print(f"connector details: {connector_detail}")

        return {
            "httpapi": [
                {
                    "item": r[0].strip().lstrip("#"),
                    "value": r[1],
                }
                for r in connector_detail
            ]
        }


class UserStat(object):
    lookup_field = "uid"

    def __init__(self, telnet):
        self.telnet = telnet

    def list_users(self):
        self.telnet.sendline("stats --users")
        self.telnet.expect([r"(.+)\n" + STANDARD_PROMPT])
        res = str(self.telnet.match.group(0)).strip().replace("\\r", "").split("\\n")
        # print(res)
        if len(res) < 3:
            return []
        return split_cols(res[2:-2])

    def list_u(self):
        user_list = self.list_users()
        # print(f"connector: {user_list}")
        return {
            "users": [
                {
                    "uid": r[0].strip().lstrip("#"),
                    "smpp_bound_conn": r[1].strip(),
                    "smpp_la": r[2].strip(),
                    "http_req_counter": r[3].strip(),
                    "http_la": r[4].strip(),
                }
                for r in user_list
            ]
        }

    def list_user(self, uid):
        self.telnet.sendline(f"stats --user {uid}")
        self.telnet.expect([r"(.+)\n" + STANDARD_PROMPT])
        res = str(self.telnet.match.group(0)).strip().replace("\\r", "").split("\\n")
        # print(f"resuls: {res}")
        if len(res) < 3:
            return []
        connector_detail = split_cols(res[2:-2])
        # print(f"connector details: {connector_detail}")

        return {
            "user": [
                {
                    "item": r[0].strip().lstrip("#"),
                    "type": [c.strip() for c in " ".join(r[1:2]).split(",")],
                    "value": r[3:],
                }
                for r in connector_detail
            ]
        }
