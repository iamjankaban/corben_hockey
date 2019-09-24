from app import app

from flask import render_template, request
from datetime import datetime

from app.forms import LigaForm, TeamsForm
from app.controllers import listLiga, teamsInLiga, teamsName, matchesList, matchesScore

from copy import copy

date = datetime.utcnow()

@app.route('/')
@app.route('/liga', methods = ['GET'])
@app.route('/results', methods = ['GET'])
def index():
    form = LigaForm()
    options = listLiga().rows

    return render_template('bot/liga.html', form = form, options = options)

@app.route('/liga', methods = ['POST'])
def start_liga():
    teams_cod,teams_nam = [],[]
    form = LigaForm(request.form)
    if form.validate():
        ligas = []
        for val in request.form.getlist('input_liga'):
            ligas.append(val)
        try:
            teams_cod = teamsInLiga(ligas).teams
            teams_nam = teamsName(teams_cod).teams_name
        except:
            pass
                
    else:
        print('ERROR',request.form)
    return render_template('bot/liga_teams.html', form = form, teams = teams_nam)

@app.route('/results', methods = ['POST'])
def results_liga():
    temps = {}
    form = TeamsForm(request.form)
    form.validate()
    print(form.errors)
    if form.validate():
        try:
            home,away = request.form.get('team_left'),request.form.get('team_right')
            temps = matchesList(home,away)
            score = matchesScore(temps.matches_cod).score
        except:
            pass                
    else:
        print('ERROR VALIDATE')
        pass
    return render_template('bot/liga_teams_list.html', form = form, score = score, temps = temps.matches, temps_name = temps.teams_name)

# @app.errorhandler(404)
# def not_found_error(error):
#     return render_template('404.html'), 404

# @app.errorhandler(500)
# def internal_error(error):
#     db.session.rollback()
#     return render_template('500.html'), 500