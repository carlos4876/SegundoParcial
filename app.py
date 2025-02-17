from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'

def generar_id():
    if 'productos' in session and len(session['productos']) > 0:
        return max(item['id'] for item in session['productos']) + 1
    return 1

@app.route("/", methods=['GET', 'POST'])
def index():
    if 'productos' not in session:
        session['productos'] = []
    return render_template('index.html', productos=session['productos'])

@app.route("/nuevo", methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        nuevo_producto = {
            'id': generar_id(),
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }
        
        if 'productos' not in session:
            session['productos'] = []
        
        session['productos'].append(nuevo_producto)
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('nuevo_producto.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    productos = session.get('productos', [])
    producto = next((p for p in productos if p['id'] == id), None)
    
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('editar.html', producto=producto)

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    productos = session.get('productos', [])
    producto = next((p for p in productos if p['id'] == id), None)
    
    if producto:
        session['productos'].remove(producto)
        session.modified = True
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)