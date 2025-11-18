#!/usr/bin/env python3
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote
from mimetypes import guess_type
from argparse import ArgumentParser
from email import policy, message_from_bytes

icons = {
    'arrow_up': '''
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-up" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 0 0 0 .5.5z"/>
</svg>
''',

    'folder': '''
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-folder" viewBox="0 0 16 16">
  <path d="M.54 3.87.5 3a2 2 0 0 1 2-2h3.672a2 2 0 0 1 1.414.586l.828.828A2 2 0 0 0 9.828 3h3.982a2 2 0 0 1 1.992 2.181l-.637 7A2 2 0 0 1 13.174 14H2.826a2 2 0 0 1-1.991-1.819l-.637-7a1.99 1.99 0 0 1 .342-1.31zM2.19 4a1 1 0 0 0-.996 1.09l.637 7a1 1 0 0 0 .995.91h10.348a1 1 0 0 0 .995-.91l.637-7A1 1 0 0 0 13.81 4H2.19zm4.69-1.707A1 1 0 0 0 6.172 2H2.5a1 1 0 0 0-1 .981l.006.139C1.72 3.042 1.95 3 2.19 3h5.396l-.707-.707z"/>
</svg>
''',

    'file-earmark-fill': '''
<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-fill" viewBox="0 0 16 16">
  <path d="M4 0h5.293A1 1 0 0 1 10 .293L13.707 4a1 1 0 0 1 .293.707V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2zm5.5 1.5v2a1 1 0 0 0 1 1h2l-3-3z"/>
</svg>
'''
}

html_template = r'''
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Simple HTTP file server</title>
        <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
        }
        a {
            text-decoration: none;
        }
        a:hover {
            color: #dc3545;
        }
        .go-up-entry {
            color: #198754
        }
        .directory-entry {
            color: #0d6efd;
        }
        .file-entry {
            color: #6610f2;
        }
        #directory-list li {
            list-style: none;
        }
        #directory-list a {
            display: inline-block;
            width: 100%;
            padding-bottom: 0.4em;
            font-size: 1.2em;
        }
        </style>
    </head>

    <body>
        <h1>Path $path</h1>
        <section>
            <h2>Upload file</h2>
            <form method="post" enctype="multipart/form-data">
                <input type="file" name="file" multiple required>
                <input type="submit" value="Upload">
            </form>
            $upload_result_html
        </section>
        <section>
            <h2>Directory listing</h2>
            <ul id="directory-list">
            <li><a class="go-up-entry" href="..">''' + icons['arrow_up'] + r'''Go up</a></li>
                $file_list_html
            </ul>
        </section>
    </body>
</html>
'''

class SimpleHTTPFileServerRequestHandler(BaseHTTPRequestHandler):
    def get_path_from_request(self):
        urlparse_result = urlparse(self.path)
        return Path(unquote(urlparse_result.path).lstrip('/'))

    def load_html(self, path, uploaded_filenames=[]):
        out_html = html_template.replace(
            '$upload_result_html',
            f'<p><span style="font-weight: bold">{len(uploaded_filenames)}</span> files have been uploaded.</p>' if uploaded_filenames else ''
        )
        file_list_html = []
        for file in sorted(path.iterdir()):
            icon, trailing_path, html_class = None, None, None
            if (file.is_dir()):
                icon = icons['folder']
                trailing_path = '/'
                html_class = 'directory-entry'
            else:
                icon = icons['file-earmark-fill']
                trailing_path = ''
                html_class = 'file-entry'
            file_list_html.append(f'<li><a class="{html_class}" href="/{file}{trailing_path}"><span>{icon} {file.name}</span></a></li>')
        return out_html.replace('$path', str(path)).replace('$file_list_html', ''.join(file_list_html))

    def do_GET(self):
        path = self.get_path_from_request()

        if path.is_file():
            mime_type = guess_type(path.name)
            self.send_response(200)
            self.send_header('Content-Type', f'{mime_type[0]}; charset={mime_type[1]}')
            self.end_headers()
            self.wfile.write(path.read_bytes())
        elif path.is_dir():
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(self.load_html(path).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write('<h1>Not found</h1>'.encode('utf-8'))


    def do_POST(self):
        path = self.get_path_from_request()
        request_length = int(self.headers['Content-Length'])
        raw_email_message = b''
        for k, v in self.headers.items():
            raw_email_message += f'{k}: {v}\r\n'.encode('ascii')
        raw_email_message += b'\r\n' + self.rfile.read(request_length)
        email_message = message_from_bytes(raw_email_message, policy=policy.strict)
        filenames = []
        for part in email_message.walk():
            filename = part.get_filename()
            if filename != None:
                target_path = Path(path / filename)
                target_path.write_bytes(part.get_content())
                filenames.append(filename)
        self.send_response(201)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(self.load_html(path, uploaded_filenames=filenames).encode('utf-8'))


def run_server(
        address, port,
        server_class = HTTPServer,
        handler_class = SimpleHTTPFileServerRequestHandler,
    ):
    server_address = (address, port)
    httpd = server_class(server_address, handler_class)
    print(f'Running HTTP file server on {address}:{port}')
    httpd.serve_forever()

if __name__ == '__main__':
    parser = ArgumentParser(description='A simple HTTP file server that supports uploading from the browser')
    parser.add_argument('-b', '--bind', type=str, metavar='ADDRESS', help='bind to address', default='0')
    parser.add_argument('port', type=int, nargs='?', help='bind to port', default=8000)
    args = parser.parse_args()
    run_server(address=args.bind, port=args.port)