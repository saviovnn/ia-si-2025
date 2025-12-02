from flask import Flask, jsonify, request, render_template
from modules.buscaNP import buscaNP

app = Flask(__name__)
buscador = buscaNP()

# Função para ler o mapa a partir do arquivo texto
def ler_mapa():
    mapa = []
    with open("data/mapa.txt", "r") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:  # Ignora linhas vazias
                continue
            mapa.append([int(x) for x in linha.split()])  # Converte valores para inteiro
    nx = len(mapa)  # Quantidade de linhas
    ny = len(mapa[0]) if nx > 0 else 0  # Quantidade de colunas
    return mapa, nx, ny

# Converte coordenadas do tipo "A,3" para índices numéricos
def coordenada_para_indices(coord):
    try:
        letra, num = coord.split(",")  # Separa letra e número
        return [ord(letra.upper()) - 65, int(num)]  # Converte letra para índice (A=0, B=1, ...)
    except Exception:
        raise ValueError("Formato inválido para coordenada")

@app.route("/")
def index():
    return render_template("index.html")  # Retorna página principal

@app.route("/api/dados")
def api_dados():
    mapa, nx, ny = ler_mapa()  # Carrega mapa

    # Encontrar máquinas, marcadas com o valor 2 no mapa
    maquinas = []
    for x in range(nx):
        for y in range(ny):
            if mapa[x][y] == 2:
                maquinas.append(f"{chr(x + 65)},{y}")  # Converte índice para coordenada

    methods = [
        "a_estrela"
    ]  # Lista de métodos disponíveis

    return jsonify({
        "mapa": mapa,
        "nx": nx,
        "ny": ny,
        "methods": methods,
        "maquinas": maquinas
    })

@app.route("/api/buscar")
def api_buscar():
    mapa, nx, ny = ler_mapa()  # Carrega mapa
    start_param = request.args.get("start")  # Ponto inicial
    end_param = request.args.get("end")  # Ponto final
    metodo = request.args.get("method")  # Método de busca

    if not start_param or not end_param or not metodo:
        return jsonify({"erro": "Parâmetros inválidos"}), 400

    try:
        inicio = coordenada_para_indices(start_param)  # Converte início
        fim = coordenada_para_indices(end_param)  # Converte destino
    except Exception:
        return jsonify({"erro": "Formato inválido para início/fim"}), 400

    caminho = None
    custo = None

    try:
        # Seleciona método com base na string recebida
        if metodo == "amplitude":
            caminho = buscador.amplitude(inicio, fim, nx, ny, mapa)
        elif metodo == "profundidade":
            caminho = buscador.profundidade(inicio, fim, nx, ny, mapa)
        elif metodo == "limitada":
            limite = request.args.get("limite", default=10, type=int)
            caminho = buscador.prof_limitada(inicio, fim, nx, ny, mapa, limite)
        elif metodo == "iterativo":
            caminho = buscador.aprof_iterativo(inicio, fim, nx, ny, mapa, 40)
        elif metodo == "bidirecional":
            caminho = buscador.bidirecional(inicio, fim, nx, ny, mapa)
        elif metodo == "custo_uniforme":
            resultado = buscador.custo_uniforme(inicio, fim, mapa, nx, ny)
            if resultado:
                caminho, custo = resultado
        elif metodo == "greedy":
            resultado = buscador.greedy(inicio, fim, mapa, nx, ny)
            if resultado:
                caminho, custo = resultado
        elif metodo == "a_estrela":
            resultado = buscador.a_estrela(inicio, fim, mapa, nx, ny)
            if resultado:
                caminho, custo = resultado
        elif metodo == "aia_estrela":
            resultado = buscador.aia_estrela(inicio, fim, mapa, nx, ny)
            if resultado:
                caminho, custo = resultado
        else:
            return jsonify({"erro": "Método inválido"}), 400
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

    # Se o caminho foi encontrado
    if caminho:
        path_ids = [f"{chr(p[0] + 65)},{p[1]}" for p in caminho]  # Converte índices para coordenadas
        return jsonify({
            "path": path_ids,
            "custo": custo if custo is not None else len(caminho)  # Se não há custo, usa tamanho do caminho
        })

    return jsonify({"path": [], "custo": None})  # Caso não exista caminho

if __name__ == "__main__":
    app.run(debug=True)  # Executa servidor Flask
