from flask import make_response,Blueprint
from models import Tabelaos, Usuarios
import csv
from io import StringIO
exp_bp=Blueprint('exportacao',__name__)

@exp_bp.route('/exportCSV')
def exportarTabela():
    tabelaexp = Tabelaos.query.all()
    si = StringIO()
    cw = csv.writer(si)
    nomeColunas = Tabelaos.__table__.columns.keys()
    nomeColunas.append('nome emissor')
    cw.writerow(nomeColunas)    
    for os in tabelaexp:
        usr=Usuarios.query.filter_by(id=os.id_usuario).first()
        cw.writerow([
            os.id, os.tipomanutencao, os.setor, os.datahoraabertura, os.maquina, 
            os.nivelurgencia, os.motivourgencia, os.tipo,
            os.descricaodoproblema, os.datahoraexecucao, os.descricaoservico,
            os.trocadeitens, os.nomeitem1, os.nomeitem2, os.nomeitem3, os.nomeitem4,
            os.nomeitem5, os.nomeitem6, os.nomeitem7, os.nomeitem8, os.nomeitem9,
            os.nomeitem10, os.nomeitem11, os.nomeitem12, os.nomeitem13, os.nomeitem14,
            os.nomeitem15, os.qtditem1, os.qtditem2, os.qtditem3, os.qtditem4,
            os.qtditem5, os.qtditem6, os.qtditem7, os.qtditem8, os.qtditem9,
            os.qtditem10, os.qtditem11, os.qtditem12, os.qtditem13, os.qtditem14,
            os.qtditem15, os.houveparada, os.manutentor, os.finalizada, os.datahorainicio,
            os.manutentor2,os.manutentor3,os.id_usuario,usr.nome
        ])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    
    return output