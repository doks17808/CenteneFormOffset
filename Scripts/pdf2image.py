import os
from pdf2image import convert_from_path

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

def pdf2image(path, out_path):
    for pdf in os.listdir(f'{path}'):
        images = convert_from_path(f'{path}/{pdf}', output_folder=f'{out_path}')