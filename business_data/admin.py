from django.contrib import admin
from . import models


@admin.register(models.RefaccionariaX)
class RefaccionariaXAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'fabricante',
                    'numero_de_pieza', 'categoria', 'precio',
                    'cantidad_en_stock', 'ubicacion', 'modelo', 'ano')
    search_fields = ('nombre', 'descripcion', 'fabricante',
                     'numero_de_pieza', 'categoria', 'ubicacion',
                     'modelo', 'ano')
    list_filter = ('fabricante', 'categoria', 'modelo', 'ano')