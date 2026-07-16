from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
import os
from datetime import datetime
import uuid
app = Flask(__name__)
ARCHIVO_VISITAS = "visitas.json"
ARCHIVO_VISITANTES = "visitantes.json"
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

    if os.path.exists(ARCHIVO_VISITAS):

        with open(ARCHIVO_VISITAS, "r", encoding="utf-8") as archivo:

            try:
                visitas = json.load(archivo)
            except:
                visitas = []

    else:
        visitas = []

    return render_template("admin.html", visitas=visitas)
    visita = {
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "hora": datetime.now().strftime("%H:%M"),
        "ip": request.remote_addr,
        "navegador": request.headers.get("User-Agent")
    }

    visitas = []

    if os.path.exists(ARCHIVO_VISITAS):

        with open(ARCHIVO_VISITAS, "r", encoding="utf-8") as archivo:

            try:
                visitas = json.load(archivo)
            except:
                visitas = []

    hoy = datetime.now().strftime("%Y-%m-%d")

    visitas = [v for v in visitas if v["fecha"] == hoy]

    visitas.append(visita)

    with open(ARCHIVO_VISITAS, "w", encoding="utf-8") as archivo:

        json.dump(visitas, archivo, indent=4, ensure_ascii=False)

@app.route("/")
def inicio():

    visitor_id = obtener_visitor_id()

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




if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
