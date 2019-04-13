#Instalar virtualenv  virtualenv nombre --python=python3.5

#pip3 install flask flask-mysqldb

from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)


#CONEXION MYSQL
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'damian'
app.config['MYSQL_PASSWORD']= 'damian82'
app.config['MYSQL_DB']= 'flaskcontacts'
mysql = MySQL(app)

#GUARDAR LA SESIÓN
app.secret_key='millavesecreta'

@app.route('/')
def Index():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts ORDER BY fullname ASC')
    data=cur.fetchall()
 #   print (data)
    return render_template("index.html", contacts = data)

@app.route('/añadir_contacto', methods=['POST'])
def add_contacto():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', (fullname, phone, email))
        mysql.connection.commit()   #Con esta función ejecutamos la función anterior e introducimos los datos en MySQL
        flash('Contacto añadido con éxito')
        return redirect(url_for('Index'))  #Una vez terminada la función rederigimos a la función index


@app.route('/editar/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('editarcontacto.html', contact = data[0])


@app.route('/update/<id>', methods = ['POST'])
def actualizar_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
            phone = %s,
            email = %s
            WHERE id = %s
        """, (fullname, phone, email, id))
        mysql.connection.commit()
        flash('Contacto actualizado correctamente')
        return redirect(url_for('Index'))



@app.route('/eliminar/<string:id>')  #Le indicamos que la ruta es eliminar/numero que le pasamos por parametro
def eliminar_contacto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto borrado')
    return redirect(url_for('Index'))



if __name__=='__main__':
    app.run(debug=True)
