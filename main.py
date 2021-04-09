# -*- coding: utf-8 -*-
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('input', 'mouse', 'mouse, disable_multitouch')
Config.set('graphics', 'multisamples', '0')

import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

import locale
locale.setlocale(locale.LC_ALL, 'pt-BR')

from decimal import Decimal

from kivy.core.window import Window
Window.size = (250, 480)

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.lang.builder import Builder
from kivy.uix.bubble import Bubble

taxas = {'estado': '1.05', 'foraestado': '1.07', 'servicos': '1.06'}

def tratar_entrada(entrada):
	entrada = locale.atof(entrada)
	return entrada

def show_popup():
	global popup
	popup = Popup(title="Configurações", content=PopupConfig(), size_hint=(1, 0.45), pos_hint=({'top': 0.83}))
	popup.open()


class MainWindow(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.keyboard = Window.request_keyboard(None, self) # Chama o teclado, os argumentos são callback = None e target = self(instância)
		self.keyboard.bind(on_key_down=self.on_keyboard) # "Binda" o teclado com uma função que é ativada ao pressionar uma tecla

	def on_keyboard(self, key, scancode, codepoint, modifier): # Função ativada quando uma tecla do teclado é pressinada
		if scancode == (9, 'tab'): # Neste caso, quando a tecla TAB é pressionada, o foco retorna para o campo onde inserimos o preço
			self.ids.digitado.focus = True

	def configbtn(self):
		show_popup()


	def calculo(self):

		if self.ids.opcoes.text == "Compras no Estado":
			taxaest = taxas['estado']
			try:
				valordigitado = tratar_entrada(self.ids.digitado.text)
				valordigitado = Decimal(valordigitado)
				valorfinal = valordigitado * Decimal(taxaest)
				self.ids.resultado.text = f'R$ {locale.format_string("%.2f", valorfinal, grouping=True)}'
				self.ids.digitado.text = ""
			except:
				self.ids.resultado.text = 'Digite um valor válido.'
				self.ids.digitado.text = ""

		if self.ids.opcoes.text == "Compras fora do Estado":
			taxafest = taxas['foraestado']
			try:
				valordigitado = tratar_entrada(self.ids.digitado.text)
				valordigitado = Decimal(valordigitado)
				valorfinal = valordigitado * Decimal(taxafest)
				self.ids.resultado.text = f'R$ {locale.format_string("%.2f", valorfinal, grouping=True)}'
				self.ids.digitado.text = ""
			except:
				self.ids.resultado.text = 'Digite um valor válido.'
				self.ids.digitado.text = ""


		if self.ids.opcoes.text == "Serviços":
			taxaserv = taxas['servicos']
			try:
				valordigitado = tratar_entrada(self.ids.digitado.text)
				valordigitado = Decimal(valordigitado)
				valorfinal = valordigitado * Decimal(taxaserv)
				self.ids.resultado.text = f'R$ {locale.format_string("%.2f", valorfinal, grouping=True)}'
				self.ids.digitado.text = ""
			except:
				self.ids.resultado.text = 'Digite um valor válido.'
				self.ids.digitado.text = ""

class PopupConfig(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.ids.campo1.text = taxas['estado']
		self.ids.campo2.text = taxas['foraestado']
		self.ids.campo3.text = taxas['servicos']

	def configurar(self):
		campoestado = self.ids.campo1.text
		campofestado = self.ids.campo2.text
		camposervico = self.ids.campo3.text

		taxaest = taxas['estado']
		taxafest = taxas['foraestado']
		taxaserv = taxas['servicos']

		if campoestado != taxaest:
			taxas['estado'] = campoestado

		if campofestado != taxafest:
			taxas['foraestado'] = campofestado

		if camposervico != taxaserv:
			taxas['servicos'] = camposervico

	def salvbtn(self): # Define o que faz o botão 'Salvar'
		self.configurar()
		popup.dismiss()


class MarkupApp(App):
	def build(self):
		Builder.load_string(open("stylesheet.kv", encoding="utf-8").read(), rulesonly=True) #Importa o arquivo .kv através do Builder
		return MainWindow()


if __name__ == '__main__':
	MarkupApp().run()