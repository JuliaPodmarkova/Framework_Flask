import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_FILE = 'notes.json'

def load_notes():
    """Загружает записи из JSON-файла."""
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"Моя первая запись": "Сегодня я начал создавать свой дневник на Flask. Это так круто!"}


def save_notes(notes):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=4)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    notes_dict = load_notes()

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        if title and text:

            notes_dict[title] = text
            save_notes(notes_dict)

        return redirect(url_for('notes'))

    return render_template('notes.html', notes=notes_dict)


if __name__ == '__main__':
    app.run(debug=True)
