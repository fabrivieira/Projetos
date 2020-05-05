from flask import render_template, redirect, flash, request, url_for, send_file
from app.models.forms import Owner, Pet
from app.models.tables import Pets, Proprietarios
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from app import app, db, SERVER_NAME
import qrcode, os

ROUTE_INDEX  = "/"
ROUTE_INDEX2 = "/index/"
ROUTE_LOGIN =  "/login/"
ROUTE_LOGOUT = "/logout/"
ROUTE_REGISTER = "/register/"
ROUTE_LAYOUT_STATIC = "/layout_static/"
ROUTE_PASSWORD = "/password/"
ROUTE_TABLES = "/tables/"
ROUTE_CHARTS = "/charts/"
ROUTE_LAYOUT_SIDENAV_LIGHT = "/layout_sidenav_light/"
ROUTE_OWNER = "/owner/"
ROUTE_PET = "/pet/"
ROUTE_GET_PET = "/get_pet/"
ROUTE_GET_FILE = "/get_file/"

@app.route(ROUTE_INDEX)
@app.route(ROUTE_INDEX2, methods=('POST', 'GET'))
@login_required
def index():
    print(os.path.abspath(__file__))
    return render_template("/index.html/")

@app.route(ROUTE_LOGIN, methods=['POST', 'GET'])
def login():

    form = Owner()

    if request.method == "POST": 
        
        proprietario = Proprietarios.query.filter_by(email=request.form['email']).first()

        if (proprietario and proprietario.senha == request.form['senha']):
            login_user(proprietario)

            # url_for utiliza o nome do método
            return redirect(url_for("index"))
        else:
            flash("Usuário ou senha inválida")

    return render_template("login.html", form=form)

@app.route(ROUTE_LOGOUT, methods=('POST', 'GET'))
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))    

@app.route(ROUTE_REGISTER)
def register():
    return render_template("/register.html/")      



@app.route(ROUTE_LAYOUT_STATIC)
@login_required
def layout_static():
    return render_template("/layout-static.html/")

@app.route(ROUTE_PASSWORD)
@login_required
def password():
    return render_template("/password.html/")    

@app.route(ROUTE_TABLES)
@login_required
def tables():
    return render_template("/tables.html/")    

@app.route(ROUTE_CHARTS)
@login_required
def charts():
    return render_template("/charts.html/")   

@app.route(ROUTE_LAYOUT_SIDENAV_LIGHT)
@login_required
def layout_sidenav():
    return render_template("/layout-sidenav-light.html/")   

@app.route(ROUTE_OWNER, methods=('POST', 'GET'))
@login_required
def form_owner():
    
    form = Owner()   

    if form.validate_on_submit():

        nome = form.nomeProprietario.data
        cpf = form.cpfProprietario.data
        email = form.emailProprietario.data
        senha = form.senhaProprietario.data    
        
        db.session.add(Proprietarios(nome, cpf, email, senha))
        db.session.commit()

    return render_template("/owner.html/", form=form)

@app.route(ROUTE_PET, methods=('POST', 'GET'))
@login_required
def form_pet():

    form = Pet()

    if request.method == "POST" and request.form.get('action'):

        if request.form['action'] == "insert":
            id_proprietario = current_user.id
            nome   = request.form['nomePet']
            dtnasc = datetime.strptime(request.form['dtNascPet'], '%Y-%m-%d').date()  

            new_pet = Pets(id_proprietario, nome, dtnasc,'')
            db.session.add(new_pet)
            db.session.commit()

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4
            )
            hash = str(new_pet.id) + "_" + str(id_proprietario) 
            url = SERVER_NAME + ROUTE_GET_PET + hash 
            img_file = app.config['UPLOAD_PATH'] + hash + ".png"  
            qr.add_data(url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.save(img_file)

            new_pet.qrcode = os.path.basename(img_file)
            db.session.commit()         

        if request.form['action'] == "delete":
            id_proprietario = current_user.id
            id_pet   = request.form['id']

            db.session.delete(Pets.query.filter_by(id_proprietario=current_user.id, id=id_pet).first())
            db.session.commit()            

    pets = Pets.query.filter_by(id_proprietario=current_user.id)
    return render_template("/pet.html/", pets=pets, form=form)


@app.route(ROUTE_GET_PET + "<hash>", methods=('GET','POST'))
def get_pet(hash):

    form = Pet()
    ids = hash.split('_')   

    pet = Pets.query.filter_by(id=int(ids[0]), id_proprietario=int(ids[1])).first()
    return render_template("/get_pet.html/", pet=pet) 

@app.route(ROUTE_GET_FILE + "<file>", methods=('GET','POST'))
def get_file(file):
    return send_file(app.config['UPLOAD_PATH'] + file, mimetype='image/png')     


    







#@app.errorhandler(404)
#def not_found(error):
#    render_template("/404.html/") , 404
