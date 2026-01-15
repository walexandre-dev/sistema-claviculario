# 🔐 Sistema de Claviculário Digital

> **Status:** Protótipo Funcional (MVP)  
> **Tecnologia:** Python (Flask) + SQLite + Bootstrap 5

Este projeto é um protótipo de sistema web para gerenciamento e controle de chaves em ambientes corporativos ou educacionais. Ele substitui o livro de papel por um controle digital seguro, permitindo rastrear quem retirou cada chave, quando e garantir que a devolução foi conferida.

---

## 🚀 Funcionalidades Principais

* **Dashboard Visual:** Status das chaves em tempo real (Disponível 🟢, Em Uso 🔴, Aguardando Conferência 🟡).
* **Controle de Acesso:**
    * **Administrador:** Gerencia usuários, cadastra chaves e confirma devoluções.
    * **Usuário Comum:** Apenas retira e solicita devolução.
* **Fluxo de Segurança:** Devoluções feitas por usuários comuns ficam como "Pendentes" até a validação física de um administrador.
* **Histórico e Relatórios:**
    * Log completo de retiradas e devoluções.
    * Filtro por período de datas.
    * **Exportação para PDF** com um clique.
* **Gestão de Usuários:** Cadastro de novos usuários com níveis de permissão (apenas Admin).
* **Interface Responsiva:** Funciona em Desktop e Mobile (Bootstrap 5).

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3, Flask, Flask-SQLAlchemy (ORM), Flask-Login (Auth).
* **Frontend:** HTML5, Jinja2, Bootstrap 5 (UI), FontAwesome (Ícones).
* **Banco de Dados:** SQLite (Arquivo local `banco.db`).
* **Relatórios:** FPDF (Geração de PDF).

---

## 📦 Como Instalar e Rodar

### Pré-requisitos
* Python 3.x instalado.

### Passo a Passo

1.  **Clone ou baixe o projeto:**
    ```bash
    git clone [https://github.com/seu-usuario/claviculario-digital.git](https://github.com/seu-usuario/claviculario-digital.git)
    cd claviculario-digital
    ```

2.  **Crie um ambiente virtual (Opcional, mas recomendado):**
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install flask flask-sqlalchemy flask-login fpdf
    ```

4.  **Execute o servidor:**
    ```bash
    python app.py
    ```

5.  **Configuração Inicial (Primeira Execução):**
    Abra o navegador e acesse a rota de configuração para criar o banco de dados e usuários padrão:
    * Acesse: `http://127.0.0.1:5000/setup`

---

## 👤 Como Usar (Logins Padrão)

Após rodar o setup, o sistema cria automaticamente dois usuários para teste:

| Nível | E-mail | Senha | Funcionalidades |
| :--- | :--- | :--- | :--- |
| **Administrador** | `admin@escola.com` | `123` | Acesso total, confirmar devolução, criar usuários. |
| **Funcionário** | `joao@escola.com` | `123` | Retirar chaves, solicitar devolução. |

---

## 📂 Estrutura do Projeto

```text
claviculario_app/
│
├── app.py                # Lógica principal (Rotas, Models, Config)
├── banco.db              # Banco de dados (gerado automaticamente)
│
└── templates/            # Telas do sistema (HTML)
    ├── base.html         # Layout base (Menu e Rodapé)
    ├── index.html        # Dashboard e Histórico
    ├── login.html        # Tela de Login
    └── cadastro_usuario.html # Tela de Cadastro (Admin)