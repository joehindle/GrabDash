from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

#Data Class
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean,default=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Task {self.id}"


@app.route("/", methods=["GET", "POST"])
def example():
    #Add a task
    if request.method == "POST":
        current_task=request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"     
    #See all current tasks
    else:
        all_tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", all_tasks=all_tasks)

#Delete an item
@app.route("/delete/<int:id>")
def delete(id):
    delete_task=MyTask.query.get_or_404(id)
    db.session.delete(delete_task)
    db.session.commit()
    return redirect("/")

#Update an item
@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    update_task=MyTask.query.get_or_404(id)
    if request.method=="POST":
        update_task.content=request.form['edit-content']
        db.session.commit()
        return redirect("/")
    else:
        return render_template("edit.html", task=update_task)

    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=8000)
