# Escolha 1 - Seleção de Personagem:
personagens = ["Assassina", "Ladrão", "Mago", "Rei", "Cardeal", "Alquimista", "Navegador", "Senhor da Guerra"]
habilidades = ["Assassinato", "Roubo", "Magia", "Nobreza", "Imposto", "Transmutação", "Pirataria", "Guerra"]
a=0
print("Escolha um personagem: ")
for i in personagens:
    a+=1
    print(f"{a}- {i}")
Personagem=int(input())
print(f"Voce escolheu: {personagens[Personagem-1]}\n\n")

# Escolha 2 - "Ação de Compra":
print('''Escolha sua próxima ação:
1- Pegue duas cartas e escolha uma;
2- Pegue duas moedas''')
escolha=["Pegue duas cartas e escolha uma","Pegar duas moedas"]
y=int(input())
print(f"Você escolheu {escolha[y-1]}")

# Escolha 3 - Contrução de Distrito:


# Escolha 4 - Habilidade do Personagem:

print(f"Voce executou a habilidade: {habilidades[Personagem -1]}")