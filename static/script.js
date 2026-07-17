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

if(modo === "ip"){

    let ipValida =
    /^(\d{1,3}\.){3}\d{1,3}$/.test(valor);

    if(!ipValida){

   cambiarLucas(
    "lucas_confundido.png",
    "Eso no parece una IP 🥺"
);


setTimeout(() => {

    cambiarLucas(
        "lucas_idle.png",
        "Listo para otra búsqueda 🦆"
    );

}, 1500);

        document.getElementById("resultado").innerHTML =
        "<h2>IP no válida</h2>";

        return;

    }

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
const frasesLucas = [

    "Esperando una nueva búsqueda 🦆",
    "Cuac cuac, todo tranquilo por aquí",
    "Lucas está vigilando los datos 👀",
    "Los patos también investigan misterios",
    "Preparando mis poderes de pato ⚡"

];

setInterval(()=>{

    let frase =
    frasesLucas[
        Math.floor(Math.random() * frasesLucas.length)
    ];


    cambiarLucas(
        "lucas_idle.png",
        frase
    );


},15000);

let tiempoInactivo;


function reiniciarLucas(){

    clearTimeout(tiempoInactivo);


    tiempoInactivo = setTimeout(()=>{

        let frase =
        frasesLucas[
            Math.floor(
                Math.random() * frasesLucas.length
            )
        ];


        cambiarLucas(
            "lucas_idle.png",
            frase
        );


    },15000);

}
