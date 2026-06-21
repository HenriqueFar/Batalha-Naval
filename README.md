   BATALHA NAVAL — README / INSTRUÇÕES DE JOGO
==================================================

SOBRE O JOGO

Versão em Python, para terminal, do clássico jogo Batalha Naval,
para 2 jogadores no mesmo computador (modo "passa e joga").
Cada jogador posiciona sua frota em um tabuleiro 10x10 e os dois
se revezam tentando afundar os navios do adversário.


REQUISITOS

- Python 3 instalado (versão 3.6 ou superior).
- Terminal/console que suporte cores ANSI:
    * Linux e macOS: funciona normalmente no terminal padrão.
    * Windows: use o Windows Terminal, ou o PowerShell/CMD mais
      recentes (Windows 10/11 já suportam cores ANSI). Se as
      cores aparecerem como códigos estranhos (ex: "\033[34m"),
      tente rodar pelo Windows Terminal.


COMO RODAR

1. Abra o terminal (Prompt de Comando, PowerShell, Terminal do
   Linux/Mac, etc).
2. Navegue até a pasta onde está o arquivo do jogo, por exemplo:
       cd caminho/para/a/pasta
3. Execute o comando:
       python3 batalha_naval.py
   (no Windows pode ser apenas "python batalha_naval.py")


COMO JOGAR

1. No menu principal, escolha:
     [1] Novo jogo  — inicia uma nova partida
     [2] Regras     — mostra as regras na tela
     [0] Sair        — encerra o programa

2. Digite o nome dos dois jogadores quando solicitado.

3. POSICIONAMENTO DOS NAVIOS
   Cada jogador, na sua vez, escolhe como posicionar a frota:
     [1] Manualmente: você informa a coordenada inicial de cada
         navio (ex: A1) e a orientação (H para horizontal ou
         V para vertical). O jogo avisa se a posição for
         inválida (fora do tabuleiro ou sobre outro navio).
     [2] Automático: o jogo posiciona todos os navios de forma
         aleatória para você.

   Quantidade de navios de cada jogador:
     Porta-aviões  - 5 células
     Encouraçado   - 4 células
     Cruzador      - 3 células
     Submarino     - 3 células
     Destroyer     - 2 células

   IMPORTANTE: como o jogo é "passa e joga" no mesmo computador,
   quando for a vez do outro jogador posicionar a frota, o jogo
   pede para passar o dispositivo e pressionar Enter — assim o
   jogador 1 não vê onde o jogador 2 colocou os navios.

4. ATAQUES
   Os jogadores se revezam atacando coordenadas do tabuleiro do
   adversário, digitando algo como: A1, B7, J10.
     - 💥 ACERTO  -> o ataque atingiu um navio inimigo.
     - 💧 ÁGUA    -> o ataque não atingiu nada.

   Não é possível atacar a mesma coordenada duas vezes.

5. VITÓRIA
   Vence o jogador que afundar todos os navios do adversário
   primeiro (ou seja, acertar todas as células de navio do
   oponente).


LEGENDA DO TABULEIRO

   ~   Água (sem navio, sem ataque ali ainda)
   O   Navio (só aparece no seu próprio tabuleiro)
   X   Acerto (navio atingido)
   *   Tiro na água


DICAS

- As coordenadas seguem o padrão LETRA + NÚMERO, onde a letra
  vai de A a J (linha) e o número de 1 a 10 (coluna). Exemplo:
  A1 é o canto superior esquerdo, J10 é o canto inferior direito.
- Durante a partida, cada jogador só vê seu próprio tabuleiro
  completo e o tabuleiro de ataques (onde já atirou) contra o
  adversário — os navios do oponente ficam ocultos até serem
  atingidos.
- Se o terminal não estiver exibindo cores corretamente, isso
  não afeta a jogabilidade, só a aparência visual.


Feito por - Enzo, Henrique e Kenzo
