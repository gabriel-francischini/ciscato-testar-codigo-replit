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
    pass


def modo3():
    global arqent
    global arqsai
    global chave
    pass


def modoU():
    global arqent
    global arqsai
    global chave

    arqent_str = arqent.read()

    # C: while ((ch = fgetc(arqent)) != EOF){ ...
    for pos in range(len(arqent_str)):
        ch = arqent_str[pos]

        if ch != '\r':
            arqsai.write(ch)
        else:
            prox_ch = arqent_str[pos + 1]

            if prox_ch == '\n':
                arqsai.write('\n')
            # C: ungetc(prox_ch, arqent); err = fputc('\r', arqsai);
            else:
                arqsai.write('\r')


def strcasecmp(s1, s2):
    return s1.lower() == s2.lower()


def abrir_arqsai(caminho_arqent, ext1, ext2):
    """ ext1 -- ex: ".INV"
        ext2 -- ex: ".DNV"
    """
    global arqent
    global arqsai
    global chave
    posUltimoPonto = caminho_arqent.rfind('.')
    ext_a_usar = ""

    if posUltimoPonto != -1:
        ultimoPonto = caminho_arqent[posUltimoPonto:]
        print("Extensao do arquivo de entrada (indice {}): {}"
              .format(posUltimoPonto, ultimoPonto))

        ext_arqent = ultimoPonto

        # Se o arquivo tiver a extensão ext1, quer dizer que o arquivo...
        # ... deve ser convertido para ext2.
        if ext_arqent.lower() == ext1.lower():
            print("Arquivo de entrada usa o padrao FORMARQ: {}".format(ext1))
            ext_a_usar = ext2
        else:
            ext_a_usar = ext1
    else:
        posUltimoPonto = len(caminho_arqent)
        print("Arquivo nao tem extensao (indice {})".format(posUltimoPonto))
        ext_a_usar = ext1

    print("Extensao do arquivo de saida: {}".format(ext_a_usar))

    caminho_arqsai = caminho_arqent[:posUltimoPonto] + ext_a_usar
    tamanho_nova_string = len(caminho_arqsai)
    ext_arqsai = caminho_arqsai[posUltimoPonto:]

    print("Escrevendo arquivo: {}".format(caminho_arqsai))

    arqsai = open(caminho_arqsai, "w")

    del caminho_arqsai
    del ext_arqsai



ARG_NOME_PROGRAMA = 0
ARG_CAMINHO_ARQENT = 1
ARG_MODO = 2
ARG_CHAVE = 3

def main(argc, argv):
    global arqent
    global arqsai
    global chave
    print("Iniciando programa FORMARQ...")

    if argc <= ARG_MODO:
        print("Faltou escolher o arquivo ou comando.")
        exit(-1)

    modo = argv[ARG_MODO]

    if modo == 'C':
        if argc <= ARG_CHAVE:
            print("Faltou escolher a chave.")
            exit(-1)
        else:
            chave = argv[ARG_CHAVE]

    caminho_arqent = argv[ARG_CAMINHO_ARQENT]
    arqent = open(caminho_arqent, "r")

    print("Modo de operação: {}".format(modo.upper()))

    if modo == 'I':
        abrir_arqsai(caminho_arqent, ".INV", ".DNV")
    elif modo == 'C':
        abrir_arqsai(caminho_arqent, ".CRP", ".DRP")
    elif modo == 'D':
        abrir_arqsai(caminho_arqent, ".DOS", ".DOS")
    elif modo == 'U':
        abrir_arqsai(caminho_arqent, ".UNX", ".UNX")
    else:
        print("Modo nao reconhecido.")
        exit(-1)

    # Em C, aqui tem um pouco de error handling. Python não precisa disso.

    if modo == 'I':
        modo1(arqent, caminho_arqent)
    elif modo == 'C':
        modo2()
    elif modo == 'D':
        modo3()
    elif modo == 'U':
        modoU()



main(len(sys.argv), sys.argv)
