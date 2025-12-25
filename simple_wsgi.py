def application(environ, start_response):
    # Извлекаем GET-параметры
    query_string = environ.get('QUERY_STRING', '')

    # Извлекаем POST-параметры
    content_length = int(environ.get('CONTENT_LENGTH', 0) or 0)
    post_data = environ['wsgi.input'].read(content_length).decode('utf-8') if content_length > 0 else "No POST params"

    # Формируем текст ответа
    response_text = f"GET params: {query_string}\nPOST params: {post_data}\n"

    # Отправляем заголовки
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain'), ('Content-Length', str(len(response_text)))]
    start_response(status, response_headers)

    return [response_text.encode('utf-8')]
