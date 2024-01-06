from collections import OrderedDict

from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError

from main.core.utils import is_int
from main.core.tools import set_ikeys, split_cols
from main.core.exceptions import (
    JasminError,
    JasminSyntaxError,
    UnknownError,
    ObjectNotFoundError,
)

import logging, random  # noqa: E401

STANDARD_PROMPT = settings.STANDARD_PROMPT
INTERACTIVE_PROMPT = settings.INTERACTIVE_PROMPT

logger = logging.getLogger(__name__)


class MTInterceptor:
    lookup_field = "order"

    def __init__(self, telnet):
        self.telnet = telnet

    def _list(self):
        self.telnet.sendline("mtinterceptor -l")
        self.telnet.expect([r"(.+)\n" + STANDARD_PROMPT])
        mtinterceptor_result = (
            str(self.telnet.match.group(0)).strip().replace("\\r", "").split("\\n")
        )
        print(f"mtinterceptor: {mtinterceptor_result}")

        if len(mtinterceptor_result) < 3:
            return {
                "mtinterceptor": [],
            }

        mtinterceptor_results = [
            l.replace(", ", ",").replace("(!)", "")
            for l in mtinterceptor_result[2:-2]
            if l
        ]
        print(f"mtinterceptor results: {mtinterceptor_results}")
        intercept = split_cols(mtinterceptor_results)

        return {
            "mtinterceptor": [
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
        "List MT interceptor. No parameters"
        return self._list()

    def get_router(self, order):
        "Return data for one mtinterceptor as Python dict"
        intercept = self._list()["mtinterceptor"]
        try:
            return {
                "mtinterceptor": next(
                    m for m in intercept if m["order"] == order
                )  # , None
            }
        except StopIteration:
            raise ObjectNotFoundError("No mtinterceptor with order: %s" % order)

    def flush(self):
        "Flush entire Interceptor table"
        self.telnet.sendline("mtinterceptor -f")
        self.telnet.expect([r"(.+)\n" + STANDARD_PROMPT])
        self.telnet.sendline("persist")
        self.telnet.expect(r".*" + STANDARD_PROMPT)
        return {"mtinterceptor": []}

    def retrieve(self, order):
        "Details for one MORouter by order (integer)"
        return self.get_router(order)

    def create(self, data):
        self.telnet.sendline("mtinterceptor -a")

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

    def simple_mtinterceptor_action(self, action, order, return_mointercept=True):
        self.telnet.sendline("mtinterceptor -%s %s" % (action, order))
        matched_index = self.telnet.expect(
            [
                r".+Successfully(.+)" + STANDARD_PROMPT,
                r".+Unknown mtinterceptor: (.+)" + STANDARD_PROMPT,
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

    def update(self, order, data):
        delete = self.get_router(order)
        if not delete:
            raise UnknownError(detail="No Interceptor:" + order)

        created = self.create(data)

        return created

    def destroy(self, order):
        """Delete a mtinterceptor. One parameter required, the router identifier (a string)

        HTTP codes indicate result as follows

        - 200: successful deletion
        - 404: nonexistent router
        - 400: other error
        """
        return self.simple_mtinterceptor_action("r", order, return_mointercept=False)


# DefaultInterceptor, StaticMTInterceptor
