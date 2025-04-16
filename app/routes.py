from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from .models import db, Despesa, User
import os
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

bp = Blueprint('main', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')

@bp.route('/')
def index():
    despesas = Despesa.query.order_by(Despesa.data_cadastro.desc()).all()
    return render_template('adminlte/dashboard.html', despesas=despesas)

@bp.route('/nova', methods=['GET', 'POST'])
def nova_despesa():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        data_vencimento = datetime.strptime(request.form['data_vencimento'], '%Y-%m-%d')
        data_execucao = request.form.get('data_execucao')
        data_execucao = datetime.strptime(data_execucao, '%Y-%m-%d') if data_execucao else None
        status = request.form['status']
        destino = request.form['destino']
        comprovante = request.files['comprovante']

        nome_arquivo = secure_filename(comprovante.filename)
        caminho_comprovante = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        comprovante.save(caminho_comprovante)

        despesa = Despesa(
            titulo=titulo,
            descricao=descricao,
            valor=valor,
            data_vencimento=data_vencimento,
            data_execucao=data_execucao,
            status=status,
            destino=destino,
            comprovante=nome_arquivo
        )
        db.session.add(despesa)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('adminlte/nova_despesa.html')

@bp.route('/comprovantes/<filename>')
def comprovante(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_despesa(id):
    despesa = Despesa.query.get_or_404(id)

    if request.method == 'POST':
        despesa.titulo = request.form['titulo']
        despesa.descricao = request.form['descricao']
        despesa.valor = float(request.form['valor'])
        despesa.data_vencimento = datetime.strptime(request.form['data_vencimento'], '%Y-%m-%d')
        data_execucao = request.form.get('data_execucao')
        despesa.data_execucao = datetime.strptime(data_execucao, '%Y-%m-%d') if data_execucao else None
        despesa.status = request.form['status']
        despesa.destino = request.form['destino']

        novo_comprovante = request.files.get('comprovante')
        if novo_comprovante and novo_comprovante.filename:
            nome_arquivo = secure_filename(novo_comprovante.filename)
            caminho_comprovante = os.path.join(UPLOAD_FOLDER, nome_arquivo)
            novo_comprovante.save(caminho_comprovante)
            despesa.comprovante = nome_arquivo

        db.session.commit()
        flash('Despesa atualizada com sucesso!', 'success')
        return redirect(url_for('main.index'))

    return render_template('adminlte/editar_despesa.html', despesa=despesa)

@bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_despesa(id):
    despesa = Despesa.query.get_or_404(id)
    db.session.delete(despesa)
    db.session.commit()
    flash('Despesa excluída com sucesso!', 'success')
    return redirect(url_for('main.index'))



@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.senha, senha):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Usuário ou senha inválidos', 'danger')

    return render_template('adminlte/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))