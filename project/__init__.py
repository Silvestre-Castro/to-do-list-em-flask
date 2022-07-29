from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, select
from flask_login import LoginManager, UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


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
    

class Tarefa(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    descrição = db.Column(db.String, nullable = True)
    completa = db.Column(db.Boolean, default=False)


# Login =============================================

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):

    return db.session.get(Usuário, user_id)




# Admin =============================================

admin = Admin(app, template_mode="bootstrap3")

admin.add_view(ModelView(Usuário, db.session))
admin.add_view(ModelView(Tarefa, db.session))


# Views =============================================




@app.route("/")
def home():

    return render_template("home.html")


@app.route("/todo/")
def todo():

    stmt = select(Tarefa)
    result = list(db.session.execute(stmt))

    lista_de_tarefas = []
    for tupla in result:

        lista_de_tarefas.append(tupla[0])


    return render_template("todo.html", lista_de_tarefas = lista_de_tarefas)


@app.route("/todo/add/", methods = ["POST"])
def add():

    if request.method == "POST":

        descrição = request.form.get("descrição")

        tarefa = Tarefa(descrição = descrição)

        db.session.add(tarefa)
        db.session.commit()

        # acha a rota de função "todo" de redireciona para ela.
        return redirect(url_for("todo"))


@app.route("/todo/<int:id_tarefa>/check/")
def check(id_tarefa):

    tarefa = db.session.get(Tarefa, id_tarefa)
    tarefa.completa = not tarefa.completa
    
    db.session.flush()
    db.session.commit()

    return redirect(url_for("todo"))


@app.route("/todo/<int:id_tarefa>/delete/")
def delete(id_tarefa):

    tarefa = db.session.get(Tarefa, id_tarefa)
    
    db.session.delete(tarefa)
    db.session.commit()

    return redirect(url_for("todo"))