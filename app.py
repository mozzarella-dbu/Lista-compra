from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate


app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///basededatos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


db=SQLAlchemy(app)
migrate=Migrate(app, db)

class Productos(db.Model):
    __tablename__="Productos"

    id=db.Column(db.Integer, primary_key=True)
    Producto=db.Column(db.String(20), unique=True, nullable=False)
    Cantidades=db.Column(db.Integer, nullable=False)


def añadir_producto(producto, cantidades):
    with app.app_context():
        print("Añadiendo producto:", producto)
        nuevo_producto=Productos(Producto=producto, Cantidades=cantidades)
        db.session.add(nuevo_producto)
        db.session.commit()
        print("Producto agregado correctamente")


@app.route("/", methods=["GET", "POST"])
def index():
    mensaje=""
    if request.method=="POST":
        producto=request.form.get("Producto")
        cantidad=request.form.get("Cantidad")
        
        comprobacion=Productos.query.filter_by(Producto=producto).first()
        if comprobacion:
            mensaje="El producto introducido ya está en la lista, prueba de nuevo"
        else:
            nuevo_producto=Productos(Producto=producto, Cantidades=cantidad)
            db.session.add(nuevo_producto)
            db.session.commit()
            mensaje="El producto y su cantidad se ha ingresado correctamente"
    
    productos=Productos.query.all()

    return render_template("index.html", mensaje=mensaje, productos=productos)

@app.route("/eliminar/<Producto>", methods=["GET", "POST"])
def eliminar(Producto):
    
    producto=Productos.query.filter_by(Producto=Producto).first()
    if producto:
        db.session.delete(producto)
        db.session.commit()
        mensaje="Producto eliminado"
    else:
        mensaje="El producto especificado no se encontró"
    productos=Productos.query.all()
    return render_template("index.html", mensaje=mensaje, productos=productos)


if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
    with app.app_context():
        db.create_all()
    app.run(debug=True, use_reloader=True)
