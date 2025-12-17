from flask import Flask, render_template, request, url_for
from datetime import datetime, timedelta

app = Flask(__name__)

def gerar_horarios():
    horarios = []
    # Segunda a sexta: 08:00 às 18:00
    atual = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    fim_expediente = atual.replace(hour=18)

    while atual + timedelta(minutes=60) <= fim_expediente:
        horarios.append(atual.strftime('%H:%M'))
        # 60 min de sessão + 15 min de intervalo
        atual += timedelta(minutes=75) 
    return horarios

@app.route('/')
def index():
    horarios = gerar_horarios()
    return render_template('index.html', horarios=horarios)

@app.route('/confirmar', methods=['POST'])
def confirmar():
    nome = request.form.get('nome')
    whatsapp = request.form.get('whatsapp')
    hora = request.form.get('hora')
    
    return f"""
    <div style="text-align:center; margin-top:50px; font-family:sans-serif; color:#4a4a4a;">
        <h2>Obrigado, {nome}!</h2>
        <p>Seu agendamento para às <b>{hora}</b> foi recebido.</p>
        <p>A terapeuta Gilciane entrará em contato pelo número {whatsapp}.</p>
        <a href="/">Voltar ao início</a>
    </div>
    """

if __name__ == '__main__':
    app.run(debug=True)