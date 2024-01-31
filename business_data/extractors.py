import os
import openpyxl
from business_data import models


def refaccionaria_x_xlsx(file_path: os.path):
    """ Extract data from xlsx file and save to database

    Args:
        file_path (os.path): File path with data
    """
    
    # Open excel file
    wb = openpyxl.load_workbook(file_path)
    sheet = wb["database"]
    
    # Read data from file
    rows = sheet.max_row
    columns = sheet.max_column
    data = []
    for row in range(1, rows + 1):

        row_data = []
        for column in range(1, columns + 1):
            cell_data = sheet.cell(row, column).value
            row_data.append(cell_data)

        data.append(row_data)
        
    # Delete old products
    models.RefaccionariaX.objects.all().delete()
        
    # Save data to database
    for row in data[1:]:
        models.RefaccionariaX.objects.create(
            id=row[0],
            nombre=row[1].strip(),
            descripcion=row[2].strip(),
            fabricante=row[3].strip(),
            numero_de_pieza=row[4].strip(),
            categoria=row[5].strip(),
            precio=row[6],
            cantidad_en_stock=row[7],
            ubicacion=row[8].strip(),
            estante=row[9].strip(),
            modelo=row[10].strip(),
            ano=row[11].strip(),
        )
        
    print("Done!")


def refaccionaria_y_xlsx(file_path: os.path):
    """ Extract data from xlsx file and save to database

    Args:
        file_path (os.path): File path with data
    """
    
    # Open excel file
    wb = openpyxl.load_workbook(file_path)
    sheet = wb["database"]
    
    # Read data from file
    rows = sheet.max_row
    columns = sheet.max_column
    data = []
    for row in range(1, rows + 1):

        row_data = []
        for column in range(1, columns + 1):
            cell_data = sheet.cell(row, column).value
            row_data.append(cell_data)

        data.append(row_data)
        
    # Delete old products
    models.RefaccionariaY.objects.all().delete()
        
    # Save data to database
    for row in data[1:]:
        models.RefaccionariaY.objects.create(
            id=row[0],
            nombre=row[1].strip(),
            descripcion=row[2].strip(),
            fabricante=row[3].strip(),
            numero_de_pieza=row[4].strip(),
            categoria=row[5].strip(),
            precio=row[6],
            cantidad_en_stock=row[7],
            ubicacion=row[8].strip(),
            estante=row[9].strip(),
            modelo=row[10].strip(),
            ano=row[11].strip(),
        )
        
    print("Done!")
    
    
# Relation between business name and file extension
FILES_RELATION = {
    "refaccionaria x": {
        "xlsx": refaccionaria_x_xlsx,
    },
    "refaccionaria y": {
        "xlsx": refaccionaria_y_xlsx,
    }
}