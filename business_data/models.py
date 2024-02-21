from django.db import models
from assistent_chatgpt.models import Business


class File(models.Model):
    file_path = models.FileField(upload_to='files/')
    bussiness = models.ForeignKey(Business, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.file_path.name} ({self.bussiness.name})"
    

class RefaccionariaX(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fabricante = models.CharField(max_length=100)
    numero_de_pieza = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    precio = models.FloatField()
    cantidad_en_stock = models.IntegerField()
    ubicacion = models.CharField(max_length=100)
    estante = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.CharField(max_length=10)
    
    def __str__(self):
        return f"({self.numero_de_pieza}) {self.nombre}"
    
    def get_cols(self):
        """ Return table columns """
        columns = [
            'id',
            'nombre',
            'descripcion',
            'fabricante',
            'numero_de_pieza',
            'categoria',
            'precio',
            'cantidad_en_stock',
            'ubicacion',
            'estante',
            'modelo',
            'ano'
        ]
        return ", ".join(columns)
        
    def get_str(self):
        """ Return a string with all the fields of the model """
        
        values = [
            str(self.id),
            self.nombre,
            self.descripcion,
            self.fabricante,
            self.numero_de_pieza,
            self.categoria,
            str(self.precio),
            str(self.cantidad_en_stock),
            self.ubicacion,
            self.estante,
            self.modelo,
            self.ano
        ]
        return ", ".join(values)
    
    class Meta:
        verbose_name_plural = "Refaccionaria X Products"
        verbose_name = "Refaccionaria X Product"
        
        
class RefaccionariaY(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fabricante = models.CharField(max_length=100)
    numero_de_pieza = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    precio = models.FloatField()
    cantidad_en_stock = models.IntegerField()
    ubicacion = models.CharField(max_length=100)
    estante = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.CharField(max_length=10)
    
    def __str__(self):
        return f"({self.numero_de_pieza}) {self.nombre}"
    
    def get_cols(self):
        columns = [
            'id',
            'nombre',
            'descripcion',
            'fabricante',
            'numero_de_pieza',
            'categoria',
            'precio',
            'cantidad_en_stock',
            'ubicacion',
            'estante',
            'modelo',
            'ano'
        ]
        return ", ".join(columns)
        
    def get_str(self):
        """ Return a string with all the fields of the model """
        
        values = [
            str(self.id),
            self.nombre,
            self.descripcion,
            self.fabricante,
            self.numero_de_pieza,
            self.categoria,
            str(self.precio),
            str(self.cantidad_en_stock),
            self.ubicacion,
            self.estante,
            self.modelo,
            self.ano
        ]
        return ", ".join(values)
    
    class Meta:
        verbose_name_plural = "Refaccionaria Y Products"
        verbose_name = "Refaccionaria Y Product"


class RefaccionariaGonzalez(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    compatibility = models.TextField()
    price = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return f"({self.sku}) {self.name}"
    
    def get_cols(self):
        """ Return table columns """
        
        columns = [
            'id',
            'Nombre del producto',
            'Código universal de producto',
            'Marca',
            'Origen',
            'Compatibilidad con vehículos',
            'Precio',
            'Categoría',
            'Descripción de producto'
        ]
        return ", ".join(columns)
    
    def get_str(self):
        """ Return a string with all the fields of the model """
        
        values = [
            str(self.id),
            self.name,
            self.sku,
            self.brand,
            self.origin,
            self.compatibility,
            self.price,
            self.category
        ]
        return ", ".join(values)
    
    class Meta:
        verbose_name_plural = "Refaccionaria Gonzales Products"
        verbose_name = "Refaccionaria Gonzales Product"
        
        
class RemoteFile(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file_link = models.TextField()
    
    def __str__(self):
        return self.name
    
        
# Excel tables relation
business_tables = {
    "refaccionaria x": RefaccionariaX,
    "refaccionaria y": RefaccionariaY,
    "refaccionaria gonzalez": RefaccionariaGonzalez,
    "bancomext": None,
}