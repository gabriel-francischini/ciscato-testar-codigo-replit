import subprocess
import sys
import shutil
import os
import pathlib
import subprocess



# Python was suddenly consuming 80% of 12GB of RAM in less than 12 seconds
# (total runtime since script startup). That's unaceptable.
# So we restrict it to 2GB tops.
import resource
soft, hard = resource.getrlimit(resource.RLIMIT_AS)
resource.setrlimit(resource.RLIMIT_AS, (1 * int(1e9), 2 * int(1e9)))



print("Iniciando script de testes...")

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import colorama
    from termcolor import colored
    import Levenshtein
except ImportError as e:
    print("Instalando bibliotecas necessárias via PIP...")
    install('colorama')
    install('termcolor')
    install('python-Levenshtein')
    import colorama
    from termcolor import colored
    import Levenshtein
    print("\n\n\n\n\n\n\n")

colorama.init()



script_path = os.path.dirname(sys.argv[0])
if len(script_path) == 0:
    script_path = '.'
if not pathlib.Path(script_path + '/main.exe').is_file():
    print('Copie o executável do FORMARQ para a pasta de testes e'
          ' renomeie o arquivo para "main.exe". \nA extensão ".exe" é'
          ' obrigatória mesmo em sistemas linux, e é case-INsensitive no'
          ' Windows e case-SENsitive no linux.')
    exit(-1)




def emit_warning(string):
    print(colored(string, 'yellow'))


testar_so_um_modo = sys.argv[1] if len(sys.argv) == 2 else None
def iter_arquivos_teste():
    pares_teste = []

    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(script_path + "/testes"):
        if testar_so_um_modo and ('/' + testar_so_um_modo) not in root:
            continue

        # Se tiver arquivos com ".in.txt" E arquivos com ".out.txt"
        # provavelmente é uma pasta que contém arquivos de entrada
        if (any(map(lambda x: ".in.txt" in x.lower(), files))
            and any(map(lambda x: ".out.txt" in x.lower(), files))):
            arquivos_teste = [os.path.join(root, fp) for fp in files]

            for fp in arquivos_teste:
                # Arquivos de teste sempre terminam com
                # a extensão ".in.txt" ou ".out.txt"
                if (fp.lower().endswith(".in.txt")
                    or fp.lower().endswith(".out.txt")):

                    other_ext = (".in.txt"
                                 if fp.lower().endswith(".out.txt")
                                 else ".out.txt")

                    # Arquivo válido
                    basename = fp[ : fp.rfind('.', 0, -len('.txt'))]
                    matching_fp = basename + other_ext
                    matching_fps = [x for x in arquivos_teste
                                    if x.lower() == matching_fp.lower()]

                    if len(matching_fps) == 1:
                        in_out_pair = tuple(sorted([fp, basename + other_ext]))
                        pares_teste.append(in_out_pair)

                    elif len(matching_fps) == 0:
                        emit_warning('[WARNING] "{}" exists, but'
                                     .format(fp)
                                     + ' "{}" don\'t.'
                                     .format(matching_fp))

                    elif len(matching_fps) > 1:
                        emit_warning('[WARNING] O arquivo de teste "{}" tem'
                                     .format(fp)
                                     + ' vários arquivos correspondentes: '
                                     + ', '.join(['"{}"'.format(x)
                                                  for x in matching_fps]))
                else:
                    # Não tem uma extensão reconhecida pelo nosso
                    # framework de testes
                    emit_warning('[WARNING] O arquivo "{}" não tem'.format(fp)
                                 + ' um formato de um arquivo de teste.')
        else:
            if len(files) != 0:
                emit_warning('[WARNING] A pasta "{}" não contem arquivos de'
                              ' teste, mas contem os arquivos:'.format(root))
                for fp in files:
                    emit_warning(" " * (len('[WARNING]' + 4))
                                 + "* "
                                 + str(os.path.join(root, fp)))
            # Se a pasta não tiver nenhum arquivo mas tiver diretórios,
            # pode significar que essa pasta contem pastas com testes dentro
            # dela mesma.
            elif len(dirs) > 0:
                emit_warning('[WARNING] A pasta "{}" não contem arquivos de teste.'
                              .format(root))


    pares_teste = list(set(pares_teste))
    pares_teste.sort()

    return pares_teste


last_inputpath = ""
last_main_exe_invocation = ""
last_main_exe_stdout = ""
def run_input_file(inputpath, gabaritopath, args=[]):
    """Roda o main.exe recebendo o arquivo inputpath como entrada, usando args.

    Args: uma lista de argumentos para ser passada para subprocess.run().
    Retorna: uma tupla (entrada_bytes, esperado_bytes, real_bytes) contendo
      o conteúdo do arquivo de entrada, do arquivo de gabarito, e do arquivo de
      saída.
    """
    global last_main_exe_invocation
    global last_inputpath
    global last_main_exe_stdout
    keyword = "arqent"
    tempfile = keyword + ".input"

    # Copia o arquivo de entrada usando um nome pré-determinado
    shutil.copyfile(inputpath, tempfile)

    # Salva como estamos rodando os arquivos para caso algo dê errados possamos
    # mostrar um traceback de como reproduzir o erro.
    last_main_exe_invocation = [script_path + "/main.exe",
                                tempfile] + args
    last_inputpath = inputpath

    # Roda o programa pra ver o que ele faz com o arquivo de entrada
    try:
        main_exe = subprocess.run(last_main_exe_invocation, stdout=subprocess.PIPE, timeout=5)
        last_main_exe_stdout = main_exe.stdout.decode('utf-8')

        # Remove o arquivo temporário que usamos como entrada para o main.exe
        os.remove(tempfile)

        outfilepath = [fp for fp in os.listdir('.')
                       if fp.startswith(keyword)]


        # Programa gerou um arquivo de saída corretamente
        if len(outfilepath) > 0:
            outfilepath = outfilepath[0]
            with open(outfilepath, "rb") as data:
                output_contents = bytes(data.read())
            with open(inputpath, "rb") as data:
                input_contents = bytes(data.read())
            with open(gabaritopath, "rb") as data:
                gabarito_contents = bytes(data.read())

            # Deleta o arquivo de saída que o main.exe gerou, para deixar
            # o diretório limpo para o próximo teste que for rodado.
            os.remove(outfilepath)

            return (input_contents, gabarito_contents, output_contents)
        # Programa provavelmente crashou, pois não gerou um arquivo de saída
        else:
            print(colored('[ERRO] main.exe não produziu arquivo de saída', 'red'))

            with open(inputpath, "rb") as data:
                input_contents = bytes(data.read())
            with open(gabaritopath, "rb") as data:
                gabarito_contents = bytes(data.read())
            return (input_contents,
                    gabarito_contents,
                    b'main.exe nao produziu saida')
    except subprocess.TimeoutExpired as e:
        # Uh-oh, nosso programa provavelmente travou em algum arquivo
        print(colored('[ERRO] main.exe travou ao processar arquivo', 'red'))

        with open(inputpath, "rb") as data:
            input_contents = bytes(data.read())
        with open(gabaritopath, "rb") as data:
            gabarito_contents = bytes(data.read())

        # Remove o arquivo temporário que usamos como entrada para o main.exe
        os.remove(tempfile)

        outfilepath = [fp for fp in os.listdir(".") if fp.startswith(keyword)]
        # Deleta o arquivo de saída que o main.exe gerou, para deixar
        # o diretório limpo para o próximo teste que for rodado.
        [os.remove(o) for o in outfilepath]

        return (input_contents,
                gabarito_contents,
                b'main.exe travou em um arquivo')

def color_diffs(bytes_src, bytes_dest):
    if len(bytes_src) > 128:
        print(colored('[ERRO] python acredita que um dos arquivos '
                      'tem {} bytes. Limitando a 128.'.format(len(bytes_src)),
                      'red'))
        bytes_src = bytes_src[:128]
    if len(bytes_dest) > 128:
        print(colored('[ERRO] python acredita que um dos arquivos '
                      'tem {} bytes. Limitando a 128.'.format(len(bytes_dest)),
                      'red'))
        bytes_dest = bytes_dest[:128]

    hex2bin = {
        '0': '0000', '1': '0001', '2': '0010', '3': '0011',
        '4': '0100', '5': '0101', '6': '0110', '7': '0111',
        '8': '1000', '9': '1001', 'a': '1010', 'b': '1011',
        'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111',
        ' ': ' '
    }

    byte2hex = lambda b: bytes([b]).hex()
    byte2bin = lambda b: ''.join([hex2bin[ch] if ch in hex2bin
                                  else ch
                                  for ch in byte2hex(b)])

    hexdiff = ''

    bin_line = ''
    ascii_line = ''

    # These don't contain special characters for color-coding, so we can
    # use them to calculate spaces and alignments
    raw_bin_line = ''
    raw_ascii_line = ''


    # Colorizes the byte-wise difference between bytes_src and bytes_dest.
    # After N character, we build up a line and appends it to 'hexdiff'
    for i, byte_ in enumerate(bytes_src):

        # Converts byte_ into a char called ch
        try:
            # ASCII representation of byte
            ch = bytes([byte_]).decode('ascii')
            # Replace it if it isn't a printable char
            ch = ch if ch.isprintable() else '�'
        except UnicodeDecodeError:
            # Well, it wasn't a non-extended ASCII valid character anyway
            ch = '�'

        raw_bin_line += byte2bin(byte_)
        raw_ascii_line += ch


        # Dirty flag so we don't process the same byte twice
        byte_processed = False

        # Checks if this byte is part of a diff
        for op_, from_, to_ in Levenshtein.editops(bytes_src, bytes_dest):

            # If this byte is a diff source, colorize it depending on the
            # diff.
            if from_ == i:
                if op_ == 'insert':
                    bin_line += colored(byte2bin(byte_), 'magenta', 'on_green')
                    ascii_line += colored(ch, 'magenta', 'on_green')

                elif op_ == 'delete':
                    bin_line += colored(byte2bin(byte_), 'magenta', 'on_red')
                    ascii_line += colored(ch, 'magenta', 'on_red')
                elif op_ == 'replace':
                    src_bin = byte2bin(byte_)
                    dest_bin = byte2bin(bytes_dest[to_])

                    # Replaces can happen at the bit-level
                    for j in range(len(src_bin)):
                        if src_bin[j] == dest_bin[j]:
                            bin_line += src_bin[j]
                        else:
                            bin_line += colored(src_bin[j], 'magenta', 'on_yellow')
                    ascii_line += colored(ch, 'magenta', 'on_yellow')
                else:
                    bin_line += byte2bin(byte_)
                    ascii_line += ch

                byte_processed = True
                break

        if not byte_processed:
            bin_line += byte2bin(byte_)
            ascii_line += ch

        # Every each 3 bytes, we add a line
        if (((i + 1) % 4) == 0) or (i == len(bytes_src) - 1):
            vbar = ''
            offset = ' 0x{:09x} │ '.format(4 * (i // 4))

            # In order to align in a table, we fill in the spaces after the
            # last byte if our file doesn't end in a nice printable boundary
            space_after = ' ' * ((4*8+3) - len(raw_bin_line))
            bin_line = bin_line + space_after

            space_after = ' ' * (4 - len(raw_ascii_line))
            ascii_line += space_after

            hexdiff += offset + bin_line + ' │ ' + ascii_line + '  \n'

            bin_line, ascii_line, raw_bin_line, raw_ascii_line = '', '', '', ''
        else:
            bin_line += ' '
            raw_bin_line += ' '


    # A parte a seguir é um hack pra fazer a tabela ficar bonitinha
    header = ''
    #header  = '0123456789_12┬0123456789_123456789_123456789_123456┬0123456┐' + '\n'
    header += '┌─────────────┬─────────────────────────────────────┬───────┐' + '\n'
    header += '│   OFFSET    │    BINARY REPRESENTATION OF FILE    │ ASCII │' + '\n'
    header += '│─────────────┼─────────────────────────────────────┼───────│' + '\n'

    if len(bytes_src) > 0:
        hexdiff = '│' + hexdiff.replace('\n', '│\n│').rstrip('│').rstrip('\n') + '\n'
    footer  = '└─────────────┴─────────────────────────────────────┴───────┘'
    return (header + hexdiff + footer)


def show_diff(bytes_entrada, bytes_gabarito, bytes_resultado):
    print('')

    diff_entrada = color_diffs(bytes_entrada, bytes_entrada)
    diff_gabarito = color_diffs(bytes_gabarito, bytes_resultado)
    diff_resultado = color_diffs(bytes_resultado, bytes_gabarito)

    print(' ' * 8 + ' Arquivo de entrada: ')
    print(' ' * 8 + diff_entrada.replace('\n', '\n' + ' ' * 8))

    print('\n')
    print(' ' * 8 + ' Resultado esperado: ')
    print(' ' * 8 + diff_gabarito.replace('\n', '\n' + ' ' * 8))

    print('')
    print(' ' * 8 + ' Resultado obtido: ')
    print(' ' * 8 + diff_resultado.replace('\n', '\n' + ' ' * 8))


testes = list(iter_arquivos_teste())
passes = 0
falhas = 0
for num, (entrada_fp, gabarito_fp) in enumerate(testes):
    # Os argumentos pro programa estão contidos no caminho para o arquivo.
    # Nós vamos ignorar a pasta "testes" e o nome do arquivo, pois esses não
    # deveriam fazer parte dos argumentos
    args = entrada_fp.rsplit('testes/')[-1].split('/')[:-1]

    entrada_data, gabarito_data, saida_data = run_input_file(entrada_fp, gabarito_fp, args)

    passou = gabarito_data == saida_data


    por100 = "[{: >2.0f}%]".format(100 * (num + 1) / len(testes))
    if passou:
        print(colored(por100 + " PASSOU: {} --> {}"
                      .format(entrada_fp, gabarito_fp), 'green'))
    else:
        print('')
        print(colored(por100 + " FALHOU: {} --> {}"
                      .format(entrada_fp, gabarito_fp), 'red'))
        print(8 * ' ' + 'Invocação do programa: ')
        print(12 * ' '
              + ' cp -vf "{}" "{}" && '.format(entrada_fp, 'arqent.input')
              + ' '.join(['"' + i + '"' for i in last_main_exe_invocation]) + '\n')
        print(colored(8 * ' ' + '{:-^40s}'.format(' Saída do main.exe: '),
                      'yellow'))
        print(16*' '+ last_main_exe_stdout.replace('\n', '\n' + 12 * ' ').strip())
        print(colored(8 * ' ' + '='*40, 'yellow'))
        show_diff(entrada_data, gabarito_data, saida_data)
        print('')

