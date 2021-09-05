![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
[![Build status](https://ci.appveyor.com/api/projects/status/2yw8sjkjqn0c45q4?svg=true)](https://ci.appveyor.com/project/rodrigorf/crawler-mercadolivre)

## Como funciona?

-> Coleta dados de produtos a partir dos links de categoras do MercadoLivre<br>
-> Grava imagens na pasta data/output/imagens<br>
-> Grava xlsx dos itens coletados na pasta data/output<br>
-> Os links das categorias devem ser informados no arquivo config.py<br>

**OBSERVAÇÃO**: a responsabilidade de uso é de cada um, utilize para adquirir conhecimento e
contribuições são bem-vindas, o projeto possui muitas melhorias que podem ser feitas e 
infinitas formas de chegar ao mesmo resultado.

## O que este código não é e não faz!

-> Não é multithreaded<br>
-> Não é escalável<br>
-> Não usa proxys

## Instruções de instalação

    1. Instale o python(testado na 3.8.x) - Gerenciador de pacotes PIP<br>
    2. pip install virtualenv<br>
    3. Execute: virtualenv venv (pode escolher outro nome mas lembre de modificar no exec.bat se for usar)
    4. Ative o ambiente virtual: cd venv/scripts & activate
    5. Execute: "pip install -r requirements.txt" para instalar os packages<br>

## Instruções de configuração

    * executarCategorias -> lista com os links das categorias do ML
    * PAGE_SIZE -> total de produtos por página
    * BAIXAR_IMAGENS -> Se true, serão baixadas para pasta data/output/imagens.
    * LIMITE_PRODUTOS -> a quantidade que deseja processar, se quiser tudo coloque um valor elevado. Ex: 99999
    * HEADER_TOTAL_SIZE -> colunas do excel que será gerado. Funciona junto com configuração CSV_HEADER.

## Seja feliz!
    EXECUTE: exec.bat ou python run.py

[Blog - rodrigoreisf.com.br](http://rodrigoreisf.com.br)
