from flask import render_template, flash, request, redirect, url_for, abort
from comunidadepostify import app, database, bcrypt
from comunidadepostify.forms import FormCriarConta, FormLogin, FormEditarPerfil, FormCriarPost, FormEditPost
from comunidadepostify.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image
import secrets, os
import cloudinary.uploader
import io

@app.route("/")
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)

@app.route('/contatos')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login_cadastro():
    if current_user.is_authenticated:
        flash('Você já está logado!', 'alert-info')
        return redirect(url_for('home'))

    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if request.method == 'POST':
    
        if "botao_submit_login" in request.form:
            if form_login.validate():
            
                usuario = Usuario.query.filter_by(email=form_login.email.data).first()
                if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
                    login_user(usuario, remember=form_login.lembrar_dados.data)
                    flash('Login realizado com sucesso', 'alert-success')
                    return redirect(url_for('home'))
                else:
                    flash('Falha no login: E-mail ou Senha incorretos.', 'alert-danger')

        elif "botao_submit_criarconta" in request.form:
            if form_criarconta.validate():
                
                try:
                    senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')

                    usuario = Usuario(
                        username=form_criarconta.username.data,
                        email=form_criarconta.email.data,
                        senha=senha_cript
                    )
                    database.session.add(usuario)
                    database.session.commit()

                    flash('Conta criada com sucesso!', 'alert-success')
                    return redirect(url_for('home'))

                except Exception as e:
                    database.session.rollback()
                    flash('Erro ao criar conta.', 'alert-danger')
        
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Você foi desconectado.', 'alert-success')
    return redirect(url_for('home'))
    

@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = current_user.foto_perfil
    return render_template('perfil.html', foto_perfil=foto_perfil)
    

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com suceso.', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


def salvar_imagem(imagem):
    # adicionar um código ao nome da imagem
    codigo = secrets.token_hex(8)
    nome, ext = os.path.splitext(imagem.filename)
    nome_imagem = nome + "_" + codigo + ext
    # reduzir tamanho da imagem
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # salvar imagem na pasta fotos_perfil
    buffer = io.BytesIO()
    imagem_reduzida.save(buffer, format=imagem_reduzida.format or 'PNG')
    buffer.seek(0)

    # upload para Cloudinary
    resultado = cloudinary.uploader.upload(
        buffer,
        public_id=nome_imagem
    )
    # retorna URL da imagem
    return resultado['secure_url']  

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    if len(lista_cursos) < 1:
        lista_cursos.append('Não informado')
    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form_edit = FormEditarPerfil()
    usuario_cursos = current_user.cursos.casefold().split(";")
    if request.method == 'GET':
        form_edit.email.data = current_user.email
        form_edit.username.data = current_user.username
    if form_edit.validate_on_submit():
        current_user.email = form_edit.email.data
        current_user.username = form_edit.username.data
        
        if form_edit.foto_perfil.data:
            nome_imagem = salvar_imagem(form_edit.foto_perfil.data)
            # mudar o campo foto_perfil do database para o novo nome da imagem
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form_edit)
        database.session.commit()
        flash('Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
   
    foto_perfil = current_user.foto_perfil
    return render_template('editar_perfil.html', foto_perfil=foto_perfil, form_edit=form_edit, usuario_cursos=usuario_cursos)

@app.route("/perfil/posts")
@login_required
def meus_posts():
    posts = Post.query.filter(Post.autor == current_user).order_by(Post.id.desc())
    foto_perfil = current_user.foto_perfil
    return render_template('meus_posts.html', foto_perfil=foto_perfil, posts=posts)

@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user == post.autor:
        form = FormEditPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            post.editado = True
            database.session.commit()
            flash('Post atualizado com sucesso!', 'alert-success')
            return redirect(url_for('home'))
    else:   
        form = None
    return render_template('post.html', post=post, form=form)



@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído com Sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)

@app.route("/usuario/<int:user_id>")
@login_required
def perfil_usuario(user_id):
    posts = Post.query.filter(Post.autor.has(id=user_id)).order_by(Post.id.desc())
    usuario = Usuario.query.get_or_404(user_id)
    foto_perfil = usuario.foto_perfil
    return render_template('perfil_usuarios.html', posts=posts, usuario=usuario, foto_perfil=foto_perfil)

@app.route('/termos')
def termos_uso():
    return render_template('termos.html')
