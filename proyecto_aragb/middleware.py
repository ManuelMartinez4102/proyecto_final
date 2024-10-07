from django.shortcuts import redirect

class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Aquí verificas si la URL no es la raíz, y si no lo es, la rediriges
        if not request.path == '/':
            return redirect('/')
        response = self.get_response(request)
        return response
