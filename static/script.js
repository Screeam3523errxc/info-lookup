let modo = "ip";


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


    document.getElementById("loading").style.display="block";

    document.getElementById("resultado").innerHTML="";


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


        mostrarDatos(datos);



    }catch(error){


        document.getElementById("loading").style.display="none";


        document.getElementById("resultado").innerHTML =
        "<h2>Error de conexión</h2>";

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
