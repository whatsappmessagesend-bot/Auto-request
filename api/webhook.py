import os
import json
import urllib.request
from http.server import BaseHTTPRequestHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN")


def telegram_api(method, data):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"

    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        response = {
            "ok": True,
            "service": "Auto Request Join",
            "status": "running"
        }

        self.wfile.write(
            json.dumps(response).encode("utf-8")
        )

    def do_POST(self):
        try:
            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = self.rfile.read(content_length)

            update = json.loads(
                body.decode("utf-8")
            )

            # Telegram Join Request
            join_request = update.get(
                "chat_join_request"
            )

            if join_request:

                chat = join_request.get(
                    "chat", {}
                )

                user = join_request.get(
                    "from", {}
                )

                chat_id = chat.get("id")
                user_id = user.get("id")

                if chat_id and user_id and BOT_TOKEN:

                    result = telegram_api(
                        "approveChatJoinRequest",
                        {
                            "chat_id": chat_id,
                            "user_id": user_id
                        }
                    )

                    print(
                        "Join request approved:",
                        result
                    )

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "ok": True
                }).encode("utf-8")
            )

        except Exception as error:

            print(
                "Webhook error:",
                str(error)
            )

            # Telegram को हमेशा 200 response देने की कोशिश
            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "ok": False,
                    "error": str(error)
                }).encode("utf-8")
                  )
