from django.utils.deprecation import MiddlewareMixin

class NgrokFixMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response["ngrok-skip-browser-warning"] = "true"
        return response
