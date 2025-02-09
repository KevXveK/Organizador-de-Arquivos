import os #módulo das interfaces de sistema operacional
import shutil # módulo que permita interagir com arquivos e diretorios
import logging #módulo de rastreador de evento
import tkinter as tk #modulo da interdface padrão
from tkinter import filedialog, messagebox

# Configuração do sistema de logs
logging.basicConfig( # define o comportamento basico do registro dos logs
    filename="organizador_arquivos.log", #nome do arquivo de log
    level=logging.INFO, #nivel de log
    format="%(asctime)s - %(levelname)s - %(message)s", #froamto da mensagem
    datefmt="%Y-%m-%d %H:%M:%S" #formato da data/hora
)

def organizar_pasta(caminho_pasta):
    # Verifica se a pasta especificada existe
    if not os.path.exists(caminho_pasta):
        # se a pasta não existir, registra um erro no log
        logging.error(f"A pasta {caminho_pasta} não existe.") #Exibe uma mensagem de rro na interface gráfica
        messagebox.showerror("Erro", f"A pasta {caminho_pasta} não existe.") # Encerra a função, pois não ha pasta para organizar
        return

    arquivos = os.listdir(caminho_pasta)
    #lista todos os arquivos e pastas dentro do caminho especificado

    for arquivo in arquivos: #iteração
        # Verifica se a pasta 'caminho_pasta' existe
        if os.path.isdir(os.path.join(caminho_pasta, arquivo)):
            continue
        # Se for uma pasta, ignora e continua para o proximo item
           
        extensao = os.path.splitext(arquivo)[1].lower()
        #cria uma extensão do arquivo( ex: png, .pdf) e converte para minusculas

        if extensao: # verifica se o arquivo tem uma extensão
            subpasta = os.path.join(caminho_pasta, extensao[1:].capitalize() + "Files")
        else: # se o arquivo não existe ele cria uma subpasta com o nome "outros"
            subpasta = os.path.join(caminho_pasta, "Outros")

        if not os.path.exists(subpasta): #verifica se a subpasta ja existe
            os.makedirs(subpasta) # se não existir cria a subpasta
            logging.info(f"Criada a subpasta: {subpasta}") #Registra no log que a subpasta foi criada

        caminho_arquivo_original = os.path.join(caminho_pasta, arquivo) #define o comportamento completo do arquivo original
        caminho_arquivo_novo = os.path.join(subpasta, arquivo) #define o caminho completo do arquivo na nova subpasta
        shutil.move(caminho_arquivo_original, caminho_arquivo_novo) #move o arquivo para a subpasta correspondente
        logging.info(f"Movido: {arquivo} -> {subpasta}") #Registra no log que o arquivo foi  movido

    messagebox.showinfo("Concluído", "Arquivos organizados com sucesso!") #exibe uma mensagem apos o registro

def selecionar_pasta(): #abre uma janela para o usuario selecionar uma pasta
    caminho_pasta = filedialog.askdirectory() #Verifica se o usuario selecionou uma pasta
    if caminho_pasta: # chama a função organizar_pasta com o caminho da pasta selecionada
        organizar_pasta(caminho_pasta)

def sair():
    if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
        root.destroy()  # Fecha a janela principal

# Interface gráfica
root = tk.Tk()
root.title("Organizador de Arquivos")

# Botão para selecionar a pasta
btn_selecionar = tk.Button(root, text="Selecionar Pasta", command=selecionar_pasta)
btn_selecionar.pack(pady=10)

# Botão para sair
btn_sair = tk.Button(root, text="Sair", command=sair)
btn_sair.pack(pady=10)

# Inicia a interface gráfica
root.mainloop()