from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime
import os

app = Flask(__name__)

def get_profile():
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    prof_list = []
    for i in c.execute('SELECT * FROM persons'):
        prof_list.append({'id':i[0],'name':i[1],'age':i[2],'sex':i[3]})
    conn.commit()
    conn.close()
    return prof_list

def update_profile(prof):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    c.execute('UPDATE persons SET name=(?), age=(?), sex=(?) WHERE id=(?)', [prof['name'], prof['age'], prof['sex'], prof['id']])
    conn.commit()
    conn.close()

def add_profile(prof):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    c.execute('INSERT INTO persons (name, age, sex) VALUES ((?), (?), (?))', [prof['name'], prof['age'], prof['sex']])
    conn.commit()
    conn.close()

def delete_profile(id):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    c.execute('DELETE FROM persons WHERE id=(?)', [id])
    conn.commit()
    conn.close()

@app.route('/profile')
def profile():
    prof_list = get_profile()
    return render_template('profile.html', title='sql', user=prof_list)

@app.route('/edit/<int:id>')
def edit(id):
    prof_list = get_profile()
    for prof_dict in prof_list:
        if prof_dict['id'] == id:
            edit_prof_dict = prof_dict
            break
    return render_template('edit.html', title='sql', user=edit_prof_dict)

@app.route('/add_prof')
def add_prof():
    False
    return render_template('add.html', title='sql', user = False)

@app.route('/delete_prof/<int:id>')
def delete_prof(id):
    prof_list = get_profile()
    for prof_dict in prof_list:
        if prof_dict['id'] == id:
            delete_prof_dict = prof_dict
            break
    return render_template('delete.html', title='sql', user = delete_prof_dict)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    prof_list = get_profile()
    for prof_dict in prof_list:
        if prof_dict['id'] == id:
        # prof_dictの値を変更
            prof_dict['name'] = request.form['name']
            prof_dict['age'] = request.form['age']
            prof_dict['sex'] = request.form['sex']
            break
    update_profile(prof_dict)
    return redirect(url_for('profile'))

@app.route('/add', methods=['POST'])
def add():
    prof_dict = {}
    prof_dict['name'] = request.form['name']
    prof_dict['age'] = request.form['age']
    prof_dict['sex'] = request.form['sex']
    add_profile(prof_dict)
    return redirect(url_for('profile'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    prof_list = get_profile()
    for prof_dict in prof_list:
        if prof_dict['id'] == id:
            delete_profile(id)
            break
    return redirect(url_for('profile'))



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5001)), threaded=True)
