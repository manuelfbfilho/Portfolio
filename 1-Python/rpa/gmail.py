from imbox import Imbox
import json

with open("credenciais_gmail.json", "r") as file:
    credenciais = json.loads(file.read())

email = credenciais["e-mail"]
senha = credenciais["password"]
servidor = credenciais["host"]

with Imbox(
    hostname=servidor,
    username=email,
    password=senha) as imb:

    mensagens = imb.messages()

    if not mensagens:
        print("Ocorreu um erro!")
        
    
    for uid, msg in mensagens:
        print(msg.subject)
        print(msg.sent_from[0]['email'])
        print(msg.body['html'][0])
        break


 
