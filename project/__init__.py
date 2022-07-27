from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, select


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///banco.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Tarefa(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    descrição = db.Column(db.String, nullable = True)
    completa = db.Column(db.Boolean, default=False)


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