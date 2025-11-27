# Locomotiva Front

Este projeto foi desenvolvido como trabalho da matéria de **Inteligência Artificia I** do professor [Luis Fernando de Almeida](https://www.linkedin.com/in/luis-fernando-de-almeida/) na **UNITAU**.


### Tema do Projeto

**Planejamento de abastecimento linha**

- **Objetivo:** Rotas de trens logísticos atendendo múltiplas estações sob janelas de tempo

Este frontend utiliza os algoritmos de busca em grafos implementados na API para calcular e visualizar as rotas ferroviárias otimizadas. Para mais detalhes sobre os algoritmos disponíveis, consulte a documentação da API.

## Demo do Projeto

[![Video](https://img.youtube.com/vi/zYT4hnvumOs/0.jpg)](https://www.youtube.com/watch?v=zYT4hnvumOs)

## Disclaimer

Nem todas as estações vão coincidir exatamente com a rota desenhada no mapa, pode haver uma variação.

Em casos de dúvida sobre qual estação está sendo referenciada, basta apenas clicar na mesma.

## Tecnologias

- Vue 3 (Composition API com `<script setup>`)
- Pinia (Gerenciamento de estado)
- Axios (Requisições HTTP)
- Leaflet (Mapas)
- Vite (Build tool)

## Instalação

```bash
npm install
```

## Desenvolvimento

```bash
npm run dev
```

A aplicação estará disponível em `http://localhost:5173`

## Build

```bash
npm run build
```

## Requisitos

- Node.js 18+
- API rodando em `http://localhost:8000`
