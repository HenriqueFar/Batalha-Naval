import random
import os
import sys
import time

# Cores ------------------------------------------------------------------------
class Cor:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    AZUL    = "\033[34m"
    CIANO   = "\033[36m"
    VERDE   = "\033[32m"
    AMARELO = "\033[33m"
    VERMELHO= "\033[31m"
    BRANCO  = "\033[97m"
    CINZA   = "\033[90m"
    MAGENTA = "\033[35m"

def c(texto, *estilos): #concatena as cores nas strings (pra deixar colorido)
    return "".join(estilos) + texto + Cor.RESET

#Constantes --------------------------------------------------------------------
TAMANHO     = 10
LINHAS      = "ABCDEFGHIJ"
AGUA        = "~"
NAVIO       = "O"
ACERTO      = "X"
FALHA       = "*"

NAVIOS = [("Porta-aviões", 5), ("Encouraçado", 4), ("Cruzador", 3), ("Submarino", 3), ("Destroyer", 2)]

# Utilitários --------------------------------------------------------------------
def limpar():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def pausar(msg="Pressione Enter para continuar..."):
    print(c(f"\n  {msg}", Cor.CINZA))
    input() #espera o enter

def titulo():
    limpar()
    print(c("""
  ╔══════════════════════════════════════════╗
  ║         B A T A L H A   N A V A L        ║
  ╚══════════════════════════════════════════╝
""", Cor.CIANO, Cor.BOLD))

def cabecalho(texto):
    print(c(f"\n  ── {texto} ──", Cor.AMARELO, Cor.BOLD))

# Tabuleiro --------------------------------------------------------------------
def criarTabuleiro():
    return [[AGUA] * TAMANHO for _ in range(TAMANHO)]

def padraoCoordenada(coord):
    coord = coord.strip().upper()
    if len(coord) < 2 or len(coord) > 3:
        return None, None #retorna None se a entrada do usuário for inválida
    letra = coord[0] #primeira posição da string
    numero = coord[1:] #segunda posição da string
    if letra not in LINHAS:
        return None, None
    if not numero.isdigit(): #verifica se a ssegunda casa é um dígito
        return None, None
    col = int(numero) - 1
    lin = LINHAS.index(letra)
    if col < 0 or col >= TAMANHO:
        return None, None
    return lin, col

def imprimirTabuleiro(tabuleiro, ocultar_navios=False, titulo_tab=""):
    mapa_cor = {
        AGUA:   c("~", Cor.AZUL),
        NAVIO:  c("O", Cor.VERDE, Cor.BOLD),
        ACERTO: c("X", Cor.VERMELHO, Cor.BOLD),
        FALHA:  c("*", Cor.AMARELO),
    }
    if titulo_tab:
        print(c(f"  {titulo_tab}", Cor.CIANO, Cor.BOLD))
    colunas = "  " + "".join(c(f" {i+1:2}", Cor.BRANCO) for i in range(TAMANHO))
    print(colunas)
    for i, linha in enumerate(tabuleiro):
        linha_str = c(f"  {LINHAS[i]} ", Cor.BRANCO)
        for celula in linha:
            if ocultar_navios and celula == NAVIO:
                simbolo = mapa_cor[AGUA]
            else:
                simbolo = mapa_cor.get(celula, celula)
            linha_str += f" {simbolo} "
        print(linha_str)
    print()

def imprimirDoisTabuleiros(tab_proprio, tab_adversario, nome_proprio, nome_adv):
    print()
    # cabeçalhos
    w = TAMANHO * 3 + 6
    titulo_p = c(f"  Seu tabuleiro ({nome_proprio})", Cor.VERDE, Cor.BOLD)
    titulo_a = c(f"  Tiro em ({nome_adv})", Cor.VERMELHO, Cor.BOLD)
    print(titulo_p + " " * (w - len(nome_proprio) - 20) + titulo_a)
    # numeros das colunas
    cols = "  " + "".join(c(f" {i+1:2}", Cor.BRANCO) for i in range(TAMANHO))
    print(cols + "      " + cols)
    # linhas
    mapa_cor = {
        AGUA:   c("~", Cor.AZUL),
        NAVIO:  c("O", Cor.VERDE, Cor.BOLD),
        ACERTO: c("X", Cor.VERMELHO, Cor.BOLD),
        FALHA:  c("*", Cor.AMARELO),
    }
    for i in range(TAMANHO):
        def formatar(tab, ocultar=False):
            s = c(f"  {LINHAS[i]} ", Cor.BRANCO)
            for celula in tab[i]:
                if ocultar and celula == NAVIO:
                    s += f" {mapa_cor[AGUA]} "
                else:
                    s += f" {mapa_cor.get(celula, celula)} "
            return s
        print(formatar(tab_proprio) + "   " + formatar(tab_adversario, ocultar=True))
    print()

# ----- posicionamento --------------------------------
def _posicoesNavio(lin, col, tamanho, orientacao):
    posicoes = []
    for i in range(tamanho):
        r = lin + (i if orientacao == "V" else 0)
        c_ = col + (i if orientacao == "H" else 0)
        posicoes.append((r, c_))
    return posicoes

def validarPosicionamento(tabuleiro, lin, col, tamanho, orientacao):
    posicoes = _posicoesNavio(lin, col, tamanho, orientacao)
    for r, c_ in posicoes:
        if r < 0 or r >= TAMANHO or c_ < 0 or c_ >= TAMANHO:
            return False, "fora do tabuleiro."
        if tabuleiro[r][c_] == NAVIO:
            return False, "sobreposição"
    return True, ""

def colocarNavio(tabuleiro, lin, col, tamanho, orientacao):
    for r, c_ in _posicoesNavio(lin, col, tamanho, orientacao):
        tabuleiro[r][c_] = NAVIO

def posicionarNaviosAuto(tabuleiro):
    for _, tamanho in NAVIOS: #o "_" significa que o valor existe mas não vai ser usado
        colocado = False
        while not colocado:
            orientacao = random.choice(["H", "V"])
            lin = random.randint(0, TAMANHO - 1)
            col = random.randint(0, TAMANHO - 1)
            ok, _ = validarPosicionamento(tabuleiro, lin, col, tamanho, orientacao)
            if ok:
                colocarNavio(tabuleiro, lin, col, tamanho, orientacao)
                colocado = True

def posicionarNaviosManual(tabuleiro, nome_jogador):
    for nome_navio, tamanho in NAVIOS:
        while True:
            titulo()
            cabecalho(f"{nome_jogador} — Posicionar {nome_navio} (tamanho {tamanho})")
            imprimirTabuleiro(tabuleiro, titulo_tab="Seu tabuleiro:")
            coord_raw = input(c(f"  Coordenada inicial (ex: A1): ", Cor.BRANCO)).strip()
            lin, col = padraoCoordenada(coord_raw)
            if lin is None:
                print(c("  ✗ Coordenada inválida.", Cor.VERMELHO))
                time.sleep(1.2)
                continue
            ori_raw = input(c("  Orientação [H]orizontal / [V]ertical: ", Cor.BRANCO)).strip().upper()
            if ori_raw not in ("H", "V"):
                print(c("  ✗ Digite H ou V.", Cor.VERMELHO))
                time.sleep(1.2)
                continue
            ok, msg = validarPosicionamento(tabuleiro, lin, col, tamanho, ori_raw)
            if not ok:
                print(c(f"  ✗ {msg}", Cor.VERMELHO))
                time.sleep(1.2)
                continue
            colocarNavio(tabuleiro, lin, col, tamanho, ori_raw)
            break

def posicionarNavios(tabuleiro, nome_jogador):
    titulo()
    cabecalho(f"Posicionamento de navios — {nome_jogador}")
    print(c("\n  [1] Posicionar manualmente", Cor.BRANCO))
    print(c("  [2] Posicionamento automático", Cor.BRANCO))
    escolha = input(c("\n  Escolha: ", Cor.AMARELO)).strip()
    if escolha == "2":
        posicionarNaviosAuto(tabuleiro)
        titulo()
        cabecalho(f"{nome_jogador} — Navios posicionados automaticamente")
        imprimirTabuleiro(tabuleiro, titulo_tab="Seu tabuleiro:")
        pausar()
    else:
        posicionarNaviosManual(tabuleiro, nome_jogador)

# ------- mecanica de ataque ------------------------
def validarJogada(tabuleiro_ataques, lin, col):
    if lin is None or col is None:
        return False, "Coordenada inválida."
    if tabuleiro_ataques[lin][col] in (ACERTO, FALHA):
        return False, "Você já atacou essa posição."
    return True, ""

def realizarAtaque(tabuleiro_defesa, tabuleiro_ataques, lin, col):
    if tabuleiro_defesa[lin][col] == NAVIO:
        tabuleiro_defesa[lin][col] = ACERTO
        tabuleiro_ataques[lin][col] = ACERTO
        return "acerto"
    else:
        tabuleiro_defesa[lin][col] = FALHA
        tabuleiro_ataques[lin][col] = FALHA
        return "agua"

def verificarVitoria(tabuleiro):
    for linha in tabuleiro:
        if NAVIO in linha:
            return False
    return True

def contarNavios(tabuleiro):
    return sum(linha.count(NAVIO) for linha in tabuleiro)

# --------- Turno ----------------------
def turno(atacante, defensor, tab_defensor, tab_ataques_atacante, tab_proprio_atacante, jogadas):
    """executa um turno completo de quem ta atacando"""
    while True:
        titulo()
        print(c(f"  🎯  Vez de: {atacante}", Cor.AMARELO, Cor.BOLD))
        navios_restantes = contarNavios(tab_defensor)
        print(c(f"  Navios restantes do {defensor}: {navios_restantes} células\n", Cor.CINZA))
        imprimirDoisTabuleiros(tab_proprio_atacante, tab_ataques_atacante, atacante, defensor)

        coord_raw = input(c("  Coordenada de ataque (ex: B7): ", Cor.BRANCO)).strip()
        lin, col = padraoCoordenada(coord_raw)
        ok, msg = validarJogada(tab_ataques_atacante, lin, col)
        if not ok:
            print(c(f"\n  ✗ {msg}", Cor.VERMELHO))
            time.sleep(1.4)
            continue

        resultado = realizarAtaque(tab_defensor, tab_ataques_atacante, lin, col)
        jogadas[0] += 1

        titulo()
        if resultado == "acerto":
            print(c(f"\n  💥  ACERTO em {coord_raw.upper()}!", Cor.VERMELHO, Cor.BOLD))
        else:
            print(c(f"\n  💧  ÁGUA em {coord_raw.upper()}.", Cor.AZUL))

        imprimirDoisTabuleiros(tab_proprio_atacante, tab_ataques_atacante, atacante, defensor)
        pausar()
        break

# ------ Tela de vitória --------------------
def telaVitoria(vencedor, total_jogadas):
    titulo()
    print(c("""
  ╔══════════════════════════════════════════╗
  ║                 VITÓRIA!                 ║
  ╚══════════════════════════════════════════╝
""", Cor.AMARELO, Cor.BOLD))
    print(c(f"  Parabéns, {vencedor}!", Cor.VERDE, Cor.BOLD))
    print(c(f"  Todos os navios adversários foram destruídos.", Cor.BRANCO))
    print(c(f"  Total de jogadas: {total_jogadas}", Cor.CIANO))
    print()

# ------ Menu principal -------------------------
def menuPrincipal():
    titulo()
    print(c("  Bem-vindo ao Batalha Naval!", Cor.BRANCO, Cor.BOLD))
    print()
    print(c("  [1] Novo jogo", Cor.VERDE))
    print(c("  [2] Regras", Cor.CIANO))
    print(c("  [0] Sair", Cor.CINZA))
    return input(c("\n  Escolha: ", Cor.AMARELO)).strip()

def exibirRegras():
    titulo()
    cabecalho("Regras")
    print(c("""
  • Cada jogador possui um tabuleiro 10x10.
  • Os navios são posicionados antes da partida.
  • Os jogadores se alternam atacando coordenadas
    do adversário (ex: A1, B5, J10).
  • 💥 ACERTO  — o navio foi atingido.
  • 💧 ÁGUA    — tiro na água.
  • Vence quem destruir todos os navios do adversário.

  Navios disponíveis:
    Porta-aviões  ▬▬▬▬▬  (5 células)
    Encouraçado   ▬▬▬▬   (4 células)
    Cruzador      ▬▬▬    (3 células)
    Submarino     ▬▬▬    (3 células)
    Destroyer     ▬▬     (2 células)

  Legenda do tabuleiro:
    ~  Água       O  Navio       X  Acerto    *  Tiro na água
""", Cor.BRANCO))
    pausar()

def coletarNomes():
    titulo()
    cabecalho("Nome dos jogadores")
    j1 = input(c("  Nome do Jogador 1: ", Cor.VERDE)).strip() or "Jogador 1"
    j2 = input(c("  Nome do Jogador 2: ", Cor.CIANO)).strip() or "Jogador 2"
    return j1, j2

def transicaoEntreJogadores(proximo):
    limpar()
    print(c(f"""
  ┌─────────────────────────────────────┐
  │  Passe o dispositivo para {proximo:<12}│
  │  Pressione Enter quando estiver     │
  │  pronto.                            │
  └─────────────────────────────────────┘
""", Cor.MAGENTA, Cor.BOLD))
    input()

# ---- loop principal ------------------------------------------------------
def jogar():
    nome1, nome2 = coletarNomes()

    # tabuleiros de defesa (onde os navios estão)
    tab1 = criarTabuleiro()
    tab2 = criarTabuleiro()
    # tabuleiros de jogo, o que cada jogador vê do adversário
    ataques1 = criarTabuleiro()  # ataques do jogador 1
    ataques2 = criarTabuleiro()  # ataques do jogador 2

    # posicionamento
    posicionarNavios(tab1, nome1)
    transicaoEntreJogadores(nome2)
    posicionarNavios(tab2, nome2)

    jogadas = [0]
    jogador_atual = 0

    nomes    = [nome1, nome2]
    defesas  = [tab1, tab2]
    ataques  = [ataques1, ataques2]

    while True:
        atk  = jogador_atual
        dfs = 1 - jogador_atual

        transicaoEntreJogadores(nomes[atk])

        turno(
            atacante=nomes[atk],
            defensor=nomes[dfs],
            tab_defensor=defesas[dfs],
            tab_ataques_atacante=ataques[atk],
            tab_proprio_atacante=defesas[atk],
            jogadas=jogadas,
        )

        if verificarVitoria(defesas[dsf]):
            telaVitoria(nomes[atk], jogadas[0])
            break

        jogador_atual = dfs   # alterna turno

# ----Ponto de entrada ---------------
def main():
    while True:
        escolha = menuPrincipal()
        if escolha == "1":
            jogar()
            pausar("Pressione Enter para voltar ao menu...")
        elif escolha == "2":
            exibirRegras()
        elif escolha == "0":
            limpar()
            print(c("  Até logo! ⚓\n", Cor.CIANO))
            sys.exit(0)

if __name__ == "__main__":
    main()
