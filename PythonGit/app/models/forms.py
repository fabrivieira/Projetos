from flask_wtf import FlaskForm
from wtforms import StringField, validators

class Owner(FlaskForm):
        nomeProprietario = StringField('nomeProprietario', [validators.Length(min=4, max=25), validators.DataRequired()])
        senhaProprietario = StringField('senhaProprietario', [validators.Length(min=4, max=25), validators.DataRequired()])        
        cpfProprietario = StringField('cpfProprietario', [validators.Length(min=4, max=25), validators.DataRequired()])
        emailProprietario = StringField('emailProprietario', [validators.Length(min=4, max=25), validators.DataRequired()]) 

class Pet(FlaskForm):
        nomePet = StringField('nomePet', [validators.Length(min=4, max=25), validators.DataRequired()])
        nomePet = StringField('nomePet', [validators.Length(min=4, max=25), validators.DataRequired()])    
        dtNascPet = StringField('dtNascPet', [validators.Length(min=4, max=25), validators.DataRequired()]) 

       
          