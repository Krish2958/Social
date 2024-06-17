import time

from social_network.env_variables import EnvVariables

from ..log_config import init_logger


class LoggingMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization.
        self.get_response = get_response
        self.logger = init_logger()

    def __call__(self, request):
        time_to_execute = time.time()
        response = self.get_response(request)
        time_to_execute = int((time.time() - time_to_execute) * 1000)

        request_body = request.data if hasattr(request, "data") else None
        request_params = request.META.get("QUERY_STRING") or None

        request_user_info = {
            "Email": request.user.email
            if request.user.is_authenticated
            else "User is not logged in.",
            "System": request.headers.get("User-Agent"),
            "Request User IP": {request.META.get("REMOTE_ADDR")},
        }

        response_content = response.content if hasattr(response, "content") else None

        log = {
            "access_token": request.headers.get("Authorization"),
            "request_route": request.get_full_path(),
            "request_method": request.method,
            "request_content_type": request.headers.get("Accept"),
            "request_headers": request.headers,
            "request_user_info": request_user_info,
            "execution_time": f"{time_to_execute} ms",
            "request_params": request_params,
            "request_body": request_body,
            "response_status_code": response.status_code,
            "response": response_content,
        }
        # Disabling the request/response logging on local.
        if EnvVariables.ENVIRONMENT.value != "local":
            self.logger.info(log)

        return response