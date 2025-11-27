# Locomotiva API

Este projeto foi desenvolvido como trabalho da matéria de **Inteligência Artificia I** do professor [Luis Fernando de Almeida](https://www.linkedin.com/in/luis-fernando-de-almeida/) na **UNITAU**.

### Tema do Projeto

**Planejamento de abastecimento linha**

- **Objetivo:** Rotas de trens logísticos atendendo múltiplas estações sob janelas de tempo

Esta API implementa algoritmos de busca em grafos para calcular rotas ferroviárias otimizadas, permitindo o planejamento de abastecimento considerando múltiplas estações e restrições de janelas de tempo.

## Fonte dos Dados

Os [dados](https://www.gov.br/transportes/pt-br/assuntos/dados-de-transportes/bit/bit-mapas) utilizados foram obtidos do site oficial do governo.

**Data de coleta:** 8 de outubro de 2025

Os dados estão localizados na pasta `dados-brasil/` e incluem:
- `BaseFerro.csv` - Base de dados das estações ferroviárias
- `grafo_bitola_Larga.json` - Grafo da bitola larga (1,60m)
- `grafo_bitola_Metrica.json` - Grafo da bitola métrica (1,00m)
- `grafo_bitola_Standart.json` - Grafo da bitola padrão (1,435m)
- `linhas_ferroviarias.geojson` - Linhas ferroviárias em formato GeoJSON

## Pré-requisitos

- Python 3.8+ instalado
- Terminal

## Instalação

1. Abra o terminal na pasta `locomotiva-api`
2. Execute: `python -m venv venv`
3. Execute: `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Mac/Linux)
4. Execute: `pip install -r requirements.txt`

## Execução

1. Execute: `uvicorn main:app --reload`
2. A API estará rodando em `http://localhost:8000`

## Documentação da API

A documentação interativa da API está disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints Principais

- `POST /mapa-rota` - Busca uma rota entre duas cidades e retorna dados completos para montar o mapa
- `POST /coordenadas-cidades` - Obtém as coordenadas de múltiplas cidades de uma vez
- `GET /coordenadas-cidade/{cidade}` - Obtém as coordenadas de uma cidade específica
- `GET /cidades/{bitola}` - Lista todas as cidades disponíveis para uma bitola
- `GET /rotas/{bitola}` - Lista todas as rotas de uma bitola


## Notas

- A API roda na porta 8000 por padrão
- O CORS está habilitado para permitir requisições do frontend
- Os dados são carregados em memória na inicialização da API

