import werkzeug


def application_unproxied(environ, start_response):
    return werkzeug.exceptions.NotFound("No handler found.\n")(environ, start_response)


def application(environ, start_response):
    return application_unproxied(environ, start_response)
