let modo = "ip";
function cambiarLucas(imagen, mensaje){

    document.getElementById("lucas").src =
    "/static/" + imagen + "?t=" + Date.now();

    document.getElementById("lucas-dialogo").innerHTML =
    "🦆 " + mensaje;

}

function mostrarIP(){

    modo = "ip";

    document.getElementById("entrada").placeholder = "8.8.8.8";

}


function mostrarTelefono(){

    modo = "telefono";

    document.getElementById("entrada").placeholder = "+525512345678";

}



async function buscarIP(){


    let valor = document.getElementById("entrada").value;


    if(valor.trim() === ""){

        alert("Escribe un dato");

        return;

    }


document.getElementById("loading").style.display="flex";
    document.getElementById("resultado").innerHTML="";
cambiarLucas(
    "lucas_hacker.png",
    "Analizando información..."
);

    let url="";
    let cuerpo={};



    if(modo === "ip"){

        url="/ip";

        cuerpo={
            ip:valor
        };


    }else{


        url="/telefono";

        cuerpo={
            numero:valor
        };
	

    }



    try{


        let respuesta = await fetch(url,{

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify(cuerpo)

        });



        let datos = await respuesta.json();


        document.getElementById("loading").style.display="none";
setTimeout(() => {

    cambiarLucas(
        "lucas_idle.png",
        "¡Encontré información!"
    );

}, 1500);

        mostrarDatos(datos);



    }catch(error){


        document.getElementById("loading").style.display="none";


        document.getElementById("resultado").innerHTML =
        "<h2>Error de conexión</h2>";
cambiarLucas(
    "lucas_confundido.png",
    "Algo salió mal..."
);
    }


}





function mostrarDatos(datos){


    let html="";


    for(let dato in datos){


        html += `

        <div class="card">

            <h3>${dato}</h3>

            <p>${datos[dato] ?? "N/D"}</p>

        </div>

        `;


    }


    document.getElementById("resultado").innerHTML=html;


}
