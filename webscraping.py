
# coding: utf-8

# # Web Scraping 

# Resumo: Trata-se de um WEB SCRAPING: no qual o usuário insere um endereço WEB e o sistema gera um arquivo texto com todos os links da primeira página daquele site. Feito com a linguagem Python.
# Objetivo: Gerar links de um website
# Entrada: URL de algum website
# Saída: Lista de links da primeira página (num arquivo txt)
# 
# Produzido por: Roger C. Sampaio 05/06/2020. Mentor da dataminutes (www.dataminutes.com) 
# Contato: rogercsampaio@dataminutes.com
# Site: https://www.dataminutes.com/portfolio

# In[6]:


# Bibliotecas
# BeautifulSoup (para o web-scraping extraindo o texto da página HTML) 
# tkinter (para interface gráfica)
# validator_collection (para validar url)
# request para requisição
# os para manipular funções do sistema operacional
import requests
from bs4 import BeautifulSoup
from tkinter import *
import tkinter as tk
from validator_collection import validators, checkers
import os


# In[9]:


# Interface gráfica
class Application:
    def __init__(self, master=None):
        # Criação dos containers
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        self.primeiroContainer.pack()
  
        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()
        
        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()
        
        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer.pack()
        
        self.quintoContainer = Frame(master)
        self.quintoContainer["pady"] = 20
        self.quintoContainer.pack()
        
        self.sextoContainer = Frame(master)
        self.sextoContainer["pady"] = 20
        self.sextoContainer.pack()
        
        self.titulo = Label(self.primeiroContainer, text="Extrator")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()
        
        self.nomeLabel = Label(self.segundoContainer,text="Site", font=self.fontePadrao)
        self.nomeLabel.pack(side=LEFT)
        
    
        # Criação dos widgets (elementos na TELA)
        self.site = Entry(self.segundoContainer)
        self.site["width"] = 30
        self.site["font"] = self.fontePadrao
        self.site.pack(side=LEFT)
        
        self.extrair = Button(self.terceiroContainer)
        self.extrair ["text"] = "Extrair Links"
        self.extrair ["font"] = ("Calibri", "8")
        self.extrair ["width"] = 12
        self.extrair ["command"] = self.iniciarExtracao
        self.extrair.pack()
        
        self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()
        
        self.botaoGerarArquivo = Button(self.quintoContainer)
        self.botaoGerarArquivo ["text"] = "Abrir arquivo"
        self.botaoGerarArquivo ["font"] = ("Calibri", "8")
        self.botaoGerarArquivo ["width"] = 12
        self.botaoGerarArquivo ["command"] = self.abrirArquivo
        
        self.informacoes = Button(self.sextoContainer)
        self.informacoes ["text"] = "Informações"
        self.informacoes ["font"] = ("Calibri", "8")
        self.informacoes ["width"] = 12
        self.informacoes ["command"] = self.obterInfoPrograma
        self.informacoes.pack()
        
    # evento para o botão: Informações (para saber o propósito do programa)   
    def obterInfoPrograma(self):
        popup = tk.Tk()
        popup.wm_title("Sobre")
        label = tk.Label(popup, text="Programa criado por Roger C. Sampaio \nTrata-se de um WEB SCRAPING: no qual o usuário insere um endereço WEB válido\ne o sistema gera um arquivo texto com todos os links da primeira página daquele site.\nFeito com a linguagem Python.")
        label.pack(side="top", fill="x", pady=10)
        B1 = tk.Button(popup, text="OK", command = popup.destroy)
        B1.pack()      
        
    # evento para o clique do botão: Extrair Links
    def iniciarExtracao(self):
        # Validação da url
        siteWeb = self.site.get()
        if (siteWeb == ''):
            self.mensagem["text"] = "Digite um site para iniciar a extração!\n Ex:https://www.google.com"
        elif checkers.is_url(siteWeb) == False:
            self.mensagem["text"] = "Erro.Site válido!"
        else:
            self.mensagem["text"] = "Extração de Links Iniciada!"
           # Conectar no site e criar a lista de links
            try:
                req = requests.get(siteWeb,stream=True)
                if (req.status_code == 200):
                    content = req.content
                    soup = BeautifulSoup(content, 'html.parser')
                    # TAG <a href> 
                    # ex: <a class="pw-link dbh-link" target="_blank" href="/wcsstore/DebenhamsUKSite/faq/delivery_and_collection_information/home_delivery.html">
                    # tagsA = list(soup.find_all('a'))
                    
                    # Gera a lista de links
                    listaLinks = []
                    for link in soup.find_all('a'):
                        stringLinkHref = link.get('href')
                        # Link do tipo: <https: ... https...>
                        if (not (stringLinkHref.startswith('http'))):
                            item = siteWeb + stringLinkHref
                        else:
                            item = stringLinkHref
                        listaLinks.append(item)
                        
                    # Gera o arquivo TXT com os links
                    with open('resultado.txt', 'w') as arquivo:
                        for item in listaLinks:
                            arquivo.write(item + "\n") 
                    self.mensagem["text"] = 'Arquivo gerado com sucesso!'
                    self.botaoGerarArquivo.pack()
                    
            # Trata exceções: 1 - se não houver conexão com a net, 2 - site não encontrado (404) ... entre outros
            except Exception: 
                self.mensagem["text"] = "Erro ao conectar na página!"
                
    def abrirArquivo(self):
        if (os.path.exists('resultado.txt') == False):
           self.mensagem["text"] = 'Erro ao abrir o arquivo! O arquivo não existe!'
        else:
            os.system("start notepad.exe resultado.txt")


# Como se fosse um método MAIN para manipular a interface gráfica
root = Tk()
root.title("WEB SCRAPING")
Application(root)
root.mainloop()

