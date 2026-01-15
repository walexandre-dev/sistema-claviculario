from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
from fpdf import FPDF

# --- Configuração Inicial ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_muito_secreta_123' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Configuração do Login ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redireciona para cá se não estiver logado

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# --- MODELOS ---
class Usuario(UserMixin, db.Model):
    # UserMixin adiciona métodos padrão: is_authenticated, etc.
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False) # Em produção, usar hash!
    tipo = db.Column(db.String(20)) # 'Admin' ou 'Comum'

class Chave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Disponivel')

class Movimentacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chave_id = db.Column(db.Integer, db.ForeignKey('chave.id'))
    usuario_nome = db.Column(db.String(100))
    data_retirada = db.Column(db.DateTime, default=datetime.now)
    data_devolucao = db.Column(db.DateTime, nullable=True)
    chave = db.relationship('Chave', backref=db.backref('movimentacoes', lazy=True))

# --- ROTAS ---
@app.route('/')
@login_required
def index():
    # 1. Dados Básicos
    chaves = Chave.query.all()
    movimentacoes_ativas = {
        m.chave_id: m.usuario_nome 
        for m in Movimentacao.query.filter_by(data_devolucao=None).all()
    }

    # 2. Lógica de Filtro de Histórico
    data_inicio_str = request.args.get('data_inicio')
    data_fim_str = request.args.get('data_fim')
    
    query = Movimentacao.query.order_by(Movimentacao.data_retirada.desc())

    if data_inicio_str and data_fim_str:
        try:
            # Converter string para objeto datetime
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d')
            # Ajuste para pegar o dia final completo (até 23:59:59)
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d') + timedelta(days=1)
            
            # Aplica o filtro
            query = query.filter(Movimentacao.data_retirada >= data_inicio, Movimentacao.data_retirada < data_fim)
            historico = query.all() # Traz tudo no intervalo
            tab_ativa = 'historico' # Força a aba histórico a abrir
        except ValueError:
            # Caso dê erro na conversão, volta ao padrão
            historico = query.limit(5).all()
            tab_ativa = 'chaves'
    else:
        # Padrão: Últimos 5 registros
        historico = query.limit(5).all()
        # Se não filtrou, abre na aba principal
        tab_ativa = 'chaves' 

    return render_template('index.html', 
                           chaves=chaves, 
                           historico=historico, 
                           mov_ativas=movimentacoes_ativas, 
                           usuario=current_user,
                           tab_ativa=tab_ativa) # Passamos essa variável nova

#--- AUTENTICAÇÃO ---
#Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        user = Usuario.query.filter_by(email=email).first()
        
        if user and user.senha == senha:
            login_user(user)
            flash(f'Bem-vindo, {user.nome}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login inválido. Verifique e-mail e senha.', 'danger')
            
    return render_template('login.html')

#Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('login'))

#--- CONFIGURAÇÃO INICIAL DO BANCO ---
# Rota para criar o banco e usuários iniciais
@app.route('/setup')
def setup():
    db.create_all()
    
    # Cria Usuários Padrão se não existirem
    if not Usuario.query.filter_by(email='admin@escola.com').first():
        admin = Usuario(nome="Administrador", email="admin@escola.com", senha="123", tipo="Admin")
        user = Usuario(nome="João Silva", email="joao@escola.com", senha="123", tipo="Comum")
        db.session.add(admin)
        db.session.add(user)

    # Cria Chaves Padrão se não existirem
    if not Chave.query.first():
        chaves = [
            Chave(nome="Sala 101", status="Disponivel"),
            Chave(nome="Lab Info", status="Disponivel"),
            Chave(nome="Auditório", status="Disponivel")
        ]
        db.session.add_all(chaves)
    
    db.session.commit()
    return "Banco resetado! <br>Login Admin: admin@escola.com / 123 <br>Login Comum: joao@escola.com / 123"

#--- CADASTRO DE NOVO USUÁRIO ---
# Rota para cadastrar novo usuário (Apenas Admin)
@app.route('/usuarios/novo', methods=['GET', 'POST'])
@login_required
def novo_usuario():
    # 1. Segurança: Apenas Admin pode acessar
    if current_user.tipo != 'Admin':
        flash('Acesso negado. Apenas administradores podem cadastrar usuários.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo') # Vai receber 'Admin' ou 'Comum'

        # 2. Validação: E-mail já existe?
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Erro: Já existe um usuário com este e-mail.', 'danger')
            return redirect(url_for('novo_usuario'))

        # 3. Criar Usuário
        novo_user = Usuario(nome=nome, email=email, senha=senha, tipo=tipo)
        db.session.add(novo_user)
        db.session.commit()

        flash(f'Usuário {nome} cadastrado com sucesso!', 'success')
        return redirect(url_for('index')) # Ou redirecionar para uma lista de usuários

    return render_template('cadastro_usuario.html')


#--- LÓGICA DE RETIRADA E DEVOLUÇÃO ---
@app.route('/retirar/<int:chave_id>', methods=['POST'])
@login_required
def retirar(chave_id):
    chave = Chave.query.get_or_404(chave_id)
    
    # Regra: Só pode retirar se estiver 100% disponível
    if chave.status == 'Disponivel':
        chave.status = 'Em Uso'
        nova_mov = Movimentacao(chave_id=chave.id, usuario_nome=current_user.nome)
        db.session.add(nova_mov)
        db.session.commit()
        flash('Chave retirada com sucesso!', 'success')
    else:
        flash('Chave indisponível para retirada.', 'danger')
    
    return redirect(url_for('index'))

@app.route('/devolver/<int:chave_id>', methods=['POST'])
@login_required
def devolver(chave_id):
    chave = Chave.query.get_or_404(chave_id)
    
    if chave.status == 'Em Uso':
        # LÓGICA DE BLOQUEIO / VALIDAÇÃO
        if current_user.tipo == 'Admin':
            # Admin devolve imediatamente
            chave.status = 'Disponivel'
            fechar_movimentacao(chave.id)
            flash('Devolução confirmada pelo Administrador.', 'success')
        else:
            # Utilizador comum coloca em estado de conferência
            chave.status = 'Pendente'
            flash('Devolução registada. Aguarde a conferência do Administrador.', 'warning')
        
        db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/confirmar/<int:chave_id>', methods=['POST'])
@login_required
def confirmar(chave_id):
    # Rota exclusiva para Admin finalizar a pendência
    if current_user.tipo != 'Admin':
        flash('Acesso negado.', 'danger')
        return redirect(url_for('index'))

    chave = Chave.query.get_or_404(chave_id)
    
    if chave.status == 'Pendente':
        chave.status = 'Disponivel'
        fechar_movimentacao(chave.id)
        flash('Conferência realizada. Chave disponível novamente.', 'success')
        db.session.commit()
        
    return redirect(url_for('index'))

def fechar_movimentacao(chave_id):
    """Função auxiliar para fechar o registo no histórico"""
    mov = Movimentacao.query.filter_by(chave_id=chave_id, data_devolucao=None).first()
    if mov:
        mov.data_devolucao = datetime.now()

#--- EXPORTAÇÃO PARA PDF ---
@app.route('/exportar_pdf')
@login_required
def exportar_pdf():
    # 1. Recuperar Filtros (Mesma lógica do index)
    data_inicio_str = request.args.get('data_inicio')
    data_fim_str = request.args.get('data_fim')
    
    query = Movimentacao.query.order_by(Movimentacao.data_retirada.desc())
    periodo_texto = "Histórico Completo"

    if data_inicio_str and data_fim_str:
        try:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d')
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d') + timedelta(days=1)
            query = query.filter(Movimentacao.data_retirada >= data_inicio, Movimentacao.data_retirada < data_fim)
            periodo_texto = f"Periodo: {datetime.strptime(data_inicio_str, '%Y-%m-%d').strftime('%d/%m/%Y')} a {datetime.strptime(data_fim_str, '%Y-%m-%d').strftime('%d/%m/%Y')}"
        except ValueError:
            pass
            
    movimentacoes = query.all()

    # 2. Configuração do PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Relatório de Movimentações - Claviculário", ln=True, align='C')
    
    # Subtítulo (Data)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')} | {periodo_texto}", ln=True, align='C')
    pdf.ln(10)

    # Cabeçalho da Tabela
    pdf.set_fill_color(200, 220, 255) # Azul claro
    pdf.set_font("Arial", style="B", size=10)
    pdf.cell(50, 10, "Chave", 1, 0, 'C', fill=True)
    pdf.cell(50, 10, "Usuário", 1, 0, 'C', fill=True)
    pdf.cell(45, 10, "Retirada", 1, 0, 'C', fill=True)
    pdf.cell(45, 10, "Devolução", 1, 1, 'C', fill=True)

    # Linhas da Tabela
    pdf.set_font("Arial", size=10)
    for mov in movimentacoes:
        # Tratamento de Strings (remove acentos bugados no FPDF simples)
        chave_nome = mov.chave.nome.encode('latin-1', 'ignore').decode('latin-1')
        usuario_nome = mov.usuario_nome.encode('latin-1', 'ignore').decode('latin-1')
        
        data_ret = mov.data_retirada.strftime('%d/%m %H:%M')
        data_dev = mov.data_devolucao.strftime('%d/%m %H:%M') if mov.data_devolucao else "EM ABERTO"
        
        pdf.cell(50, 10, chave_nome, 1)
        pdf.cell(50, 10, usuario_nome, 1)
        pdf.cell(45, 10, data_ret, 1, 0, 'C')
        pdf.cell(45, 10, data_dev, 1, 1, 'C')

    # 3. Retornar o arquivo
    from flask import make_response
    response = make_response(pdf.output(dest='S').encode('latin-1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=relatorio_chaves.pdf'
    return response

if __name__ == '__main__':
    app.run(debug=True)