from django.db import models


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
    modelo = models.CharField(max_length=100)
    ano = models.CharField(max_length=10)
    
    def __str__(self):
        return f"({self.umero_de_pieza}) {self.nombre}"
    
    class Meta:
        verbose_name_plural = "Refaccionaria X Products"
        verbose_name = "Refaccionaria X Product"