from collections import OrderedDict

from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError

from main.core.utils import is_int
from main.core.tools import set_ikeys, split_cols
from main.core.exceptions import (
    JasminError,
    JasminSyntaxError,
    UnknownError,
    MissingKeyError,
    MutipleValuesRequiredKeyError,
    ObjectNotFoundError,
)

import logging, random  # noqa: E401

STANDARD_PROMPT = settings.STANDARD_PROMPT
INTERACTIVE_PROMPT = settings.INTERACTIVE_PROMPT

logger = logging.getLogger(__name__)


class MOInterceptor:
    lookup_field = "order"

    def __init__(self, telnet):
        self.telnet = telnet

    def _list(self):
        self.telnet.sendline("mointerceptor -l")
        self.telnet.expect([r"(.+)\n" + STANDARD_PROMPT])
        mointerceptor_result = (
            str(self.telnet.match.group(0)).strip().replace("\\r", "").split("\\n")
        )
        print(f"mointerceptor: {mointerceptor_result}")

        if len(mointerceptor_result) < 3:
            return {
                "mointerceptor": [],
            }

        mointerceptor_results = [
            l.replace(", ", ",").replace("(!)", "")
            for l in mointerceptor_result[2:-2]
            if l
        ]
        print(f"mointerceptor results: {mointerceptor_results}")
        intercept = split_cols(mointerceptor_results)

        return {
            "mointerceptor": [
                {
                    "order": r[0].strip().lstrip("#"),
                    "type": r[1],
                    "script": [c.strip() for c in r[3:]],
                    "filters": [c.strip() for c in " ".join(r[-1]).split(",")],
                }
                for r in intercept
            ]
        }

    def list(self):
        "List MO interceptor. No parameters"
        return self._list()

    def get_router(self, order):
        "Return data for one morouter as Python dict"
        intercept = self._list()["mointerceptor"]
        try:
            return {
                "mointerceptor": next(
                    m for m in intercept if m["order"] == order
                )  # , None
            }
        except StopIteration:
            raise ObjectNotFoundError("No MOInterceptor with order: %s" % order)

    def flush(self):
        "Flush entire Interceptor table"
        self.telnet.sendline("mointerceptor -f")
        self.telnet.expect([r"(.+)\n" + STANDARD_PROMPT])
        self.telnet.sendline("persist")
        self.telnet.expect(r".*" + STANDARD_PROMPT)
        return {"mointerceptor": []}

    def retrieve(self, order):
        "Details for one MORouter by order (integer)"
        return self.get_router(order)

    def create(self, data):
        self.telnet.sendline("mointerceptor -a")

        updates = data
        for k, v in updates.items():
            if not ((isinstance(updates, dict)) and (len(updates) >= 1)):
                raise JasminSyntaxError("updates should be a a key value array")
            self.telnet.sendline("%s %s" % (k, v))
            matched_index = self.telnet.expect(
                [
                    r".*(Unknown SMPPClientConfig key:.*)" + INTERACTIVE_PROMPT,
                    r".*(Error:.*)" + STANDARD_PROMPT,
                    r".*" + INTERACTIVE_PROMPT,
                    r".+(.*)(" + INTERACTIVE_PROMPT + "|" + STANDARD_PROMPT + ")",
                ]
            )
            if matched_index != 2:
                raise JasminSyntaxError(
                    detail=" ".join(self.telnet.match.group(1).split())
                )
        self.telnet.sendline("ok")
        self.telnet.sendline("persist")
        self.telnet.expect(r".*" + STANDARD_PROMPT)
        return {"order": data["order"]}

        # try:
        #     rtype, order = data.get("type"), data.get("order")
        #     self.retrieve(order)
        # except IndexError:
        #     raise MissingKeyError("MO Interceptor already exists!")

        # rtype = rtype.lower()
        # self.telnet.sendline("mointerceptor -a")
        # self.telnet.expect(r"Adding a new MO Interceptor(.+)\n" + INTERACTIVE_PROMPT)
        # ikeys = OrderedDict({"type": rtype, "order": order})

        # if rtype != "defaultinterceptor":
        #     try:
        #         filters = data["filters"] or ""
        #         filters = filters.split(",")
        #     except MultiValueDictKeyError as e:
        #         logger.error(f"Missing key error while handling filters: {e}")
        #         raise MissingKeyError("%s Interceptor requires filters" % rtype)
        # ikeys["order"] = order if is_int(order) else str(random.randrange(1, 99))

        # script = data.get("script") or ""

        # scripts = ["python3(%s)" % c for c in script]

        # if rtype == "staticmointerceptor":
        #     ikeys["script"] = scripts[0]

        # else:
        #     if len(script) != 1:
        #         logger.error("One and only one connector required")
        #         raise MissingKeyError("One and only one connector required")
        #     ikeys["script"] = scripts[0]

        # set_ikeys(self.telnet, ikeys)
        # self.telnet.sendline("persist")
        # self.telnet.expect(r".*" + STANDARD_PROMPT)
        # return {"mointerceptor": self.get_router(order)}

    def update(self, order, data):
        get_order = self.get_router(order)
        if not get_order:
            raise UnknownError(detail="No Interceptor:" + order)

        created = self.create(data)

        return created

    def simple_mointerceptor_action(self, action, order, return_mointercept=True):
        self.telnet.sendline("mointerceptor -%s %s" % (action, order))
        matched_index = self.telnet.expect(
            [
                r".+Successfully(.+)" + STANDARD_PROMPT,
                r".+Unknown MOInterceptor: (.+)" + STANDARD_PROMPT,
                r".+(.*)" + STANDARD_PROMPT,
            ]
        )
        # print(f"fid: {fid}")
        if matched_index == 0:
            self.telnet.sendline("persist")
            if return_mointercept:
                self.telnet.expect(r".*" + STANDARD_PROMPT)
                return {"morouter": self.get_router(fid)}
            else:
                return {"order": self.get_router(order)}
        elif matched_index == 1:
            raise UnknownError(detail="No Interceptor:" + order)
        else:
            raise JasminError(self.telnet.match.group(1))

    def destroy(self, order):
        """Delete a morouter. One parameter required, the router identifier (a string)

        HTTP codes indicate result as follows

        - 200: successful deletion
        - 404: nonexistent router
        - 400: other error
        """
        return self.simple_mointerceptor_action("r", order, return_mointercept=False)
