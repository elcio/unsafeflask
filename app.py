from flask import Flask, request
from db import query
from datetime import datetime
import glob

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        skel = {
            'datahora': str(datetime.now())
        }
        skel.update(request.form)
        query(f'''
            INSERT INTO comentario
                (titulo, texto, datahora)
            VALUES
                ('%(titulo)s', '%(texto)s', '%(datahora)s')
        ''' % skel)

    comentarios = query('SELECT * FROM comentario ORDER BY datahora')
    comentarios_html = ''
    br = '\n'
    for comentario in comentarios:
        comentarios_html += f'''
            <div>
                <h2>{comentario["titulo"]}</h2>
                <p>{comentario["texto"].replace(br, '<br>')}</p>
                <p><em>{comentario["datahora"]}</em></p>
            </div>
            '''
    return f'''
        <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
        {comentarios_html}
        <form method='POST'>
            <input name="titulo" placeholder="Tĩtulo" /><br>
            <textarea name="texto" placeholder="Comentário"></textarea><br>
            <button>Enviar</button>
        </form>
        '''


def soma(a, b):
    return a + b

def produto(a, b):
    return a * b

def diferenca(a, b):
    return a - b


@app.route('/calc', methods=['GET', 'POST'])
def calc():
    resultado = ''
    if request.method == 'POST':
        fn = eval(request.form['op'])
        resultado = fn(eval(request.form['a']), eval(request.form['b']))
    return f'''
        <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
        <form method='POST'>
            <input name="a" type="number" />
            <select name="op">
                <option value="soma">+</option>
                <option value="produto">*</option>
                <option value="diferenca">-</option>
            </select>
            <input name="b" type="number" />
            <button>=</button>
            {resultado}
        </form>
        '''


@app.route('/files')
def files():
    filelist = [
        f'<a href="?f={f}">{f.split("/")[-1]}</a>'
        for f in glob.glob('dados/*')
    ]
    filelist = '<br>'.join(filelist)
    filecontent = ''
    if 'f' in request.args:
        filecontent = open(request.args['f']).read()
    return f'''
        <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
        <div style="display: flex">
            <div style="flex: 1">
                {filelist}
            </div>
            <div style="flex: 1">
                <pre>{filecontent}</pre>
            </div>
        </div>
        '''
