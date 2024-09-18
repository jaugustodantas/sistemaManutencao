from flask_wtf import FlaskForm
from wtforms import StringField, validators,DateTimeField,SubmitField,TextAreaField
from datetime import datetime

def validacaoData(form,field):
    if form.inicioManutencao.data > form.fimManutencao.data:
        raise validators.ValidationError("A data do fim não pode ser menor que a do começo")

class FormularioAbriOs(FlaskForm):
    nomeMaquina = StringField('Máquina',[validators.data_required()])
    setor = StringField('Setor',[validators.data_required()])
    motivoUrgencia = StringField('Máquina')
    descricao = TextAreaField('Descrição do serviço', [validators.data_required()])
    enviar = SubmitField('Enviar')

class FormularioFecharOs(FlaskForm):
    descricaoDoServico = ('Descrição do serviço',[validators.data_required()])
    inicioManutencao = DateTimeField("Início da manutenção (dd:mm:aaaa HH:MM)",format='%d/%m/%Y hh:mm',validators=[validators.DataRequired()])
    fimManutencao = DateTimeField("Fim da manutenção (dd:mm:aaaa HH:MM)",format='%d/%m/%Y hh:mm',validators=[validators.DataRequired(),validacaoData])
    enviar = SubmitField('Enviar')