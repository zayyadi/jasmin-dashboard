from django.conf import settings

from config.settings.com import STANDARD_PROMPT
from main.core.exceptions import ObjectNotFoundError


class Stats:
    lookup_field = "uid"

    def __init__(self, telnet):
        self.telnet = telnet

    def get_user(self, uid, silent=False):
        self.telnet.sendline(f"stats --user={uid}")
        matched_index = self.telnet.expect(
            [
                r".+Unknown User:.*" + STANDARD_PROMPT,
                r".+Usage: user.*" + STANDARD_PROMPT,
                r"(.+)\n" + STANDARD_PROMPT,
            ]
        )
        if matched_index != 2:
            if silent:
                return
            else:
                raise ObjectNotFoundError("Unknown user: %s" % uid)
        result = self.telnet.match.group(1)
        user = {}
        for line in [l for l in result.splitlines() if l][1:]:  # noqa: E741
            d = [str(x, "utf-8") for x in line.split() if x]
            if len(d) == 2:
                user[d[0]] = d[1]
            elif len(d) == 4:
                # Not DRY, could be more elegant
                if d[0] not in user:
                    user[d[0]] = {}
                if d[1] not in user[d[0]]:
                    user[d[0]][d[1]] = {}
                if d[2] not in user[d[0]][d[1]]:
                    user[d[0]][d[1]][d[2]] = {}
                user[d[0]][d[1]][d[2]] = d[3]
            # each line has two or four lines so above exhaustive
        return user

    def list(self):
        "List users. No parameters"
        self.telnet.sendline("stats --users")
        self.telnet.expect([r"(.+)\n" + STANDARD_PROMPT])
        result = self.telnet.match.group(0).strip()
        if len(result) < 3:
            return {"users": []}

        results = [l for l in result.splitlines() if l]  # noqa: E741
        annotated_uids = [str(u.split(None, 1)[0][1:], "utf-8") for u in results[2:-2]]
        print(f"annotated: {annotated_uids}")
        users = []
        for auid in annotated_uids:
            if auid[0] == "!":
                udata = self.get_user(auid[1:], True)
                udata["status"] = "disabled"
            else:
                udata = self.get_user(auid, True)
                udata["status"] = "enabled"
            users.append(udata)
        return {
            # return users skipping None (== nonexistent user)
            "users": [u for u in users if u]
        }
