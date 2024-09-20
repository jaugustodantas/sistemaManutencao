from flask_wtf import FlaskForm
from wtforms import StringField, validators,DateTimeField,SubmitField,TextAreaField
from datetime import datetime

class FormularioAbriOs(FlaskForm):
    nomeMaquina = StringField('Máquina',[validators.data_required()])
    setor = StringField('Setor',[validators.data_required()])
    motivoUrgencia = StringField('Máquina')
    descricao = TextAreaField('Descrição do serviço', [validators.data_required()])
    enviar = SubmitField('Enviar')

class FormularioFecharOs(FlaskForm):
    descricaoDoServico = TextAreaField('Descrição do serviço',[validators.data_required()])
    inicioManutencao = DateTimeField("Início da manutenção (dd:mm:aaaa HH:MM)",format='%d/%m/%Y %H:%M',validators=[validators.DataRequired()])
    fimManutencao = DateTimeField("Fim da manutenção (dd:mm:aaaa HH:MM)",format='%d/%m/%Y %H:%M',validators=[validators.DataRequired()])
    manutentor1 = StringField('Manutentor 1',[validators.data_required()])
    manutentor2 = StringField('Manutentor 2',[validators.data_required()])
    manutentor3 = StringField('Manutentor 3')
    enviar = SubmitField('Enviar')

class FomularioEstoque(FlaskForm):
    nomeDoItem = StringField('Nome do item',[validators.data_required()])
    quantidade = StringField('Quantidade do item',[validators.data_required()])
    codigoDoItem = StringField('Código do item')
    enviar = SubmitField('Enviar')