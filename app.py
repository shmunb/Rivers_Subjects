from flask import Flask, request, render_template
from sqlalchemy import text
from db import DB
from dbparser import *


app = Flask(__name__, template_folder=os.path.abspath('./tmp'))


print(app.template_folder)
app.config['DEBUG'] = True
DB = DB()


@app.route('/')
def main_page():
    return render_template('main.html')


@app.route('/waters')
def waters():
    waters = DB.get_waters()

    return render_template('waters.html', waters=waters)


@app.route('/waters/sorted_by=<sorted_by>')
def waters_sorted(sorted_by):
    waters = DB.get_waters(order=sorted_by)

    return render_template('waters.html', waters=waters)

@app.route('/waters/<water_id>')
def water(water_id):
    water_data = DB.get_water_info(water_id)
    subjects_data = DB.get_subjects_for_water(water_id)

    return render_template('water.html', water=water_data, subjects=subjects_data)


@app.route('/waters/add', methods=['GET', 'POST'])
def add_water():
    if request.method == 'POST':
        name = request.form.get('name')
        type = water_type[request.form.get('type')]
        size = request.form.get('size')
        DB.add_water(name, type, size)

    return render_template('add_water.html')


@app.route('/waters/remove', methods=['GET', 'POST'])
def remove_water():
    if request.method == 'POST':
        name = request.form.get('name')
        DB.remove_water(name)

    return render_template('remove_water.html')


@app.route('/waters/<water_id>/add_subject', methods=['GET', 'POST'])
def add_subject_to_water(water_id):
    if request.method == 'POST':
        water_name = request.form.get('water_name')
        subject_name = request.form.get('subject_name')
        DB.add_subject_to_water(water_name, subject_name)

    return render_template('add_subject_to_water.html')


@app.route('/subjects')
def subjects():
   subjects = DB.get_subjects()

   return render_template('subjects.html', subjects=subjects)


@app.route('/subjects/sorted_by=<sorted_by>')
def subjects_sorted(sorted_by):
   subjects = DB.get_subjects(order=sorted_by)

   return render_template('subjects.html', subjects=subjects)

@app.route('/subjects/<subject_id>')
def subject(subject_id):
    subject_data = DB.get_subject_info(subject_id)
    water_data = DB.get_water_for_subject(subject_id)

    return render_template('subject.html', waters=water_data, subject=subject_data)

@app.route('/subjects/add', methods=['GET', 'POST'])
def add_subject():
  if request.method == 'POST':
    name = request.form.get('name')
    typ = request.form.get('typ')
    creation_year = request.form.get('creation_year')
    DB.add_subject(name, typ, creation_year)

  return render_template('add_subject.html')


@app.route('/subjects/remove', methods=['GET', 'POST'])
def remove_subject():
  if request.method == 'POST':
    name = request.form.get('name')
    DB.remove_subject(name)

  return render_template('remove_subject.html')


@app.route('/subjects/add_water_to_subject', methods=['GET', 'POST'])
def add_water_to_subject():
    if request.method == 'POST':
        water_name = request.form.get('water_name')
        subject_name = request.form.get('subject_name')
        DB.add_subject_to_water(water_name, subject_name)

    return render_template('add_subject_to_water.html')


@app.route('/waters/remove_subject_from_water', methods=['GET', 'POST'])
def remove_subject_from_water():
    if request.method == 'POST':
        subject_name = request.form.get('subject_name')
        DB.remove_subject_from_water(subject_name)

    return render_template('remove_subject_from_water.html')


#run_base(DB)
#DB.drop_tables()
#parse_waters(DB)
#parse_subjects(DB)
#parse_relations(DB)
#parse_inflows(DB)

for row in DB.engine.execute('SELECT * FROM waters;'):
    print(dict(row))
for row in DB.engine.execute('SELECT * FROM subjects;'):
    print(dict(row))

#DB.engine.execute(('SELECT * FROM subjects;'))

app.run(host='127.0.0.1', port=5021)
