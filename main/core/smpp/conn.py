from django.conf import settings

import pexpect

from ..exceptions import (
    TelnetUnexpectedResponse,
    TelnetConnectionTimeout,
    TelnetLoginFailed,
)

from django_tenants.utils import get_tenant


class TelnetConnection(object):
    def __init__(self, request):
        current_tenant = get_tenant(request)
        
        telnet_host = current_tenant.jasmin_host
        telnet_port = current_tenant.jasmin_port
        telnet_username = current_tenant.jasmin_username
        telnet_password = current_tenant.jasmin_password
        try:
            telnet = pexpect.spawn(
                "telnet %s %s" % (telnet_host, telnet_port),
                timeout=settings.TELNET_TIMEOUT,
            )
            telnet.expect_exact("Username: ")
            telnet.sendline(telnet_username)
            telnet.expect_exact("Password: ")
            telnet.sendline(telnet_password)
        except pexpect.EOF:
            raise TelnetUnexpectedResponse
        except pexpect.TIMEOUT:
            raise TelnetConnectionTimeout
        try:
            telnet.expect_exact(settings.STANDARD_PROMPT)
        except pexpect.EOF:
            raise TelnetLoginFailed
        else:
            self.telnet = telnet

    def __del__(self):
        "Make sure telnet connection is closed when unleashing response back to client"
        try:
            self.telnet.sendline("quit")
        except pexpect.ExceptionPexpect:
            self.telnet.kill(9)
