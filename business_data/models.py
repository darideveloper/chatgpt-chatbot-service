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
    
    class Meta:
        verbose_name_plural = "Refaccionaria X Products"
        verbose_name = "Refaccionaria X Product"