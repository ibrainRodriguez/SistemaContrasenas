(function () {

   
  
   window.onload = function () {

      $('[data-toggle="popover"]').popover();
      var formulario = document.getElementById("formulario");
      formulario.onsubmit = function (event) {
         var nombre = document.getElementById("nombre");
         var nick = document.getElementById("nick");
         var correo = document.getElementById("correo");
         var contra = document.getElementById("contra");
         var contrac = document.getElementById("contrac");
         var errores = document.getElementById("errores");

         var c = correo.value.trim();
         var expregc = /^\S{1,15}@\S{2,15}\.\S{2,9}$/;

         var p = contra.value.trim();
         
         var expreg = /^(?=(?:.*\d))(?=.*[A-Z])(?=.*[a-z])(?=.*[.,*!?@¿¡/#$%&])\S{8,20}$/;
         

         errores.innerHTML = "";
         if (nombre.value.trim() == "") {
            errores.innerHTML += "El nombre de usuario no puede estar vacío <br/>";
            $("#modelId").modal('show');
            event.preventDefault();
         }

         if (nick.value.trim() == "") {
            errores.innerHTML += "El nick no puede estar vacío <br/>";
            $("#modelId").modal('show');
            event.preventDefault();
         }

         if (correo.value.trim() == ""){
            errores.innerHTML += "El Correo no puede estar vacío <br/>";
            $("#modelId").modal('show');
            event.preventDefault();
         }
         
         if (!expregc.test(c)) {
            errores.innerHTML += "El correo debe cumplir con el formato: usuario@servidor.com<br/>";
            $("#modelId").modal('show');
            event.preventDefault();
         }

         if (contra.value.trim() == ""){
            errores.innerHTML += "La contraseña no puede estar vacía <br/>";
            $("#modelId").modal('show');
            event.preventDefault();
         }
         if (!expreg.test(p)) {
            errores.innerHTML +=
               'La contraseña no cumple con las politicas de seguridad<br/>';
            $("#modelId").modal('show');
            event.preventDefault(); // no se evía el formulario
         }

         if(contra.value.trim() != contra.value.trim()){
            errores.innerHTML +=
               "Las contraseñas no coinciden";
            $("#modelId").modal('show');
            event.preventDefault();
         }
         // checar que el pass tien números, mayúsculas, minúsculas y al menos un carácter especial (_,.,-,$)

    };
    
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
