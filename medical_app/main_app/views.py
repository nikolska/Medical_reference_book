from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


class HomePageView(View):
    template = 'home_page.html'

    def get(self, request):
        return render(request, self.template)

