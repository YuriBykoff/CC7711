from chatbot import ChatBot
from colorama import init, Fore, Style
import os  # Importa a biblioteca os para limpar o terminal

# Inicializar o colorama
init()

myChatBot = ChatBot()

# Apenas carregar um modelo pronto
myChatBot.load_model()

# Limpar o histórico do chat (terminal) e inserir quebras de linha
os.system('cls' if os.name == 'nt' else 'clear')
print("\n\n")  # Duas quebras de linha para melhor espaçamento

print(Fore.GREEN + "Bem vindo ao Chatbot" + Style.RESET_ALL)

pergunta = input(Fore.CYAN + "Como posso te ajudar? " + Style.RESET_ALL)
resposta, intencao = myChatBot.chatbot_response(pergunta)
print(Fore.YELLOW + resposta + "   [" + intencao[0]['intent'] + "]" + Style.RESET_ALL)

while intencao[0]['intent'] != "despedida":
    pergunta = input(Fore.CYAN + "Posso lhe ajudar com algo a mais? " + Style.RESET_ALL)
    resposta, intencao = myChatBot.chatbot_response(pergunta)
    print(Fore.YELLOW + resposta + "   [" + intencao[0]['intent'] + "]" + Style.RESET_ALL)

print(Fore.GREEN + "Foi um prazer atender você" + Style.RESET_ALL)
