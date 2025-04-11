#================== Autores ==================
#                 Caio Brito
#                 Murilo Vital
#============================================= 

import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

class Pagina:
    def __init__(self, numero):
        self.numero = numero
        self.bit_referencia = 0

def makePizza(frame, pages_in_memory):
        
    for i in range(len(pages_in_memory)):
        
        sizes = [1] * frames  # Tamanhos iguais para cada categoria
        # Cor única para todas as fatias
        colors = ['skyblue']
        # Criação do gráfico de pizza
        plt.pie(sizes, labels=[f"{pages_in_memory[i][j]}" for j in reversed(range(frames))], colors=colors, startangle=90, pctdistance=0.85,wedgeprops=dict(width=0.75, edgecolor='black', linewidth=2))
        centre_circle = plt.Circle((0, 0), 0.25, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        # Adiciona um título
        plt.title('Frames de memória')
        # Exibe o gráfico
        plt.show()
    

def ler_paginas_do_arquivo(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r') as arquivo:
            paginas = list(map(int, arquivo.read().split()))
        return paginas
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo: {str(e)}")

def algoritmo_segunda_chance(frames, rest_time, paginas):
    if frames < 3 or frames > 9:#define erro caso o usuario de entrada invalida
        raise ValueError("O número de frames deve estar entre 3 e 9")

    quadros = [None] * frames #cria o numero de quadros na memoria dinamicamente
    ponteiro = 0 #aponta para o quadro atual
    tempo_sem_reset = 0 #serve para fazer a verificação, como um contador de tempo
    total_page_faults = 0
    pages_in_memory = [] #Cria um vetor de vetores para salvar todas as paginas apos inserções

    for pagina_numero in paginas: #Pagina é o numero de requisições(paginas) no arquivo
        pagina_encontrada = False

        for quadro in quadros: #Verifica quadro por quadro da memória, chamado de frame no plot
            if quadro and quadro.numero == pagina_numero: #Se achou na memoria
                quadro.bit_referencia = 1 #1 porque acabou de ser usada
                pagina_encontrada = True #Sinaliza que encontrou a página
                break

        if not pagina_encontrada: #Se não encontrou página
            total_page_faults += 1 #Adiciona um pagefault
            while True:
                pagina_atual = quadros[ponteiro] #aponta para uma instancia atual do quadro

                if not pagina_atual or pagina_atual.bit_referencia == 0: #Verifica se a pagina atual pode ser substituida, caso não tenha mais chances
                    quadros[ponteiro] = Pagina(pagina_numero)
                    ponteiro = (ponteiro + 1) % frames
                    break
                else: #Se a pagina teve segunda chance, o bit dela recebe zero e o ponteiro vai pro proximo
                    pagina_atual.bit_referencia = 0

                ponteiro = (ponteiro + 1) % frames #Faz o giro ser circular no ponteiro

        tempo_sem_reset += 1 # Conta uma unidade de tempo

        if tempo_sem_reset == rest_time: #Se o tempo chegar no limite dado pelo usuario, reseta geral
            for quadro in quadros:
                if quadro:
                    quadro.bit_referencia = 0
            tempo_sem_reset = 0

        pages_in_memory.append([quadro.numero if quadro else None for quadro in quadros]) #Guarda a página atual no fim do vetor de vetores que salva os estados da memória

    return total_page_faults, pages_in_memory

def iniciar_simulacao():
    global frames, rest_time, paginas

    try:
        frames = int(frames_entry.get())
        rest_time = int(rest_time_entry.get())

        file_path = filedialog.askopenfilename()
        paginas = ler_paginas_do_arquivo(file_path)

        resultado_text.delete(1.0, tk.END)#Deleta a saída antiga que estava na caixa de dialogo

        total_page_faults, pages_in_memory = algoritmo_segunda_chance(frames, rest_time, paginas)

        for i, pages in enumerate(pages_in_memory):
            resultado_text.insert(tk.END, f"Páginas em memória: {pages}\n")
        resultado_text.insert(tk.END, f"\nPage Faults: {total_page_faults}\n")
        resultado_text.see(tk.END)
        
        print(f"{pages_in_memory[1][1]}")
        makePizza(frames, pages_in_memory)
        
    except ValueError as e:
        messagebox.showerror("Erro", str(e))

root = tk.Tk()
root.title("Simulação de Algoritmo de Segunda Chance")

tk.Label(root, text="Número de Frames (entre 3 e 9):").pack()
frames_entry = tk.Entry(root)
frames_entry.pack()

tk.Label(root, text="Tempo de Reset:").pack()
rest_time_entry = tk.Entry(root)
rest_time_entry.pack()

selecionar_arquivo_button = tk.Button(root, text="Selecionar Arquivo", command=iniciar_simulacao)
selecionar_arquivo_button.pack()

resultado_text = tk.Text(root, height=20, width=50)
resultado_text.pack()

root.mainloop() 