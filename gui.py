import random
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Toplevel, Label

OUTPUT_PATH = Path(__file__).resolve().parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

# Mapa de transição de estados
def f(estado_atual, entrada):
    transicao = {
        's0': {0.25: 's1', 0.50: 's2', 1.00: 's4'},
        's1': {0.25: 's2', 0.50: 's3', 1.00: 's5'},
        's2': {0.25: 's3', 0.50: 's4', 1.00: 's6'},
        's3': {0.25: 's4', 0.50: 's5', 1.00: 's7'},
        's4': {0.25: 's5', 0.50: 's6', 1.00: 's8'},
        's5': {0.25: 's6', 0.50: 's7', 1.00: 's8'},
        's6': {0.25: 's7', 0.50: 's8', 1.00: 's8'},
        's7': {0.25: 's8', 0.50: 's8', 1.00: 's8'},
        's8': {0.25: 's8', 0.50: 's8', 1.00: 's8'}
    }
    
    return transicao[estado_atual].get(entrada, estado_atual)  # Retorna o próximo estado ou o mesmo

# Função de saída
def g(estado_atual, entrada):
    troco = {
        's5': {0.50: 0.0, 1.00: 0.25},
        's6': {0.50: 0.25, 1.00: 0.50},
        's7': {0.25: 0.25, 0.50: 0.50, 1.00: 0.75},
        's8': {0.25: 0.25, 0.50: 0.50, 1.00: 1.00}
    }
    
    return troco.get(estado_atual, {}).get(entrada, 0)  # Retorna o troco ou 0 se não houver

# Inicializando o estado atual
estado_atual = 's0'

# Função para inserir o valor, apenas se for válido (R$0.25, R$0.50 ou R$1.00)
def inserir():
    global valor_inicial, estado_atual
    try:
        new_inserir = float(entry_1.get())

        # Verifica se o valor inserido é válido (0.25, 0.50 ou 1.00)
        if new_inserir not in [0.25, 0.50, 1.00]:
            exibir_popup_erro(new_inserir)  # Exibe o popup de erro com o valor inválido
            return

        # Atualiza o estado e calcula o troco
        proximo_estado = f(estado_atual, new_inserir)

        # Se o valor total + inserido ultrapassar 2.00, calcula o troco
        if valor_inicial + new_inserir > 2.0:
            troco_excedente = (valor_inicial + new_inserir) - 2.0
            exibir_popup(troco_excedente)
            valor_inicial = 2.0
            estado_atual = proximo_estado

        else:
            estado_atual = proximo_estado  # Atualiza o estado atual
            valor_inicial += new_inserir  # Atualiza o valor inserido

        # Atualiza o valor exibido
        canvas.itemconfig(valor_inicial_texto, text=f"R${valor_inicial:.2f}")

    except ValueError:
        exibir_popup_erro(0)  # Exibe o popup caso o valor não seja um número

# Definir o ícone e o nome da janela
icone_path = relative_to_assets("icone.png")
window.iconphoto(False, PhotoImage(file=icone_path))
window.title("Máquina de Vendas")

largura_janela = 545
altura_janela = 768
window.geometry("545x768")
# Função para centralizar a janela
def centralizar_janela():
    tela_largura = window.winfo_screenwidth()
    tela_altura = window.winfo_screenheight()
    x = (tela_largura // 2) - (largura_janela // 2)
    y = (tela_altura // 2) - (altura_janela // 2)
    window.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

centralizar_janela()
window.configure(bg = "#FFFFFF")

# Função para centralizar os pop-up
def centralizar_popup(popup, largura, altura):
    tela_largura = popup.winfo_screenwidth()
    tela_altura = popup.winfo_screenheight()
    x = (tela_largura // 2) - (largura // 2)
    y = (tela_altura // 2) - (altura // 2)
    popup.geometry(f"{largura}x{altura}+{x}+{y}")

# Função para exibir as regras da máquina em um popup
def exibir_regras():
    popup = Toplevel(window)
    popup.geometry("") # Deixa que o proprio tkinter escolha o tamanho
    popup.minsize(600, 250) # Tamanho mínimo
    popup.title("Regras da Máquina")
    popup.grab_set() # Não deixa o usuário interagir com a tela principal quando o pop-up estiver aberto
    popup.resizable(False, False) # Não deixa o usuário mexer no tamanho da tela

    regras_texto = (
        "1- São apenas aceitas moedas de R$0.25, R$0.50 e R$1.00\n"
        "2- Caso sejam inseridas moedas de outro valor, a máquina devolverá.\n"
        "3- Todos os itens custam R$2.00.\n"
        "4- Se ultrapassar o valor de R$2.00, a máquina devolverá o troco automaticamente.\n"
        "5- Caso tente resgatar o produto com um valor abaixo de R$2.00, o usuário deverá inserir mais moedas."
    )

    Label(popup, text=regras_texto, font=("Arial", 16), justify="left").pack(pady=20)
    Button(popup, text="OK", command=popup.destroy).pack(pady=10)
    popup.update_idletasks()  # Atualiza o layout para obter o tamanho correto, pra q fique proporcional ao tamanho da fonte
    largura_popup = popup.winfo_width() 
    altura_popup = popup.winfo_height()
    centralizar_popup(popup, largura_popup, altura_popup)  # Centraliza o pop-up

valor_inicial = 0

# Exibe o pop-up de erro
def exibir_popup_erro(valor_inserido):
    popup = Toplevel(window)
    popup.title("Valor Inválido")
    popup.grab_set() # Não deixa o usuário interagir com a tela principal quando o pop-up estiver aberto
    popup.resizable(False, False) # Não deixa o usuário mexer no tamanho da tela

    mensagem = (
        f"Você inseriu um valor diferente, por favor, insira apenas moedas de R$0.25, R$0.50 e R$1.00.\n"
        f"Aqui está seu dinheiro: R${valor_inserido:.2f}"
    )

    largura_popup = 400
    altura_popup = 150

    popup.geometry(f"{largura_popup}x{altura_popup}")
    popup.resizable(False, False)

    Label(popup, text=mensagem, font=("Arial", 10), justify="left", wraplength=350).pack(pady=20)
    Button(popup, text="OK", command=popup.destroy).pack(pady=10)
    centralizar_popup(popup, largura_popup, altura_popup)  # Centraliza o pop-up

# Função para validar a entrada de dados (apenas números e um ponto)
def validar_entrada(texto):
    if texto == "" or texto.isdigit() or (texto.count(".") == 1 and texto.replace(".", "").isdigit()):
        return True
    return False

# Adiciona a validação de entrada
valida_comando = (window.register(validar_entrada), '%P')

# Pop-up do troco
def exibir_popup(valor_devolvido):
    popup = Toplevel(window)
    popup.geometry("300x100")
    popup.title("Valor Devolvido")
    popup.grab_set() # Não deixa o usuário interagir com a tela principal quando o pop-up estiver aberto
    popup.resizable(False, False) # Não deixa o usuário mexer no tamanho da tela

    Label(popup, text=f"Você inseriu valor a mais. Valor devolvido: R${valor_devolvido:.2f}", font=("Arial", 10)).pack(pady=20)
    Button(popup, text="OK", command=popup.destroy).pack(pady=10)

    centralizar_popup(popup, 300, 100)  # Centraliza o pop-up!!

# Função para exibir o popup com mensagem e imagem da bebida
def exibir_popup_bebida(imagem=None):
    popup = Toplevel(window)
    popup.geometry("300x200")
    popup.title("Sua Bebida")
    popup.grab_set() # Não deixa o usuário interagir com a tela principal quando o pop-up estiver aberto
    popup.resizable(False, False) # Não deixa o usuário mexer no tamanho da tela

    centralizar_popup(popup, 300, 200)  # Centraliza o pop-up

    if imagem:
        img = PhotoImage(file=relative_to_assets(imagem))
        Label(popup, text="Aqui está sua bebida!", font=("Arial", 12)).pack(pady=20)
        Label(popup, image=img).pack(pady=10)
        # Mantém a referência da imagem para evitar que o garbage collector a remova
        popup.image = img
    else:
        Label(popup, text="Valor insuficiente, insira mais moedas.", font=("Arial", 12)).pack(pady=20)

    Button(popup, text="OK", command=popup.destroy).pack(pady=10)

# Função chamada ao pressionar o botão verde
def liberar_produto():
    global valor_inicial

    if valor_inicial == 2.0:
        # Escolhe uma imagem de bebida aleatória entre as 5
        imagem_escolhida = random.choice([
            "Group_1.png", "Group_2.png", "Group_3.png", 
            "Group_4.png", "Group_5.png"
        ])
        exibir_popup_bebida(imagem_escolhida)
        valor_inicial = 0  # Resetar o valor
    else:
        exibir_popup_bebida()

    # Atualiza o valor na interface, mantendo o valor inicial ou voltando para 0
    canvas.itemconfig(valor_inicial_texto, text=f"R${valor_inicial:.2f}")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 768,
    width = 545,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    272.0,
    384.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    481.6785583496094,
    230.30355834960938,
    image=image_image_2
)

valor_inicial_texto = canvas.create_text(
    431.0,
    220.0,
    anchor="nw",
    text="R$0,00",
    fill="#000000",
    font=("Lalezar Regular", 23 * -1)
)

canvas.create_text(
    426.0,
    163.0,
    anchor="nw",
    text="Valor Inserido",
    fill="#FFFFFF",
    font=("Lalezar Regular", 19 * -1)
)

canvas.create_text(
    433.0,
    292.0,
    anchor="nw",
    text="Inserir Valor",
    fill="#FFFFFF",
    font=("Lalezar Regular", 19 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    468.0,
    339.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    validate="key",  # Ativa a validação na digitação
    validatecommand=valida_comando  # Chama a função de validação
)
entry_1.place(
    x=432.0,
    y=325.0,
    width=72.0,
    height=27.0
)

canvas.create_text(
    430.0,
    366.0,
    anchor="nw",
    text="Liberar Produto",
    fill="#FFFFFF",
    font=("Lalezar Regular", 15 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=liberar_produto,  # Chama a função para verificar o valor
    relief="flat"
)
button_1.place(
    x=457.25,
    y=394.78570556640625,
    width=49.017852783203125,
    height=49.07145309448242
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=inserir,
    relief="flat"
)
button_2.place(
    x=504.0,
    y=325.0,
    width=29.0,
    height=29.0
)
# Atualiza o comando do button_image_3 para chamar a função exibir_regras
button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=exibir_regras,  # Exibe as regras quando o botão é pressionado
    relief="flat"
)
button_3.place(
    x=458.0,
    y=27.0,
    width=49.0,
    height=49.0
)
window.resizable(False, False)
window.mainloop()
