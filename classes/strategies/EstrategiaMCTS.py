import numpy as np
import random


from classes.enum.TipoAcao import TipoAcao
from classes.enum.TipoTabela import TipoTabela
from classes.enum.TipoModeloAcao import TipoModeloAcao
from classes.model.CartaDistrito import CartaDistrito
from classes.model.CartaPersonagem import CartaPersonagem
from classes.strategies.Estrategia import Estrategia
from classes.model.Estado import Estado
from classes.model.Jogador import Jogador


class EstrategiaMCTS(Estrategia):
    def __init__(self, caminho_modelo: str, tipo_treino: int = 2, nome: str = 'MCTS'):
        super().__init__(nome)
        # Caminho inicial dos arquivos do modelo
        self.caminho_modelo: str = caminho_modelo
        # 0 - treino zerado, 1 - treino continuado a partir de modelo pré-existente, 2 - apenas teste
        self.tipo_treino: int = tipo_treino
        self.treino: bool = self.tipo_treino < 2
        self.modelos_mcts: list[list[np.ndarray]] = []
        self.modelos_historico: list[np.ndarray] = []
        if self.tipo_treino == 0:
            for tipo_modelo in TipoModeloAcao:
                self.modelos_mcts.append(self.inicializar_modelo_mcts(tipo_modelo.tamanho))
        else:
            self.modelos_mcts = self.ler_modelos()
        self.tipo_tabela: TipoTabela | None = None

    # Carrega os modelos a partir dos arquivos CSV
    def ler_modelos(self) -> list[list[np.ndarray]]:
        modelos_mcts = []
        for tipo_modelo in TipoModeloAcao:
            modelo = []
            for tipo_tabela in TipoTabela:
                a = np.genfromtxt(self.caminho_modelo + '/modelos_mcts/' + tipo_modelo.name + '/' + tipo_tabela.name + '.csv', delimiter=',')
                modelo.append(a)
            modelos_mcts.append(modelo)
        return modelos_mcts

    # Cria modelo MCTS (tabelas) preenchidas com um valor inicial
    @staticmethod
    def inicializar_modelo_mcts(qtd_acoes: int, valor_inicial: int = 1) -> list[np.ndarray]:
        modelo = []
        for tabela in TipoTabela:
            modelo.append(np.ones((tabela.tamanho, qtd_acoes * 2)) * valor_inicial)
        return modelo

    # Reinicia dados do histórico
    def iniciar_historico(self):
        self.modelos_historico = []
        for tipo_modelo in TipoModeloAcao:
            self.modelos_historico.append(self.inicializar_modelo_mcts(tipo_modelo.tamanho, 0))

    # Salva os modelos em arquivos CSV
    def salvar_modelos(self):
        for (modelo, tipo_modelo) in zip(self.modelos_mcts, TipoModeloAcao):
            for (i, tipo_tabela) in zip(modelo, TipoTabela):
                    np.savetxt(self.caminho_modelo + '/modelos_mcts/' + tipo_modelo.name + '/' + tipo_tabela.name + '.csv', i, delimiter=',', fmt='%7u')

    def modelo_mcts_escolha(self, qtd_opcoes: int, opcoes_disponiveis: np.ndarray) -> int:
        if self.treino:
            # Computar divisão proporcional
            divisao_proporcional = self.computar_divisao_proporcional(np.array(opcoes_disponiveis))
            # Escolher opção seguindo distribuição da divisão
            escolha = random.choices(range(0, qtd_opcoes), divisao_proporcional)[0]
            return escolha
        else:
            soma_colunas = np.sum(opcoes_disponiveis, axis=0)
            # Computar divisão proporcional com soma das colunas (considera apenas vitórias)
            divisao_proporcional = self.computar_divisao_proporcional(soma_colunas, 1, True)
            # Escolher opção seguindo distribuição da divisão
            escolha = random.choices(range(0, qtd_opcoes), divisao_proporcional)[0]
            return escolha

    # Estratégia usada na fase de escolha dos personagens
    def escolher_personagem(self, estado: Estado) -> int:
        tipo_modelo_acao = TipoModeloAcao.EscolherPersonagem
        if self.treino:
            # Tabela a ser treinada
            indice_linha_tabela = estado.converter_estado()[self.tipo_tabela.idx]
            linha_tabela = self.modelos_mcts[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for personagem in estado.tabuleiro.baralho_personagens:
                opcoes_disponiveis.append(linha_tabela[personagem.rank - 1])
            for personagem in estado.tabuleiro.baralho_personagens:
                opcoes_disponiveis.append(linha_tabela[personagem.rank - 1 + tipo_modelo_acao.tamanho])
            # Aplica modelo MCTS para escolha das opções dentre as opções disponíveis
            escolha = self.modelo_mcts_escolha(len(estado.tabuleiro.baralho_personagens), np.array(opcoes_disponiveis))
            # Salvar histórico das escolhas para acrescentar no modelo após resultado
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][estado.tabuleiro.baralho_personagens[escolha].rank-1] = 1
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][estado.tabuleiro.baralho_personagens[escolha].rank-1 + tipo_modelo_acao.tamanho] = 1
            return escolha
        else:
            # Converte estado e monta a consulta a partir de todas as tabelas individuais
            estado_vetor = estado.converter_estado()
            tabela_consulta = np.zeros((len(TipoTabela), tipo_modelo_acao.tamanho * 2))
            for i in range(len(TipoTabela)):
                tabela_consulta[i] = self.modelos_mcts[tipo_modelo_acao.idx][i][estado_vetor[i]]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for personagem in estado.tabuleiro.baralho_personagens:
                opcoes_disponiveis.append(tabela_consulta[:, personagem.rank - 1])
            opcoes_disponiveis = np.stack(opcoes_disponiveis, axis=1)
            return self.modelo_mcts_escolha(len(estado.tabuleiro.baralho_personagens), opcoes_disponiveis)

    # Estratégia usada na fase de escolha das ações no turno
    def escolher_acao(self, estado: Estado, acoes_disponiveis: list[TipoAcao]) -> int:
        tipo_modelo_acao = TipoModeloAcao.EscolherAcao
        if self.treino:
            # Tabela a ser treinada
            indice_linha_tabela = estado.converter_estado()[self.tipo_tabela.idx]
            linha_tabela = self.modelos_mcts[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for acao in acoes_disponiveis:
                opcoes_disponiveis.append(linha_tabela[acao.value])
            for acao in acoes_disponiveis:
                opcoes_disponiveis.append(linha_tabela[acao.value + tipo_modelo_acao.tamanho])
            # Aplica modelo MCTS para escolha das opções dentre as opções disponíveis
            escolha = self.modelo_mcts_escolha(len(acoes_disponiveis), np.array(opcoes_disponiveis))
            # Salvar histórico das escolhas para acrescentar no modelo após resultado
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][acoes_disponiveis[escolha].value] = 1
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][acoes_disponiveis[escolha].value + tipo_modelo_acao.tamanho] = 1
            return escolha
        else:
            # Converte estado e monta a consulta a partir de todas as tabelas individuais
            estado_vetor = estado.converter_estado()
            tabela_consulta = np.zeros((len(TipoTabela), tipo_modelo_acao.tamanho * 2))
            for i in range(len(TipoTabela)):
                tabela_consulta[i] = self.modelos_mcts[tipo_modelo_acao.idx][i][estado_vetor[i]]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for acao in acoes_disponiveis:
                opcoes_disponiveis.append(tabela_consulta[:, acao.value])
            opcoes_disponiveis = np.stack(opcoes_disponiveis, axis=1)
            return self.modelo_mcts_escolha(len(acoes_disponiveis), opcoes_disponiveis)

    # Estratégia usada na ação de coletar cartas
    def coletar_cartas(self, estado: Estado, cartas_compradas: list[CartaDistrito], qtd_cartas: int) -> int:
        tipo_modelo_acao = TipoModeloAcao.ColetarCartas
        if self.treino:
            # Tabela a ser treinada
            indice_linha_tabela = estado.converter_estado()[self.tipo_tabela.idx]
            linha_tabela = self.modelos_mcts[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for carta in cartas_compradas:
                opcoes_disponiveis.append(linha_tabela[carta.idx])
            for carta in cartas_compradas:
                opcoes_disponiveis.append(linha_tabela[carta.idx + tipo_modelo_acao.tamanho])
            # Aplica modelo MCTS para escolha das opções dentre as opções disponíveis
            escolha = self.modelo_mcts_escolha(len(cartas_compradas), np.array(opcoes_disponiveis))
            # Salvar histórico das escolhas para acrescentar no modelo após resultado
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][cartas_compradas[escolha].idx] = 1
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][cartas_compradas[escolha].idx + tipo_modelo_acao.tamanho] = 1
            return escolha
        else:
            # Converte estado e monta a consulta a partir de todas as tabelas individuais
            estado_vetor = estado.converter_estado()
            tabela_consulta = np.zeros((len(TipoTabela), tipo_modelo_acao.tamanho * 2))
            for i in range(len(TipoTabela)):
                tabela_consulta[i] = self.modelos_mcts[tipo_modelo_acao.idx][i][estado_vetor[i]]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for carta in cartas_compradas:
                opcoes_disponiveis.append(tabela_consulta[:, carta.idx])
            opcoes_disponiveis = np.stack(opcoes_disponiveis, axis=1)
            return self.modelo_mcts_escolha(len(cartas_compradas), opcoes_disponiveis)

    # Estratégia usada na ação de construir distritos
    def construir_distrito(self, estado: Estado,
                           distritos_para_construir: list[CartaDistrito],
                           distritos_para_construir_covil_ladroes: list[(CartaDistrito, int, int)]) -> int:
        tipo_modelo_acao = TipoModeloAcao.ConstruirDistrito
        tem_opcoes_covil = 0
        if len(distritos_para_construir_covil_ladroes) > 0:
            tem_opcoes_covil = 1
        if self.treino:
            # Tabela a ser treinada
            indice_linha_tabela = estado.converter_estado()[self.tipo_tabela.idx]
            linha_tabela = self.modelos_mcts[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for carta in distritos_para_construir:
                opcoes_disponiveis.append(linha_tabela[carta.idx])
            if tem_opcoes_covil:
                opcoes_disponiveis.append(linha_tabela[tipo_modelo_acao.tamanho - 1])
            for carta in distritos_para_construir:
                opcoes_disponiveis.append(linha_tabela[carta.idx + tipo_modelo_acao.tamanho])
            if tem_opcoes_covil:
                opcoes_disponiveis.append(linha_tabela[tipo_modelo_acao.tamanho - 1 + tipo_modelo_acao.tamanho])
            # Aplica modelo MCTS para escolha das opções dentre as opções disponíveis
            escolha = self.modelo_mcts_escolha(len(distritos_para_construir) + tem_opcoes_covil, np.array(opcoes_disponiveis))
            # Escolheu contruir com habilidade do covil - será escolhido uma opção aleatória das disponíveis dentro dessa opção
            if escolha == len(distritos_para_construir):
                escolha = random.randint(0, len(distritos_para_construir_covil_ladroes) - 1) + len(distritos_para_construir)
                # Salvar histórico das escolhas para acrescentar no modelo após resultado
                self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][tipo_modelo_acao.tamanho - 1] = 1
                self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][tipo_modelo_acao.tamanho - 1 + tipo_modelo_acao.tamanho] = 1
            else:
                # Salvar histórico das escolhas para acrescentar no modelo após resultado
                self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][distritos_para_construir[escolha].idx] = 1
                self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][distritos_para_construir[escolha].idx + tipo_modelo_acao.tamanho] = 1
            return escolha
        else:
            # Converte estado e monta a consulta a partir de todas as tabelas individuais
            estado_vetor = estado.converter_estado()
            tabela_consulta = np.zeros((len(TipoTabela), tipo_modelo_acao.tamanho * 2))
            for i in range(len(TipoTabela)):
                tabela_consulta[i] = self.modelos_mcts[tipo_modelo_acao.idx][i][estado_vetor[i]]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for carta in distritos_para_construir:
                opcoes_disponiveis.append(tabela_consulta[:, carta.idx])
            if tem_opcoes_covil:
                opcoes_disponiveis.append(tabela_consulta[:, tipo_modelo_acao.tamanho - 1])
            opcoes_disponiveis = np.stack(opcoes_disponiveis, axis=1)
            escolha = self.modelo_mcts_escolha(len(distritos_para_construir) + tem_opcoes_covil, opcoes_disponiveis)
            # Escolheu contruir com habilidade do covil - será escolhido uma opção aleatória das disponíveis dentro dessa opção
            if escolha == len(distritos_para_construir):
                escolha = random.randint(0, len(distritos_para_construir_covil_ladroes) - 1) + len(distritos_para_construir)
            return escolha

    # Estratégia usada na ação de construir distritos (efeito Covil dos Ladrões)
    def construir_distrito_covil_dos_ladroes(self, estado: Estado, qtd_cartas: int, i: int) -> int:
        tipo_modelo_acao = TipoModeloAcao.ConstruirDistritoCovilDosLadroes
        if self.treino:
            # Tabela a ser treinada
            indice_linha_tabela = estado.converter_estado()[self.tipo_tabela.idx]
            linha_tabela = self.modelos_mcts[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for carta in estado.jogador_atual.cartas_distrito_mao:
                opcoes_disponiveis.append(linha_tabela[carta.idx])
            for carta in estado.jogador_atual.cartas_distrito_mao:
                opcoes_disponiveis.append(linha_tabela[carta.idx + tipo_modelo_acao.tamanho])
            # Aplica modelo MCTS para escolha das opções dentre as opções disponíveis
            escolha = self.modelo_mcts_escolha(len(estado.jogador_atual.cartas_distrito_mao), np.array(opcoes_disponiveis))
            # Salvar histórico das escolhas para acrescentar no modelo após resultado
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][estado.jogador_atual.cartas_distrito_mao[escolha].idx] = 1
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][estado.jogador_atual.cartas_distrito_mao[escolha].idx + tipo_modelo_acao.tamanho] = 1
            return escolha
        else:
            # Converte estado e monta a consulta a partir de todas as tabelas individuais
            estado_vetor = estado.converter_estado()
            tabela_consulta = np.zeros((len(TipoTabela), tipo_modelo_acao.tamanho * 2))
            for i in range(len(TipoTabela)):
                tabela_consulta[i] = self.modelos_mcts[tipo_modelo_acao.idx][i][estado_vetor[i]]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for carta in estado.jogador_atual.cartas_distrito_mao:
                opcoes_disponiveis.append(tabela_consulta[:, carta.idx])
            opcoes_disponiveis = np.stack(opcoes_disponiveis, axis=1)
            return self.modelo_mcts_escolha(len(estado.jogador_atual.cartas_distrito_mao), np.array(opcoes_disponiveis))

    # Estratégia usada na habilidade da Assassina
    def habilidade_assassina(self, estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        tipo_modelo_acao = TipoModeloAcao.HabilidadeAssassina
        if self.treino:
            # Tabela a ser treinada
            indice_linha_tabela = estado.converter_estado()[self.tipo_tabela.idx]
            linha_tabela = self.modelos_mcts[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for personagem in opcoes_personagem:
                opcoes_disponiveis.append(linha_tabela[personagem.rank - 1])
            for personagem in opcoes_personagem:
                opcoes_disponiveis.append(linha_tabela[personagem.rank - 1 + tipo_modelo_acao.tamanho])
            # Aplica modelo MCTS para escolha das opções dentre as opções disponíveis
            escolha = self.modelo_mcts_escolha(len(opcoes_personagem), np.array(opcoes_disponiveis))
            # Salvar histórico das escolhas para acrescentar no modelo após resultado
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][opcoes_personagem[escolha].rank-1] = 1
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][opcoes_personagem[escolha].rank-1 + tipo_modelo_acao.tamanho] = 1
            return escolha
        else:
            # Converte estado e monta a consulta a partir de todas as tabelas individuais
            estado_vetor = estado.converter_estado()
            tabela_consulta = np.zeros((len(TipoTabela), tipo_modelo_acao.tamanho * 2))
            for i in range(len(TipoTabela)):
                tabela_consulta[i] = self.modelos_mcts[tipo_modelo_acao.idx][i][estado_vetor[i]]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for personagem in opcoes_personagem:
                opcoes_disponiveis.append(tabela_consulta[:, personagem.rank - 1])
            opcoes_disponiveis = np.stack(opcoes_disponiveis, axis=1)
            return self.modelo_mcts_escolha(len(opcoes_personagem), opcoes_disponiveis)

    # Estratégia usada na habilidade do Ladrão
    def habilidade_ladrao(self, estado: Estado, opcoes_personagem: list[CartaPersonagem]) -> int:
        tipo_modelo_acao = TipoModeloAcao.HabilidadeLadrao
        if self.treino:
            # Tabela a ser treinada
            indice_linha_tabela = estado.converter_estado()[self.tipo_tabela.idx]
            linha_tabela = self.modelos_mcts[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for personagem in opcoes_personagem:
                opcoes_disponiveis.append(linha_tabela[personagem.rank - 1])
            for personagem in opcoes_personagem:
                opcoes_disponiveis.append(linha_tabela[personagem.rank - 1 + tipo_modelo_acao.tamanho])
            # Aplica modelo MCTS para escolha das opções dentre as opções disponíveis
            escolha = self.modelo_mcts_escolha(len(opcoes_personagem), np.array(opcoes_disponiveis))
            # Salvar histórico das escolhas para acrescentar no modelo após resultado
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][opcoes_personagem[escolha].rank-1] = 1
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][opcoes_personagem[escolha].rank-1 + tipo_modelo_acao.tamanho] = 1
            return escolha
        else:
            # Converte estado e monta a consulta a partir de todas as tabelas individuais
            estado_vetor = estado.converter_estado()
            tabela_consulta = np.zeros((len(TipoTabela), tipo_modelo_acao.tamanho * 2))
            for i in range(len(TipoTabela)):
                tabela_consulta[i] = self.modelos_mcts[tipo_modelo_acao.idx][i][estado_vetor[i]]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for personagem in opcoes_personagem:
                opcoes_disponiveis.append(tabela_consulta[:, personagem.rank - 1])
            opcoes_disponiveis = np.stack(opcoes_disponiveis, axis=1)
            return self.modelo_mcts_escolha(len(opcoes_personagem), opcoes_disponiveis)

    # Estratégia usada na habilidade da Ilusionista (escolha do jogador alvo)
    def habilidade_ilusionista_trocar(self, estado: Estado, opcoes_jogadores: list[Jogador]) -> int:
        # Abstrai jogador com maior pontuacao e jogador com mais cartas
        jogador_cartas = jogador_pontos = opcoes_jogadores[0]
        for jogador in opcoes_jogadores:
            if len(jogador.cartas_distrito_mao) > len(jogador_cartas.cartas_distrito_mao):
                jogador_cartas = jogador
            if jogador.pontuacao > jogador_pontos.pontuacao:
                jogador_pontos = jogador
        tipo_modelo_acao = TipoModeloAcao.HabilidadeIlusionistaTrocar
        if self.treino:
            # Tabela a ser treinada
            indice_linha_tabela = estado.converter_estado()[self.tipo_tabela.idx]
            linha_tabela = self.modelos_mcts[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela]
            # (0 - escolher jogador com mais cartas, 1 - escolher jogador com mais pontos dentre os que tem cartas na mão)
            opcoes_disponiveis = []
            for opcao in range(2):
                opcoes_disponiveis.append(linha_tabela[opcao])
            for opcao in range(2):
                opcoes_disponiveis.append(linha_tabela[opcao + tipo_modelo_acao.tamanho])
            # Aplica modelo MCTS para escolha das opções dentre as opções disponíveis
            escolha = self.modelo_mcts_escolha(2, np.array(opcoes_disponiveis))
            # Salvar histórico das escolhas para acrescentar no modelo após resultado
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][escolha] = 1
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][escolha + tipo_modelo_acao.tamanho] = 1
        else:
            # Converte estado e monta a consulta a partir de todas as tabelas individuais
            estado_vetor = estado.converter_estado()
            tabela_consulta = np.zeros((len(TipoTabela), tipo_modelo_acao.tamanho * 2))
            for i in range(len(TipoTabela)):
                tabela_consulta[i] = self.modelos_mcts[tipo_modelo_acao.idx][i][estado_vetor[i]]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for opcao in range(2):
                opcoes_disponiveis.append(tabela_consulta[:, opcao])
            opcoes_disponiveis = np.stack(opcoes_disponiveis, axis=1)
            escolha = self.modelo_mcts_escolha(2, opcoes_disponiveis)
        if escolha == 0:
            return opcoes_jogadores.index(jogador_cartas)
        else:
            return opcoes_jogadores.index(jogador_pontos)

    # Estratégia usada na habilidade da Ilusionista (escolha de quantas cartas serão descartadas)
    def habilidade_ilusionista_descartar_qtd_cartas(self, estado: Estado, qtd_maxima: int) -> int:
        tipo_modelo_acao = TipoModeloAcao.HabilidadeIlusionistaDescartarQtdCartas
        if qtd_maxima > 4:
            qtd_maxima = 4
        if self.treino:
            # Tabela a ser treinada
            indice_linha_tabela = estado.converter_estado()[self.tipo_tabela.idx]
            linha_tabela = self.modelos_mcts[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for qtd in range(1, qtd_maxima + 1):
                opcoes_disponiveis.append(linha_tabela[qtd_maxima - 1])
            for qtd in range(1, qtd_maxima + 1):
                opcoes_disponiveis.append(linha_tabela[qtd_maxima - 1 + tipo_modelo_acao.tamanho])
            # Aplica modelo MCTS para escolha das opções dentre as opções disponíveis
            escolha = self.modelo_mcts_escolha(qtd_maxima, np.array(opcoes_disponiveis))
            # Salvar histórico das escolhas para acrescentar no modelo após resultado
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][escolha-1] = 1
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][escolha-1 + tipo_modelo_acao.tamanho] = 1
            return escolha
        else:
            # Converte estado e monta a consulta a partir de todas as tabelas individuais
            estado_vetor = estado.converter_estado()
            tabela_consulta = np.zeros((len(TipoTabela), tipo_modelo_acao.tamanho * 2))
            for i in range(len(TipoTabela)):
                tabela_consulta[i] = self.modelos_mcts[tipo_modelo_acao.idx][i][estado_vetor[i]]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for qtd in range(1, qtd_maxima + 1):
                opcoes_disponiveis.append(tabela_consulta[:, qtd_maxima - 1])
            opcoes_disponiveis = np.stack(opcoes_disponiveis, axis=1)
            return self.modelo_mcts_escolha(qtd_maxima, opcoes_disponiveis)

    # Estratégia usada na habilidade da Ilusionista (escolha de qual carta descartar)
    def habilidade_ilusionista_descartar_carta(self, estado: Estado, qtd_cartas: int, i: int) -> int:
        tipo_modelo_acao = TipoModeloAcao.HabilidadeIlusionistaDescartarCarta
        if self.treino:
            # Tabela a ser treinada
            indice_linha_tabela = estado.converter_estado()[self.tipo_tabela.idx]
            linha_tabela = self.modelos_mcts[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for carta in estado.jogador_atual.cartas_distrito_mao:
                opcoes_disponiveis.append(linha_tabela[carta.idx])
            for carta in estado.jogador_atual.cartas_distrito_mao:
                opcoes_disponiveis.append(linha_tabela[carta.idx + tipo_modelo_acao.tamanho])
            # Aplica modelo MCTS para escolha das opções dentre as opções disponíveis
            escolha = self.modelo_mcts_escolha(len(estado.jogador_atual.cartas_distrito_mao), np.array(opcoes_disponiveis))
            # Salvar histórico das escolhas para acrescentar no modelo após resultado
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][estado.jogador_atual.cartas_distrito_mao[escolha].idx] = 1
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][estado.jogador_atual.cartas_distrito_mao[escolha].idx + tipo_modelo_acao.tamanho] = 1
            return escolha
        else:
            # Converte estado e monta a consulta a partir de todas as tabelas individuais
            estado_vetor = estado.converter_estado()
            tabela_consulta = np.zeros((len(TipoTabela), tipo_modelo_acao.tamanho * 2))
            for i in range(len(TipoTabela)):
                tabela_consulta[i] = self.modelos_mcts[tipo_modelo_acao.idx][i][estado_vetor[i]]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for carta in estado.jogador_atual.cartas_distrito_mao:
                opcoes_disponiveis.append(tabela_consulta[:, carta.idx])
            opcoes_disponiveis = np.stack(opcoes_disponiveis, axis=1)
            return self.modelo_mcts_escolha(len(estado.jogador_atual.cartas_distrito_mao), np.array(opcoes_disponiveis))

    # Estratégia usada na habilidade do Senhor da Guerra
    def habilidade_senhor_da_guerra_destruir(self, estado: Estado, distritos_para_destruir: list[(CartaDistrito, Jogador)]) -> int:
        tipo_modelo_acao = TipoModeloAcao.HabilidadeSenhorDaGuerraDestruir
        if self.treino:
            # Tabela a ser treinada
            indice_linha_tabela = estado.converter_estado()[self.tipo_tabela.idx]
            linha_tabela = self.modelos_mcts[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for (carta, _) in distritos_para_destruir:
                opcoes_disponiveis.append(linha_tabela[carta.idx])
            for (carta, _) in distritos_para_destruir:
                opcoes_disponiveis.append(linha_tabela[carta.idx + tipo_modelo_acao.tamanho])
            # Aplica modelo MCTS para escolha das opções dentre as opções disponíveis
            escolha = self.modelo_mcts_escolha(len(distritos_para_destruir), np.array(opcoes_disponiveis))
            # Salvar histórico das escolhas para acrescentar no modelo após resultado
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][distritos_para_destruir[escolha][0].idx] = 1
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][distritos_para_destruir[escolha][0].idx + tipo_modelo_acao.tamanho] = 1
            return escolha
        else:
            # Converte estado e monta a consulta a partir de todas as tabelas individuais
            estado_vetor = estado.converter_estado()
            tabela_consulta = np.zeros((len(TipoTabela), tipo_modelo_acao.tamanho * 2))
            for i in range(len(TipoTabela)):
                tabela_consulta[i] = self.modelos_mcts[tipo_modelo_acao.idx][i][estado_vetor[i]]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for (carta, _) in distritos_para_destruir:
                opcoes_disponiveis.append(tabela_consulta[:, carta.idx])
            opcoes_disponiveis = np.stack(opcoes_disponiveis, axis=1)
            return self.modelo_mcts_escolha(len(distritos_para_destruir), np.array(opcoes_disponiveis))

    # Estratégia usada na ação do Laboratório
    def laboratorio(self, estado: Estado) -> int:
        tipo_modelo_acao = TipoModeloAcao.Laboratorio
        if self.treino:
            # Tabela a ser treinada
            indice_linha_tabela = estado.converter_estado()[self.tipo_tabela.idx]
            linha_tabela = self.modelos_mcts[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for carta in estado.jogador_atual.cartas_distrito_mao:
                opcoes_disponiveis.append(linha_tabela[carta.idx])
            for carta in estado.jogador_atual.cartas_distrito_mao:
                opcoes_disponiveis.append(linha_tabela[carta.idx + tipo_modelo_acao.tamanho])
            # Aplica modelo MCTS para escolha das opções dentre as opções disponíveis
            escolha = self.modelo_mcts_escolha(len(estado.jogador_atual.cartas_distrito_mao), np.array(opcoes_disponiveis))
            # Salvar histórico das escolhas para acrescentar no modelo após resultado
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][estado.jogador_atual.cartas_distrito_mao[escolha].idx] = 1
            self.modelos_historico[tipo_modelo_acao.idx][self.tipo_tabela.idx][indice_linha_tabela][estado.jogador_atual.cartas_distrito_mao[escolha].idx + tipo_modelo_acao.tamanho] = 1
            return escolha
        else:
            # Converte estado e monta a consulta a partir de todas as tabelas individuais
            estado_vetor = estado.converter_estado()
            tabela_consulta = np.zeros((len(TipoTabela), tipo_modelo_acao.tamanho * 2))
            for i in range(len(TipoTabela)):
                tabela_consulta[i] = self.modelos_mcts[tipo_modelo_acao.idx][i][estado_vetor[i]]
            # Deixar apenas colunas das ações disponíveis no estado atual
            opcoes_disponiveis = []
            for carta in estado.jogador_atual.cartas_distrito_mao:
                opcoes_disponiveis.append(tabela_consulta[:, carta.idx])
            opcoes_disponiveis = np.stack(opcoes_disponiveis, axis=1)
            return self.modelo_mcts_escolha(len(estado.jogador_atual.cartas_distrito_mao), np.array(opcoes_disponiveis))

    # Computa divisão proporcional entre vitórias (diretamente) e quantidade de simulações (inversamente)
    @staticmethod
    def computar_divisao_proporcional(linha_tabela: np.ndarray, peso_explotacao: float = 1, apenas_vitorias: bool = False) -> list[float]:
        if apenas_vitorias:
            qtd_acoes = len(linha_tabela)
            divisao = np.zeros(qtd_acoes)
            total = 0
            for i in range(qtd_acoes):
                divisao[i] = linha_tabela[i] ** peso_explotacao
                total += divisao[i]
        else:
            qtd_acoes = int(len(linha_tabela)/2)
            divisao = np.zeros(qtd_acoes)
            total = 0
            for i in range(qtd_acoes):
                divisao[i] = linha_tabela[i] ** peso_explotacao / linha_tabela[i+qtd_acoes]
                total += divisao[i]
        return divisao/total
