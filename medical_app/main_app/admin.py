from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Disease, DiseaseSymptom, GeographicalArea, Organ, Symptom, Treatment


class DiseaseSymptomInline(admin.TabularInline):
    """Disease symptom class references Disease.symptoms.through"""
    model = DiseaseSymptom
    extra = 1


class OrganModelAdmin(admin.ModelAdmin):
    """Organ model"""
    list_display = ('name', 'get_image',)
    search_fields = ('name',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="150">')

    get_image.short_description = 'image'


class SymptomModelAdmin(admin.ModelAdmin):
    """Symptom model"""
    list_display = ('name', )
    list_filter = ('affected_organ',)
    search_fields = ('name',)


class TreatmentModelAdmin(admin.ModelAdmin):
    """Treatment model"""
    list_display = ('treatment', )
    search_fields = ('treatment',)


class GeographicalAreaModelAdmin(admin.ModelAdmin):
    """Geographical area model"""
    list_display = ('area', 'get_image',)
    search_fields = ('area',)
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="150">')

    get_image.short_description = 'image'


class DiseaseModelAdmin(admin.ModelAdmin):
    """Disease model"""
    fields = ('name', 'description', 'affected_organs', 'geographical_area', 'treatment')
    list_display = ('name', )
    list_filter = ('geographical_area', 'symptoms', 'affected_organs')
    search_fields = ('name',)
    inlines = (DiseaseSymptomInline,)
    save_on_top = True


class DiseaseSymptomModelAdmin(admin.ModelAdmin):
    """Disease symptom model"""
    list_display = ('disease', 'symptom', 'symptom_frequency')
    list_filter = ('disease', 'symptom', 'symptom_frequency')
    search_fields = ('disease', 'symptom', 'symptom_frequency')


admin.site.register(Organ, OrganModelAdmin)
admin.site.register(Symptom, SymptomModelAdmin)
admin.site.register(Treatment, TreatmentModelAdmin)
admin.site.register(GeographicalArea, GeographicalAreaModelAdmin)
admin.site.register(Disease, DiseaseModelAdmin)
admin.site.register(DiseaseSymptom, DiseaseSymptomModelAdmin)
