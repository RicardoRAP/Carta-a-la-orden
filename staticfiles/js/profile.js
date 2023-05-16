var input_profile_img = document.querySelector('#formProfile_img')
var img = document.querySelector('.form-profile-img .current-img')

const readURL = file => {
  return new Promise((res, rej) => {
      const reader = new FileReader();
      reader.onload = e => res(e.target.result);
      reader.onerror = e => rej(e);
      reader.readAsDataURL(file);
  });
};

const preview = async event => {
  const file = event.target.files[0];
  const url = await readURL(file);
  img.src = url;
};

input_profile_img.addEventListener('change', preview);

var address = document.querySelectorAll('.address')
var full = document.querySelector('input#saveFull_address')
var show_full = document.querySelector('input#showFull_address')

function FullAddress(){
  var dir = ""
  address.forEach((element) => {
    if (element.value != ''){
      dir += element.value + ', '
    }
  })
  dir = dir.slice(0, -2);
  return dir
}

address.forEach((item) => {
  item.addEventListener('input', function(e){
    var dir = FullAddress()
    full.value = dir
    show_full.value = dir
  })
})

var others_serv = document.querySelectorAll('input.others-serv')
var others_s = document.querySelector('input#saveDelivery')

others_serv[0].addEventListener('click', function(e){
  if(this.checked || others_serv[1].checked){
    others_s.parentElement.classList.remove("d-none")
  }
  else{
    others_s.parentElement.classList.add("d-none")
    others_s.value = ''
  }
})
others_serv[1].addEventListener('click', function(e){
  if(this.checked || others_serv[0].checked){
    others_s.parentElement.classList.remove("d-none")
  }
  else{
    others_s.parentElement.classList.add("d-none")
    others_s.value = ''
  }
})
window.addEventListener('load', function(e){
  var dir = FullAddress()
  show_full.value = dir

  if(others_serv[1].checked || others_serv[0].checked){
    others_s.parentElement.classList.remove("d-none")
  }
  else{
    others_s.parentElement.classList.add("d-none")
    others_s.value = ''
  }
})
function ValidateBefore() {
  var valid = validateForm()
  if (!valid[0]) return showMessage(valid[1])
  try{
    var p = document.querySelector(".message-error")
    p.remove()
  }catch{}
  document.getElementById("FormProfile").submit()
  return false;
}

function validateForm() {
  var v, w, x, y, z, i, j, img, patt, result
  x = document.getElementById("FormProfile")
  y = x.getElementsByTagName("input")
  z = x.getElementsByTagName("select")
  img = document.querySelector(".current-img")
  try{
    var p = document.querySelector(".message-error")
    p.remove()
  }catch{}
  for(j = 0; j < y.length; j++){
    y[j].classList.remove("invalid")
    if(y[j].type == "file"){
      img.parentNode.classList.remove("invalid")
    }
  }
  z[0].classList.remove("invalid")
  z[1].classList.remove("invalid")
  // valida los input por cada pestaña del formulario
  for (i = 0; i <= y.length; i++) {
    if(i < y.length){
      if (y[i].value == "" || y[i].value == " ") {
        y[i].className += " invalid"
        if(y[i].type == "file"){
          if (img.src.toString().includes("/restaurants/profile.png")){
            img.parentNode.className += " invalid"
            return [false,"Ingrese una imagen"]
          }
        }else if (y[i].type != "checkbox" && y[i].name != "delivery"){
          return [false,"Uno de los campos está vacío"]
        }
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
    }else{
      if (z[0].value == "") {
        z[0].className += " invalid"
        return [false, "Seleccione un Estado."]
      }
      if (z[1].value == "") {
        z[1].className += " invalid"
        return [false, "Seleccione uno de nuestros planes."]
      }
    } 
  }
  w = x.querySelectorAll("input[type='checkbox']")
  v = x.querySelector("input[name='delivery']")
  if (w[0].checked == false && w[1].checked == false && w[2].checked == false && w[3].checked == false){
    if(w[0].checked == false){
      w[0].className += " invalid"
    }
    if(w[1].checked == false){
      w[1].className += " invalid"
    }
    if(w[2].checked == false){
      w[2].className += " invalid"
    }
    if(w[3].checked == false){
      w[3].className += " invalid"
    }
    return [false, "Marque que tipo de servicio posee"]
  }else if(w[2].checked || w[3].checked){
    if(v.value == "" || v.value == " "){
      v.className += " invalid"
      return [false, "Indique que tipo de servicio posse"]
    }
  }
  return [true, "Se ha guardado con exito"]
}

function showMessage(message){
  var form = document.querySelector("#FormProfile")
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

var select = document.querySelector("#savePlan")
var selectState = document.querySelector("#saveState")
selectState.addEventListener("input",function(){
  if(this.classList.contains("invalid")){
    this.classList.remove("invalid")
  }
})
select.addEventListener("input",function(){
  if(this.classList.contains("invalid")){
    this.classList.remove("invalid")
  }
})
window.addEventListener("load", ValideateMessage)
function ValideateMessage(){
  let text, inputerror
  var messages = document.querySelectorAll(".message-error")
  if (messages.length >= 1){
    for(var i = 0; i < messages.length; i++){
      text = messages[i].textContent
      if(text.includes("nombre de usuario")){
        inputerror = document.querySelector("input[name='username']")
        if(!inputerror.classList.contains("invalid")){
          inputerror.classList.add("invalid")
        }
      }
      if(text.includes("email")){
        inputerror = document.querySelector("input[name='email']")
        if(!inputerror.classList.contains("invalid")){
          inputerror.classList.add("invalid")
        }
      }
      if(text.includes("mayor o igual")){
        inputerror = document.querySelector("input[name='start_schedule']")
        if(!inputerror.classList.contains("invalid")){
          inputerror.classList.add("invalid")
        }
        inputerror = document.querySelector("input[name='end_schedule']")
        if(!inputerror.classList.contains("invalid")){
          inputerror.classList.add("invalid")
        }
      }
    }
  }
}