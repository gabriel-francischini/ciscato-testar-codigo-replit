#!/bin/bash
arqent=$1
chave=$2

echo "Executando: ./main $arqent C $chave"
./main $arqent C $chave


printf "\n\n\nDescriptografando...\n"
echo "Executando: ./main arqent.CRP C $chave"
./main arqent.CRP C $chave


printf "\n---\n\n$arqent:\n"
xxd -b arqent.txt

printf "\n---\nChave:\n"
xxd -b <(printf "$chave")

printf "\n---\narqent.CRP:\n"
xxd -b arqent.CRP

printf "\n---\narqent.DRP:\n"
xxd -b arqent.DRP
