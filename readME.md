# 🛒 API de Gerenciamento de Pedidos (FastAPI)

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

Uma API RESTful robusta desenvolvida com **FastAPI** e **SQLAlchemy** para o gerenciamento de usuários, produtos, itens e pedidos. O sistema conta com autenticação segura baseada em tokens JWT e controle de permissões de acesso (Administrador vs. Usuário Comum).

## 🚀 Funcionalidades

- **Autenticação e Segurança:**
    - Criação de contas de usuário com hash de senhas (`Bcrypt`).
    - Login e geração de Tokens `JWT` (Access e Refresh tokens).
    - Proteção de rotas baseada no token do usuário.
    - Controle de acesso por escopo (Admin vs. Usuário).
- **Gerenciamento de Pedidos:**
    - Criação de novos pedidos associados ao usuário logado.
    - Adição e remoção de itens dentro de um pedido com cálculo automático do valor total.
    - Fluxo de status (Criação, Finalização e Cancelamento).
    - Histórico de pedidos filtrado por dono da conta. (Usuários veem apenas seus pedidos; Admins veem todos).
- **Banco de Dados:**
    - Banco de dados SQLite pronto para uso local.
    - ORM `SQLAlchemy` com suporte a migrações via `Alembic`.
    - Relacionamentos Complexos (One-to-Many / Many-to-Many).

## 🛠️ Tecnologias Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/):** Framework web moderno e de alta performance.
- **[SQLAlchemy](https://www.sqlalchemy.org/):** ORM (Object Relational Mapper) para comunicação com o banco de dados.
- **[Pydantic](https://docs.pydantic.dev/):** Validação de dados e serialização.
- **[Passlib & Bcrypt](https://passlib.readthedocs.io/en/stable/lib/passlib.hash.bcrypt.html):** Criptografia segura de senhas.
- **[Python-JOSE](https://jose.authlib.org/en/guide/jwt/):** Geração e decodificação de JSON Web Tokens (JWT).
- **[SQLite](https://sqlite.org/):** Banco de dados relacional leve e embutido.

---

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

- [Python 3.9+](https://www.python.org/downloads/)
- Gerenciador de pacotes `pip`

---

## 💻 Instalação e Execução local

Siga o passo a passo abaixo para rodar o projeto na sua máquina:

### 1. Clone o repositório

```bash
git clone [https://github.com/VagnerKM/FastAPI.git](https://github.com/VagnerKM/FastAPI.git)
cd FastAPI
```

### 2. Crie e ative um ambiente virtual

**No Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**No Linux/macOS:**

```Bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias contidas no arquivo de requisitos:

```Bash
pip install -r requirements.txt
```

## 4. Configuração do Banco de Dados

Como o projeto utiliza o SQLite, o banco de dados deve ser gerado automaticamente na raiz do projeto durante a primeira execução da aplicação. Caso o projeto utilize Alembic para gerenciar as migrações, você deve rodar o seguinte comando antes de iniciar o servidor:

```Bash
alembic upgrade head
```

### 5. Execute o servidor localmente

Inicie a aplicação utilizando o Uvicorn:

```Bash
uvicorn main:app --reload
```

(Nota: Se o arquivo principal da aplicação estiver dentro de uma pasta, por exemplo, app, utilize uvicorn app.main:app --reload)

O servidor estará rodando em: http://127.0.0.1:8000

### 📖 Documentação da API (Swagger e ReDoc)

O FastAPI gera automaticamente a documentação interativa da sua API. Com o servidor rodando em sua máquina, você pode acessá-la e testar todos os endpoints diretamente pelo navegador:

Swagger UI: http://127.0.0.1:8000/docs (Interface interativa que permite realizar requisições de teste diretamente da página).

ReDoc: http://127.0.0.1:8000/redoc (Visualização limpa e focada na leitura da documentação técnica).

### 🔐 Testando a Autenticação (JWT)

Para testar as rotas protegidas (como a criação e listagem de pedidos), siga os passos abaixo usando o Swagger UI (/docs):

- **Criar um Usuário:** Utilize a rota de criação de usuários (POST) para registrar uma nova conta.

- **Fazer Login:** Acesse a rota de login (POST), insira as credenciais que acabou de criar e execute. Copie o token de acesso (access token) retornado na resposta.

- **Autorizar:** No canto superior direito da tela do Swagger, clique no botão verde "Authorize" 🔒. Cole o seu token no campo de texto e clique em Authorize.

Pronto! Agora o cabeçalho Authorization: Bearer <seu-token> será enviado automaticamente nas próximas requisições e você poderá interagir com as rotas de pedidos e itens de forma segura.

### 🤝 Como Contribuir

Faça um Fork deste repositório.

Crie uma branch com a sua funcionalidade:

```Bash
git checkout -b minha-feature
```

Commit suas alterações:

```Bash
git commit -m 'feat: adicionando nova funcionalidade x'
```

Faça o Push para a sua branch:

```Bash
git push origin minha-feature
```

Abra um Pull Request detalhando o que foi feito.

### 📝 Autor e Licença

Projeto desenvolvido e mantido por [VagnerKM](https://github.com/VagnerKM). Sinta-se à vontade para explorar, adaptar e utilizar este código para aprendizado ou projetos pessoais!
