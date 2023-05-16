function ValidateBefore() {
  var valid = validateForm()
  if (!valid[0]) return showMessage(valid[1])
  try{
    var p = document.querySelector(".message-error")
    p.remove()
  }catch{}
  document.getElementById("FormBrand").submit()
  return false;
}

function validateForm() {
  var s, v, w, x, y, z, i, j, hms, hms2, target, target2
  var now = new Date()
  var nowDateTime = now.toISOString()
  var nowDate = nowDateTime.split('T')[0]
  x = document.getElementById("FormBrand")
  y = x.getElementsByTagName("input")
  s = x.getElementsByTagName("select")
  try{
    var p = document.querySelector(".message-error")
    p.remove()
  }catch{}
  for(j = 0; j < y.length; j++){
    y[j].classList.remove("invalid")
  }
  s[0].classList.remove("invalid")
  // valida los input del formulario
  for (i = 0; i <= y.length; i++) {
    if(i < y.length){
      if (y[i].value == "" || y[i].value == " ") {
        y[i].className += " invalid"
        if (y[i].type != "checkbox" && y[i].name != "delivery" && y[i].type != "hidden" && y[i].id != "showFull_address"){
          return [false,"Uno de los campos está vacío."]
        }
      }
    }else{
      if (s[0].value == "") {
        s[0].className += " invalid"
        return [false, "Seleccione un Estado."]
      }
    }
  }
  z = x.querySelectorAll("input[type='time']")
  console.log(z)
  hms = z[0].value
  hms2 = z[1].value
  target = new Date(nowDate + 'T' + hms)
  target2 = new Date(nowDate + 'T' + hms2)
  if(target >= target2){
    z[0].className += " invalid"
    z[1].className += " invalid"
    return [false, "El comienzo del horario no puede ser mayor o igual al final del horario."]
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
    return [false, "Marque que tipo de servicio posee."]
  }else if(w[2].checked || w[3].checked){
    if(v.value == "" || v.value == " "){
      v.className += " invalid"
      return [false, "Indique que tipo de servicio posse."]
    }
  }
  return [true, "Se ha guardado con exito."]
}

function showMessage(message){
  var form = document.querySelector("#FormBrand")
  var lastnode = document.querySelector(".modal-bttn")
  var p = document.querySelector(".message-error")
  if (p == null){
    p = document.createElement("p")
    p.className = "message-error mb-2"
    p.textContent = message
    form.insertBefore(p,lastnode)
  }else{
    p.textContent = message
  }
  return false
}

var selectState = document.querySelector("#registerState")
selectState.addEventListener("input",function(){
  if(this.classList.contains("invalid")){
    this.classList.remove("invalid")
  }
})

var others_serv = document.querySelectorAll('input.others-serv')
var others_s = document.querySelector('input#registerDelivery')

others_serv[0].addEventListener('click', function(e){
  if(this.checked || others_serv[1].checked){
    others_s.parentElement.classList.remove("d-none")
  }
  else{
    others_s.parentElement.classList.add("d-none")
    others_s.value = ""
  }
})
others_serv[1].addEventListener('click', function(e){
  if(this.checked || others_serv[0].checked){
    others_s.parentElement.classList.remove("d-none")
  }
  else{
    others_s.parentElement.classList.add("d-none")
    others_s.value = ""
  }
})

var address = document.querySelectorAll('.address')
var full = document.querySelector('input#registerFull_address')
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