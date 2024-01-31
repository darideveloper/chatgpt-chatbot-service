from django.contrib import admin
from . import models
from business_data.extractors import FILES_RELATION


@admin.register(models.File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file_path', 'bussiness',)
    list_filter = ('bussiness',)
    search_fields = ('file_path',)
    
    # Custom error when save model
    def save_model(self, request, obj, form, change):
        file_path = obj.file_path
        file_ext = file_path.name.split('.')[-1]
        bussiness_name = obj.bussiness.name
        
        # Validate bussiness name
        if bussiness_name not in FILES_RELATION:
            # Show error message to user in admin
            self.message_user(
                request,
                f"The business name '{bussiness_name}'"
                " is not ready for process files",
                level='ERROR'
            )
            return
        
        # Validate file extension
        functions = FILES_RELATION[bussiness_name]
        if file_ext not in functions:
            # Show error message to user in admin
            self.message_user(
                request,
                f"The file extension '{file_ext}'"
                " is not ready for process files",
                level='ERROR'
            )
            return
        
        # Extract data from file
        functions[file_ext](file_path)
        
        super(FileAdmin, self).save_model(request, obj, form, change)


@admin.register(models.RefaccionariaX)
class RefaccionariaXAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'fabricante',
                    'numero_de_pieza', 'categoria', 'precio',
                    'cantidad_en_stock', 'ubicacion', 'modelo', 'ano')
    search_fields = ('nombre', 'descripcion', 'fabricante',
                     'numero_de_pieza', 'categoria', 'ubicacion',
                     'modelo', 'ano')
    list_filter = ('fabricante', 'categoria', 'modelo', 'ano')
    
    
@admin.register(models.RefaccionariaY)
class RefaccionariaYAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'fabricante',
                    'numero_de_pieza', 'categoria', 'precio',
                    'cantidad_en_stock', 'ubicacion', 'modelo', 'ano')
    search_fields = ('nombre', 'descripcion', 'fabricante',
                     'numero_de_pieza', 'categoria', 'ubicacion',
                     'modelo', 'ano')
    list_filter = ('fabricante', 'categoria', 'modelo', 'ano')