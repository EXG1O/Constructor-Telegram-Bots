from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render
import global_methods as GlobalMethods

# Create your views here.
def main(request: WSGIRequest):
	data = GlobalMethods.get_navbar_buttons_data(request)
	return render(request, 'main.html', data)