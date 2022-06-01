from core import app, db
from core.models import Todo
from flask import Flask, Markup, render_template, request, flash, redirect, url_for

blank_error = Markup('<div class="header">ToDo item cannot be blank.</div><p>You need to enter an item.</p>')

@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    if not title:
        flash(blank_error)
        return redirect(url_for("home"))
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))
