import PyPDF2

def PDFsplit(pdf, outputpdf, start):  
    pdfFileObj = open(pdf, 'rb') 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    pdfWriter = PyPDF2.PdfFileWriter()
    if start == 0:
        end = 20
        for page in range(start, end):
            pdfWriter.addPage(pdfReader.getPage(page))
        with open(outputpdf, "wb") as f:
            pdfWriter.write(f)
    else:
        end =  start + 3
        for page in range(start, end):
            pdfWriter.addPage(pdfReader.getPage(page))
        with open(outputpdf, "wb") as f:
            pdfWriter.write(f)
    pdfFileObj.close() 
               

if __name__ == '__main__':
    pdf = 'test.pdf'
    PDFsplit(pdf, 0)