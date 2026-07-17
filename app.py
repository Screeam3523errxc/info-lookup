from flask import Flask, render_template, request, jsonify, make_response, redirect
import requests
import json
import os
from datetime import datetime
import uuid
app = Flask(__name__)
ARCHIVO_VISITAS = "visitas.json"
ARCHIVO_VISITANTES = "visitantes.json"
ARCHIVO_LISTA_NEGRA = "lista_negra.json"
ARCHIVO_LISTA_BLANCA = "lista_blanca.json"
def cargar_visitantes():

    if os.path.exists(ARCHIVO_VISITANTES):

        with open(
            ARCHIVO_VISITANTES,
            "r",
            encoding="utf-8"
        ) as archivo:

            try:
                return json.load(archivo)

            except:

                return {}

    return {}
def guardar_visitantes(datos):

    with open(
        ARCHIVO_VISITANTES,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False
        )
def cargar_lista(archivo):

    if os.path.exists(archivo):

        with open(
            archivo,
            "r",
            encoding="utf-8"
        ) as f:

            try:
                return json.load(f)

            except:
                return []

    return []


def guardar_lista(archivo, datos):

    with open(
        archivo,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            datos,
            f,
            indent=4,
            ensure_ascii=False
        )
def obtener_visitor_id():

    visitor_id = request.cookies.get("visitor_id")

    if not visitor_id:

        visitor_id = str(uuid.uuid4())

    return visitor_id
def obtener_ip():

    return request.headers.get(
        "X-Forwarded-For",
        request.remote_addr
    )


def obtener_navegador():

    return request.headers.get(
        "User-Agent"
    )
def guardar_visita():

    visitor_id = obtener_visitor_id()

    visitantes = cargar_visitantes()

    ahora = datetime.now()

    ip = obtener_ip()

    navegador = obtener_navegador()


    if visitor_id in visitantes:

        visitante = visitantes[visitor_id]

        visitante["visitas"] += 1

        visitante["ultima_visita"] = ahora.strftime("%Y-%m-%d %H:%M")


        if ip not in visitante["ips"]:
            visitante["ips"].append(ip)


        if navegador not in visitante["navegadores"]:
            visitante["navegadores"].append(navegador)


    else:

        visitantes[visitor_id] = {

            "visitas": 1,

            "primera_visita": ahora.strftime("%Y-%m-%d %H:%M"),

            "ultima_visita": ahora.strftime("%Y-%m-%d %H:%M"),

            "ips": [
                ip
            ],

            "navegadores": [
                navegador
            ],

            "bloqueado": False

        }


    guardar_visitantes(visitantes)
    #aqui va el codigo que guarda las visitas
#visitaa


@app.route("/admin")
def admin():

    visitantes = cargar_visitantes()

    return render_template(
        "admin.html",
        visitantes=visitantes
    )
def esta_bloqueado(visitor_id, ip):

    lista_negra = cargar_lista(
        ARCHIVO_LISTA_NEGRA
    )

    if visitor_id in lista_negra:
        return True


    if ip in lista_negra:
        return True


    return False
@app.route("/")
def inicio():

    visitor_id = obtener_visitor_id()

    ip = obtener_ip()


    if esta_bloqueado(visitor_id, ip):

        return """
        <h1>🚫 Has sido bloqueado</h1>
        <p>El administrador ha restringido el acceso.</p>
        """


    guardar_visita()
    respuesta = make_response(
        render_template("index.html")
    )

    respuesta.set_cookie(

        "visitor_id",

        visitor_id,

        max_age=60*60*24*365

    )

    return respuesta


@app.route("/ip", methods=["POST"])
def buscar_ip():

    ip = request.json.get("ip")

    try:

        respuesta = requests.get(
            f"https://ipwho.is/{ip}"
        )

        datos = respuesta.json()


        if not datos.get("success"):
            return jsonify({
                "Error": "IP no válida"
            })


        resultado = {

            "IP": datos.get("ip"),

            "País": datos.get("country"),

            "Bandera": datos.get("flag", {}).get("emoji"),

            "Ciudad": datos.get("city"),

            "Región": datos.get("region"),

            "Continente": datos.get("continent"),

            "Código país": datos.get("country_code"),

            "ISP": datos.get("connection", {}).get("isp"),

            "Organización": datos.get("connection", {}).get("org"),

            "ASN": datos.get("connection", {}).get("asn"),

            "Zona horaria": datos.get("timezone", {}).get("id"),

            "Latitud": datos.get("latitude"),

            "Longitud": datos.get("longitude")

        }


        return jsonify(resultado)


    except Exception as e:

        return jsonify({
            "Error": str(e)
        })




@app.route("/telefono", methods=["POST"])
def buscar_telefono():

    numero = request.json.get("numero")


    limpio = numero.replace(" ","").replace("-","")


    datos = {}


    datos["Número"] = numero

    datos["Número limpio"] = limpio

    datos["Cantidad de dígitos"] = len(
        limpio.replace("+","")
    )



    if limpio.startswith("+52"):

        datos["País"] = "México 🇲🇽"

        datos["Código internacional"] = "+52"


        nacional = limpio[3:]


        datos["Prefijo"] = nacional[:2]


        if len(nacional) == 10:

            datos["Formato"] = "Correcto ✅"

        else:

            datos["Formato"] = "Revisar número ⚠️"



        prefijos_movil = [

            "55",
            "56",
            "81",
            "33",
            "44"

        ]


        if nacional[:2] in prefijos_movil:

            datos["Tipo probable"] = "Móvil 📱"

        else:

            datos["Tipo probable"] = "No identificado"



    elif limpio.startswith("+1"):


        datos["País"] = "Estados Unidos / Canadá 🇺🇸🇨🇦"

        datos["Código internacional"] = "+1"

        datos["Tipo probable"] = "No identificado"



    elif limpio.startswith("+34"):


        datos["País"] = "España 🇪🇸"

        datos["Código internacional"] = "+34"

        datos["Tipo probable"] = "No identificado"



    else:


        datos["País"] = "Desconocido"

        datos["Código internacional"] = "No detectado"



    return jsonify(datos)



@app.route("/desbloquear/<visitor_id>")
def desbloquear(visitor_id):

    lista_negra = cargar_lista(ARCHIVO_LISTA_NEGRA)

    if visitor_id in lista_negra:
        lista_negra.remove(visitor_id)

    guardar_lista(
        ARCHIVO_LISTA_NEGRA,
        lista_negra
    )

    return redirect("/admin")

@app.route("/bloquear/<visitor_id>")
def bloquear(visitor_id):

    lista_negra = cargar_lista(ARCHIVO_LISTA_NEGRA)

    if visitor_id not in lista_negra:
        lista_negra.append(visitor_id)

    guardar_lista(
        ARCHIVO_LISTA_NEGRA,
        lista_negra
    )

    return redirect("/admin")

# AQUÍ empieza el arranque del servidor
@app.route("/bloquear_ip/<ip>")
def bloquear_ip(ip):

    lista_negra = cargar_lista(
        ARCHIVO_LISTA_NEGRA
    )

    if ip not in lista_negra:
        lista_negra.append(ip)

    guardar_lista(
        ARCHIVO_LISTA_NEGRA,
        lista_negra
    )

    return redirect("/admin")
@app.route("/desbloquear_ip/<ip>")
def desbloquear_ip(ip):

    lista_negra = cargar_lista(
        ARCHIVO_LISTA_NEGRA
    )

    if ip in lista_negra:
        lista_negra.remove(ip)

    guardar_lista(
        ARCHIVO_LISTA_NEGRA,
        lista_negra
    )

    return redirect("/admin")
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

