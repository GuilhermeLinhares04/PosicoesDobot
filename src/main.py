from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB('caminhos.json')
robot_table = db.table('robot')

# Rota para listar as posições
@app.route('/')
def index():
    return render_template('index.html')

# Rota para postar as posições e guardá-las na database
@app.route('/novo', methods=['POST'])
def post():
    x = request.form['x']
    y = request.form['y']
    z = request.form['z']
    r = request.form['r']
    robot_table.insert({'x': x, 'y': y, 'z': z, 'r': r})
    caminhos = db.all()
    return render_template('index.html', x=x, y=y, z=z, r=r, caminhos=caminhos)

# Rota para receber o id do caminho e devolver as posições
@app.route('/pegar_caminho/<int:id>')
def caminho(id):
    robot = Query()
    result = robot_table.get(doc_id=id)
    return render_template('index.html', result=result)

# Rota para listar todos os caminhos
@app.route('/listar_caminhos')
def caminhos():
    caminhos = db.all()
    return render_template('index.html', caminhos=caminhos)

# Rota para atualizar as posições
@app.route('/atualizar_caminho/<int:id>', methods=['POST'])
def atualizar_caminho(id):
    robot = Query()
    x = request.form['x']
    y = request.form['y']
    z = request.form['z']
    r = request.form['r']
    robot_table.update({'x': x, 'y': y, 'z': z, 'r': r}, doc_ids=[id])
    return redirect(url_for('index'))

# Rota para deletar um caminho
@app.route('/deletar_caminho/<int:id>')
def deletar_caminho(id):
    robot_table.remove(doc_ids=[id])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)