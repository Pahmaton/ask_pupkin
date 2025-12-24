from urllib.parse import parse_qsl


def application(environ, start_response):
    method = environ.get('REQUEST_METHOD', 'GET')

    query_string = environ.get('QUERY_STRING', '')
    get_params = parse_qsl(query_string)

    post_params = []
    if method == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(request_body_size).decode('utf-8')
            post_params = parse_qsl(request_body)
        except (ValueError, KeyError):
            pass

    response_body = f"Method: {method}\n"
    response_body += f"GET params: {dict(get_params)}\n"
    response_body += f"POST params: {dict(post_params)}\n"

    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body.encode('utf-8')]
