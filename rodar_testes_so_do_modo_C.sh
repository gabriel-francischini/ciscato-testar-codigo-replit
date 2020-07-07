#!/bin/bash

# Compila
clang-7 -pthread -lm -o main main.c && chmod +x main

# Se compilar de boas, testa
if [ $? -eq 0 ]
then
  echo "Executando suíte de testes..."
  cp -v main ./sistema_de_testes/main.exe
  if [ $? -eq 0 ]
  then
    cd sistema_de_testes
    python main.py C
    cd ..
  else
    echo "Deu erro ao fazer a cópia do programa main. Não foi possível rodar os testes."
  fi
else
  echo "Deu ruim na hora de compilar o programa. Não foi possível rodas os testes."
fi
