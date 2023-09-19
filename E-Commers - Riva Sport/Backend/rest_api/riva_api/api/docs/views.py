from django.shortcuts import render
from django.views import View

class Index(View):
    def get(self, request):
        template_name = 'riva_api/pages/docs.html'
        return render(request, template_name)