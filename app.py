from flask import Flask, request
from db import query
from datetime import datetime
import glob

app = Flask(__name__)

HEADER = """
<link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
<nav>
    <a href="/">Comentários</a>
    <a href="/busca">Busca</a>
    <a href="/calc">Calculadora</a>
    <a href="/files">Arquivos</a>
    <a href="/svg">SVG</a>
</nav>
"""

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
        {HEADER}
        {comentarios_html}
        <form method='POST'>
            <input name="titulo" placeholder="Tĩtulo" /><br>
            <textarea name="texto" placeholder="Comentário"></textarea><br>
            <button>Enviar</button>
        </form>
        '''


@app.route('/busca')
def busca():
    comentarios=[]
    if 'q' in request.args:
        comentarios = query(f'''SELECT *
                                FROM comentario
                                WHERE titulo LIKE '%{request.args["q"]}%'
                                ORDER BY datahora''')
    tbl_comentarios = ''
    for comentario in comentarios:
        tbl_comentarios += f'''
            <tr>
                <td>{comentario['titulo']}</td>
                <td>{comentario['texto']}</td>
                <td>{comentario['datahora']}</td>
            </tr>
        '''
    return f'''
        {HEADER}
        <form>
            <input name="q" placeholder="Buscar" />
            <button>Buscar</button>
        </form>
        <table>
            {tbl_comentarios}
        </table>
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
        {HEADER}
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
        {HEADER}
        <div style="display: flex">
            <div style="flex: 1">
                {filelist}
            </div>
            <div style="flex: 1">
                <pre>{filecontent}</pre>
            </div>
        </div>
        '''


@app.route('/svg')
def svg():
    return f'''
        {HEADER}
        <svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
        <polygon id="triangle" points="0,0 0,50 50,0" fill="#009900" stroke="#004400"/>
        <script type="text/javascript">
            alert("XSS Here!");
        </script>
        </svg>'''
