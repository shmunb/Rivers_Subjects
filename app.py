from flask import Flask, request, render_template
from sqlalchemy import text
from db import DB

app = Flask(__name__)
app.config['DEBUG'] = True
DB = DB()


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/waters')
def waters():
    waters = DB.get_waters()

    return render_template('waters.html', waters=waters)


@app.route('/waters/<water_id>')
def waters(water_id):
    water_data = DB.get_waters_info(water_id)
    subjects_data = DB.get_subjects_for_water(water_id)

    return render_template('water.html', water=water_data, subjects=subjects_data)


@app.route('/museums/add', methods=['GET', 'POST'])
def add_museum():
    if request.method == 'POST':
        name = request.form.get('name')
        foundation_year = request.form.get('foundation_year')
        city = request.form.get('city')
        DB.add_museum(name, foundation_year, city)

    return render_template('add_museum.html')


@app.route('/museums/remove', methods=['GET', 'POST'])
def remove_museum():
    if request.method == 'POST':
        name = request.form.get('name')
        DB.remove_museum(name)

    return render_template('remove_museum.html')


@app.route('/museums/add_exhibit', methods=['GET', 'POST'])
def add_exhibit_to_museum():
    if request.method == 'POST':
        museum_name = request.form.get('museum_name')
        exhibit_name = request.form.get('exhibit_name')
        DB.add_exhibit_to_museum(museum_name, exhibit_name)

    return render_template('add_exhibit_to_museum.html')


@app.route('/museums/remove_exhibit', methods=['GET', 'POST'])
def remove_exhibit_from_museum():
    if request.method == 'POST':
        exhibit_name = request.form.get('exhibit_name')
        DB.remove_exhibit_from_museum(exhibit_name)

    return render_template('remove_exhibit_from_museum.html')