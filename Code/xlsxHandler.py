import xlsxwriter

class XlsxHandler :
    #self.listVid =
    numberPages = 0
    listVid = {}
    listVidActr = {}


    def __init__(self, nameInit ):
        # self.listVid = listVid
        # self.listVidActr = listVidActr
        self.nameInit = nameInit
        self.numberPages = 1
        self.workbook = xlsxwriter.Workbook(f"{self.nameInit}.xlsx")
        self.worksheetTitulo = self.workbook.add_worksheet("ListaMaster")
        self.worksheetActress = self.workbook.add_worksheet("ListaActr")
        self.worksheetAct = self.workbook.add_worksheet("linkAct")

        self.rowTitulo = 0
        self.rowActress = 0
        
        column = 0
        self.worksheetTitulo.write(self.rowTitulo,column,'Codigo')
        column+=1
        self.worksheetTitulo.write(self.rowTitulo,column,'Titulo')
        column+=1
        self.worksheetTitulo.write(self.rowTitulo,column,'thumb')
        self.rowTitulo+=1

        self.row = 0
        column = 0
        self.worksheetActress.write(self.rowActress,column,'Codigo')
        column+=1
        self.worksheetActress.write(self.rowActress,column,'Titulo')
        self.rowActress+=1


        

    def increasePages (self):
        self.numberPages += 1

    def writeExcel(self, listaVideo,listaActress,linkAct):

        print("writing")

        self.worksheetAct.write(0,0,linkAct)

        for f in listaVideo:
            
            column = 0
            self.worksheetTitulo.write (self.rowTitulo,column,f)
            column +=1
            self.worksheetTitulo.write (self.rowTitulo,column,listaVideo[f][0])
            column +=1
            self.worksheetTitulo.write (self.rowTitulo,column,listaVideo[f][1])            
            self.rowTitulo +=1

        for f in listaActress:
            
            for a in listaActress[f]:
                column = 0
                self.worksheetActress.write (self.rowActress,column,f)
                column +=1
                self.worksheetActress.write (self.rowActress,column,a)
                self.rowActress +=1

            # row +=1
    def close (self):
        print("closing file")
        self.workbook.close()