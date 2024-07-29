from flask import render_template, request, redirect, url_for, send_file, make_response
from app import app, db
from models import Producto
import pandas as pd
import pdfkit
from io import BytesIO

@app.route('/')
def index():
    total_productos = Producto.query.count()
    productos_en_stock = Producto.query.filter(Producto.cantidad > 0).count()
    productos_bajo_stock = Producto.query.filter(Producto.cantidad <= Producto.min_stock).count()
    return render_template('index.html', 
                           total_productos=total_productos, 
                           productos_en_stock=productos_en_stock, 
                           productos_bajo_stock=productos_bajo_stock)


@app.route('/productos')
def productos():
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)

@app.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        min_stock = request.form['min_stock']
        nuevo_producto = Producto(nombre=nombre, precio=precio, cantidad=cantidad, min_stock=min_stock)
        db.session.add(nuevo_producto)
        db.session.commit()
        return redirect(url_for('productos'))
    return render_template('nuevo_producto.html')

@app.route('/producto/<int:id>/editar', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio = request.form['precio']
        producto.cantidad = request.form['cantidad']
        producto.min_stock = request.form['min_stock']
        db.session.commit()
        return redirect(url_for('productos'))
    return render_template('editar_producto.html', producto=producto)

@app.route('/producto/<int:id>/eliminar', methods=['POST'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('productos'))

@app.route('/reportes')
def reportes():
    productos = Producto.query.all()
    return render_template('reportes.html', productos=productos)

@app.route('/download_report/<file_type>')
def download_report(file_type):
    productos = Producto.query.all()
    
    data = {
        'ID': [producto.id for producto in productos],
        'Nombre': [producto.nombre for producto in productos],
        'Precio': [producto.precio for producto in productos],
        'Cantidad': [producto.cantidad for producto in productos],
        'Min Stock': [producto.min_stock for producto in productos]
    }
    
    if file_type == 'excel':
        df = pd.DataFrame(data)
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        writer.save()
        output.seek(0)
        
        return send_file(output, download_name='reporte_productos.xlsx', as_attachment=True)

    elif file_type == 'pdf':
        html = render_template('reporte_pdf.html', productos=productos)
        pdf = pdfkit.from_string(html, False)
        
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=reporte_productos.pdf'
        return response

    return redirect(url_for('reportes'))
