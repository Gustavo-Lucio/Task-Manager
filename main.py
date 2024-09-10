from flask import render_template, redirect, url_for
from config import app, db
from models import load_user, User
from flask_login import login_required, login_user, logout_user, current_user


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    from forms import RegisterForm
    from werkzeug.security import generate_password_hash

    formulario = RegisterForm()

    if formulario.validate_on_submit():
        usu = formulario.username.data
        sen = generate_password_hash(formulario.password.data)
        # print(f'{usu} - {sen}')

        usuBanco = User.query.filter_by(usuario=usu).first()
        if usuBanco:
            print('usuario ja existe')
        else:
            novoUsuario = User(usuario=usu, senha=sen)
            db.session.add(novoUsuario)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('register.html', form=formulario)


@app.route('/login', methods=['GET', 'POST'])
def login():
    from forms import LoginForm
    from werkzeug.security import check_password_hash

    formulario = LoginForm()

    if formulario.validate_on_submit():
        usu = formulario.username.data
        usuBanco = User.query.filter_by(usuario=usu).first()

        if usuBanco:
            sen = formulario.password.data
            senhaHash = usuBanco.senha

            if check_password_hash(senhaHash, sen):
                login_user(usuBanco)
                return redirect(url_for('dashboard'))
            # else:
            #    print('erro')

    return render_template('login.html', form=formulario)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    from models import Event
    todos_eventos = Event.query.all()  # Recupera todos os eventos
    meus_eventos = Event.query.filter_by(user_id=current_user.id).all()  # Recupera os eventos do usuário logado

    return render_template('dashboard.html', todos_eventos=todos_eventos, meus_eventos=meus_eventos)


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    from forms import EventForm
    from models import Event
    formulario = EventForm()  # Instancie o formulário

    if formulario.validate_on_submit():
        nome_evento = formulario.event_name.data
        data_evento = formulario.event_date.data
        descricao = formulario.description.data

        # Crie uma nova instância do modelo Event, associando o usuário atual
        novo_evento = Event(
            nome=nome_evento,
            data_evento=data_evento,
            descricao=descricao,
            user_id=current_user.id  # Associando o evento ao usuário logado
        )

        # Adicione o evento ao banco de dados
        db.session.add(novo_evento)
        db.session.commit()

        return redirect(url_for('dashboard'))  # Redireciona após criar o evento

    return render_template('create_event.html', form=formulario)


@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    from forms import EventForm
    from models import Event

    # Buscar o evento pelo ID
    evento = Event.query.get_or_404(event_id)

    if evento.user_id != current_user.id:
        return redirect(url_for('dashboard'))

    formulario = EventForm(obj=evento)

    if formulario.validate_on_submit():
        evento.nome = formulario.event_name.data
        evento.data_evento = formulario.event_date.data
        evento.descricao = formulario.description.data
        db.session.commit()
        return redirect(url_for('dashboard'))

    # Teste manual forçando os dados do formulário
    formulario.event_name.data = evento.nome
    formulario.event_date.data = evento.data_evento
    formulario.description.data = evento.descricao

    return render_template('edit_event.html', form=formulario)


@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    from models import Event

    # Buscar o evento pelo ID
    evento = Event.query.get_or_404(event_id)

    # Verificar se o usuário logado é o dono do evento
    if evento.user_id != current_user.id:
        return redirect(url_for('dashboard'))

    # Deletar o evento
    db.session.delete(evento)
    db.session.commit()

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)

"""
pip install flask, flask-wtf, 
flask_sqlalchemy, flask_login
"""
