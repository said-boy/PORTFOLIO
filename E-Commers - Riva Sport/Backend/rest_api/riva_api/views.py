from django.shortcuts import render
from django.views import View

# Create your views here.

class Index(View):
    def get(self, request):
        template_name = 'riva_api/pages/index.html'
        return render(request, template_name)