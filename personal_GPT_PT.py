# Versão 1.0
# Data: 7 de abril de 2024
# ISENÇÃO DE RESPONSABILIDADE: Este script é fornecido "como está", sem garantia de qualquer tipo, expressa ou implícita, incluindo, mas não se limitando a, garantias de comercialização, adequação a um fim específico e não infração. Em nenhum caso os autores ou detentores dos direitos autorais serão responsáveis por qualquer reivindicação, danos ou outra responsabilidade, seja em uma ação de contrato, delito ou de outra forma, decorrente, fora de ou em conexão com o script ou o uso ou outras negociações no script.

import os
import openai
from pathlib import Path

def coletar_mensagens():
    mensagens = []
    # Instrução inicial do sistema para a IA
    instrucao_sistema = input("Por favor, defina o papel da IA, o contexto e a tarefa: ")
    mensagens.append({"role": "system", "content": instrucao_sistema})
    
    while True:
        entrada_usuario = input("Digite sua mensagem (ou digite 'fim' para terminar): ")
        if entrada_usuario.lower() == 'fim':
            break
        mensagens.append({"role": "user", "content": entrada_usuario})
    
    return mensagens

def salva_arquivo():
    while True:
        opcao = input("Deseja salvar os resultados em um arquivo .txt? (S / N) ").upper()
        if opcao not in ["S", "N"]:
            print("Digite apenas \"Y\" ou \"N\". Tente novamente.")
            continue
        if opcao == "S":
            print("O arquivo será salvo em seu diretório pessoal.")
            print("ATENÇÃO: Se já existir um arquivo com o mesmo nome, o arquivo anterior será substituído.")
            nomearquivo = input("IMPORTANTE: Não use espaços no nome do arquivo. Digite o nome do arquivo: ")
            return nomearquivo.lower()
        else:
            return None

os.system("cls" if os.name == "nt" else "clear")
# Solicita ao usuário por mensagens
mensagens = coletar_mensagens()
# Solicita ao usuário que salve os resultados em um arquivo
nomearquivo = salva_arquivo()
# Solicita ao usuário para escolher um modelo
try:
    modelo = input("Escolha um modelo: gpt-4-turbo-preview ou gpt-4 (padrão gpt-4): ")
except ValueError:
    modelo = "gpt-4" # Modelo padrão
# Garante que o modelo seja gpt-4-turbo-preview ou gpt-4
if modelo not in ["gpt-4-turbo-preview", "gpt-4"]:
    modelo = "gpt-4"
    print("Valor de modelo inválido. Definindo para o padrão (gpt-4).")
# Solicita ao usuário para definir a temperatura
try:
    temperatura = float(input("Defina a temperatura: 0.0 a 2.0 (padrão 0.5): "))
except ValueError:
    temperatura = 0.5  # Temperatura padrão
    print("Valor de temperatura inválido. Definindo para o padrão (0.5).")
# Garante que a temperatura esteja dentro do intervalo aceitável
if temperatura < 0.0 or temperatura > 2.0:
    temperatura = 0.5
    print("Valor de temperatura inválido. Definindo para o padrão (0.5).")
# Chave da API OpenAI (Substitua "your_api_key_here" pela sua verdadeira chave da API OpenAI)
openai.api_key = 'your_api_key_here'
try:
    # Chama a API OpenAI
    resposta = openai.chat.completions.create(
        model=modelo,
        messages=mensagens,
        temperature=temperatura,
        # max_tokens=100,
        timeout=200
    )
    # Exibe o resultado
    print("Resposta da IA:")
    print(resposta.choices[0].message.content)
except Exception as e:
    print(f"Ocorreu um erro: {e}")

if nomearquivo is not None:
    nome_arquivo = f"{nomearquivo}.txt"
    caminho_completo = Path.home() / nome_arquivo
    print("\n")
    try:
        with open(caminho_completo, "w") as resultado:
            resultado.write(resposta.choices[0].message.content)
        print(f"Resposta salva com sucesso em {caminho_completo}.")
    except Exception as e:
        print(f"Ocorreu um erro ao gravar o arquivo: {e}.")