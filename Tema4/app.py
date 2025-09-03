from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200), nullable=True)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Note {self.id}: {self.title}>'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']
        if title and text:
            new_note = Note(title=title, subtitle=subtitle, text=text)

            db.session.add(new_note)
            db.session.commit()

        return redirect(url_for('notes'))

    all_notes = Note.query.order_by(Note.id.desc()).all()
    return render_template('notes.html', notes=all_notes)

if __name__ == '__main__':
    with app.app_context():
        upgrade()
    app.run(debug=True)