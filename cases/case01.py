"""
# Caso de Teste 01 - Sistema de Cadastro de Usuário

Um sistema para permitir a criação e armazenamento de Usuários

## Regras de Negócio

- RN01: Todos os usuários devem possuir nome, email e senha;
- RN02: O email deve conter o caractere @;
- RN03: A senha deve ter, no mínimo, 6 caracteres;
- RN04: Não é permitido cadastrar dois usuário com o mesmo email.

## Requisitos Funcionais

- RF01: O sistema deve permitir cadastrar um usuário;
- RF02: O sistema deve validar se o email é válido;
- RF03: O sistema deve impedir cadastro de email duplicado;
- RF04: O sistema deve lançar uma exceção em caso de uma falha.

## Diagrama de classes UML

[Class] Usuario
+ nome: str
+ email: str
- senha: str

[Class] UsuarioService
+ cadastrar(nome: str, email: str, senha: str) -> Usuario

## Erros Mapeados

- E01: Não valida nome vazio;
- E02: Valida email apenas como string não vazia;
- E03: Não valida tamanho mínimo da senha;
- E04: Não verifica email duplicado.
"""


from typing import List


class User:
    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password


class UserService:
    def __init__(self):
        self._users: List[User] = []

    def register(self, name: str, email: str, password: str) -> User:
        # Não valida nome vazio

        if not email:  # Valida email apenas como string como não vazia
            raise "Erro: email obrigatório"

        # Não valida tamanho mínimo da senha

        user = User(name, email, password)
        self._users.append(user)  # Não verifica email duplicado

        return user