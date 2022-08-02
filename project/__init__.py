from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, select
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///banco.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Gty$$asd567456uihds45'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


# DB e Models ===========================================

db = SQLAlchemy(app)



class Usuário(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    senha = db.Column(db.String, nullable = False)
    admin = db.Column(db.Boolean, default = False)

    tarefas = db.relationship('Tarefa', backref = 'usuário')

    def __repr__(self):
        return f"<Usuário: {self.nome}>"

    

class Tarefa(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    descrição = db.Column(db.String, nullable = True)
    completa = db.Column(db.Boolean, default=False)

    id_usuário = db.Column(db.Integer, db.ForeignKey("usuário.id"), nullable = False)

# Login =============================================

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):

    return db.session.get(Usuário, user_id)


# Admin =============================================


class MyAdminIndexView(AdminIndexView):

    def is_accessible(self):

        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class MyModelView(ModelView):

    def is_accessible(self):

        return current_user.is_authenticated and current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

    
admin = Admin(app, template_mode="bootstrap3", index_view=MyAdminIndexView())

admin.add_view(MyModelView(Usuário, db.session))
admin.add_view(MyModelView(Tarefa, db.session))


# Views =============================================


@app.route("/")
def home():

    return render_template("home.html")


# Views de Login --------------------------------


@app.route("/login/", methods = ["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get('email')
        senha = request.form.get('senha')
        

        stmt = select(Usuário).where(Usuário.email == email)
        result = list(db.session.execute(stmt))
        
        usuário = None

        if result:
            usuário = result[0][0]
 
        if not usuário:
            flash("usuário não existe")

        elif not check_password_hash(usuário.senha, senha):

            flash("Senha incorreta!")

        elif check_password_hash(usuário.senha, senha):

            login_user(usuário)

            return redirect(url_for("todo"))
    

    return render_template("login.html")


@app.route("/cadastro/", methods = ["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        

        stmt = select(Usuário).where(Usuário.email == email)
        result = list(db.session.execute(stmt))
        

        if result:
            
            flash('email já cadastrado')
        
        else:

            novo_usuário = Usuário(
                nome = nome,
                email = email,
                senha = generate_password_hash(senha, method='sha256')
            )

            db.session.add(novo_usuário)
            db.session.commit()
            flash('Efetue seu login para começar!')
            return redirect(url_for('login'))        
    

    return render_template("cadastro.html")


@app.route("/logout/")
def logout():

    logout_user()

    return redirect(url_for("login"))


# Views do To-Do -------------------------------


@app.route("/todo/")
@login_required
def todo():

    # to acessando as tarefas do current_user direto no template jinja, por isso não tem mais código aqui.
    #print(current_user.tarefas)

    return render_template("todo.html")


@app.route("/todo/add/", methods = ["POST"])
@login_required
def add():

    if request.method == "POST":

        descrição = request.form.get("descrição")

        tarefa = Tarefa(descrição = descrição, usuário = current_user)

        db.session.add(tarefa)
        db.session.commit()

        # acha a rota de função "todo" de redireciona para ela.
        return redirect(url_for("todo"))


@app.route("/todo/<int:id_tarefa>/check/")
@login_required
def check(id_tarefa):

    tarefa = db.session.get(Tarefa, id_tarefa)
    tarefa.completa = not tarefa.completa
    
    db.session.flush()
    db.session.commit()

    return redirect(url_for("todo"))


@app.route("/todo/<int:id_tarefa>/delete/")
@login_required
def delete(id_tarefa):

    tarefa = db.session.get(Tarefa, id_tarefa)
    
    db.session.delete(tarefa)
    db.session.commit()

    return redirect(url_for("todo"))


# APIs ==============================================


@app.route("/api/usuários/", methods = ["GET"])
def api_get_usuários():

    if request.method == "GET":
        stmt = select(Usuário)
        result = list(db.session.execute(stmt))

        print(result)

        list_of_dicts = []

        for tupla in result:

            dicio = tupla[0].__dict__.copy()
            dicio.pop('_sa_instance_state')
            dicio.pop('senha')
            list_of_dicts.append(dicio)

        print(list_of_dicts)

        return jsonify(usuários = list_of_dicts)


@app.route("/api/usuário/<int:id_usuário>/", methods = ["GET"])
def api_get_usuário_por_id(id_usuário):

    usuário = db.session.get(Usuário, id_usuário)

    if usuário:

        user_dict = usuário.__dict__.copy()

        print(user_dict)


    return jsonify(data = user_dict)
