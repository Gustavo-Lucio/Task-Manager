from flask import render_template, redirect, url_for, Flask
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
    return render_template('dashboard.html')


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    from forms import EventForm
    formulario = EventForm()  # Instancie o formulário

    if formulario.validate_on_submit():  # Verifique se o formulário foi validado
        # lógica para criar evento
        pass

    return render_template('create_event.html', form=formulario)


@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    return render_template('edit_event.html')


@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    pass


if __name__ == '__main__':
    app.run(debug=True)

"""
pip install flask, flask-wtf, 
flask_sqlalchemy, flask_login
"""
