from flask import Flask, render_template, request, jsonify
import requests


app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")



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
