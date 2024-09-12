from flask import render_template, redirect, url_for, flash, request
from config import app, db
from models import load_user, User, Event
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

    status_filtro = request.args.get('status')  # Pegar o status do filtro (GET param)

    # Buscar eventos criados pelo usuário logado, filtrando por status se existir
    if status_filtro:
        meus_eventos = Event.query.filter_by(user_id=current_user.id, status=status_filtro).all()
    else:
        meus_eventos = Event.query.filter_by(user_id=current_user.id).all()

    # Buscar eventos criados pelo usuário logado
    meus_eventos = Event.query.filter_by(user_id=current_user.id).all()

    # Buscar eventos em que o usuário logado é participante
    eventos_participante = current_user.participated_events

    # Verificar se há eventos para exibir
    if not meus_eventos and not eventos_participante:
        flash('Você não tem eventos para mostrar.', 'info')

    return render_template('dashboard.html', meus_eventos=meus_eventos, eventos_participante=eventos_participante)




@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    from forms import EventForm
    from models import Event, User
    formulario = EventForm()

    usuarios = User.query.filter(User.id != current_user.id).all()
    formulario.participants.choices = [(user.id, user.usuario) for user in usuarios]

    if formulario.validate_on_submit():
        titulo = formulario.event_titulo.data
        status = formulario.event_status.data
        descricao = formulario.description.data

        print(f"Título: {titulo}, Status: {status}, Descrição: {descricao}")

        novo_evento = Event(
            titulo=titulo,
            status=status,
            descricao=descricao,
            user_id=current_user.id
        )

        participantes_selecionados = formulario.participants.data
        for user_id in participantes_selecionados:
            user = User.query.get(user_id)
            novo_evento.participants.append(user)

        db.session.add(novo_evento)
        db.session.commit()

        print("Evento criado com sucesso")
        return redirect(url_for('dashboard'))

    else:
        print(formulario.errors)

    return render_template('create_event.html', form=formulario)


@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    from forms import EventForm
    from models import Event, User

    evento = Event.query.get_or_404(event_id)

    if evento.user_id != current_user.id and current_user not in evento.participants:
        flash('Você não tem permissão para editar este evento.', 'danger')
        return redirect(url_for('dashboard'))

    formulario = EventForm(obj=evento)

    usuarios = User.query.filter(User.id != current_user.id).all()
    formulario.participants.choices = [(user.id, user.usuario) for user in usuarios]

    if request.method == 'GET':
        formulario.participants.data = [user.id for user in evento.participants]

    if formulario.validate_on_submit():
        evento.titulo = formulario.event_titulo.data
        evento.status = formulario.event_status.data
        evento.descricao = formulario.description.data

        participantes_selecionados = formulario.participants.data
        evento.participants = [User.query.get(user_id) for user_id in participantes_selecionados]

        db.session.commit()
        flash('Evento atualizado com sucesso!', 'success')
        return redirect(url_for('dashboard'))

    formulario.event_titulo.data = evento.titulo
    formulario.event_status.data = evento.status
    formulario.description.data = evento.descricao

    return render_template('edit_event.html', form=formulario)



@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    from models import Event

    evento = Event.query.get_or_404(event_id)

    if evento.user_id != current_user.id:
        return redirect(url_for('dashboard'))

    db.session.delete(evento)
    db.session.commit()

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)

"""
pip install flask, flask-wtf, 
flask_sqlalchemy, flask_login
"""
