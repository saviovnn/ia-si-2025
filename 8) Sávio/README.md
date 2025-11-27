# Locomotiva - Solução Completa

Este projeto foi desenvolvido como trabalho da matéria de **Inteligência Artificial I** do professor [Luis Fernando de Almeida](https://www.linkedin.com/in/luis-fernando-de-almeida/) na **UNITAU**.

## 📋 Sobre o Projeto

**Tema:** Planejamento de abastecimento linha

**Objetivo:** Rotas de trens logísticos atendendo múltiplas estações sob janelas de tempo

A **Locomotiva** é uma solução completa para planejamento e visualização de rotas ferroviárias no Brasil. O sistema utiliza algoritmos de busca em grafos para calcular rotas otimizadas entre estações ferroviárias, considerando diferentes tipos de bitola e múltiplos algoritmos de busca.

## 🏗️ Arquitetura da Solução

A solução Locomotiva é composta por **dois repositórios principais**:

### 1. **Locomotiva API** (Backend)
API REST desenvolvida em Python com FastAPI que implementa os algoritmos de busca em grafos e fornece endpoints para cálculo de rotas ferroviárias.

**Principais funcionalidades:**
- Implementação de múltiplos algoritmos de busca (Amplitude, Profundidade, Bidirecional, A*, Greedy, Custo Uniforme, entre outros)
- Suporte a três tipos de bitola ferroviária (Larga, Métrica, Standart)
- Cálculo de rotas otimizadas entre estações
- Fornecimento de coordenadas geográficas das estações
- Documentação interativa com Swagger/ReDoc

**Tecnologias:** Python 3.8+, FastAPI, Pandas

### 2. **Locomotiva Front** (Frontend)
Interface web desenvolvida em Vue.js para visualização interativa das rotas ferroviárias em mapas.

**Principais funcionalidades:**
- Visualização de rotas em mapas interativos (Leaflet)
- Seleção de origem, destino, bitola e algoritmo de busca
- Exibição de todas as rotas disponíveis para uma bitola
- Interface responsiva (desktop e mobile)
- Feedback visual com toasts e modais informativos

**Tecnologias:** Vue 3, Pinia, Leaflet, Axios, Vite

## 🎯 Funcionalidades Principais

- **Busca de Rotas:** Calcula a melhor rota entre duas estações ferroviárias usando diversos algoritmos de busca
- **Múltiplas Bitolas:** Suporte para bitola Larga (1,60m), Métrica (1,00m) e Standart (1,435m)
- **Visualização em Mapas:** Exibe rotas calculadas em mapas interativos com marcadores e linhas
- **Dados Reais:** Utiliza dados oficiais do governo brasileiro sobre a malha ferroviária nacional
- **Algoritmos Avançados:** Implementa algoritmos clássicos e heurísticos de busca em grafos

## 📊 Dados Utilizados

Os dados foram obtidos do [site oficial do governo](https://www.gov.br/transportes/pt-br/assuntos/dados-de-transportes/bit/bit-mapas) e incluem:
- Base de dados das estações ferroviárias brasileiras
- Grafos das três principais bitolas (Larga, Métrica, Standart)
- Coordenadas geográficas das estações
- Linhas ferroviárias em formato GeoJSON

## 🚀 Como Executar

Para mais detalhes sobre instalação e execução, consulte:
- [README da API](./locomotiva-api/README.md) - Instruções para o backend
- [README do Frontend](./locomotiva-front/README.md) - Instruções para o frontend
- [LEIAME.txt](./LEIAME.txt) - Guia rápido de instalação

**Resumo rápido:**
1. Instalar dependências da API: `cd locomotiva-api && pip install -r requirements.txt`
2. Instalar dependências do Frontend: `cd locomotiva-front && npm install`
3. Executar API: `uvicorn main:app --reload` (porta 8000)
4. Executar Frontend: `npm run dev` (porta 5173)

## 📹 Demonstração

[![Video](https://img.youtube.com/vi/zYT4hnvumOs/0.jpg)](https://www.youtube.com/watch?v=zYT4hnvumOs)

## 📝 Notas

- A API precisa estar rodando antes de usar o frontend
- Ambos os serviços devem estar rodando simultaneamente
- Os dados são carregados em memória na inicialização da API
- Nem todas as estações podem coincidir exatamente com a rota desenhada no mapa (pode haver variação)

