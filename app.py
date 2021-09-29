from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Project %i>' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "<User %i>" % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        new_project = Project(
            name=request.form['name'],
            description=request.form['description'],
            contact=request.form['contact']
        )

        try:
            db.session.add(new_project)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your project'

    else:
        projects = Project.query.order_by(Project.date_created).all()
        return render_template('index.html', projects=projects)


@app.route('/delete/<int:id>')
def delete(id):
    project_to_delete = Project.query.get_or_404(id)

    try:
        db.session.delete(project_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that project'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    project = Project.query.get_or_404(id)

    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your project'

    else:
        return render_template('update.html', project=project)


if __name__ == "__main__":
    app.run(debug=True)
