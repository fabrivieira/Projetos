from app import db, login_manager

class Proprietarios(db.Model):
    __tablename__ = "proprietarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)    


    @login_manager.user_loader
    def load_user(id):
        return Proprietarios.query.filter_by(id=id).first()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)    

    def __init__(self, nome, cpf, email, senha):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha

    def __repr__(self):
        return '<Proprietario %r>' % self.nome
        


class Pets(db.Model):
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_proprietario = db.Column(db.Integer, db.ForeignKey('proprietarios.id'))
    nome = db.Column(db.String(80), nullable=False)
    dtNasc = db.Column(db.Date, nullable=False)
    qrcode = db.Column(db.String(80))

    def __init__(self, id_proprietario, nome, dtNasc, qrcode):
        self.id_proprietario = id_proprietario
        self.nome = nome
        self.dtNasc = dtNasc
        self.qrcode = qrcode

    def __repr__(self):
        return '<Pet %r>' % self.id