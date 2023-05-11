var currentTab = 0
showTab(currentTab)

function showTab(n) {
  var x = document.getElementsByClassName("contact-form__block")
  x[n].style.display = "block"
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none"
  } else {
    document.getElementById("prevBtn").style.display = "inline-block"
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").classList.add("d-none")
    document.getElementById("submitBtn").classList.remove("d-none")
  } else {
    document.getElementById("nextBtn").classList.remove("d-none")
    document.getElementById("submitBtn").classList.add("d-none")
  }
}

function nextPrev(n) {
  var x = document.getElementsByClassName("contact-form__block")
  var valid = validateForm()
  if (n == 1 && !valid[0]) return showMessage(valid[1])
  x[currentTab].style.display = "none"
  currentTab = currentTab + n
  try{
    var p = document.querySelector(".message-error")
    p.remove()
  }catch{}
  if (currentTab >= x.length) {
    var pass = x[currentTab-1].querySelectorAll("input.input-pass")
    for(var j = 0; j < pass.length; j++){
      pass[j].type = "password";
    }
    document.getElementById("regForm").submit()
    return false;
  }else{
    showTab(currentTab)
  }
}

function validateForm() {
  var x, y, i, z, patt, patt1, patt2, patt3, result, result1, result2, result3, result4;
  x = document.getElementsByClassName("contact-form__block")
  y = x[currentTab].getElementsByTagName("input")
  if(currentTab == 0){
    z = x[currentTab].getElementsByTagName("select")
  }
  try{
    var p = document.querySelector(".message-error")
    p.remove()
  }catch{}
  // valida los input por cada pestaña del formulario
  for (i = 0; i <= y.length; i++) {
    if(i < y.length){
      if (y[i].value == "" || y[i].value == " ") {
        y[i].className += " invalid"
        return [false,"Algún campo esta vacío."]
      }
      if(y[i].type == "email"){
        // valida el formato del email
        patt = new RegExp("^[a-zA-Z0-9\.\-\_]+[\@][a-zA-Z0-9]+[\.][a-zA-Z\-]{3,5}$", "g");
        result = patt.test(y[i].value)
        if(result == false){
          y[i].className += " invalid"
          return [false, "El email no cumple con el formato."]
        }
      }
      if(y[i].type == "tel"){
        // valida que el número de teléfono tenga 11 o mas números y es opcional el +
        patt = new RegExp("^[+]?[0-9]{11,}$", "g");
        result = patt.test(y[i].value)
        if(result == false){
          y[i].className += " invalid"
          return [false, "El formato del número de teléfono es invalido. ejemplo: XXXXXXXXXXX"]
        }
      }
      if(y[i].type == "password"){
        // valida que tenga 4 números
        patt1 = new RegExp("(?=(.*?[0-9]){4})", "g");
        result1 = patt1.test(y[i].value)
        // valida que tenga 4 letras
        patt2 = new RegExp("(?=(.*?[a-z-A-Z]){4})")
        result2 = patt1.test(y[i].value)
        // valida que tenga uno de los siguientes símbolos /, $, &, * y #
        patt3 = new RegExp("(?=(.*?([/]|[&]|[$]|[*]|[#])))")
        result3 = patt1.test(y[i].value)
        // valida que por lo menos tenga 9 caracteres
        result4 = y[i].value.length >= 9
        if(result1 == false || result2 == false || result3 == false || result4 == false){
          y[i].className += " invalid"
          return [false, "La contraseña debe tener por lo menos 9 caracteres, 4 números, 4 letras y alguno de estos símbolos /, $, &, * y #"]
        }
      }
      if (y[i].id == "registerCheck"){
        if(y[i].checked == false){
          return [false, "Acepte nuestros terminos y condiciones"]
        }
      }
    }else{
      if(currentTab == 0){
        if (z[0].value == "") {
          z[0].className += " invalid"
          return [false, "Seleccione uno de nuestros planes."]
        }
      }
    } 
  }
  return [true, "pass"]
}

function showMessage(message){
  var form = document.querySelector("#regForm")
  var p = document.querySelector(".message-error")
  if (p == null){
    p = document.createElement("p")
    p.className = "message-error"
    p.textContent = message
    form.appendChild(p)
  }else{
    p.textContent = message
  }
  return false
}

var select = document.querySelector("#registerPlan")
select.addEventListener("input",function(){
  if(this.classList.contains("invalid")){
    this.classList.remove("invalid")
  }
})
select.addEventListener("mouseover", function(){
  var tootlip = document.querySelector(".tootlip-plan")
  tootlip.classList.remove("d-none")
})
select.addEventListener("mouseout", function(){
  var tootlip = document.querySelector(".tootlip-plan")
  tootlip.classList.add("d-none")
})

function ShowPass(){
  var x = document.querySelectorAll(".input-pass");
  x.forEach(elem => {
    if (elem.type === "password") {
      elem.type = "text";
    } else {
      elem.type = "password";
    }
  })
}

