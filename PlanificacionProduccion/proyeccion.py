import calendar
import sys
from datetime import timedelta, date
import pandas as pd
import numpy as np
import requests
from pandas import json_normalize
 
from PyQt5.QtWidgets import QDialog, QApplication

from interfaz import *


class PlanificacionAplicacion(QDialog):

    def __init__(self):

        super().__init__()
        self.dialogo = Ui_Proyeccion_produccion()
        self.dialogo.setupUi(self)
        now = date.today()
        fecha_inicial = date(now.year-1, now.month, 1) # Ventas del mes actual, un año atras
        fecha_final = fecha_inicial + timedelta(365/2) # Busco las ventas semestrales
        fecha_final= date(fecha_final.year, fecha_final.month, calendar.monthrange(fecha_final.year, fecha_final.month)[1])# Actualizo el ultimo dìa de mes.
        self.dialogo.fechaDesde.setDate(fecha_inicial)
        self.dialogo.fechahasta.setDate(fecha_final)
        self.dialogo.btn_buscar.clicked.connect(self.buscar_ventas)
        self.show()

    def buscar_ventas(self):

        fechaDesde = self.dialogo.fechaDesde.date().toString("yyyy-MM-dd")
        fechaHasta = self.dialogo.fechahasta.date().toString("yyyy-MM-dd")

        self.dialogo.etiqueta.setText("Se buscan ventas del periodo "
                                      + fechaDesde + " - " + fechaHasta)


        #urlToken = 'https://1.teamplace.finneg.com/BSA/api/oauth/token?grant_type=client_credentials&client_id=d1b55163e09bfe454f4c83c74ddafd54&client_secret=210aaa7a0f51683ef139a0856c0ca2af'
        f= open('token.txt')

        urlToken= f.read()
        f.close()
        token = requests.get(urlToken).text


        argsRS = {'ACCESS_TOKEN': token,
                  'PARAMWEBREPORT_Empresa': 'PUNCH_PRUEBA38',
                  'PARAMWEBREPORT_AgruparPor': 1
                  }

        argsAF = {'ACCESS_TOKEN': token,
                  'PARAMWEBREPORT_Empresa': 'PUNCH34',
                  'PARAMWEBREPORT_FechaDesde': fechaDesde,
                  'PARAMWEBREPORT_FechaHasta': fechaHasta

                  }
        argsAF2 = {'ACCESS_TOKEN': token,
                   'PARAMWEBREPORT_Empresa': 'PUNCH_PRUEBA38',
                   'PARAMWEBREPORT_FechaDesde': fechaDesde,
                   'PARAMWEBREPORT_FechaHasta': fechaHasta

                   }
        urlResumenStock = 'https://api.teamplace.finneg.com/api/reports/RESUMENSTOCK?'

        urlAnalisisFacturacion = 'https://api.teamplace.finneg.com/api/reports/ANAFACTURACION'
        responseRS = requests.get(urlResumenStock, params=argsRS)
        responseAF = requests.get(urlAnalisisFacturacion, params=argsAF)
        responseAF2 = requests.get(urlAnalisisFacturacion, params=argsAF2)

        self.dialogo.etiqueta.setWordWrap(True)
        mensaje= " Resultado consultas : \n"

        if responseRS.status_code == 200:
            responseRS_json = responseRS.json()
            stock = json_normalize(responseRS_json)
            mensaje= mensaje + "Consulta de Stock= OK\n"

        if responseAF.status_code == 200:
            responseAF_json = responseAF.json()
            ventas = json_normalize(responseAF_json)
            mensaje = mensaje + "Consulta facturacion 1/2= OK\n"

        if responseAF2.status_code == 200:
            responseAF2_json = responseAF2.json()
            ventas2 = json_normalize(responseAF2_json)
            mensaje = mensaje + "Consulta facturacion 2/2 = OK\n"

        ventasTotales = pd.concat([ventas, ventas2])
        self.dialogo.label_mensaje_request.setText(mensaje)

        meses = list(set(ventasTotales['ANO-MES']))
        meses.sort()

        stock_total = stock[['PRODUCTO', 'CANTIDAD1'
                             #   ,'DEPOSITO'
                             ]].groupby(by=["PRODUCTO"]).agg('sum').rename(columns={'CANTIDAD1': 'Stock'})

        stock_total.Stock = stock_total.Stock.astype(int)

        # cols = ventasTotales.columns.tolist()
        # print(cols)

        TotalventasPorProducto = ventasTotales[['PRODUCTO', 'CANTIDAD', 'ANO-MES']].groupby(
            by=['PRODUCTO']).sum().rename(columns={'CANTIDAD': 'Ventas Periodo'})


        TotalventasPorProducto['Ventas Periodo'] = TotalventasPorProducto['Ventas Periodo'].astype(int)

        Ventas_Por_Mes = pd.pivot_table(ventasTotales[['FAMILIA', 'PRODUCTO', 'ANO-MES', 'CANTIDAD']],
                                        values='CANTIDAD', index=['PRODUCTO'], columns=['ANO-MES'], aggfunc=np.sum,
                                        fill_value=0)

        merged_inner = pd.merge(left=Ventas_Por_Mes, right=stock_total, left_on='PRODUCTO', right_on='PRODUCTO')

        tablafinal = pd.merge(left=merged_inner, right=TotalventasPorProducto, left_on='PRODUCTO', right_on='PRODUCTO')

        nombreArchivo= 'proyeccion desde ' + fechaDesde + ' hasta ' + fechaHasta + '.xlsx'



        def aFabricar(fila):

            resultado = fila['Ventas Periodo'] - fila['Stock']
            if resultado < 0:
                resultado = 0
            return resultado

        tablafinal['A fabricar'] = tablafinal.apply(aFabricar, axis=1)
        tablafinal.to_excel(nombreArchivo, sheet_name='Proyeccion')
        mensaje += "\nExcel descargado : " + nombreArchivo

        self.dialogo.label_mensaje_request.setText(mensaje)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogo = PlanificacionAplicacion()
    dialogo.show()
    sys.exit(app.exec_())

