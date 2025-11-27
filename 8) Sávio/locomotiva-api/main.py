from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
import pandas as pd

from BuscaNP import buscaNP

app = FastAPI(
    title="API de Busca de Rotas Ferroviárias", 
    description="API para encontrar a melhor rota entre cidades usando algoritmos de busca",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/dados", StaticFiles(directory="./dados-brasil"), name="dados")

# Modelos Pydantic para validação
#---------------------------------

class MapaRequest(BaseModel):
    origem: str = Field(
        ...,
        description="Cidade de origem no formato 'Cidade_UF'",
        example="Taubaté_SP"
    )
    destino: str = Field(
        ...,
        description="Cidade de destino no formato 'Cidade_UF'",
        example="Leme_SP"
    )
    bitola: str = Field(
        default="Larga",
        description="Tipo de bitola ferroviária",
        example="Larga"
    )
    algoritmo: str = Field(
        default="amplitude",
        description="Algoritmo de busca a ser utilizado",
        example="amplitude"
    )
    profundidade: int = Field(
        default=20,
        description="Profundidade máxima para algoritmos que requerem (prof_limitada, aprofundamento_iterativo)",
        example=20,
        ge=1,
        le=100
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "origem": "Taubaté_SP",
                "destino": "Leme_SP",
                "bitola": "Larga",
                "algoritmo": "amplitude",
                "profundidade": 20
            }
        }
    }

class CoordenadasCidadesRequest(BaseModel):
    cidades: List[str] = Field(
        ...,
        description="Lista de cidades no formato 'Cidade_UF'",
        example=["Leme_SP", "Taubaté_SP", "São Paulo_SP"]
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "cidades": ["Leme_SP", "Taubaté_SP", "São Paulo_SP"]
            }
        }
    }

class MapaResponse(BaseModel):
    sucesso: bool = Field(..., description="Indica se a busca foi bem-sucedida")
    rota: Optional[Dict[str, Any]] = Field(None, description="Dados da rota encontrada")
    cidades: Optional[List[Dict[str, Any]]] = Field(None, description="Lista de cidades com coordenadas")
    conexoes: Optional[List[Dict[str, Any]]] = Field(None, description="Lista de conexões entre cidades")
    mensagem: str = Field(..., description="Mensagem descritiva do resultado")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "sucesso": True,
                "rota": {
                    "caminho": ["Taubaté_SP", "Tremembé_SP", "Leme_SP"],
                    "distancia_total": 35.5,
                    "numero_paradas": 2,
                    "algoritmo_usado": "amplitude",
                    "bitola_usada": "Larga",
                    "origem": "Taubaté_SP",
                    "destino": "Leme_SP"
                },
                "cidades": [
                    {
                        "nome": "Taubaté_SP",
                        "latitude": -23.02627004199995,
                        "longitude": -45.55426145299994,
                        "uf": "SP",
                        "municipio": "Taubaté"
                    },
                    {
                        "nome": "Tremembé_SP",
                        "latitude": -22.95627004199995,
                        "longitude": -45.54426145299994,
                        "uf": "SP",
                        "municipio": "Tremembé"
                    },
                    {
                        "nome": "Leme_SP",
                        "latitude": -22.23614280399994,
                        "longitude": -47.36555590599994,
                        "uf": "SP",
                        "municipio": "Leme"
                    }
                ],
                "conexoes": [
                    {
                        "origem": "Taubaté_SP",
                        "destino": "Tremembé_SP",
                        "distancia": 8.93,
                        "coordenadas_origem": {
                            "latitude": -23.02627004199995,
                            "longitude": -45.55426145299994
                        },
                        "coordenadas_destino": {
                            "latitude": -22.95627004199995,
                            "longitude": -45.54426145299994
                        }
                    },
                    {
                        "origem": "Tremembé_SP",
                        "destino": "Leme_SP",
                        "distancia": 26.57,
                        "coordenadas_origem": {
                            "latitude": -22.95627004199995,
                            "longitude": -45.54426145299994
                        },
                        "coordenadas_destino": {
                            "latitude": -22.23614280399994,
                            "longitude": -47.36555590599994
                        }
                    }
                ],
                "mensagem": "Rota encontrada com sucesso entre 'Taubaté_SP' e 'Leme_SP'"
            }
        }
    }

# Instâncias dos grafos por bitola
grafos = {}

def carregar_grafos():
    global grafos
    
    bitola_arquivos = {
        "Larga": "./dados-brasil/grafo_bitola_Larga.json",
        "Metrica": "./dados-brasil/grafo_bitola_Metrica.json",
        "Standart": "./dados-brasil/grafo_bitola_Standart.json",
    }
    
    for bitola, arquivo in bitola_arquivos.items():
        if os.path.exists(arquivo):
            try:
                grafos[bitola] = buscaNP(arquivo)
                print(f"Grafo {bitola} carregado com sucesso")
            except Exception as e:
                print(f"Erro ao carregar grafo {bitola}: {e}")
        else:
            print(f"Arquivo {arquivo} não encontrado")

dados_csv = None

def carregar_dados_csv():
    global dados_csv
    try:
        csv_path = "./dados-brasil/BaseFerro.csv"
        if os.path.exists(csv_path):
            dados_csv = pd.read_csv(csv_path)
            print(f"Dados CSV carregados: {len(dados_csv)} registros")
        else:
            print("Arquivo CSV não encontrado")
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")

def obter_coordenadas_cidade(cidade_nome):
    if dados_csv is None:
        return None
    
    # Extrair nome da cidade e UF do formato "Cidade_UF"
    if '_' in cidade_nome:
        nome_cidade, uf = cidade_nome.rsplit('_', 1)
    else:
        nome_cidade = cidade_nome
        uf = None
    
    # Buscar no CSV
    if uf:
        mask = (dados_csv['municipio'].str.contains(nome_cidade, case=False, na=False)) & \
               (dados_csv['uf'] == uf)
    else:
        mask = dados_csv['municipio'].str.contains(nome_cidade, case=False, na=False)
    
    resultado = dados_csv[mask]
    
    if len(resultado) > 0:
        # Pegar o primeiro resultado e extrair coordenadas do geometry
        geometry = resultado.iloc[0]['geometry']
        if geometry and geometry.startswith('LINESTRING'):
            # Extrair primeiro ponto da linha
            coords_str = geometry.split('(')[1].split(')')[0]
            first_point = coords_str.split(',')[0].strip()
            lon, lat = first_point.split()
            return {
                'nome': cidade_nome,
                'latitude': float(lat),
                'longitude': float(lon),
                'uf': resultado.iloc[0]['uf'],
                'municipio': resultado.iloc[0]['municipio']
            }
    
    return None

# Carregar grafos e dados CSV na inicialização
carregar_grafos()
carregar_dados_csv()

@app.post("/mapa-rota", response_model=MapaResponse)
def obter_dados_mapa(request: MapaRequest):
    """
    Retorna dados para montar mapa com a rota encontrada entre duas cidades.
    
    **Algoritmos disponíveis:**
    - `amplitude` - Busca em amplitude
    - `profundidade` - Busca em profundidade
    - `bidirecional` - Busca bidirecional
    - `prof_limitada` - Profundidade limitada (requer profundidade)
    - `aprofundamento_iterativo` - Aprofundamento iterativo (requer profundidade)
    - `custo_uniforme` - Custo uniforme
    - `greedy` - Busca gulosa
    - `a_estrela` - Algoritmo A*
    - `aia_estrela` - A* Iterativo
    
    **Exemplos de cidades por bitola:**
    
    **Larga:**
    - Origem: `Taubaté_SP`, Destino: `Leme_SP`
    - Origem: `Leme_SP`, Destino: `Araras_SP`
    
    **Metrica:**
    - Origem: `São Paulo_SP`, Destino: `Osasco_SP`
    
    **Standart:**
    - Origem: `Santana_AP`, Destino: `Macapá_AP`
    """
    
    # Normalizar parâmetros
    bitola_normalizada = request.bitola.lower().strip()
    algoritmo_normalizado = request.algoritmo.lower().strip()
    
    # Validar bitola - aceita qualquer formato (larga, LARGA, LaRgA, etc.)
    bitola_encontrada = None
    for key in grafos.keys():
        if key.lower() == bitola_normalizada:
            bitola_encontrada = key
            break
    
    if bitola_encontrada is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Bitola '{request.bitola}' não encontrada. Bitolas disponíveis: {list(grafos.keys())}"
        )
    
    grafo = grafos[bitola_encontrada]
    
    # Validar se as cidades existem
    if not grafo.grafo_loader.verificar_cidade_existe(request.origem):
        raise HTTPException(
            status_code=404, 
            detail=f"Cidade de origem '{request.origem}' não encontrada na bitola {bitola_encontrada}"
        )
    
    if not grafo.grafo_loader.verificar_cidade_existe(request.destino):
        raise HTTPException(
            status_code=404, 
            detail=f"Cidade de destino '{request.destino}' não encontrada na bitola {bitola_encontrada}"
        )
    
    # Executar busca baseada no algoritmo - aceita qualquer formato
    try:
        if algoritmo_normalizado in ["amplitude", "breadth", "bfs"]:
            caminho = grafo.amplitude(request.origem, request.destino)
        elif algoritmo_normalizado in ["profundidade", "depth", "dfs"]:
            caminho = grafo.profundidade(request.origem, request.destino)
        elif algoritmo_normalizado in ["bidirecional", "bidirectional", "bi"]:
            caminho = grafo.bidirecional(request.origem, request.destino)
        elif algoritmo_normalizado in ["prof_limitada", "profundidade_limitada", "limited_depth"]:
            caminho = grafo.prof_limitada(request.origem, request.destino, request.profundidade)
        elif algoritmo_normalizado in ["aprofundamento_iterativo", "iterative_deepening", "ida"]:
            caminho = grafo.aprof_iterativo(request.origem, request.destino, request.profundidade)
        elif algoritmo_normalizado in ["custo_uniforme", "uniform_cost", "ucs"]:
            caminho = grafo.custo_uniforme(request.origem, request.destino)
        elif algoritmo_normalizado in ["greedy", "gulosa", "best_first"]:
            caminho = grafo.greedy(request.origem, request.destino)
        elif algoritmo_normalizado in ["a_estrela", "a_star", "astar"]:
            caminho = grafo.a_estrela(request.origem, request.destino)
        elif algoritmo_normalizado in ["aia_estrela", "aia_star", "iterative_astar"]:
            caminho = grafo.aia_estrela(request.origem, request.destino)
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Algoritmo '{request.algoritmo}' não suportado. Algoritmos disponíveis: amplitude/breadth/bfs, profundidade/depth/dfs, bidirecional/bidirectional/bi, prof_limitada/limited_depth, aprofundamento_iterativo/iterative_deepening/ida, custo_uniforme/uniform_cost/ucs, greedy/gulosa/best_first, a_estrela/a_star/astar, aia_estrela/aia_star/iterative_astar"
            )
        
        if caminho is None:
            return MapaResponse(
                sucesso=False,
                mensagem=f"Não foi possível encontrar uma rota entre '{request.origem}' e '{request.destino}'"
            )
        
        # Calcular distância total
        distancia_total = 0
        for i in range(len(caminho) - 1):
            distancia = grafo.grafo_loader.obter_distancia(caminho[i], caminho[i + 1])
            if distancia != float('inf'):
                distancia_total += distancia
        
        # Obter coordenadas das cidades
        cidades_rota = []
        for cidade in caminho:
            coords = obter_coordenadas_cidade(cidade)
            if coords:
                cidades_rota.append(coords)
        
        # Criar conexões
        conexoes_rota = []
        for i in range(len(caminho) - 1):
            cidade_origem = caminho[i]
            cidade_destino = caminho[i + 1]
            distancia = grafo.grafo_loader.obter_distancia(cidade_origem, cidade_destino)
            
            coords_origem = obter_coordenadas_cidade(cidade_origem)
            coords_destino = obter_coordenadas_cidade(cidade_destino)
            
            if coords_origem and coords_destino:
                conexoes_rota.append({
                    'origem': cidade_origem,
                    'destino': cidade_destino,
                    'distancia': distancia,
                    'coordenadas_origem': {
                        'latitude': coords_origem['latitude'],
                        'longitude': coords_origem['longitude']
                    },
                    'coordenadas_destino': {
                        'latitude': coords_destino['latitude'],
                        'longitude': coords_destino['longitude']
                    }
                })
        
        dados_rota = {
            'caminho': caminho,
            'distancia_total': round(distancia_total, 2),
            'numero_paradas': len(caminho) - 1,
            'algoritmo_usado': algoritmo_normalizado,
            'bitola_usada': bitola_encontrada,
            'origem': request.origem,
            'destino': request.destino
        }
        
        return MapaResponse(
            sucesso=True,
            rota=dados_rota,
            cidades=cidades_rota,
            conexoes=conexoes_rota,
            mensagem=f"Rota encontrada com sucesso entre '{request.origem}' e '{request.destino}'"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno durante a busca: {str(e)}")


@app.get("/coordenadas-cidade/{cidade}")
async def obter_coordenadas_cidade_endpoint(
    cidade: str = Path(..., description="Nome da cidade no formato 'Cidade_UF'", example="Leme_SP")
):
    """
    Retorna as coordenadas de uma cidade específica.
    
    **Exemplo de uso:**
    - `/coordenadas-cidade/Leme_SP`
    - `/coordenadas-cidade/São Paulo_SP`
    - `/coordenadas-cidade/Macapá_AP`
    """
    coords = obter_coordenadas_cidade(cidade)
    if coords:
        return {
            "cidade": cidade,
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
            "uf": coords["uf"],
            "municipio": coords["municipio"]
        }
    else:
        raise HTTPException(status_code=404, detail=f"Cidade '{cidade}' não encontrada")

@app.post("/coordenadas-cidades")
async def obter_coordenadas_multiplas_cidades(request: CoordenadasCidadesRequest):
    """
    Retorna as coordenadas de múltiplas cidades de uma vez.
    
    Aceita uma lista de cidades e retorna todas as coordenadas encontradas.
    Cidades não encontradas não serão incluídas no resultado.
    
    **Exemplo de uso:**
    ```json
    {
        "cidades": ["Leme_SP", "Taubaté_SP", "São Paulo_SP"]
    }
    ```
    
    **Resposta:**
    ```json
    {
        "total": 3,
        "encontradas": 3,
        "coordenadas": [
            {
                "nome": "Leme_SP",
                "latitude": -22.23614280399994,
                "longitude": -47.36555590599994,
                "uf": "SP",
                "municipio": "Leme"
            },
            ...
        ]
    }
    ```
    """
    coordenadas_encontradas = []
    
    for cidade in request.cidades:
        coords = obter_coordenadas_cidade(cidade)
        if coords:
            coordenadas_encontradas.append({
                "nome": cidade,
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "uf": coords["uf"],
                "municipio": coords["municipio"]
            })
    
    return {
        "total": len(request.cidades),
        "encontradas": len(coordenadas_encontradas),
        "coordenadas": coordenadas_encontradas
    }

@app.get("/cidades/{bitola}")
def listar_cidades(
    bitola: str = Path(..., description="Tipo de bitola (Larga, Metrica, Standart)", example="Larga")
):
    """
    Lista todas as cidades disponíveis para uma bitola específica.
    
    **Bitolas disponíveis:**
    - `Larga`: 851 cidades
    - `Metrica`: 1127 cidades
    - `Standart`: 5 cidades
    
    **Exemplo de uso:**
    - `/cidades/Larga`
    - `/cidades/Metrica`
    - `/cidades/Standart`
    """
    # Normalizar bitola para aceitar qualquer formato
    bitola_normalizada = bitola.lower().strip()
    bitola_encontrada = None
    for key in grafos.keys():
        if key.lower() == bitola_normalizada:
            bitola_encontrada = key
            break
    
    if bitola_encontrada is None:
        raise HTTPException(status_code=404, detail=f"Bitola '{bitola}' não encontrada. Bitolas disponíveis: {list(grafos.keys())}")
    
    todas_cidades = grafos[bitola_encontrada].grafo_loader.listar_cidades()
    
    return {
        "bitola": bitola_encontrada,
        "total_cidades": len(todas_cidades),
        "cidades": todas_cidades
    }

@app.get("/rotas/{bitola}")
def obter_rotas(
    bitola: str = Path(..., description="Tipo de bitola (Larga, Metrica, Standart)", example="Larga")
):
    """
    Retorna todas as rotas possíveis entre cidades para uma bitola específica.
    
    Retorna todas as conexões diretas entre cidades na bitola especificada.
    
    **Exemplo de uso:**
    - `/rotas/Larga` - Retorna todas as 943 conexões da bitola larga
    - `/rotas/Metrica` - Retorna todas as 1267 conexões da bitola métrica
    - `/rotas/Standart` - Retorna todas as 4 conexões da bitola padrão
    """
    # Normalizar bitola para aceitar qualquer formato
    bitola_normalizada = bitola.lower().strip()
    bitola_encontrada = None
    for key in grafos.keys():
        if key.lower() == bitola_normalizada:
            bitola_encontrada = key
            break
    
    if bitola_encontrada is None:
        raise HTTPException(status_code=404, detail=f"Bitola '{bitola}' não encontrada. Bitolas disponíveis: {list(grafos.keys())}")
    
    grafo = grafos[bitola_encontrada]
    todas_rotas = []
    
    # Obter todas as cidades
    todas_cidades = grafo.grafo_loader.listar_cidades()
    
    # Para cada cidade, obter suas conexões diretas
    for cidade in todas_cidades:
        sucessores = grafo.grafo_loader.obter_sucessores(cidade)
        for sucessor in sucessores:
            distancia = grafo.grafo_loader.obter_distancia(cidade, sucessor)
            todas_rotas.append({
                "origem": cidade,
                "destino": sucessor,
                "distancia": distancia
            })
    
    return {
        "bitola": bitola_encontrada,
        "total_rotas": len(todas_rotas),
        "total_cidades": len(todas_cidades),
        "rotas": todas_rotas
    }

