# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 20:59:09 2019

@author: User
"""
import math
import random
from datetime import datetime, timedelta
from itertools import product

from colorama import Back, Fore, Style, deinit, init

import tableformatter as tf


#Função para obter o símbolo que representa cada peça
def tipo(peça):
  cod= peça.tipo
  if cod == 1:
    return "王"  #Rei
  if cod == 2:
    return "飛"  #Carruagem voadora
  if cod == 3:
    return "龍"  #Dragão
  if cod == 4:
    return "角"  #Angulador
  if cod == 5:
    return "馬"  #Cavalo Dragão
  if cod == 6:
    return "金"  #General de Ouro
  if cod == 7:
    return "銀"  #General de Prata
  if cod == 8:
    return "全"  #Prata promovido
  if cod == 9:
    return "桂"  #Cavalo
  if cod == 10:
    return "今"   #Cavalo promovido
  if cod == 11:
    return "香"   #Carruagem de Incenso
  if cod == 12:
    return "仝"   #Incenso promovido
  if cod == 13:
    return "歩"   #Soldado Raso
  else:
    return "と"   #Tokin

#Definição dos objetos: Peça, Jogador, Tabuleiro etc.  
class Peça:
  def __init__(self, tipo, jogador, coords):
    self.tipo= tipo
    self.jogador= jogador
    self.coords= coords

class Jogador:
  def __init__(self, cor):
    self.cor= cor
    if cor == "Preto":
      self.peças= [Peça(13, 1, (6,0)), Peça(13, 1, (6,1)), Peça(13, 1, (6,2)), Peça(13, 1, (6,3)), Peça(13, 1, (6,4)), 
             Peça(13, 1, (6,5)), Peça(13, 1, (6,6)), Peça(13, 1, (6,7)), Peça(13, 1, (6,8)), Peça(4, 1, (7,1)),
             Peça(2, 1, (7,7)), Peça(11, 1, (8,0)), Peça(9, 1, (8,1)), Peça(7, 1, (8,2)), Peça(6, 1, (8,3)), 
             Peça(1, 1, (8,4)), Peça(6, 1, (8,5)), Peça(7, 1, (8,6)), Peça(9, 1, (8,7)), Peça(11, 1, (8,8))]
      self.rei= (8,4)
    else:
      self.peças= [Peça(13, 2, (2,0)), Peça(13, 2, (2,1)), Peça(13, 2, (2,2)), Peça(13, 2, (2,3)), Peça(13, 2, (2,4)), 
             Peça(13, 2, (2,5)), Peça(13, 2, (2,6)), Peça(13, 2, (2,7)), Peça(13, 2, (2,8)), Peça(4, 2, (1,7)),
             Peça(2, 2, (1,1)), Peça(11, 2, (0,0)), Peça(9, 2, (0,1)), Peça(7, 2, (0,2)), Peça(6, 2, (0,3)), 
             Peça(1, 2, (0,4)), Peça(6, 2, (0,5)), Peça(7, 2, (0,6)), Peça(9, 2, (0,7)), Peça(11, 2, (0,8))]
      self.rei= (0,4)
    self.reserva= []
    
#Variável que representa as posições vazias do tabuleiro
casasVazias=[(1,0), (1,2), (1,3), (1,4), (1,5), (1,6), (1,8),
        (3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7), (3,8),
        (4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7), (4,8),
        (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8),
        (7,0), (7,2), (7,3), (7,4), (7,5), (7,6), (7,8)]

jogadores= (Jogador("Preto"), Jogador("Branco"))


class Estado:
  def __init__(self, turno):
    self.turno= turno
    self.peças1= jogadores[0].peças.copy()
    self.peças2= jogadores[1].peças.copy()
    self.reserva1= jogadores[0].reserva.copy()
    self.reserva2= jogadores[1].reserva.copy()
    self.vazias= casasVazias.copy()
    self.tsumi= 0
    self.rei1= jogadores[0].rei
    self.rei2= jogadores[1].rei
    
  def copy(self):
    copia= Estado(self.turno)
    copia.peças1= []
    copia.peças2= []
    copia.reserva1= []
    copia.reserva2= []
    copia.vazias= []
    for peça in self.peças1:
      copia.peças1.append(Peça(peça.tipo, peça.jogador, peça.coords))
    for peça in self.peças2:
      copia.peças2.append(Peça(peça.tipo, peça.jogador, peça.coords))
    for peça in self.reserva1:
      copia.reserva1.append(Peça(peça.tipo, peça.jogador, peça.coords))
    for peça in self.reserva2:
      copia.reserva2.append(Peça(peça.tipo, peça.jogador, peça.coords))
    for par in self.vazias:
      copia.vazias.append((par[0], par[1]))
    copia.tsumi= self.tsumi
    copia.rei1= self.rei1
    copia.rei2= self.rei2
    return copia

historico= [Estado(0)]

#Funções para mostrar o estado atual do tabuleiro no terminal
def montaMatriz(s):
  mat= [["  " for j in range(9)] for i in range(9)]
  for peça in s.peças1:
    mat[peça.coords[0]][peça.coords[1]]= (Style.BRIGHT + Fore.BLUE + tipo(peça))
  for peça in s.peças2:
    mat[peça.coords[0]][peça.coords[1]]= (Style.BRIGHT + Fore.RED + tipo(peça))
  return mat

def montaMatriz1(s):
  mat= [[Fore.WHITE + " " for j in range(9)] for i in range(9)]
  for peça in s.peças1:
    mat[peça.coords[0]][peça.coords[1]]= (Fore.WHITE + tipo(peça))
  for peça in s.peças2:
    mat[peça.coords[0]][peça.coords[1]]= (Fore.BLUE + tipo(peça))
  return mat


def mostra(s):
  tabuleiro= montaMatriz(s)
  peças1= []
  peças2= []
  for peça in s.reserva1:
    peças1.append(tipo(peça))
  for peça in s.reserva2:
    peças2.append(tipo(peça))
  print(Fore.WHITE + "Mão Branca: " + " ".join(peças2) + "\n")
  print(Fore.WHITE + "Mão Preta: " + " ".join(peças1) + "\n")
  
  for i in range(9):
    for j in range(9):
      print(tabuleiro[i][j], end= " ")
    print("")
  
def mostraTabuleiro(s):
  tabuleiro= montaMatriz1(s)
  peças1= []
  peças2= []
  for peça in s.reserva1:
    peças1.append(tipo(peça))
  for peça in s.reserva2:
    peças2.append(tipo(peça))
  print("Mão Branca: " + " ".join(peças2) + "\n")
  print("Mão Preta: " + " ".join(peças1) + "\n")
  init()
  print(tf.generate_table(tabuleiro))
  deinit()
  

# Retorna o jogador no estado/turno s
def jogadorAtual(s):
  if s.turno%2 == 0:
    return 1
  else:
    return 2
  
#Verificação se a posição especificada está livre ou ocupada por uma peça aliada   
def verificaOcupado(s, coords):
  p= jogadorAtual(s)
  if p < 2:
    areaDeBusca= s.peças1
  else:
    areaDeBusca= s.peças2
  for peça in areaDeBusca:
    if peça.coords == coords:
      return True
  return False

#Verificação se a posição especificada está livre ou ocupada por uma peça inimiga
def verificaCaptura(s, coords):
  p= jogadorAtual(s)
  if p < 2:
    areaDeBusca= s.peças2
  else:
    areaDeBusca= s.peças1
  for peça in areaDeBusca:
    if peça.coords == coords:
      if p == 1:
        return s.peças2.index(peça)
      else:
        return s.peças1.index(peça)
  return -1

#Função auxiliar para formar a lista das ações possíveis
def açãoDeMovimento(ação, lista, s, indice):
  if verificaOcupado(s, ação[1]):
    return
  capturado= verificaCaptura(s, ação[1])
  
  p= jogadorAtual(s)
  if p == 1:
    peça= s.peças1[indice]
    if capturado >= 0:
      ação= (ação[0], ação[1], capturado)
  else:
    peça= s.peças2[indice]
    if capturado >= 0:
      ação= (ação[0], ação[1], capturado)
  if (peça.tipo < 6 and peça.tipo%2 > 0) or (peça.tipo > 5 and peça.tipo%2 < 1):
    if p == 1:
      lista.append((*ação, s.peças1.index(peça), False))
    else:
      lista.append((*ação, s.peças2.index(peça), False))
  elif (peça.tipo > 8 and peça.tipo%2 > 0) and ((p < 2 and ação[1][0] < 1) or (p > 1 and ação[1][0] > 7)):
    if p == 1:
      lista.append((*ação, s.peças1.index(peça), True))
    else:
      lista.append((*ação, s.peças2.index(peça), True))
  elif peça.tipo == 9 and ((p < 2 and ação[1][0] < 2) or (p > 1 and ação[1][0] > 6)):
    if p == 1:
      lista.append((*ação, s.peças1.index(peça), True))
    else:
      lista.append((*ação, s.peças2.index(peça), True))
  elif (p < 2 and (ação[0][0] < 3 or ação[1][0] < 3) or (p > 1 and(ação[0][0] > 5 or ação[1][0] > 5))):
    if p == 1:
      lista.append((*ação, s.peças1.index(peça), False))
      lista.append((*ação, s.peças1.index(peça), True))
    else:
      lista.append((*ação, s.peças2.index(peça), False))
      lista.append((*ação, s.peças2.index(peça), True))
  else:
    if p == 1:
      lista.append((*ação, s.peças1.index(peça), False))
    else:
      lista.append((*ação, s.peças2.index(peça), False))
      
#Função para determinar todos os drops possíveis no turno atual
def dropsPossíveis(s, p):
  if len(s.vazias) == 0:
    return []
  if p < 2:
    indices= []
    i= 0
    for peça in s.reserva1:
      indices.append(i)
      i= i+1
    cartesiano= list(product(indices, s.vazias))
    for par in cartesiano:
      if s.reserva1[par[0]].tipo != 13 and s.reserva1[par[0]].tipo != 11 and s.reserva1[par[0]].tipo != 9:
        continue
      if s.reserva1[par[0]].tipo == 13 and (par[1][0] == (s.rei2[0] - 1)) and (par[1][1] == s.rei2[1]):
        cartesiano.remove(par)
        continue
      if par[1][0] == 0:
        cartesiano.remove(par)
        continue
      if s.reserva1[par[0]].tipo == 9 and par[1][0] == 1:
        cartesiano.remove(par)
        continue
      if s.reserva1[par[0]].tipo == 13:
        flag= False
        for peça in s.peças1:
          if peça.tipo == 13 and peça.coords[1] == par[1][1]:
            cartesiano.remove(par)
            flag= True
            break
        if flag:
          continue
  else:
    indices= []
    i= 0
    for peça in s.reserva2:
      indices.append(i)
      i= i+1
    cartesiano= list(product(indices, s.vazias))
    for par in cartesiano:
      if s.reserva2[par[0]].tipo != 13 and s.reserva2[par[0]].tipo != 11 and s.reserva2[par[0]].tipo != 9:
        continue
      if s.reserva2[par[0]].tipo == 13 and (par[1][0] == (s.rei1[0] - 1)) and (par[1][1] == s.rei1[1]):
        cartesiano.remove(par)
        continue
      if par[1][0] == 8:
        cartesiano.remove(par)
        continue
      if s.reserva2[par[0]].tipo == 9 and par[1][0] == 7:
         cartesiano.remove(par)
         continue
      if s.reserva2[par[0]].tipo == 13:
        flag= False
        for peça in s.peças2:
          if peça.tipo == 13 and peça.coords[1] == par[1][1]:
            cartesiano.remove(par)
            flag= True
            break
        if flag:
          continue
  return cartesiano

#Função principal para determinar os movimentos de peças possíveis no turno atual
def movimentosPossíveis(s, peça):
  listaAções= []
  if peça.jogador == 1:
    if peça.tipo == 1:
      if peça.coords[0] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1])), listaAções, s, s.peças1.index(peça))
        if peça.coords[1] > 0:
          açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1] - 1)), listaAções, s, s.peças1.index(peça))
        if peça.coords[1] < 8:
          açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1] + 1)), listaAções, s, s.peças1.index(peça))
      if peça.coords[0] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1])), listaAções, s, s.peças1.index(peça))
        if peça.coords[1] > 0:
          açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1] - 1)), listaAções, s, s.peças1.index(peça))
        if peça.coords[1] < 8:
          açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1] + 1)), listaAções, s, s.peças1.index(peça))
      if peça.coords[1] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] - 1)), listaAções, s, s.peças1.index(peça))
      if peça.coords[1] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] + 1)), listaAções, s, s.peças1.index(peça))
    elif peça.tipo == 2:
      if peça.coords[0] > 0:
        for i in range(peça.coords[0] - 1, -1, -1):
          ação= (peça.coords, (i, peça.coords[1]))
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (i, peça.coords[1]))
          if capturado >= 0:
            #listaAções.append((ação[0], ação[1], capturado, a))
            if s.peças2[capturado].tipo == 1:
              return [(*ação, capturado, s.peças1.index(peça), False)]
            ação= (*ação, capturado)
            if (ação[0][0] < 3 or ação[1][0] < 3):
              listaAções.append((*ação, s.peças1.index(peça), False))
              listaAções.append((*ação, s.peças1.index(peça), True))
            else:
              listaAções.append((*ação, s.peças1.index(peça), False))
            break
          if (ação[0][0] < 3 or ação[1][0] < 3):
            listaAções.append((*ação, s.peças1.index(peça), False))
            listaAções.append((*ação, s.peças1.index(peça), True))
          else:
            listaAções.append((*ação, s.peças1.index(peça), False))
      if peça.coords[0] < 8:
        for i in range(peça.coords[0] + 1, 9):
          ação= (peça.coords, (i, peça.coords[1]))
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (i, peça.coords[1]))
          if capturado >= 0:
            if s.peças2[capturado].tipo == 1:
              return [(*ação, capturado, s.peças1.index(peça), False)]
            ação= (*ação, capturado)
            if (ação[0][0] < 3 or ação[1][0] < 3):
              listaAções.append((*ação, s.peças1.index(peça), False))
              listaAções.append((*ação, s.peças1.index(peça), True))
            else:
              listaAções.append((*ação, s.peças1.index(peça), False))
            #listaAções.append((ação[0], ação[1], capturado, a))
            break
          if (ação[0][0] < 3 or ação[1][0] < 3):
            listaAções.append((*ação, s.peças1.index(peça), False))
            listaAções.append((*ação, s.peças1.index(peça), True))
          else:
            listaAções.append((*ação, s.peças1.index(peça), False))
      if peça.coords[1] > 0:
        for i in range(peça.coords[1] - 1, -1, -1):
          ação= ((peça.coords[0], i), peça.coords)
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (peça.coords[0], i))
          if capturado >= 0:
            #listaAções.append((ação[0], ação[1], capturado, a))
            if s.peças2[capturado].tipo == 1:
              return [(*ação, capturado, s.peças1.index(peça), False)]
            ação= (*ação, capturado)
            if (ação[0][0] < 3 or ação[1][0] < 3):
              listaAções.append((*ação, s.peças1.index(peça), False))
              listaAções.append((*ação, s.peças1.index(peça), True))
            else:
              listaAções.append((*ação, s.peças1.index(peça), False))
            break
          if (ação[0][0] < 3 or ação[1][0] < 3):
            listaAções.append((*ação, s.peças1.index(peça), False))
            listaAções.append((*ação, s.peças1.index(peça), True))
          else:
            listaAções.append((*ação, s.peças1.index(peça), False))
      if peça.coords[1] < 8:
        for i in range(peça.coords[1] + 1, 9):
          ação= ((peça.coords[0], i), peça.coords)
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (peça.coords[0], i))
          if capturado >= 0:
            if s.peças2[capturado].tipo == 1:
              return [(*ação, capturado, s.peças1.index(peça), False)]
            ação= (*ação, capturado)
            if (ação[0][0] < 3 or ação[1][0] < 3):
              listaAções.append((*ação, s.peças1.index(peça), False))
              listaAções.append((*ação, s.peças1.index(peça), True))
            else:
              listaAções.append((*ação, s.peças1.index(peça), False))
            #listaAções.append((ação[0], ação[1], capturado, a))
            break
          if (ação[0][0] < 3 or ação[1][0] < 3):
            listaAções.append((*ação, s.peças1.index(peça), False))
            listaAções.append((*ação, s.peças1.index(peça), True))
          else:
            listaAções.append((*ação, s.peças1.index(peça), False))
    elif peça.tipo == 3:
      if peça.coords[0] > 0:
        if peça.coords[1] > 0:
          açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1] - 1)), listaAções, s, s.peças1.index(peça))
        if peça.coords[1] < 8:
          açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1] + 1)), listaAções, s, s.peças1.index(peça))
        for i in range(peça.coords[0] - 1, -1, -1):
          ação= (peça.coords, (i, peça.coords[1]))
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (i, peça.coords[1]))
          if capturado >= 0:
            if s.peças2[capturado].tipo == 1:
              return [(*ação, capturado, s.peças1.index(peça), False)]
            listaAções.append((ação[0], ação[1], capturado, s.peças1.index(peça), False))
            break
          listaAções.append((*ação, s.peças1.index(peça), False))
      if peça.coords[0] < 8:
        if peça.coords[1] > 0:
          açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1] - 1)), listaAções, s, s.peças1.index(peça))
        if peça.coords[1] < 8:
          açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1] + 1)), listaAções, s, s.peças1.index(peça))
        for i in range(peça.coords[0] + 1, 9):
          ação= (peça.coords, (i, peça.coords[1]))
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, ação[1])
          if capturado >= 0:
            if s.peças2[capturado].tipo == 1:
              return [(*ação, capturado, s.peças1.index(peça), False)]
            listaAções.append((ação[0], ação[1], capturado, s.peças1.index(peça), False))
            break
          listaAções.append((*ação, s.peças1.index(peça), False))
      if peça.coords[1] > 0:
        for i in range(peça.coords[1] - 1, -1, -1):
          ação= ((peça.coords[0], i), peça.coords)
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (peça.coords[0], i))
          if capturado >= 0:
            #listaAções.append((ação[0], ação[1], capturado, a))
            if s.peças2[capturado].tipo == 1:
              return [(*ação, capturado, s.peças1.index(peça), False)]
            ação= (*ação, capturado)
            listaAções.append((*ação, s.peças1.index(peça), False))
            break
          listaAções.append((*ação, s.peças1.index(peça), False))
      if peça.coords[1] < 8:
        for i in range(peça.coords[1] + 1, 9):
          ação= ((peça.coords[0], i), peça.coords)
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (peça.coords[0], i))
          if capturado >= 0:
            if s.peças2[capturado].tipo == 1:
              return [(*ação, capturado, s.peças1.index(peça), False)]
            ação= (*ação, capturado)
            listaAções.append((*ação, s.peças1.index(peça), False))
            #listaAções.append((ação[0], ação[1], capturado, a))
            break
          listaAções.append((*ação, s.peças1.index(peça), False))
      if peça.coords[1] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] - 1)), listaAções, s, s.peças1.index(peça))
      if peça.coords[1] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] + 1)), listaAções, s, s.peças1.index(peça))
    elif peça.tipo == 4:
      if peça.coords[0] > 0:
        if peça.coords[1] > 0:
          for i in range(min(peça.coords[0], peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] - i, peça.coords[1] - i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças2[capturado].tipo == 1:
                return [(*ação, capturado, s.peças1.index(peça), False)]
              ação= (*ação, capturado)
              #listaAções.append((ação[0], ação[1], capturado, a))
              if (ação[0][0] < 3 or ação[1][0] < 3):
                listaAções.append((*ação, s.peças1.index(peça), False))
                listaAções.append((*ação, s.peças1.index(peça), True))
              else:
                listaAções.append((*ação, s.peças1.index(peça), False))
              break
            if (ação[0][0] < 3 or ação[1][0] < 3):
              listaAções.append((*ação, s.peças1.index(peça), False))
              listaAções.append((*ação, s.peças1.index(peça), True))
            else:
              listaAções.append((*ação, s.peças1.index(peça), False))
        if peça.coords[1] < 8:
          for i in range(min(peça.coords[0], 8 - peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] - i, peça.coords[1] + i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças2[capturado].tipo == 1:
                return [(*ação, capturado, s.peças1.index(peça), False)]
              ação= (*ação, capturado)
              if (ação[0][0] < 3 or ação[1][0] < 3):
                listaAções.append((*ação, s.peças1.index(peça), False))
                listaAções.append((*ação, s.peças1.index(peça), True))
              else:
                listaAções.append((*ação, s.peças1.index(peça), False))
              #listaAções.append((ação[0], ação[1], capturado, a))
              break
            if (ação[0][0] < 3 or ação[1][0] < 3):
              listaAções.append((*ação, s.peças1.index(peça), False))
              listaAções.append((*ação, s.peças1.index(peça), True))
            else:
              listaAções.append((*ação, s.peças1.index(peça), False))
      if peça.coords[1] < 8:
        if peça.coords[1] > 0:
          for i in range(min(8 - peça.coords[0], peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] + i, peça.coords[1] - i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças2[capturado].tipo == 1:
                return [(*ação, capturado, s.peças1.index(peça), False)]
              ação= (*ação, capturado)
              #listaAções.append((ação[0], ação[1], capturado, a))
              if (ação[0][0] < 3 or ação[1][0] < 3):
                listaAções.append((*ação, s.peças1.index(peça), False))
                listaAções.append((*ação, s.peças1.index(peça), True))
              else:
                listaAções.append((*ação, s.peças1.index(peça), False))
              break
            if (ação[0][0] < 3 or ação[1][0] < 3):
              listaAções.append((*ação, s.peças1.index(peça), False))
              listaAções.append((*ação, s.peças1.index(peça), True))
            else:
              listaAções.append((*ação, s.peças1.index(peça), False))
        if peça.coords[1] < 8:
          for i in range(min(8 - peça.coords[0], 8 - peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] + i, peça.coords[1] + i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças2[capturado].tipo == 1:
                return [(*ação, capturado, s.peças1.index(peça), False)]
              ação= (*ação, capturado)
              #listaAções.append((ação[0], ação[1], capturado, a))
              if (ação[0][0] < 3 or ação[1][0] < 3):
                listaAções.append((*ação, s.peças1.index(peça), False))
                listaAções.append((*ação, s.peças1.index(peça), True))
              else:
                listaAções.append((*ação, s.peças1.index(peça), False))
              break
            if (ação[0][0] < 3 or ação[1][0] < 3):
              listaAções.append((*ação, s.peças1.index(peça), False))
              listaAções.append((*ação, s.peças1.index(peça), True))
            else:
              listaAções.append((*ação, s.peças1.index(peça), False))
    elif peça.tipo == 5:
      if peça.coords[0] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1])), listaAções, s, s.peças1.index(peça))
        if peça.coords[1] > 0:
          for i in range(min(peça.coords[0], peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] - i, peça.coords[1] - i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças2[capturado].tipo == 1:
                return [(*ação, capturado, s.peças1.index(peça), False)]
              listaAções.append((ação[0], ação[1], capturado, s.peças1.index(peça), False))
              break
            listaAções.append((*ação, s.peças1.index(peça), False))
        if peça.coords[1] < 8:
          for i in range(min(peça.coords[0], 8 - peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] - i, peça.coords[1] + i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças2[capturado].tipo == 1:
                return [(*ação, capturado, s.peças1.index(peça), False)]
              listaAções.append((ação[0], ação[1], capturado, s.peças1.index(peça), False))
              break
            listaAções.append((*ação, s.peças1.index(peça), False))
      if peça.coords[0] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1])), listaAções, s, s.peças1.index(peça))
        if peça.coords[1] > 0:
          for i in range(min(8 - peça.coords[0], peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] + i, peça.coords[1] - i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças2[capturado].tipo == 1:
                return [(*ação, capturado, s.peças1.index(peça), False)]
              listaAções.append((ação[0], ação[1], capturado, s.peças1.index(peça), False))
              break
            listaAções.append((*ação, s.peças1.index(peça), False))
        if peça.coords[1] < 8:
          for i in range(min(8 - peça.coords[0], 8 - peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] + i, peça.coords[1] + i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças2[capturado].tipo == 1:
                return [(*ação, capturado, s.peças1.index(peça), False)]
              listaAções.append((ação[0], ação[1], capturado, s.peças1.index(peça), False))
              break
            listaAções.append((*ação, s.peças1.index(peça), False))
      if peça.coords[1] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] - 1)), listaAções, s, s.peças1.index(peça))
      if peça.coords[1] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] + 1)), listaAções, s, s.peças1.index(peça))
         
    elif peça.tipo == 6 or peça.tipo == 8 or peça.tipo == 10 or peça.tipo == 12 or peça.tipo == 14:
      if peça.coords[0] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1])), listaAções, s, s.peças1.index(peça))
        if peça.coords[1] > 0:
          açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1] - 1)), listaAções, s, s.peças1.index(peça))
        if peça.coords[1] < 8:
          açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1] + 1)), listaAções, s, s.peças1.index(peça))
      if peça.coords[1] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] - 1)), listaAções, s, s.peças1.index(peça))
      if peça.coords[1] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] + 1)), listaAções, s, s.peças1.index(peça))
      if peça.coords[0] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1])), listaAções, s, s.peças1.index(peça))
    elif peça.tipo == 7:
      if peça.coords[0] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1])), listaAções, s, s.peças1.index(peça))
        if peça.coords[1] > 0:
          açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1] - 1)), listaAções, s, s.peças1.index(peça))
        if peça.coords[1] < 8:
          açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1] + 1)), listaAções, s, s.peças1.index(peça))
      if peça.coords[0] < 8:
        if peça.coords[1] > 0:
          açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1] - 1)), listaAções, s, s.peças1.index(peça))
        if peça.coords[1] < 8:
          açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1] + 1)), listaAções, s, s.peças1.index(peça))
    elif peça.tipo == 9:
      if peça.coords[1] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0] - 2, peça.coords[1] - 1)), listaAções, s, s.peças1.index(peça))
      if peça.coords[1] <8:
        açãoDeMovimento((peça.coords, (peça.coords[0] - 2, peça.coords[1] + 1)), listaAções, s, s.peças1.index(peça))
    elif peça.tipo == 11:
      if peça.coords[0] > 0:
        for i in range(peça.coords[0] - 1, -1, -1):
          ação= (peça.coords, (i, peça.coords[1]))
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (i, peça.coords[1]))
          if capturado >= 0:
            if s.peças2[capturado].tipo == 1:
              return [(*ação, capturado, s.peças1.index(peça), False)]
            ação= (*ação, capturado)
            if (ação[0][0] < 1 or ação[1][0] < 1):
              listaAções.append((*ação, s.peças1.index(peça), True))
            elif ação[1][0] < 3:
              listaAções.append((*ação, s.peças1.index(peça), False))
              listaAções.append((*ação, s.peças1.index(peça), True))
            else:
              listaAções.append((*ação, s.peças1.index(peça), False))
            break
          if ação[1][0] < 1:
            listaAções.append((*ação, s.peças1.index(peça), True))
          elif (ação[0][0] < 3 or ação[1][0] < 3):
            listaAções.append((*ação, s.peças1.index(peça), False))
            listaAções.append((*ação, s.peças1.index(peça), True))
          else:
            listaAções.append((*ação, s.peças1.index(peça), False))
    elif peça.tipo == 13:
      açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1])), listaAções, s, s.peças1.index(peça))
      
  else:
    if peça.tipo == 1:
      if peça.coords[0] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1])), listaAções, s, s.peças2.index(peça))
        if peça.coords[1] > 0:
          açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1] - 1)), listaAções, s, s.peças2.index(peça))
        if peça.coords[1] < 8:
          açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1] + 1)), listaAções, s, s.peças2.index(peça))
      if peça.coords[0] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1])), listaAções, s, s.peças2.index(peça))
        if peça.coords[1] > 0:
          açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1] - 1)), listaAções, s, s.peças2.index(peça))
        if peça.coords[1] < 8:
          açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1] + 1)), listaAções, s, s.peças2.index(peça))
      if peça.coords[1] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] - 1)), listaAções, s, s.peças2.index(peça))
      if peça.coords[1] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] + 1)), listaAções, s, s.peças2.index(peça))
    elif peça.tipo == 2:
      if peça.coords[0] > 0:
        for i in range(peça.coords[0] - 1, -1, -1):
          ação= (peça.coords, (i, peça.coords[1]))
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (i, peça.coords[1]))
          if capturado >= 0:
            if s.peças1[capturado].tipo == 1:
              return [(*ação, capturado, s.peças2.index(peça), False)]
            ação= (*ação, capturado)
            if (ação[0][0] > 5 or ação[1][0] > 5):
              listaAções.append((*ação, s.peças2.index(peça), False))
              listaAções.append((*ação, s.peças2.index(peça), True))
            else:
              listaAções.append((*ação, s.peças2.index(peça), False))
            #listaAções.append((ação[0], ação[1], capturado))
            break
          if (ação[0][0] > 5 or ação[1][0] > 5):
            listaAções.append((*ação, s.peças2.index(peça), False))
            listaAções.append((*ação, s.peças2.index(peça), True))
          else:
            listaAções.append((*ação, s.peças2.index(peça), False))
      if peça.coords[0] < 8:
        for i in range(peça.coords[0] + 1, 9):
          ação= (peça.coords, (i, peça.coords[1]))
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (i, peça.coords[1]))
          if capturado >= 0:
            if s.peças1[capturado].tipo == 1:
              return [(*ação, capturado, s.peças2.index(peça), False)]
            ação= (*ação, capturado)
            if (ação[0][0] > 5 or ação[1][0] > 5):
              listaAções.append((*ação, s.peças2.index(peça), False))
              listaAções.append((*ação, s.peças2.index(peça), True))
            else:
              listaAções.append((*ação, s.peças2.index(peça), False))
            #listaAções.append((ação[0], ação[1], capturado))
            break
          if (ação[0][0] > 5 or ação[1][0] > 5):
            listaAções.append((*ação, s.peças2.index(peça), False))
            listaAções.append((*ação, s.peças2.index(peça), True))
          else:
            listaAções.append((*ação, s.peças2.index(peça), False))
      if peça.coords[1] > 0:
        for i in range(peça.coords[1] - 1, -1, -1):
          ação= (peça.coords, (peça.coords[0], i))
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (peça.coords[0], i))
          if capturado >= 0:
            if s.peças1[capturado].tipo == 1:
              return [(*ação, capturado, s.peças2.index(peça), False)]
            ação= (*ação, capturado)
            if (ação[0][0] > 5 or ação[1][0] > 5):
              listaAções.append((*ação, s.peças2.index(peça), False))
              listaAções.append((*ação, s.peças2.index(peça), True))
            else:
              listaAções.append((*ação, s.peças2.index(peça), False))
            #listaAções.append((ação[0], ação[1], capturado))
            break
          if (ação[0][0] > 5 or ação[1][0] > 5):
            listaAções.append((*ação, s.peças2.index(peça), False))
            listaAções.append((*ação, s.peças2.index(peça), True))
          else:
            listaAções.append((*ação, s.peças2.index(peça), False))
      if peça.coords[1] < 8:
        for i in range(peça.coords[1] + 1, 9):
          ação= (peça.coords, (peça.coords[0], i))
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (peça.coords[0], i))
          if capturado >= 0:
            if s.peças1[capturado].tipo == 1:
              return [(*ação, capturado, s.peças2.index(peça), False)]
            ação= (*ação, capturado)
            if (ação[0][0] > 5 or ação[1][0] > 5):
              listaAções.append((*ação, s.peças2.index(peça), False))
              listaAções.append((*ação, s.peças2.index(peça), True))
            else:
              listaAções.append((*ação, s.peças2.index(peça), False))
            #listaAções.append((ação[0], ação[1], capturado))
            break
          if (ação[0][0] > 5 or ação[1][0] > 5):
            listaAções.append((*ação, s.peças2.index(peça), False))
            listaAções.append((*ação, s.peças2.index(peça), True))
          else:
            listaAções.append((*ação, s.peças2.index(peça), False))
    elif peça.tipo == 3:
      if peça.coords[0] > 0:
        if peça.coords[1] > 0:
          açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1] - 1)), listaAções, s, s.peças2.index(peça))
        if peça.coords[1] < 8:
          açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1] + 1)), listaAções, s, s.peças2.index(peça))
        for i in range(peça.coords[0] - 1, -1, -1):
          ação= (peça.coords, (i, peça.coords[1]))
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (i, peça.coords[1]))
          if capturado >= 0:
            if s.peças1[capturado].tipo == 1:
              return [(*ação, capturado, s.peças2.index(peça), False)]
            listaAções.append((ação[0], ação[1], capturado, s.peças2.index(peça), False))
            break
          listaAções.append((*ação, s.peças2.index(peça), False))
      if peça.coords[0] < 8:
        if peça.coords[1] > 0:
          açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1] - 1)), listaAções, s, s.peças2.index(peça))
        if peça.coords[1] < 8:
          açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1] + 1)), listaAções, s, s.peças2.index(peça))
        for i in range(peça.coords[0] + 1, 9):
          ação= (peça.coords, (i, peça.coords[1]))
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, ação[1])
          if capturado >= 0:
            if s.peças1[capturado].tipo == 1:
              return [(*ação, capturado, s.peças2.index(peça), False)]
            listaAções.append((ação[0], ação[1], capturado, s.peças2.index(peça), False))
            break
          listaAções.append((*ação, s.peças2.index(peça), False))
      if peça.coords[1] > 0:
        for i in range(peça.coords[1] - 1, -1, -1):
          ação= (peça.coords, (peça.coords[0], i))
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (peça.coords[0], i))
          if capturado >= 0:
            if s.peças1[capturado].tipo == 1:
              return [(*ação, capturado, s.peças2.index(peça), False)]
            ação= (*ação, capturado)
            listaAções.append((*ação, s.peças2.index(peça), False))
            #listaAções.append((ação[0], ação[1], capturado))
            break
          listaAções.append((*ação, s.peças2.index(peça), False))
      if peça.coords[1] < 8:
        for i in range(peça.coords[1] + 1, 9):
          ação= (peça.coords, (peça.coords[0], i))
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (peça.coords[0], i))
          if capturado >= 0:
            if s.peças1[capturado].tipo == 1:
              return [(*ação, capturado, s.peças2.index(peça), False)]
            ação= (*ação, capturado)
            listaAções.append((*ação, s.peças2.index(peça), False))
            #listaAções.append((ação[0], ação[1], capturado))
            break
          listaAções.append((*ação, s.peças2.index(peça), False))
      if peça.coords[1] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] - 1)), listaAções, s, s.peças2.index(peça))
      if peça.coords[1] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] + 1)), listaAções, s, s.peças2.index(peça))
    elif peça.tipo == 4:
      if peça.coords[0] > 0:
        if peça.coords[1] > 0:
          for i in range(min(peça.coords[0], peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] - i, peça.coords[1] - i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças1[capturado].tipo == 1:
                return [(*ação, capturado, s.peças2.index(peça), False)]
              ação= (*ação, capturado)
              if (ação[0][0] > 5 or ação[1][0] > 5):
                listaAções.append((*ação, s.peças2.index(peça), False))
                listaAções.append((*ação, s.peças2.index(peça), True))
              else:
                listaAções.append((*ação, s.peças2.index(peça), False))
              #listaAções.append((ação[0], ação[1], capturado))
              break
            if (ação[0][0] > 5 or ação[1][0] > 5):
              listaAções.append((*ação, s.peças2.index(peça), False))
              listaAções.append((*ação, s.peças2.index(peça), True))
            else:
              listaAções.append((*ação, s.peças2.index(peça), False))
        if peça.coords[1] < 8:
          for i in range(min(peça.coords[0], 8 - peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] - i, peça.coords[1] + i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças1[capturado].tipo == 1:
                return [(*ação, capturado, s.peças2.index(peça), False)]
              ação= (*ação, capturado)
              if (ação[0][1] > 5 or ação[1][0] > 5):
                listaAções.append((*ação, s.peças2.index(peça), False))
                listaAções.append((*ação, s.peças2.index(peça), True))
              else:
                listaAções.append((*ação, s.peças2.index(peça), False))
              #listaAções.append((ação[0], ação[1], capturado))
              break
            listaAções.append(ação)
      if peça.coords[1] < 8:
        if peça.coords[1] > 0:
          for i in range(min(8 - peça.coords[0], peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] + i, peça.coords[1] - i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças1[capturado].tipo == 1:
                return [(*ação, capturado, s.peças2.index(peça), False)]
              ação= (*ação, capturado)
              if (ação[0][0] > 5 or ação[1][0] > 5):
                listaAções.append((*ação, s.peças2.index(peça), False))
                listaAções.append((*ação, s.peças2.index(peça), True))
              else:
                listaAções.append((*ação, s.peças2.index(peça), False))
              #listaAções.append((ação[0], ação[1], capturado))
              break
            if (ação[0][0] > 5 or ação[1][0] > 5):
              listaAções.append((*ação, s.peças2.index(peça), False))
              listaAções.append((*ação, s.peças2.index(peça), True))
            else:
              listaAções.append((*ação, s.peças2.index(peça), False))
        if peça.coords[1] < 8:
          for i in range(min(8 - peça.coords[0], 8 - peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] + i, peça.coords[1] + i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças1[capturado].tipo == 1:
                return [(*ação, capturado, s.peças2.index(peça), False)]
              ação= (*ação, capturado)
              if (ação[0][0] > 5 or ação[1][0] > 5):
                listaAções.append((*ação, s.peças2.index(peça), False))
                listaAções.append((*ação, s.peças2.index(peça), True))
              else:
                listaAções.append((*ação, s.peças2.index(peça), False))
              #listaAções.append((ação[0], ação[1], capturado))
              break
            if (ação[0][0] > 5 or ação[1][0] > 5):
              listaAções.append((*ação, s.peças2.index(peça), False))
              listaAções.append((*ação, s.peças2.index(peça), True))
            else:
              listaAções.append((*ação, s.peças2.index(peça), False))
    elif peça.tipo == 5:
      if peça.coords[0] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1])), listaAções, s, s.peças2.index(peça))
        if peça.coords[1] > 0:
          for i in range(min(peça.coords[0], peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] - i, peça.coords[1] - i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças1[capturado].tipo == 1:
                return [(*ação, capturado, s.peças2.index(peça), False)]
              listaAções.append((ação[0], ação[1], capturado, s.peças2.index(peça), False))
              break
            listaAções.append((*ação, s.peças2.index(peça), False))
        if peça.coords[1] < 8:
          for i in range(min(peça.coords[0], 8 - peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] - i, peça.coords[1] + i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças1[capturado].tipo == 1:
                return [(*ação, capturado, s.peças2.index(peça), False)]
              listaAções.append((ação[0], ação[1], capturado, s.peças2.index(peça), False))
              break
            listaAções.append((*ação, s.peças2.index(peça), False))
      if peça.coords[0] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1])), listaAções, s, s.peças2.index(peça))
        if peça.coords[1] > 0:
          for i in range(min(8 - peça.coords[0], peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] + i, peça.coords[1] - i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças1[capturado].tipo == 1:
                return [(*ação, capturado, s.peças2.index(peça), False)]
              listaAções.append((ação[0], ação[1], capturado, s.peças2.index(peça), False))
              break
            listaAções.append((*ação, s.peças2.index(peça), False))
        if peça.coords[1] < 8:
          for i in range(min(8 - peça.coords[0], 8 - peça.coords[1])):
            ação= (peça.coords, (peça.coords[0] + i, peça.coords[1] + i))
            if verificaOcupado(s, ação[1]):
              break
            capturado= verificaCaptura(s, ação[1])
            if capturado >= 0:
              if s.peças1[capturado].tipo == 1:
                return [(*ação, capturado, s.peças2.index(peça), False)]
              listaAções.append((ação[0], ação[1], capturado, s.peças2.index(peça), False))
              break
            listaAções.append((*ação, s.peças2.index(peça), False))
      if peça.coords[1] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] - 1)), listaAções, s, s.peças2.index(peça))
      if peça.coords[1] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] + 1)), listaAções, s, s.peças2.index(peça))
         
    elif peça.tipo == 6 or peça.tipo == 8 or peça.tipo == 10 or peça.tipo == 12 or peça.tipo == 14:
      if peça.coords[0] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1])), listaAções, s, s.peças2.index(peça))
        if peça.coords[1] > 0:
          açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1] - 1)), listaAções, s, s.peças2.index(peça))
        if peça.coords[1] < 8:
          açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1] + 1)), listaAções, s, s.peças2.index(peça))
      if peça.coords[1] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] - 1)), listaAções, s, s.peças2.index(peça))
      if peça.coords[1] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0], peça.coords[1] + 1)), listaAções, s, s.peças2.index(peça))
      if peça.coords[0] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1])), listaAções, s, s.peças2.index(peça))
    elif peça.tipo == 7:
      if peça.coords[0] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1])), listaAções, s, s.peças2.index(peça))
        if peça.coords[1] > 0:
          açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1] - 1)), listaAções, s, s.peças2.index(peça))
        if peça.coords[1] < 8:
          açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1] + 1)), listaAções, s, s.peças2.index(peça))
      if peça.coords[0] > 0:
        if peça.coords[1] > 0:
          açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1] - 1)), listaAções, s, s.peças2.index(peça))
        if peça.coords[1] < 8:
          açãoDeMovimento((peça.coords, (peça.coords[0] - 1, peça.coords[1] + 1)), listaAções, s, s.peças2.index(peça))
    elif peça.tipo == 9:
      if peça.coords[1] > 0:
        açãoDeMovimento((peça.coords, (peça.coords[0] + 2, peça.coords[1] - 1)), listaAções, s, s.peças2.index(peça))
      if peça.coords[1] < 8:
        açãoDeMovimento((peça.coords, (peça.coords[0] + 2, peça.coords[1] + 1)), listaAções, s, s.peças2.index(peça))
    elif peça.tipo == 11:
      if peça.coords[0] < 8:
        for i in range(peça.coords[0] + 1, 9):
          ação= (peça.coords, (i, peça.coords[1]))
          if verificaOcupado(s, ação[1]):
            break
          capturado= verificaCaptura(s, (i, peça.coords[1]))
          if capturado >= 0:
            if s.peças1[capturado].tipo == 1:
                return [(*ação, capturado, s.peças2.index(peça), False)]
            ação= (*ação, capturado)
            if (ação[0][0] > 5 or ação[1][0] > 5):
              if ação[1][0] < 8:
                listaAções.append((*ação, s.peças2.index(peça), False))
              listaAções.append((*ação, s.peças2.index(peça), True))
            else:
              listaAções.append((*ação, s.peças2.index(peça), False))
            #listaAções.append((ação[0], ação[1], capturado))
            break
          if (ação[0][0] > 5 or ação[1][0] > 5):
            if ação[1][0] < 8:
                listaAções.append((*ação, s.peças2.index(peça), False))
            listaAções.append((*ação, s.peças2.index(peça), True))
          else:
            listaAções.append((*ação, s.peças2.index(peça), False))
    else:
      açãoDeMovimento((peça.coords, (peça.coords[0] + 1, peça.coords[1])), listaAções, s, s.peças2.index(peça))
  random.shuffle(listaAções)
  return listaAções



# Retorna o conjunto de ações legais no estado s
def ações(s):
  p= jogadorAtual(s)
  listaAções= []
  if p == 1:
    for peça in s.peças1:
      listaAções.extend(movimentosPossíveis(s, peça))
    if len(s.reserva1) > 0:
      listaAções.extend(dropsPossíveis(s, p))
  else:
    for peça in s.peças2:
      listaAções.extend(movimentosPossíveis(s, peça))
    if len(s.reserva2) > 0:
      listaAções.extend(dropsPossíveis(s, p))
  return listaAções

# Retorna o estado resultante da ação a sobre o estado s
def transição(s, a):
  if len(a) < 3 :
    if jogadorAtual(s) == 1:
      peça= s.reserva1[a[0]]
      s.reserva1.remove(peça)
      peça.coords= a[1]
      s.peças1.append(peça)
    else:
      peça= s.reserva2[a[0]]
      s.reserva2.remove(peça)
      peça.coords= a[1]
      s.peças2.append(peça)
  else:
    if len(a) < 5:
      if jogadorAtual(s) == 1:
        peça= s.peças1[a[2]]
        
      else:
        peça= s.peças2[a[2]]
      peça.coords= a[1]
      
      if a[3] and peça.tipo in [2,4,7,9,11,13]:
        peça.tipo= peça.tipo+1
    else:
      if jogadorAtual(s) == 1:
        peça= s.peças1[a[3]]
        #resultante.peças1.remove(a[3])
        peça.coords= a[1]
        if a[4] and peça.tipo in [2,4,7,9,11,13]:
          peça.tipo= peça.tipo+1
        #resultante.peças1.append(peça)
        capt= s.peças2[a[2]]
        #print(a[2].coords)
        #for a2 in resultante.peças2:
          #print(a2.coords)
        if capt.coords != () and capt.jogador != peça.jogador:
          s.peças2.remove(capt)
          if capt.tipo > 1:
            capt.jogador= 1
            capt.coords= ()
            if capt.tipo in [3,5,8,10,12,14]:
              capt.tipo= capt.tipo - 1
            s.reserva1.append(capt)
          else:
            s.tsumi= 1
      else:
        peça= s.peças2[a[3]]
        #resultante.peças2.remove(a[3])
        peça.coords= a[1]
        capt= s.peças1[a[2]]
        if a[4] and peça.tipo in [2,4,7,9,11,13]:
          peça.tipo= peça.tipo+1
        #resultante.peças2.append(peça)
        if capt.coords != () and capt.jogador != peça.jogador:
          s.peças1.remove(capt)
          if capt.tipo > 1:
            capt.jogador= 2
            capt.coords= ()
            if capt.tipo in [3,5,8,10,12,14]:
              capt.tipo= capt.tipo - 1
            s.reserva2.append(capt)
          else:
            s.tsumi= 2
    if peça.tipo == 1:
      if jogadorAtual(s) == 1:
        s.rei1= a[1]
      else:
        s.rei2= a[1]
    s.vazias.append(a[0])
  s.turno= s.turno + 1
  return s

#Retorna todos os estados filhos possíveis
def listaFilhos(s):
  filhos= []
  #mostraTabuleiro(s)
  for ação in ações(s.copy()):
    filho= transição(s.copy(), ação)
    #mostraTabuleiro(filho)
    filhos.append(filho)
  #random.shuffle(filhos)
  return filhos

#Função auxiliar para identificar Sennichite
def verificaLoop(s):
  count= 0
  for estado in historico:
    if len(s.peças1) == len(estado.peças1):
      for peça in s.peças1:
        flag= False
        for aux in estado.peças1:
          if peça.tipo == aux.tipo and peça.coords == aux.coords:
            flag= True
        if not flag:
          continue
      if len(s.peças2) == len(estado.peças2):
        for peça in s.peças2:
          flag= False
          for aux in estado.peças2:
            if peça.tipo == aux.tipo and peça.coords == aux.coords:
              flag= True
          if not flag:
            continue
        if len(s.reserva1) == len(estado.reserva1):
          for peça in s.reserva1:
            flag= False
            for aux in estado.reserva1:
              if peça.tipo == aux.tipo:
                continue
            if not flag:
              return False
          if len(s.reserva2) == len(estado.reserva2):
            for peça in s.reserva2:
              flag= False
              for aux in estado.reserva2:
                if peça.tipo == aux.tipo:
                  flag= True
              if not flag:
                continue
          else:
            continue
        else:
          continue
      else:
        continue
    else:
      continue
    count= count+1
  return count

def sennichite(s):
  if verificaLoop(s) > 3:
    return True
  return False

# Retorna um booleano informando se o jogo terminou ou não
def testeTerminal(s):
  if s.tsumi == 0:# and (not sennichite(s)):
    return False
  return True 

# Retorna o valor do estado s para o jogador p
def avaliação(s):
  if s.tsumi == 2:
    return -1000
  elif s.tsumi == 1:
    return 1000
  else: 
    return 0

def estimativa1(s):
  valor= len(s.peças1) + len(s.reserva1) - (len(s.peças2) + len(s.reserva2))
  return valor

def estimativa2(s):
  valor= len(s.peças1) + len(s.reserva1)/2.0 - (len(s.peças2) + len(s.reserva2)/2.0)
  return valor

def valorDaPeça(peça):
  cod= peça.tipo
  if cod == 1:
    return 0  #Rei
  if cod == 2:
    return 2  #Carruagem voadora
  if cod == 3:
    return 2  #Dragão
  if cod == 4:
    return 2  #Angulador
  if cod == 5:
    return 2  #Cavalo Dragão
  if cod == 6:
    return 1  #General de Ouro
  if cod == 7:
    return 1  #General de Prata
  if cod == 8:
    return 1  #Prata promovido
  if cod == 9:
    return 1  #Cavalo
  if cod == 10:
    return 1   #Cavalo promovido
  if cod == 11:
    return 1   #Carruagem de Incenso
  if cod == 12:
    return 1   #Incenso promovido
  if cod == 13:
    return 1   #Soldado Raso
  else:
    return 1   #Tokin
  
def valorDaPeça2(peça):
  cod= peça.tipo
  if cod == 1:
    return 0  #Rei
  if cod == 2:
    return 8  #Carruagem voadora
  if cod == 3:
    return 10  #Dragão
  if cod == 4:
    return 8  #Angulador
  if cod == 5:
    return 10  #Cavalo Dragão
  if cod == 6:
    return 5  #General de Ouro
  if cod == 7:
    return 5  #General de Prata
  if cod == 8:
    return 5  #Prata promovido
  if cod == 9:
    return 3  #Cavalo
  if cod == 10:
    return 5   #Cavalo promovido
  if cod == 11:
    return 3   #Carruagem de Incenso
  if cod == 12:
    return 5   #Incenso promovido
  if cod == 13:
    return 1   #Soldado Raso
  else:
    return 5   #Tokin  

def estimativa3(s):
  valor= 0
  for peça in s.peças1:
    valor= valor + valorDaPeça(peça)
  for peça in s.reserva1:
    valor= valor + valorDaPeça(peça)
  for peça in s.peças2:
    valor= valor - valorDaPeça(peça)
  for peça in s.reserva2:
    valor= valor - valorDaPeça(peça)
  return valor

def estimativa4(s):
  valor= 0
  for peça in s.peças1:
    valor= valor + valorDaPeça(peça)
  for peça in s.reserva1:
    valor= valor + 0.5*valorDaPeça(peça)
  for peça in s.peças2:
    valor= valor - valorDaPeça(peça)
  for peça in s.reserva2:
    valor= valor - 0.5*valorDaPeça(peça)
  return valor

def estimativa5(s):
  valor= 0
  for peça in s.peças1:
    valor= valor + valorDaPeça2(peça)
  for peça in s.reserva1:
    valor= valor + valorDaPeça2(peça)
  for peça in s.peças2:
    valor= valor - valorDaPeça2(peça)
  for peça in s.reserva2:
    valor= valor - valorDaPeça2(peça)
  return valor

def estimativa6(s):
  valor= 0
  for peça in s.peças1:
    valor= valor + valorDaPeça2(peça)
  for peça in s.reserva1:
    valor= valor + 0.5*valorDaPeça2(peça)
  for peça in s.peças2:
    valor= valor - valorDaPeça2(peça)
  for peça in s.reserva2:
    valor= valor - 0.5*valorDaPeça2(peça)
  return valor

def minimize(s, alfa, beta, nivel, t0):
  if testeTerminal(s):
    return (s, avaliação(s))
  if nivel > 3 or datetime.utcnow() - t0 > timedelta(minutes= 25):
    return (s, estimativa4(s))
  (minFilho, minUtilidade)= (s, 2000)
  possiveis= listaFilhos(s)
  for filho in possiveis:
    #filho= transição(s.copy(), ação)
    #mostraTabuleiro(filho)
    (unused, utilidade)= maximize(filho.copy(), alfa, beta, nivel + 1, t0)
    #print(filhoRetorno)
    if utilidade < minUtilidade:
      (minFilho, minUtilidade)= (filho.copy(), utilidade)
    if minUtilidade <= alfa:
      break
    if minUtilidade < beta:
      beta= minUtilidade
  #estadosNovo= estados.copy()
  if nivel > 0:
    return (0, minUtilidade)
  return (minFilho, minUtilidade)

def maximize(s, alfa, beta, nivel, t0):
  if testeTerminal(s):
    return (s, avaliação(s))
  if nivel > 3 or datetime.utcnow() - t0 > timedelta(minutes= 25):
    return (s, estimativa4(s))
  (maxFilho, maxUtilidade)= (s, -2000)
  possiveis= listaFilhos(s)
  for filho in possiveis:
    #filho= transição(s.copy(), ação)
    #mostraTabuleiro(filho)
    (unused, utilidade)= minimize(filho.copy(), alfa, beta, nivel + 1, t0)
    if utilidade > maxUtilidade:
      (maxFilho, maxUtilidade)= (filho.copy(), utilidade)
    if maxUtilidade >= beta:
      break
    if maxUtilidade > alfa:
      alfa= maxUtilidade
  #estadosNovo= estados.copy()
  #print(nivel)
  #print(maxFilho)
  #print(maxFilho == s)
  if nivel > 0:
    return(0, maxUtilidade)
  return (maxFilho, maxUtilidade)

def movimentoAleatorio(s):
  possiveis= listaFilhos(s)
  random.shuffle(possiveis)
  return possiveis[0]

def movimentoGuloso(s):
  possiveis= listaFilhos(s)
  if len(possiveis) == 1:
      return possiveis[0]
  indice= -1
  i= 0
  menor= math.inf
  for filho in possiveis:
    if estimativa4(filho) < menor:
      menor= estimativa4(filho)
      indice= i
    i= i+1
  return possiveis[indice]  
  

# Retorna o estado seguinte
def decisão(s):
  if jogadorAtual(s) == 1:
    tempo0= datetime.utcnow()
    (filho, unused) = maximize(s.copy(), -math.inf, math.inf, 0, tempo0)
  else:
    filho= movimentoGuloso(s)
    #filho= movimentoAleatorio(s)
    #(filho, unused) = minimize(s.copy(), -math.inf, math.inf, 0)
  return filho

def jogar():
  init()
  mostra(historico[0])
  #x= input()
  t0= datetime.utcnow()
  novo= decisão(historico[0])
  ti= datetime.utcnow()
  mostra(novo)
  while not testeTerminal(novo):
    #x= input()
    print(Fore.WHITE + "Turno atual:", end= " ")
    print(novo.turno)
    tj= datetime.utcnow()
    print("Tempo decorrido neste turno: ", end=" ")
    print(tj - ti)
    print("\n\n")
    historico.append(novo)
    novo= decisão(historico[-1].copy())
    mostra(novo)
    ti= tj
    
    
  ts= datetime.utcnow()
  print("Tempo decorrido: ", end= " ") 
  print(ts - t0)
  print("Ganhador: ")
  print(novo.tsumi)  
  
  mostra(novo)
  deinit()
  # Random: 123, 225, 50, 128
  # Seq: 20, 26, 52, 50
  # Guloso: 64(1-1), 44(2-1), 34(2-2), 18(3-1), 66(3-2), 28(3-3), 80(4-1), 126(4-2), 28(4-3), 50(4-4)
  # 84(5-1), 32(5-2), 
  
  # 24(6-1), 28(6-2), 28(6-3), 28(6-4), 18(6-5), 18(6-6X), 20(6-6), 34(2-2), 62(2-3), 18(3-3), 16(4-4), 
  # 26(5-5), 26(5-1), 48(5-2), 30(5-3), 28(5-4), 22(5-6), 16(4-2), 32(4-3), 82(4-5), 16(4-6), 26(3-2)
  
  #State-space complexity: 10^43 vs 10^71
  #Game-tree complexity: 10^123 vs 10^226
  
jogar()
