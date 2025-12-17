from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

def gerar_horarios_por_dia(data_str):
    horarios = []
    data_obj = datetime.strptime(data_str, '%Y-%m-%d')
    agora = datetime.now()
    dia_semana = data_obj.weekday()  # 0=Segunda, 5=Sábado, 6=Domingo

    # 1. Definir o fecho do expediente
    hora_inicio = 8
    if dia_semana <= 4:    # Segunda a Sexta
        hora_fim = 21
    elif dia_semana == 5:  # Sábado
        hora_fim = 16
    else:                  # Domingo
        return []

    atual = data_obj.replace(hour=hora_inicio, minute=0, second=0, microsecond=0)
    fim_expediente = data_obj.replace(hour=hora_fim, minute=0, second=0, microsecond=0)

    # 2. Gerar horários respeitando a duração de 1h + 15min de intervalo
    while atual + timedelta(minutes=60) <= fim_expediente:
        # TRAVA: Só adiciona o horário se (Data for futura) OU (Data for hoje E hora for maior que agora)
        if data_obj.date() > agora.date() or atual > agora:
            horarios.append(atual.strftime('%H:%M'))
        
        atual += timedelta(minutes=75)
    
    return horarios

@app.route('/')
def index():
    hoje = datetime.now().strftime('%Y-%m-%d')
    horarios_iniciais = gerar_horarios_por_dia(hoje)
    return render_template('index.html', horarios=horarios_iniciais, hoje=hoje)

@app.route('/atualizar_horarios', methods=['POST'])
def atualizar_horarios():
    data_selecionada = request.json.get('data')
    horarios = gerar_horarios_por_dia(data_selecionada)
    return jsonify(horarios=horarios)

@app.route('/confirmar', methods=['POST'])
def confirmar():
    nome = request.form.get('nome')
    whatsapp = request.form.get('whatsapp')
    hora = request.form.get('hora')
    data = request.form.get('data')
    data_br = datetime.strptime(data, '%Y-%m-%d').strftime('%d/%m/%Y')
    
    return f"""
    <body style="font-family:sans-serif; background-color:#fdfcfb; display:flex; justify-content:center; align-items:center; height:100vh; margin:0; color:#4a4a4a;">
        <div style="text-align:center; padding:40px; background:white; border-radius:20px; box-shadow:0 10px 25px rgba(0,0,0,0.05); max-width:400px;">
            <h2 style="color:#72a1a1;">Solicitação Enviada!</h2>
            <p>Olá, <b>{nome}</b>.</p>
            <p>Seu pré-agendamento para <b>{data_br}</b> às <b>{hora}</b> foi recebido com sucesso.</p>
            <p>A Gilciane entrará em contato via WhatsApp ({whatsapp}).</p>
            <a href="/" style="display:inline-block; margin-top:20px; padding:10px 20px; background:#8fb9a8; color:white; text-decoration:none; border-radius:10px;">Voltar</a>
        </div>
    </body>
    """

if __name__ == '__main__':
    app.run(debug=True)