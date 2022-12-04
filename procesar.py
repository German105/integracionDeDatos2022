#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import csv

dirLeyesParlamento = 'sLista.csv'
dirArticulos = 'articulos.csv'

salida = 'salida.csv'

rMencionExplicita = 'ley n.° (\d+)\.(\d+)'
rMencionPorNumero = '(\d+)\.(\d+)'

if __name__ == '__main__':
    fArticulos = open(dirArticulos, 'r')
    articulos = csv.reader(fArticulos, delimiter = '\t')

    fLeyerParlament = open(dirLeyesParlamento, 'r')
    leyesParlamento = csv.DictReader(fLeyerParlament, delimiter = ',')

    tuplasArticuloMencionExplicita = []
    tuplasArticuloMencionPorNumero = []

    for a in articulos:
        articuloNormalizado = a[1].lower() + a[3].lower()

        #Match por numero
        matchPorNumero = re.findall(rMencionPorNumero, articuloNormalizado)
        resultadoDeArticuloPorNumero = []
        for tuple in matchPorNumero:
            resultadoDeArticuloPorNumero.append(tuple[0] + tuple[1])
        for i in resultadoDeArticuloPorNumero:
            if int(i) < 20079:
                tuplasArticuloMencionPorNumero.append([a[0], i])

        #Match por mencion
        matchPorMencion = re.findall(rMencionExplicita, articuloNormalizado)
        resultadoDeArticuloPorMencion = []
        for tuple in matchPorMencion:
            if tuple:
                number = tuple[0] + tuple[1]
                resultadoDeArticuloPorMencion.append(number)
        for i in resultadoDeArticuloPorMencion:
            tuplasArticuloMencionExplicita.append([a[0], i])

    f = open(salida, 'w+')
    writer = csv.writer(f)
    for i in tuplasArticuloMencionExplicita:
        fila = i
        fila.append('MencionExplicita')
        writer.writerow(fila)
    for i in tuplasArticuloMencionPorNumero:
            fila = i
            fila.append('MencionPorNumero')
            writer.writerow(fila)
    print(tuplasArticuloMencionExplicita)
