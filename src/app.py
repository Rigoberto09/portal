from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

#correo electronico
from flask import Flask
from flask_mail import Mail, Message
#generacion de contrase;a de correo electronico
from secrets import choice
from string import ascii_letters, ascii_uppercase, digits

#contrase;a del correo
from password import password_gmail

#connecion de la base de datos
from config import config

#login utilizado
# Models:
from models.ModelUser import ModelUser
from models.ModelUserN import ModelUserN
# Entities:
from models.entities.User import User
from models.entities.UserN import UserN

app = Flask(__name__)

#correo electronico
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'rpione8@gmail.com'
app.config['MAIL_PASSWORD'] = password_gmail
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)

#-------------------------

login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Contraseña no válida...")

                print(generate_password_hash('123'))
                
                return render_template('auth/login.html')
                
        else:
            flash("Correo no encontrado...")
            return redirect(url_for('home'))
            #return render_template('auth/login.html')
    else:
        
        return render_template('auth/login.html')

#desbloque de cuenta o registro de nuevo usuario
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        user = UserN(0, request.form['username'])
        logged_user = ModelUserN.login(db, user)
        if logged_user != None:
             #registro correo electronico 
            usuario = request.form['username']
            #generacion de contrase;a
            caracteres = ascii_letters + ascii_uppercase + digits
            longitud = 8  # La longitud que queremos
            cadena_aleatoria = ''.join(choice(caracteres) for caracter in range(longitud))
            #print("La cadena es: ", cadena_aleatoria)
            saludo = 'Ha realizado correctamente la inscripcion a la plataforma correctamente su contrase;a es '
            mensajeCompleto =saludo + cadena_aleatoria
            #print(mensajeCompleto)
            #sifrado de candena aleatoria
            contra = generate_password_hash(cadena_aleatoria)
            #insertar contrase;a generada al usuario
            cur = db.connection.cursor()
            cur.execute(""" 
            UPDATE user
            SET username = %s,password = %s
            WHERE username = %s """,(usuario,contra,usuario))
            db.connection.commit()

            #envio de menssage al usuario destio
            msg = Message('Hola, un gusto saludarte', sender =   usuario, recipients = [usuario])
            msg.body = mensajeCompleto
            mail.send(msg)

            flash("Inscripcion realizada correctamente")
            return render_template('auth/login.html')
            #-----------------------------------
            #return render_template('login.html')
        else:
            flash("Sin Acceso...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

#creacion de nuevo usuario
@app.route('/nuevoUser', methods=['GET', 'POST'])
def nuevoUser():
    if request.method == 'POST':
        #print(request.form['username'])
        #contra1 = request.form['password']
       # print(generate_password_hash(request.form['password']))
        user = UserN(0, request.form['username'])
        logged_user = ModelUserN.login(db, user)
        if logged_user != None:
            usuario = request.form['username']
            #contra=request.form['password']
            #contrasena = generate_password_hash(contra)
            #print (contra)
            #print (contrasena)    
            return render_template('login.html')
        else:
            flash("Sin Acceso...")
            return render_template('login.html')
    else:
        return render_template('login.html')

    #return render_template("inicio.html")
#''''-----------------------------
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/home')
def home():
    #cur = db.connect.cursor()
    #cur.execute('SELECT * FROM user WHERE username = comprobante')
    #edit = cur.fetchall()

    return render_template('inicio.html')


#posibles errores
def status_304(error):
    return "<h1>Desarrollo</h1>",304

def status_401(error):
    flash('Acceso Denegado')
    return redirect(url_for('login'))

def status_404(error):
    return "<h1>Página en desarrollo</h1>", 404



#consultas del sistema

#---actualizacion de vista
@app.route('/ActualizarDatos')
def ActualizarDatos():
    return render_template("inicio.html")

@app.route('/inicio')
#@login_required #requerido iniciar seccion
def inicio():
    return render_template("inicio.html")

# Llamando a las paginas
@app.route('/Datos', strict_slashes=False)
def Datos():
    #cur = db.connection.cursor()
    #cur.execute("""
    #SELECT c.id,p.identidad,p.nombreCompleto,c.fecha,c.sacos,c.peso,c.precio,(c.peso*c.precio) 
    #FROM compras as c, productores as p
    #WHERE p.identidad= c.identidad
    #""")
    #data = cur.fetchall()
    #return render_template("Datos.html", compras=data)
    return render_template("Datos.html")


@app.route('/Areas')
#@login_required #requerido iniciar seccion
def Areas():
    cur = db.connect.cursor()
    cur.execute(""" 
    select ar.ID_area, ar.nombre_area, ar.longitud, ar.latitud, decr.Nombre_Decreto
    from areasprotegidas as ar
	    inner join decretos as decr on decr.ID_decretos = ar.ID_decreto
    limit 50;
    """)
    data = cur.fetchall()
    return render_template("Areas.html",areas=data)

@app.route('/Asentamientos', strict_slashes=False)
#@login_required #requerido iniciar seccion
def Asentamientos():
    return render_template("Asentamientos.html")

@app.route('/Agricultura', strict_slashes=False)
#@login_required #requerido iniciar seccion
def Agricultura():
    cur = db.connect.cursor()
    cur.execute("""
    select ag.ID_Agricultura, ag.Eficiencia, ag.Poverty, ag.Potencia, mun.Nombre_Municipio, dep.Nombre_Depto
	from agricultura as ag
		inner join municipios as mun on mun.ID_Municipio = ag.ID_Municipio
			inner join  departamentos as dep on dep.ID_Depto = ag.ID_Depto
    limit 100;
    """)
    data = cur.fetchall()
    return render_template("Agricultura.html", agricula=data)

@app.route('/Censo', strict_slashes=False)
#@login_required #requerido iniciar seccion
def Censo():
    return render_template("Censo.html")

@app.route('/Desempleo', strict_slashes=False)
#@login_required #requerido iniciar seccion
def Desempleo():
    return render_template("Desempleo.html")

@app.route('/centros', strict_slashes=False)
#@login_required #requerido iniciar seccion
def centros():
    cur = db.connect.cursor()
    cur.execute("""
    SELECT ce.Nombre_centros, ce.Direccion, ce.niveles, ce.UrbanoRural,mu.Nombre_Municipio, dep.Nombre_Depto, ce.coordenadas 
    FROM CentrosEducativos as ce, municipios as mu, departamentos as dep
    WHERE ce.ID_Municipio = mu.ID_Municipio AND ce.ID_Depto=dep.ID_Depto AND ce.ID_Centro <100
    """)
    data = cur.fetchall()
    return render_template("centros.html",centros=data)

@app.route('/Dispensa', strict_slashes=False)
#@login_required #requerido iniciar seccion
def Dispensa():
    return render_template("Dispensa.html")

@app.route('/palmares', strict_slashes=False)
#@login_required #requerido iniciar seccion
def palmares():
    return render_template("palmares.html")


@app.route('/Maestro', strict_slashes=False)
#@login_required #requerido iniciar seccion
def Maestro():
    cur = db.connect.cursor()
    cur.execute("""
    SELECT m.ID_maestros, m.Nombre_Mestros, m.Escuela, m.Direccion, mu.Nombre_Municipio, dep.Nombre_Depto 
    FROM maestros as m, municipios as mu, departamentos as dep
    WHERE m.ID_Municipio = m.ID_Municipio AND m.ID_Departamento=dep.ID_Depto AND m.ID_maestros <100
    """)
    data = cur.fetchall()
    return render_template("Maestro.html",profes=data)

@app.route('/Microcuencas', strict_slashes=False)
#@login_required #requerido iniciar seccion
def Microcuencas():
    cur = db.connect.cursor()
    cur.execute("""
    SELECT micro.ID_micro, micro.NombreMicrocuenca, micro.area,mu.Nombre_Municipio, dep.Nombre_Depto 
     FROM microcuencas as micro, municipios as mu, departamentos as dep m.ID
    WHERE micro.ID_Municipio = mu.ID_Municipio AND micro.ID_Depto=dep.ID_Depto
    """)
    data = cur.fetchall()
    return render_template("Microcuencas.html",micro= data)

@app.route('/Planificacion', strict_slashes=False)
#@login_required #requerido iniciar seccion
def Planificacion():
    return render_template("Planificacion.html")

@app.route('/plantaciones', strict_slashes=False)
#@login_required #requerido iniciar seccion
def plantaciones():
    return render_template("plantaciones.html")

@app.route('/Regiones', strict_slashes=False)
#@login_required #requerido iniciar seccion
def Regiones():
    return render_template("Regiones.html")

@app.route('/Retornados', strict_slashes=False)
#@login_required #requerido iniciar seccion
def Retornados():
    return render_template("Retornados.html")

@app.route('/hospitalizados', strict_slashes=False)
#@login_required #requerido iniciar seccion
def hospitalizados():
    return render_template("hospitalizados.html")

@app.route('/salarios', strict_slashes=False)
#@login_required #requerido iniciar seccion
def Salarios():
    return render_template("salarios.html")

@app.route('/enfermedades', strict_slashes=False)
#@login_required #requerido iniciar seccion
def enfermedades():
    return render_template("enfermedades.html")

@app.route('/vacunados', strict_slashes=False)
#@login_required #requerido iniciar seccion
def vacunados():
    return render_template("vacunados.html")

@app.route('/seresvivos', strict_slashes=False)
#@login_required #requerido iniciar seccion
def seresvivos():
    return render_template("seresvivos.html")

@app.route('/Torneos', strict_slashes=False)
#@login_required #requerido iniciar seccion
def Torneos():
    return render_template("Torneos.html")

@app.route('/equipos', strict_slashes=False)
#@login_required #requerido iniciar seccion
def Equipos():
    return render_template("Equipos.html")

@app.route('/users', strict_slashes=False)
#@login_required #requerido iniciar seccion
def users():
    cur = db.connect.cursor()
    cur.execute('SELECT * FROM user')
    data = cur.fetchall()

    cur = db.connect.cursor()
    cur.execute('SELECT * FROM user')
    edit = cur.fetchall()

    return render_template("users.html",user=data,editUser=edit[0])

#----Eliminar usuarios-----------------
@app.route('/eliminar_usuarios/<string:id>')
#@login_required #requerido iniciar seccion
def eliminar_usuarios(id):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM user WHERE id = {0}'.format(id))
    db.connection.commit()
    flash('Usuario elimanado')  
    return redirect(url_for('users'))

#-------Editar usuarios--------------
#-------Agregar usuario--------------
@app.route('/agregarN', methods=['GET', 'POST'])
#@login_required #requerido iniciar seccion
def agregarN():
    if request.method == 'POST':
        user = UserN(0, request.form['username'])
        logged_user = ModelUserN.login(db, user)
        if logged_user != None:
            flash('Correo electronico registrado')
            return redirect(url_for('users')) 
        else:
            #registro correo electronico 
            usuario = request.form['username']
            #generacion de contrase;a
            caracteres = ascii_letters + ascii_uppercase + digits
            longitud = 16  # La longitud que queremos
            cadena_aleatoria = ''.join(choice(caracteres) for caracter in range(longitud))
            #print("La cadena es: ", cadena_aleatoria)
            saludo = 'Ha realizado correctamente la inscripcion a la plataforma correctamente su contrase;a es '
            mensajeCompleto =saludo + cadena_aleatoria
            #print(mensajeCompleto)
            #sifrado de candena aleatoria
            contra = generate_password_hash(cadena_aleatoria)
            #insertar contrase;a generada al usuario
            cur = db.connection.cursor()
            cur.execute(""" insert into user (username,password) values(%s,%s)""",(usuario,contra))
            db.connection.commit()

            #envio de menssage al usuario destio
            msg = Message('Hola, un gusto saludarte', sender =   usuario, recipients = [usuario])
            msg.body = mensajeCompleto
            mail.send(msg)
            flash("Usuario agregado correctamente")
            return redirect(url_for('users')) 
    else:
        flash('Metodo incorrecto')
        return redirect(url_for('users'))


    return redirect(url_for('users'))



#@app.route('/EditarCuentcas/<id>')
#def EditarCuentcas(id):
#    cur = db.connection.cursor()
#    cur.execute("""
#    SELECT micro.ID_micro, micro.NombreMicrocuenca, micro.area,mu.Nombre_Municipio, dep.Nombre_Depto
#    FROM microcuencas as micro, municipios as mu, departamentos as dep
#    WHERE micro.ID_Municipio = mu.ID_Municipio AND micro.ID_Depto=dep.ID_Depto AND micro.ID_micro = {0}
#    """.format(id))
#    data = cur.fetchall()
#    return render_template("editar/EditarCuentcas.html",Cuencas=data[0])


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
