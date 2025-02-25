import sys

def calcular_erro_percentual_arquivo(nome_arquivo, nome_arquivo_destino):
    total_porcentagens = 0
    num_inicializacoes = 0
    
    arquivo_log = open(nome_arquivo_destino, "a+", encoding="utf-8")

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        total_erros = 0
        total_acoes = 0

        for linha in arquivo:
            
            linha = linha.strip()

            if linha == "Nova partida!":
                # Se não for a primeira inicialização, processamos os dados coletados
                if total_acoes > 0:
                    erro_percentual = (total_erros / total_acoes) * 100
                    arquivo_log.write(f"Inicialização {num_inicializacoes + 1}: {erro_percentual:.2f}% de ações erradas\n")
                    arquivo_log.write(f"Numero de ações: {total_acoes}\tNumero de erros: {total_erros}\n\n")
                    total_porcentagens += erro_percentual
                    num_inicializacoes += 1

                # Resetar contadores para a próxima inicialização
                total_erros = 0
                total_acoes = 0

            elif linha.startswith("[") and linha.endswith("]"):
                valores = list(map(int, linha[1:-1].split(", ")))  # Processa os valores diretamente
                total_erros += sum(valores)
                total_acoes += len(list(valores))  # Contar número de ações

        # Processa a última inicialização caso o arquivo não termine com "Nova partida!"
        if total_acoes > 0:
            erro_percentual = (total_erros / total_acoes) * 100
            arquivo_log.write(f"Inicialização {num_inicializacoes + 1}: {erro_percentual:.2f}% de ações erradas\n")
            arquivo_log.write(f"Numero de ações: {total_acoes}\tNumero de erros: {total_erros}\n\n")
            total_porcentagens += erro_percentual
            num_inicializacoes += 1

    # Calcula a média geral
    media_geral = total_porcentagens / num_inicializacoes if num_inicializacoes > 0 else 0
    arquivo_log.write(f"\nMédia geral: {media_geral:.2f}% de ações erradas")
    arquivo_log.write(f"Numero de inicializações encontradas: {num_inicializacoes}")

    arquivo_log.close()

if __name__ == "__main__": 
    num_experimento = sys.argv[1]
    arquivo = f"../../aaa_teste_acoes_erradas/{num_experimento}/escolhas_erradas_exp{num_experimento}.txt"  # Altere para o nome correto do seu arquivo
    arquivo_destino = f"../../aaa_teste_acoes_erradas/{num_experimento}/resultado_analise_escolhas_erradas_exp{num_experimento}.txt"
    calcular_erro_percentual_arquivo(arquivo, arquivo_destino)

