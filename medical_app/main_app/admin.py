from django.contrib import admin

from .models import *


admin.site.register(Organ)
admin.site.register(Symptom)
admin.site.register(Disease)
admin.site.register(DiseaseSymptom)