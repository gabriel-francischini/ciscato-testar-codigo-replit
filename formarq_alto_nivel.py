import sys


arqent = None
arqsai = None
chave = ""


def modo1(arqent, caminho_arqent):
    pass


def modo2():
    global arqent
    global arqsai
    global chave


def modo3():
    global arqent
    global arqsai


def modoU():
    global arqent
    global arqsai

    arqent_str = arqent.read()

    for pos, ch in enumerate(arqent_str):
        # Se ainda não chegamos no fim do arquivo e existe um próximo caracter
        if pos + 1 < len(arqent_str):
            prox_ch = arqent_str[pos + 1]

        # Bug: '\r\n' é substituído por '\n\n'.
        # Mas o código fica mais claro com esse bug.
        if ch == '\r' and prox_ch == '\n':
            arqsai.write('\n')
        else:
            arqsai.write(ch)


def abrir_arqsai(caminho_arqent, ext1, ext2):
    """ ext1 -- ex: ".INV"
        ext2 -- ex: ".DNV"
    """
    global arqent
    global arqsai

    # Bug: o que acontece se o caminho de entrada não tiver nenhum ponto
    #      (i.e. não tiver nenhuma extensão)?
    # Mas o código fica mais claro com esse bug.
    nomearq__naoTemNoC, ext_arqent = caminho_arqent.rsplit('.', 1)

    # Se o arquivo tiver a extensão ext1, quer dizer que o arquivo...
    # ... deve ser convertido para ext2.
    if ext_arqent.lower() == ext1.lower():
        print("Arquivo de entrada usa o padrao FORMARQ: {}".format(ext1))
        ext_a_usar = ext2
    else:
        ext_a_usar = ext1

    caminho_arqsai = nomearq__naoTemNoC + ext_a_usar
    arqsai = open(caminho_arqsai, "w")

    print("Extensao do arquivo de entrada (indice {}): {}"
              .format(caminho_arqent.rfind('.'), ext_arqent))
    print("Extensao do arquivo de saida: {}".format(ext_a_usar))
    print("Escrevendo arquivo: {}".format(caminho_arqsai))


def main(argc, argv):
    global arqent
    global arqsai
    global chave
    print("Iniciando programa FORMARQ...")

    if argc == 3:
        nome, caminho_arqent, modo = tuple(argv)
    if argc == 4:
        nome, caminho_arqent, modo, chave = tuple(argv)

    arqent = open(caminho_arqent, "r")

    print("Modo de operação: {}".format(modo.upper()))

    if modo == 'I':
        abrir_arqsai(caminho_arqent, ".INV", ".DNV")
        modo1(arqent, caminho_arqent)

    elif modo == 'C':
        abrir_arqsai(caminho_arqent, ".CRP", ".DRP")
        modo2()

    elif modo == 'D':
        abrir_arqsai(caminho_arqent, ".DOS", ".DOS")
        modo3()

    elif modo == 'U':
        abrir_arqsai(caminho_arqent, ".UNX", ".UNX")
        modoU()

    else:
        print("Modo nao reconhecido.")
        exit(-1)


main(len(sys.argv), sys.argv)
