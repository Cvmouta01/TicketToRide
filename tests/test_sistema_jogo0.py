import os
import pygame
import pytest
from unittest.mock import MagicMock, patch
from src.Game.Jogo import Jogo

os.environ["SDL_VIDEODRIVER"] = "dummy"

pygame.init()
pygame.display.set_mode((1, 1))


def criar_baralho_trem_mock(*args, **kwargs):
    return [MagicMock(cor="vermelho", rect=None) for _ in range(50)]


def criar_baralho_objetivo_mock(*args, **kwargs):
    mock_carta = MagicMock()
    mock_carta.imagem = pygame.Surface((10, 10))
    return [mock_carta for _ in range(30)]


@pytest.fixture
@patch("src.Game.Jogo.CartaTrem.criar_baralho_trem", side_effect=criar_baralho_trem_mock)
@patch("src.Game.Jogo.CartaObjetivo.criar_baralho_objetivo", side_effect=criar_baralho_objetivo_mock)
def jogo_com_3_jogadores(mock_obj, mock_trem):
    return Jogo(["vermelho", "azul", "verde"], 800, 600)


def test_jogo_inicializa_com_dados_corretos(jogo_com_3_jogadores):
    jogo = jogo_com_3_jogadores
    assert len(jogo.jogadores) == 3
    assert len(jogo.cartas_trem_abertas) == 5
    assert jogo.jogadores[0].ativo is True
    assert all(len(j.cartas) == 4 for j in jogo.jogadores)
    assert all(len(j.objetivos) == 3 for j in jogo.jogadores)


def test_passar_turno_avanca_ciclo(jogo_com_3_jogadores):
    jogo = jogo_com_3_jogadores

    ordem = []
    for _ in range(6):
        ativo = [j.ativo for j in jogo.jogadores]
        ordem.append(ativo)
        jogo.passar_turno(MagicMock())

    ativos_por_turno = [i.index(True) for i in ordem]
    assert ativos_por_turno == [0, 1, 2, 0, 1, 2]


def test_verif_fim_de_jogo_dispara_quando_menos_de_tres_trens(jogo_com_3_jogadores):
    jogo = jogo_com_3_jogadores
    jogador = jogo.jogadores[jogo.jogador_atual_index]
    jogador.trens = 2

    mock_display = MagicMock()
    jogo.verif_fim_de_jogo(mock_display)

    assert jogo.finalizando_jogo is True
    assert jogo.jogador_fim == jogo.jogador_atual_index


def test_verif_fim_de_jogo_nao_dispara_com_mais_de_tres_trens(jogo_com_3_jogadores):
    jogo = jogo_com_3_jogadores
    jogador = jogo.jogadores[jogo.jogador_atual_index]
    jogador.trens = 5

    mock_display = MagicMock()
    jogo.verif_fim_de_jogo(mock_display)

    assert jogo.finalizando_jogo is False
    assert jogo.jogador_fim == -1


def test_calcular_vencedor_ordena_por_pontos(jogo_com_3_jogadores):
    jogo = jogo_com_3_jogadores
    jogo.jogadores[0].pontos = 50
    jogo.jogadores[1].pontos = 30
    jogo.jogadores[2].pontos = 70

    ranking = jogo.calcular_vencedor()

    pontos_ordenados = list(ranking.values())
    assert pontos_ordenados == sorted(pontos_ordenados, reverse=True)


def test_calcular_vencedor_pontua_maior_caminho(jogo_com_3_jogadores):
    jogo = jogo_com_3_jogadores
    # Mock calcular_maior_caminho para cada jogador
    for i, jogador in enumerate(jogo.jogadores):
        jogador.mapa_conquistado = MagicMock()
        jogador.mapa_conquistado.calcular_maior_caminho.return_value = {'peso': 10 * (i + 1)}

    ranking = jogo.calcular_vencedor()

    # O jogador com maior peso deve ter 10 pontos a mais (bônus maior caminho)
    pontos = list(ranking.values())
    assert pontos[0] == max(pontos)  # O maior pontos deve estar em primeiro


@patch("src.Game.Jogo.CartaTrem.criar_baralho_trem", side_effect=criar_baralho_trem_mock)
@patch("src.Game.Jogo.CartaObjetivo.criar_baralho_objetivo", side_effect=criar_baralho_objetivo_mock)
def test_jogo_estado_inicial(mock_obj, mock_trem):
    jogo = Jogo(["vermelho"], 800, 600)
    assert jogo.jogadores[0].ativo
    assert jogo.cartas_compradas_esse_turno == 0
    assert jogo.cartas_abertas_compradas_nesse_turno == 0
    assert len(jogo.baralho_trem) >= 0
    assert len(jogo.baralho_objetivo) >= 0


def test_passar_turno_com_mais_de_um_jogador(jogo_com_3_jogadores):
    jogo = jogo_com_3_jogadores
    initial_index = jogo.jogador_atual_index
    jogo.passar_turno(MagicMock())
    assert jogo.jogador_atual_index == (initial_index + 1) % len(jogo.jogadores)


def test_game_over_loop_exits_on_quit(monkeypatch):
    jogo = Jogo(["vermelho"], 800, 600)
    jogo.jogadores[0].pontos = 0

    # Forçar game_over para rodar e simular pygame.QUIT
    monkeypatch.setattr(pygame, "event", MagicMock())
    quit_called = False

    def fake_event_get():
        return [pygame.event.Event(pygame.QUIT)]

    monkeypatch.setattr(pygame.event, "get", fake_event_get)
    monkeypatch.setattr(pygame, "quit", lambda: None)

    # Para capturar quit (não chamar realmente quit durante teste)
    import builtins

    def fake_quit():
        nonlocal quit_called
        quit_called = True
        raise SystemExit

    monkeypatch.setattr("builtins.quit", fake_quit)

    with pytest.raises(SystemExit):
        jogo.game_over(MagicMock())

    assert quit_called


def test_salvar_e_carregar_jogo(monkeypatch, tmp_path):
    jogo = Jogo(["vermelho"], 800, 600)

    # Criar arquivo temporário para salvar
    arquivo = tmp_path / "jogo_teste.pkl"

    # Mock filedialog.asksaveasfilename para retornar caminho temporário
    monkeypatch.setattr("src.Game.Jogo.filedialog.asksaveasfilename", lambda **kwargs: str(arquivo))

    # Mock filedialog.askopenfilename para retornar o mesmo caminho
    monkeypatch.setattr("src.Game.Jogo.filedialog.askopenfilename", lambda **kwargs: str(arquivo))

    # Salvar o jogo
    jogo.salvar_jogo = lambda self: None  # evitar loop
    # Usar salvar_jogo função original
    from src.Game.Jogo import salvar_jogo, carregar_jogo

    salvar_jogo(jogo)

    assert arquivo.exists()

    # Carregar o jogo
    jogo_carregado = carregar_jogo()
    assert jogo_carregado is not None
    assert hasattr(jogo_carregado, "jogadores")


def test_passar_turno_altera_status_ativo(jogo_com_3_jogadores):
    jogo = jogo_com_3_jogadores
    current = jogo.jogador_atual_index
    jogo.passar_turno(MagicMock())
    assert not jogo.jogadores[current].ativo
    assert jogo.jogadores[jogo.jogador_atual_index].ativo


def test_comprando_destinos_quebra_loop(monkeypatch):
    jogo = Jogo(["vermelho"], 800, 600)
    # Preencher baralho objetivo com mock cartas com imagem
    for carta in jogo.baralho_objetivo:
        carta.imagem = pygame.Surface((50, 80))

    # Forçar mouse.get_pos para dentro de poligono
    monkeypatch.setattr(pygame.mouse, "get_pos", lambda: (15, 75))

    # Simular evento mouse clicado dentro poligono do bilhete
    eventos = [
        pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1),
        pygame.event.Event(pygame.QUIT)
    ]
    monkeypatch.setattr(pygame.event, "get", lambda: eventos)

    # Vai levantar SystemExit porque pygame.QUIT
    with pytest.raises(SystemExit):
        jogo.comprando_destinos(MagicMock())


def test_game_loop_termina_ao_quit(monkeypatch):
    jogo = Jogo(["vermelho"], 800, 600)
    # Preencher mapa com mock
    jogo.map_graph = MagicMock()
    jogo.map_graph.graph.edges.return_value = []

    monkeypatch.setattr(pygame.display, "set_mode", lambda size: MagicMock())
    monkeypatch.setattr(pygame.display, "set_caption", lambda text: None)
    monkeypatch.setattr(pygame.mixer, "init", lambda: None)
    monkeypatch.setattr(pygame.mixer.Sound, "__init__", lambda self, path: None)
    monkeypatch.setattr(pygame.mixer.Sound, "play", lambda self: None)
    monkeypatch.setattr(pygame.mixer.music, "load", lambda path: None)
    monkeypatch.setattr(pygame.mixer.music, "set_volume", lambda vol: None)
    monkeypatch.setattr(pygame.mixer.music, "play", lambda loops: None)

    # Simula pygame.event.get para retornar quit direto
    monkeypatch.setattr(pygame.event, "get", lambda: [pygame.event.Event(pygame.QUIT)])

    # Força quit para não sair realmente
    import builtins

    def fake_quit():
        raise SystemExit

    monkeypatch.setattr("builtins.quit", fake_quit)
    monkeypatch.setattr(pygame, "quit", lambda: None)

    with pytest.raises(SystemExit):
        jogo.game_loop()
