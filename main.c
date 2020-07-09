#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// A lista inteira de funções para mexer com arquivos em C
// está disponível em: https://en.cppreference.com/w/c/io

// Esses defines são a ordem dos argumentos como está no enunciado:
// FORMARQ <nome_do_arquivo> [I][C][D][U] [chave]
#define ARG_NOME_PROGRAMA 0
#define ARG_CAMINHO_ARQENT 1
#define ARG_MODO 2
#define ARG_CHAVE 3

// Códigos para lidar com erro
#define SEM_ERRO 0
#define ERRO 1

// veja: https://www.cs.bu.edu/teaching/c/file-io/intro/
// para ver as funções que lidam com arquivos
// Essas duas variáveis são globais pois são inicializadas no main()
// mas são manipuladas dentro do modo_();
FILE *arqent = NULL;
FILE *arqsai = NULL;
char *chave;


// modo do Antonio
// É uma boa idéia usar um HexEditor pra checar o resultado do ARQSAI
int  DAT_to_INV_to_DNV(FILE *arqent, FILE *arqsai){
    //Lê o arqent.
    char ch = fgetc(arqent);
    //Pega o arqsai fazendo o ponteiro *conv apontar para aqrsai.
    FILE *conv = arqsai;
    //Enquando a leitura do arqent for diferente ao fim do arquivo (EOF)
    //ele irá escrever os caracteres lidos de arqent em arqsai 
    while (ch != EOF)
    {
        fputc(ch, conv);
    }
    //Aqui verificamos se ouve um fim prematuro do arquivo
    //no fgetc da linha 33
  if (ferror(arqent) || feof(arqent)){
    printf("Erro: Fim de arquivo prematuro");
    return ERRO;
  }else {
   return SEM_ERRO; 
  }
  //Aqui verificamos se ouve um fim prematuro do arquivo
  //no fputc da linha 40
  if(fputc == EOF){
    print("Ocorreu um erro");
    return ERRO;
  }
  
}



// modo do Eduardo
// É uma boa idéia usar um HexEditor pra checar o resultado do ARQSAI
// provavelmente vai ter que usar módulo (%) e XOR (^) nesse aqui
int Crypt(FILE *arqent, FILE* arqsai,
           const char *chave){
    int i = 0;
    int ch = fgetc(arqent);

    while(ch != EOF){
        char ch_new = ch ^ *(chave+i);
        int error = fputc(ch_new, arqsai);

        if(error == EOF){
        perror("Ocorreu um erro na gravacao. Finalizando...");
          return ERRO;
        }

        // GABRIEL: Comentei pois tava dando
        // erro de compilação e impedindo de
        // rodar os testes.
        // Descomenta aí e tenta ver o que
        // deu ruim
        /*
        if(ferror(arqent) || !feof(arqent)){
            printf("Ocorreu fim prematuro de arquivo de entrada.");
            return ERRO;
        */
        
        i++;
        if (chave[i] == '\0')
            i = 0;

        ch = fgetc(arqent); 
    }
       
    if (ferror(arqent))
      puts("Erro de E/S na leitura\n");

    return SEM_ERRO;
}


// modo do Yuri
// É uma boa idéia usar um HexEditor pra checar o resultado do ARQSAI
int unix_to_dos(FILE *arqent, FILE* arqsai){
  
  int ch;
  int err = !EOF, err2 = !EOF;

  do {
    ch = fgetc(arqent);

    if(err == EOF || err2 == EOF) {
      printf("Um erro ocorreu ao escrever no arquivo de saida usando.");
      return ERRO;
    }
    if(ferror(arqent) || feof(arqent)) {
      printf("Ocorreu fim prematuro de arquivo de entrada.");
      return ERRO;
    }

    if(ch == 0x0A)
      err2 = fputc(0x0D, arqsai);
    err = fputc(ch, arqsai);
  
  } while(ch != EOF);

  return SEM_ERRO;
}


// modo do Gabriel
// É uma boa idéia usar um HexEditor pra checar o resultado do ARQSAI
int dos_to_unix(FILE *arqent, FILE* arqsai){
    // Caractere sendo lido a partir do ARQENT
    int ch;

    // Caso aconteça algum erro ao fazer fputc()
    int err;
    while ((ch = fgetc(arqent)) != EOF){
        // Nós vamos converter \r\n, então não nos importamos
        // com coisas diferentes de \r...
        if(ch != '\r'){
            err = fputc(ch, arqsai);

        // Infelizmente teremos que tentar converter \r\n para \n
        } else {
            // ungetc() funciona se passarmos EOF, então não precisamos
            // checar por EOF agora, podemos checar dentro do laço while
            int prox_ch = fgetc(arqent);

            // Se for um \r seguido de \n, convertemos pra \n
            if(prox_ch == '\n'){
                err = fputc('\n', arqsai);

            // Ei! Alguém colocou um \r perdido no texto sem um \n
            // consecutivo, melhor não mexer nele.
            } else {
                // Devolve o prox_ch para o próximo passo do loop while
                // Inclusive pode ser que prox_ch seja EOF
                ungetc(prox_ch, arqent);
                err = fputc('\r', arqsai);
            }
        }

        // Uh-oh, deu erro em algum fputc()
        if (err == EOF){
            printf("Um erro ocorreu ao escrever no arquivo de saida usando.");
            return ERRO;
        }
    }

    if(ferror(arqent) || !feof(arqent)){
        printf("Ocorreu fim prematuro de arquivo de entrada.");
        return ERRO;
    }

    return SEM_ERRO;
}


// Compara string s1 com a string s2 e retorna 0 se forem iguais,
// usando uma comparação case-insensitive.
// veja: https://stackoverflow.com/a/34589912/6141224
int strcasecmp(const char *s1, const char *s2) {
    const unsigned char *us1 = (const u_char *)s1,
                        *us2 = (const u_char *)s2;

    while (tolower(*us1) == tolower(*us2++))
        if (*us1++ == '\0')
            return (0);
    return (tolower(*us1) - tolower(*--us2));
}

// Abre um arquivo para escrita com o mesmo nome do caminho_arqent,
// porém com a extensão ext1 (ou, caso o caminho_arqent
// já use a extensão ext1, usa a extensão ext2).
// O arquivo para escrita ficará salvo na variável global arqsai
int abrir_arqsai(const char *caminho_arqent, 
                  const char *ext1 /*ex: ".INV" */, 
                  const char *ext2 /*ex: ".DNV" */){
    // veja: https://stackoverflow.com/questions/3217629
    const char *ultimoPonto = strrchr(caminho_arqent, '.');
    const char *ext_arqent = ultimoPonto;

    // Precisamos saber qual será o tamanho da nossa string com
    // a nova extensão, para poder criá-la
    int posUltimoPonto;
    const char *ext_a_usar;

    if(ultimoPonto != NULL){
        // Temos um ponto (i.e. extensão) no nome do arquivo
        posUltimoPonto = ultimoPonto - caminho_arqent;
        printf("Extensao do arquivo de entrada (indice %d): %s\n",
               posUltimoPonto, ultimoPonto);

        // Se o arquivo tiver a extensão ext1, quer dizer que
        // que o arquivo já foi processado pelo nosso programa e
        // agora deve ser convertido para ext2.
        // Caso o contrário, é a primeira vez que é visto pelo nosso
        // programa e deve ser convertido para ex1.
        if(strcasecmp(ext_arqent, ext1) == 0){
            printf("Arquivo de entrada usa o padrao FORMARQ: %s\n",
                   ext1);
            ext_a_usar = ext2;
        } else {
            ext_a_usar = ext1;
        }
    } else {
        // Não temos um ponto no nome do arquivo
        posUltimoPonto = strlen(caminho_arqent);
        printf("Arquivo nao tem extensao (indice %d)\n", posUltimoPonto);
        ext_a_usar = ext1;
    }
    printf("Extensao do arquivo de saida: %s\n", ext_a_usar);

    // Nós vamos adicionar os caracteres '.', 'I', 'N', 'V', '\0' à string
    const int tamanho_nova_string = posUltimoPonto + 4 + 1;

    char *caminho_arqsai = malloc(tamanho_nova_string * sizeof(char));

    // Deu ruim ao tentar criar a string que ia conter o caminho pro
    // arqsai, então cancele tudo.
    if(caminho_arqsai == NULL){
        printf("Deu erro ao alocar espaco para o caminho de saida\n");
        return ERRO;
    }

    strncpy(caminho_arqsai, caminho_arqent, posUltimoPonto);
    char *ext_arqsai = caminho_arqsai + posUltimoPonto;

    // Copia inclusive o \0 final que vem da ext_a_usar
    strncpy(ext_arqsai, ext_a_usar, tamanho_nova_string - posUltimoPonto);
    printf("Escrevendo arquivo: %s\n", caminho_arqsai);

    arqsai = fopen(caminho_arqsai, "w");
    int retorno = SEM_ERRO;

    if(arqsai == NULL){
        printf("Nao foi possivel escrever o arquivo %s.\n",
               caminho_arqsai);
        retorno = ERRO;
    }

    // Invalida os ponteiros que apontam pra dentro de caminho_arqsai
    free(caminho_arqsai);
    caminho_arqsai = NULL;
    ext_arqsai = NULL;

    return retorno;
}

int main(int argc, char *argv[]) {
    printf("Iniciando programa FORMARQ...\n");

    // O usuário deve fornecer pelo menos 
    // o arquivo e o modo
    if (argc <= ARG_MODO){
        // TODO: Melhorar essa screen de help/usage
        printf("Faltou escolher o arquivo ou comando.\n");
        exit(-1);
    }

    /* ... O usuário deve escolher somente um dos métodos de conversão. ... */
    const char modo = argv[ARG_MODO][0];

    // O modo 2 (Cript) requer uma chave
    if (modo == 'C'){
        if (argc <= ARG_CHAVE){
        printf("Faltou escolher a chave.\n");
        exit(-1);
        } else {
            chave = argv[ARG_CHAVE];
        }
    }

    // Independente do modo, nós temos que abrir o ARQENT para leitura
    const char *caminho_arqent = argv[ARG_CAMINHO_ARQENT];
    printf("Abrindo arquivo: %s\n", caminho_arqent);
    // PERIGO! Feche com fclose() todo arquivo que você abrir com fopen()
    arqent = fopen(caminho_arqent, "r");

    // Uh-oh, se não conseguir abrir o ARQENT, algo deu muito errado
    if (arqent == NULL){
        printf("Deu ruim ao abrir o arquivo de entrada.\n");
        exit(-1);
    }

    int err = SEM_ERRO;

    printf("Modo de operação: %C\n", modo);
    /* Abre o arquivo de saida */
    switch(modo){
        case 'I': {
            err = abrir_arqsai(caminho_arqent, ".INV", ".DNV");
        } break;

        case 'C': {
            err = abrir_arqsai(caminho_arqent, ".CRP", ".DRP");
        } break;

        case 'D': {
            err = abrir_arqsai(caminho_arqent, ".DOS", ".DOS");
        } break;

        case 'U': {
            err = abrir_arqsai(caminho_arqent, ".UNX", ".UNX");
        } break;

        default: {
            printf("Modo nao reconhecido.\n");
            // PERIGO! Feche com fclose() tudo que você abrir com fopen()
            fclose(arqent);
            exit(-1);
        } break;
    }

    if(err == ERRO){
        printf("Erro ao abrir arquivo de saida.\n");
        // PERIGO! Feche com fclose() o que você abrir com fopen()
        fclose(arqent);
        exit(-1);
    }

    /* Executa o arquivo usando o modo */
    switch(modo){
        case 'I': {
            err = DAT_to_INV_to_DNV(arqent, arqsai);
        } break;

        case 'C': {
            err = Crypt(arqent, arqsai, chave);
        } break;

        case 'D': {
            err = unix_to_dos(arqent, arqsai);
        } break;

        case 'U': {
            err = dos_to_unix(arqent, arqsai);
        } break;
    }


    if (err == ERRO){
        
    }
    // PERIGO! Feche com fclose() todo arquivo que você abrir com fopen()
    fclose(arqsai);
    fclose(arqent);
}