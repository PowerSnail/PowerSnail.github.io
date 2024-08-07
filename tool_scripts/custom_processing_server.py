import http.server
import json
from urllib.parse import parse_qs


class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/get_bibliography":
            # Content length to read the body
            content_length = int(self.headers["Content-Length"])
            # Read the body of the request
            body = self.rfile.read(content_length)

            # Parse the body for input_file and bib_file
            try:
                # Since the body is sent as form data
                post_data = parse_qs(body.decode("utf-8"))
                input_file = post_data.get("input_file", [None])[0]
                bib_file = post_data.get("bib_file", [None])[0]

                # You can process the input_file and bib_file here
                print(f"Input File: {input_file}")
                print(f"Bib File: {bib_file}")

                # Sending a response back
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                response = {
                    "status": "success",
                    "input_file": input_file,
                    "bib_file": bib_file,
                }
                self.wfile.write(json.dumps(response).encode("utf-8"))
            except Exception as e:
                # Handle exceptions or errors
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Bad request"}')
        else:
            self.send_response(404)
            self.end_headers()


def run(server_class=http.server.HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
