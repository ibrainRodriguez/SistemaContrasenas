(function () {

   
  


    window.onload = function () {
        var renovar = document.getElementById("renovar");
        renovar.onclick = function(){
            $("#modelI").modal('toggle');
        }
    };
 })();
 
 /* $(function(){
    alert("hola mundo");
    $("form").submit(function(event){
       errores.innerHTML = "";//limpiar errores
       alert("hola mundo2");
       errores.innerHTML += "Nombre no puede estar vacio"
       event.preventDefault();
       $("#modelId").modal('show')
    });
 }); */
 