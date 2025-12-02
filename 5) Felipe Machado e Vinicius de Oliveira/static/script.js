// Mapa carregado do backend, e dimensões nx (linhas) e ny (colunas)
let mapa = [], nx = 0, ny = 0;

// Cores usadas para os caminhos de cada destino
const cores = ["text-red-500", "text-green-500", "text-blue-500"];

// Quantidade atual de dropdowns de destino
let endNodeCount = 1;

// Carrega o mapa e os dados iniciais vindos da API
async function carregarDados() {
  const dados = await (await fetch("/api/dados")).json();
  mapa = dados.mapa; 
  nx = dados.nx; 
  ny = dados.ny;

  // Preenche o dropdown de métodos de busca
  const methodSel = document.getElementById("searchMethod");
  dados.methods.forEach(m => methodSel.innerHTML += `<option>${m}</option>`);

  // Preenche os possíveis pontos de início (somente células livres = 0)
  const startSel = document.getElementById("startNode");
  for (let i = 0; i < nx; i++) {
    for (let j = 0; j < ny; j++) {
      if (mapa[i][j] !== 0) continue; 
      const valor = `${String.fromCharCode(65 + i)},${j}`;
      startSel.innerHTML += `<option value="${valor}">${valor}</option>`;
    }
  }

  resetEndNodes();
  renderGrid();

  // Controle da exibição do limite quando o método for busca limitada
  document.getElementById("searchMethod").addEventListener("change", () => {
    const metodo = document.getElementById("searchMethod").value;
    const labelLimite = document.getElementById("labelLimite");
    const inputLimite = document.getElementById("inputLimite");

    if (metodo === "limitada") {
      labelLimite.classList.remove("hidden");
      inputLimite.classList.remove("hidden");
    } else {
      labelLimite.classList.add("hidden");
      inputLimite.classList.add("hidden");
    }
  });
}

// Reseta os dropdowns de destinos e recria o primeiro
function resetEndNodes() {
  endNodeCount = 1;
  const container = document.getElementById("endNodesContainer");
  container.innerHTML = "";
  adicionarDropdownDestino(1);

  // Botão para adicionar novos destinos (até 3)
  const addButton = document.createElement("button");
  addButton.id = "addEndNode";
  addButton.innerHTML = "+";
  addButton.className = "px-2 py-1 bg-green-500 text-white rounded";
  addButton.type = "button";
  container.appendChild(addButton);

  // Adiciona mais dropdowns quando clicado
  addButton.addEventListener("click", () => {
    if (endNodeCount < 3) {
      endNodeCount++;
      adicionarDropdownDestino(endNodeCount);
      if (endNodeCount === 3) addButton.style.display = "none";
    }
  });
}

// Cria um dropdown de destino (somente células com valor 2, que são máquinas)
function adicionarDropdownDestino(index) {
  const container = document.getElementById("endNodesContainer");
  const divWrapper = document.createElement("div");
  divWrapper.className = "flex flex-col items-center gap-1 relative";

  const select = document.createElement("select");
  select.id = `endNode${index}`;
  select.className = "p-2 border rounded";

  // Preenche com as posições das máquinas
  for (let i = 0; i < nx; i++) {
    for (let j = 0; j < ny; j++) {
      if (mapa[i][j] !== 2) continue;
      const valor = `${String.fromCharCode(65 + i)},${j}`;
      select.innerHTML += `<option value="${valor}">${valor}</option>`;
    }
  }

  // Botão de remover o destino (não aparece no primeiro)
  const removeButton = document.createElement("button");
  removeButton.innerHTML = "−";
  removeButton.className =
    "w-6 h-6 flex justify-center items-center rounded-full bg-red-500 text-white hover:bg-red-600 transition-colors duration-200 shadow";
  removeButton.type = "button";
  removeButton.title = "Remover destino";

  removeButton.addEventListener("click", () => {
    divWrapper.remove();
    endNodeCount--;
    document.getElementById("addEndNode").style.display = "inline-block";
  });

  divWrapper.appendChild(select);
  if (index > 1) divWrapper.appendChild(removeButton);
  container.insertBefore(divWrapper, document.getElementById("addEndNode"));
}

// Renderiza o grid com paredes, máquinas, início, destinos e setas de caminhos
function renderGrid(caminhos = []) {
  const gridContainer = document.getElementById("grid");
  gridContainer.innerHTML = "";
  gridContainer.style.gridTemplateColumns = `40px repeat(${ny}, 40px)`;

  // Mapas auxiliares para direcionamento das setas e marcações de destino
  const dirMap = {}, destinosFinais = {};

  // Processa cada caminho encontrado
  caminhos.forEach(({ path }, idx) => {
    const cor = cores[idx];

    // Gera as setas de direção entre cada par de nós
    for (let k = 0; k < path.length - 1; k++) {
      const [letra1, num1] = path[k].split(",");
      const [letra2, num2] = path[k + 1].split(",");
      const i = letra1.charCodeAt(0) - 65, j = parseInt(num1);

      let dir = i < letra2.charCodeAt(0) - 65 ? "down" :
                i > letra2.charCodeAt(0) - 65 ? "up" :
                j < parseInt(num2) ? "right" : "left";

      dirMap[`${i},${j}`] = dirMap[`${i},${j}`] || [];
      dirMap[`${i},${j}`].push({ cor, dir });
    }

    // Marca o destino final com cor específica
    const [destLetra, destNum] = path[path.length - 1].split(",");
    destinosFinais[`${destLetra.charCodeAt(0) - 65},${parseInt(destNum)}`] = cores[idx];
  });

  // Cabeçalho das colunas
  gridContainer.appendChild(createHeaderCell(""));
  for (let j = 0; j < ny; j++) gridContainer.appendChild(createHeaderCell(j));

  // Renderização das células do grid
  for (let i = 0; i < nx; i++) {
    gridContainer.appendChild(createHeaderCell(String.fromCharCode(65 + i)));

    for (let j = 0; j < ny; j++) {
      const cell = document.createElement("div");
      cell.className = "w-10 h-10 border flex items-center justify-center relative";

      // Parede
      if (mapa[i][j] === 1) {
        cell.classList.add(
          "bg-neutral-800",
          "border-neutral-900",
          "shadow-[inset_0_0_10px_rgba(0,0,0,.8)]"
        );
      }

      // Máquina
      else if (mapa[i][j] === 2) {
        const maquina = document.createElement("div");
        maquina.className = `
          w-7 h-7 bg-yellow-400 border border-yellow-700
          rounded-md shadow-md flex items-center justify-center
          text-xs font-bold text-yellow-900
        `;
        maquina.innerText = "M";
        cell.appendChild(maquina);
        cell.classList.add("bg-neutral-200");
      }

      // Piso livre
      else {
        cell.classList.add("bg-neutral-100", "border-neutral-300");
      }

      // Indica o ponto de início
      if (document.getElementById("startNode").value === `${String.fromCharCode(65 + i)},${j}`) {
        const bolaInicio = document.createElement("div");
        bolaInicio.className =
          "rounded-full w-4 h-4 bg-black border-2 border-black shadow";
        cell.appendChild(bolaInicio);
      }

      // Indica um destino final colorido
      else if (destinosFinais[`${i},${j}`]) {
        const cor = destinosFinais[`${i},${j}`];
        const bola = document.createElement("div");
        bola.className = `
          rounded-full w-4 h-4 bg-white border-2 ${cor.replace("text-", "border-")}
          shadow
        `;
        cell.appendChild(bola);
      }

      // Exibe setas quando houver caminhos passando pela célula
      else if (dirMap[`${i},${j}`]) {
        const setaContainer = document.createElement("div");
        setaContainer.className = "flex flex-wrap justify-center items-center gap-0.5";

        dirMap[`${i},${j}`].forEach(({ cor, dir }) => {
          const seta = document.createElement("span");
          seta.innerHTML = getArrow(dir);
          seta.className = `${cor} text-sm font-bold drop-shadow`;
          setaContainer.appendChild(seta);
        });

        cell.appendChild(setaContainer);
      }

      gridContainer.appendChild(cell);
    }
  }
}

// Cria uma célula de cabeçalho (letras e números)
function createHeaderCell(text) {
  const cell = document.createElement("div");
  cell.className =
    "w-10 h-10 flex items-center justify-center font-bold bg-gray-200 border";
  cell.innerText = text;
  return cell;
}

// Retorna a seta correspondente à direção
function getArrow(dir) {
  return { up: "↑", down: "↓", left: "←", right: "→" }[dir] || "";
}

// Função que executa a busca do melhor caminho passando por até 3 destinos
async function buscarRota() {
  const start = document.getElementById("startNode").value;

  // Coleta os destinos selecionados
  const finais = Array.from(document.querySelectorAll("#endNodesContainer select"))
    .map(sel => sel.value)
    .filter(v => v);

  if (!finais.length) {
    document.getElementById("mensagemErro").innerText = "Selecione pelo menos um destino";
    return;
  }

  let inicio = start, caminhos = [], resultados = [];
  document.getElementById("mensagemErro").innerText = "";

  // Processa os destinos um por um, sempre indo ao mais próximo
  while (finais.length) {
    let melhorDestino = null, melhorCaminho = null, melhorCusto = null;

    for (let destino of finais) {
      let url = `/api/buscar?start=${inicio}&end=${destino}&method=${document.getElementById("searchMethod").value}`;
      if (document.getElementById("searchMethod").value === "limitada") {
        url += `&limite=${document.getElementById("inputLimite").value}`;
      }
      const res = await (await fetch(url)).json();

      if (res.erro && res.erro !== "") {
        document.getElementById("mensagemErro").innerText = res.erro;
        return;
      }

      // Seleciona o destino mais próximo do ponto atual
      if (res.path && (!melhorCaminho || res.path.length < melhorCaminho.length)) {
        melhorCaminho = res.path;
        melhorDestino = destino;
        melhorCusto = res.custo;
      }
    }

    if (!melhorCaminho) break;

    caminhos.push({ destino: melhorDestino, path: melhorCaminho });
    resultados.push({ destino: melhorDestino, caminho: melhorCaminho, custo: melhorCusto });

    inicio = melhorDestino;
    finais.splice(finais.indexOf(melhorDestino), 1);
  }

  // Renderiza o grid já com as rotas
  renderGrid(caminhos);

  // Exibe o resumo textual das rotas
  document.getElementById("pathOutput").innerHTML = resultados.map((r, i) => {
    return `
      <div class="mb-2 p-2 rounded shadow-sm flex flex-col gap-2 border-b border-gray-200 pb-2">
        <span class="font-bold ${cores[i]}">Destino ${r.destino}:</span>
        <span class="text-sm text-gray-500">Custo: ${r.custo}</span>
        <div>${r.caminho.map(n => `<span class="px-2 py-1 bg-gray-100 rounded">${n}</span>`).join(" → ")}</div>
      </div>
    `;
  }).join("");
}

// Inicializa carregando os dados do backend
carregarDados();
