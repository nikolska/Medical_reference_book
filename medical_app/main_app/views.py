from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from .models import *


class HomePageView(View):
    template = 'home_page.html'

    def get(self, request):
        return render(request, self.template)


class OrgansListView(View):
    template = 'organs_list.html'

    def get(self, request):
        organs = Organ.objects.order_by('name')
        ctx = {'organs': organs}
        return render(request, self.template, ctx)
