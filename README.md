# 🔐 Sistema de Claviculário Digital Inteligente

> **Status:** Protótipo Funcional (v2.0)  
> **Stack:** Python (Flask) | Bootstrap 5 | SQLite

Um sistema web moderno e responsivo para o controle seguro de chaves em ambientes corporativos, escolares ou laboratoriais. O projeto foca em **Experiência do Usuário (UX)** fluida e regras de negócio seguras para rastreabilidade total de quem retirou e devolveu cada chave.

---

## 🚀 Funcionalidades

### 🛡️ Gestão e Segurança
* **Controle de Acesso (RBAC):** Níveis de permissão distintos para **Administradores** e **Usuários Comuns**.
* **Fluxo de Validação:** Usuários comuns solicitam a devolução, mas a chave entra em estado **"Pendente"** 🟡 até que um Administrador confirme o recebimento físico.
* **Gestão de Usuários:** Administradores podem cadastrar novos membros com níveis de acesso específicos.
* **Gestão de Chaves:** Cadastro e Exclusão de chaves (com trava de segurança: não é possível excluir chaves em uso).

### 💻 Interface e UX (User Experience)
* **Transições Fluidas:** Navegação entre páginas sem "piscar" (Fade In/Out e Slide Up).
* **Notificações Modernas (Toasts):** Avisos flutuantes com temporizador visual e desaparecimento automático, sem interromper o layout.
* **Dashboard Visual:** Cards coloridos indicando status instantâneo (Disponível 🟢, Em Uso 🔴, Pendente 🟡).
* **Busca em Tempo Real:** Filtragem de chaves sem recarregar a página.

### 📊 Relatórios
* **Histórico Detalhado:** Registro imutável de quem pegou, hora da retirada e hora da devolução.
* **Filtros de Data:** Busca por períodos específicos.
* **Exportação PDF:** Geração automática de relatórios formatados para impressão/arquivamento.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3, Flask.
* **Banco de Dados:** SQLite (com SQLAlchemy ORM).
* **Autenticação:** Flask-Login (Gestão de sessões e cookies).
* **Frontend:** HTML5, CSS3, JavaScript Vanilla.
* **Framework CSS:** Bootstrap 5.3 (Responsividade).
* **Relatórios:** FPDF (Geração de arquivos PDF).

---

## 📦 Instalação e Execução

### Pré-requisitos
* Python 3.x instalado.
* Git instalado.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/sistema-claviculario.git](https://github.com/SEU-USUARIO/sistema-claviculario.git)
    cd sistema-claviculario
    ```

2.  **Crie um ambiente virtual (Recomendado):**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Caso não tenha o arquivo, instale manualmente: `pip install flask flask-sqlalchemy flask-login fpdf`)*

4.  **Inicie o servidor:**
    ```bash
    python app.py
    ```

5.  **Configuração Inicial (Banco de Dados):**
    Abra o navegador e acesse a rota de setup para criar o banco e os usuários padrão:
    * 🔗 `http://127.0.0.1:5000/setup`

---

## 👤 Acesso ao Sistema (Logins Padrão)

Após rodar o setup, utilize as credenciais abaixo:

| Nível | E-mail | Senha | Permissões |
| :--- | :--- | :--- | :--- |
| **Administrador** | `admin@escola.com` | `123` | Total (Cadastros, Exclusões, Confirmações, PDF) |
| **Funcionário** | `joao@escola.com` | `123` | Básica (Retirar e Solicitar Devolução) |

---

## 📂 Estrutura do Projeto

```text
/
├── app.py                # Núcleo da aplicação (Rotas e Models)
├── banco.db              # Banco de dados SQLite (gerado no setup)
├── requirements.txt      # Lista de dependências
├── .gitignore            # Arquivos ignorados pelo Git
│
└── templates/            # Frontend
    ├── base.html         # Layout mestre (Navbar, Scripts, CSS de Transição)
    ├── index.html        # Dashboard principal (Abas de Chaves e Histórico)
    ├── login.html        # Tela de acesso
    ├── cadastro_usuario.html # Formulário de novos usuários
    └── cadastro_chave.html   # Formulário de novas chaves
```

---

## 📸 Telas do Sistema

| Dashboard (Visão Geral) | Login e Segurança |
|:---:|:---:|
| ![Dashboard Principal](screenshots/dashboard.png) | ![Tela de Login](screenshots/login.png) |

> *O sistema conta com notificações flutuantes e transições suaves entre as telas.*

