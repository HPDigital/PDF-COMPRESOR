"""
PDF COMPRESOR
"""

#!/usr/bin/env python
# coding: utf-8

# In[26]:


import fitz  # PyMuPDF
import os

def compress_pdf(input_pdf_path, output_pdf_path, min_size_kb=60, max_size_kb=100, dpi_start=30, dpi_step=10):
    # Abre el archivo PDF original
    pdf_document = fitz.open(input_pdf_path)

    # Solo aseguramos que haya una página en el PDF
    if pdf_document.page_count != 1:
        print("Este código está diseñado para manejar PDFs de una sola página.")
        return

    dpi = dpi_start
    compressed = False

    while not compressed and dpi > 5:
        # Crea un nuevo archivo PDF comprimido
        pdf_document_new = fitz.open()

        # Carga la única página del PDF
        page = pdf_document.load_page(0)  # Carga la única página
        # Reduce la resolución (DPI más bajo para mayor compresión)
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))

        # Crea una nueva página en el PDF de salida con el mismo tamaño que la original
        pdf_document_new.new_page(width=page.rect.width, height=page.rect.height)

        # Inserta la imagen (pixmap) en la nueva página
        pdf_document_new[-1].insert_image(page.rect, pixmap=pix)

        # Guarda el archivo PDF comprimido
        temp_output_path = output_pdf_path.replace(".pdf", f"_{dpi}dpi.pdf")
        pdf_document_new.save(temp_output_path)
        pdf_document_new.close()

        # Verifica el tamaño del archivo resultante
        file_size_kb = os.path.getsize(temp_output_path) / 1024  # en KB

        # Si el tamaño está entre los límites deseados, se considera éxito
        if min_size_kb <= file_size_kb <= max_size_kb:
            os.rename(temp_output_path, output_pdf_path)
            compressed = True
            print(f"Compresión exitosa con DPI={dpi}, tamaño={file_size_kb:.2f}KB")
        else:
            # Elimina el archivo temporal si no cumple con los requisitos
            os.remove(temp_output_path)
            dpi -= dpi_step  # Reduce el DPI para intentar una compresión mayor

    pdf_document.close()

    if not compressed:
        print("No se pudo alcanzar el tamaño entre 45 KB y 50 KB. Se ha intentado con el DPI más bajo posible.")
    else:
        print(f"Archivo PDF comprimido guardado en: {output_pdf_path}")

# Ruta del archivo original y comprimido
input_pdf_path = r"C:\Users\HP\Downloads\Secundaria - 6to D - Poleyn Debesson, Pierre Luk_240919_115334.pdf"
output_pdf_path = r"C:\Users\HP\Downloads\compressed_45_50.pdf"

# Ejecuta la compresión
compress_pdf(input_pdf_path, output_pdf_path)


# In[ ]:






if __name__ == "__main__":
    pass
