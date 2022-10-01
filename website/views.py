from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():

    return render_template("home.html", user=current_user)

@views.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash("Note cannot be this short", category='error')
        else:
            add_note = Note(data=note, user_id=current_user.id)
            db.session.add(add_note)
            db.session.commit()
            flash("Note added", category='success')
    return redirect(url_for('views.home'))
            

@views.route('/delete-note', methods = ['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})
