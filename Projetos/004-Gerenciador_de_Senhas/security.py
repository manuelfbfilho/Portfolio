import secrets
import string

def verificar_senha_fraca(senha: str, senhas_cadastradas: list) -> bool:
    """Verifica se uma senha é fraca com base em critérios de segurança."""
    if len(senha) < 8:
        return True
    if senha.islower() or senha.isupper():
        return True
    if not any(char.isdigit() for char in senha):
        return True
    if senha.isalnum():
        return True
    if senha in senhas_cadastradas:
        return True
    return False

def gerar_senha_forte(tamanho=12):
    """Gera uma senha forte."""
    caracteres = string.ascii_letters + string.digits + string.punctuation
    while True:
        senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
        if (any(c.islower() for c in senha) and
            any(c.isupper() for c in senha) and
            any(c.isdigit() for c in senha) and
            any(c in string.punctuation for c in senha)):
            return senha
