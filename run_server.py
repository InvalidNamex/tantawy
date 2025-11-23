import os
from waitress import serve
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tantawy.settings')

application = get_wsgi_application()

if __name__ == '__main__':
    print("Starting Tantawy API Server on http://0.0.0.0:8000")
    print("Press Ctrl+C to stop the server")
    serve(application, host='0.0.0.0', port=8000, threads=4)