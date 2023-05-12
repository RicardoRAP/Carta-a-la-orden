function ValidateBefore() {
  var valid = validateForm()
  if (!valid[0]) return showMessage(valid[1])
  try{
    var p = document.querySelector(".message-error")
    p.remove()
  }catch{}
  document.getElementById("DishForm").submit()
  return false;
}

function validateForm() {
  var x, y, z, i, j
  x = document.getElementById("DishForm")
  y = x.getElementsByTagName("input")
  z = x.getElementsByTagName("textarea")
  try{
    var p = document.querySelector(".message-error")
    p.remove()
  }catch{}
  for(j = 0; j < y.length; j++){
    y[j].classList.remove("invalid")
  }
  z[0].classList.remove("invalid")
  // valida los input por cada pestaña del formulario
  for (i = 0; i <= y.length; i++) {
    if(i < y.length){
      if (y[i].value == "" || y[i].value == " ") {
        if (y[i].type != "checkbox" && y[i].name != "tags" && y[i].name != "amount" && y[i].type != "file"){
          y[i].className += " invalid"
          return [false,"Uno de los campos está vacío."]
        }
      }
    }else{
      if (z[0].value == "") {
        z[0].className += " invalid"
        return [false, "De una descripción del platillo."]
      }
    } 
  }
  return [true, "Se ha guardado con exito."]
}

function showMessage(message){
  var form = document.querySelector("#DishForm")
  var lastnode = document.querySelector(".modal-bttn")
  var p = document.querySelector(".message-error")
  if (p == null){
    p = document.createElement("p")
    p.className = "message-error"
    p.textContent = message
    form.insertBefore(p,lastnode)
  }else{
    p.textContent = message
  }
  return false
}

var gallery = document.querySelectorAll(".gallery .item-img")
var newSelect = document.querySelector("input[name='updateSelect']")

gallery.forEach(item =>{
  item.addEventListener("click", async function(){
    var arryContent = ""
    if(item.classList.contains("select-img")){
      item.classList.remove("select-img")
    }else{
      item.classList.add("select-img")
    }
    document.querySelectorAll(".select-img").forEach(element =>{
      arryContent += element.id + ","
    })
    newSelect.value = arryContent.slice(0, -1)
  })
})

function ValidateUpdateImgBefore() {
  var valid = validateUpdateImgForm()
  if (!valid[0]) return showMessageUpdateImg(valid[1])
  try{
    var p = document.querySelector(".message-error")
    p.remove()
  }catch{}
  document.getElementById("DishImgUpdateForm").submit()
  return false;
}

function validateUpdateImgForm() {
  var x, y, i
  x = document.getElementById("DishImgUpdateForm")
  y = x.getElementsByTagName("input")
  try{
    var p = document.querySelector(".message-error")
    p.remove()
  }catch{}
  for (i = 0; i <= y.length; i++) {
    if(i < y.length){
      if ((y[i].value == "" || y[i].value == " " || y[i].value.split(',').length < 2) && y[i].type != 'hidden'){
        return [false,"Debe seleccionar por lo menos 2 imagenes."]
      }
    }
  }
  return [true, "Se ha guardado con exito."]
}

function showMessageUpdateImg(message){
  var form = document.querySelector("#DishImgUpdateForm")
  var lastnode = document.querySelectorAll(".modal-footer")[1]
  var p = document.querySelector(".message-error")
  if (p == null){
    p = document.createElement("p")
    p.className = "message-error"
    p.textContent = message
    form.insertBefore(p,lastnode)
  }else{
    p.textContent = message
  }
  return false
}

function ValidateUploadImgBefore() {
  var valid = validateUploadImgForm()
  if (!valid[0]) return showMessageUploadImg(valid[1])
  try{
    var p = document.querySelector(".message-error")
    p.remove()
  }catch{}
  document.getElementById("DishImgUploadForm").submit()
  return false;
}

function validateUploadImgForm() {
  var x, y, i
  x = document.getElementById("DishImgUploadForm")
  y = x.getElementsByTagName("input")
  try{
    var p = document.querySelector(".message-error")
    p.remove()
  }catch{}
  for (i = 0; i <= y.length; i++) {
    if(i < y.length){
      if ((y[i].value == "" || y[i].value == " ") && y[i].type != 'hidden'){
        return [false,"Debe seleccionar por lo menos una imagen."]
      }
    }
  }
  return [true, "Se ha guardado con exito."]
}

function showMessageUploadImg(message){
  var form = document.querySelector("#DishImgUploadForm")
  var lastnode = document.querySelectorAll(".modal-footer")[2]
  var p = document.querySelector(".message-error")
  if (p == null){
    p = document.createElement("p")
    p.className = "message-error"
    p.textContent = message
    form.insertBefore(p,lastnode)
  }else{
    p.textContent = message
  }
  return false
}

var input_multiple_img = document.querySelector('#upload-img')
var img = document.querySelector('#preview-imgs')

const readURL = file => {
  return new Promise((res, rej) => {
      const reader = new FileReader()
      reader.onload = e => res(e.target.result)
      reader.onerror = e => rej(e)
      reader.readAsDataURL(file)
  })
}

const Mutiplepreview = async function(input,target){
  var file, url, i, filesAmount, elementImg, reset_div
  reset_div = target.querySelectorAll(".current-img") 
  if (reset_div != []){
    reset_div.forEach(element =>{
      element.remove()
    })
  }
  if (input.files) {
    filesAmount = input.files.length;
    for (i = 0; i < filesAmount; i++) {
      file = input.files[i]
      url = await readURL(file)
      elementImg = document.createElement("img")
      elementImg.setAttribute("src", url)
      elementImg.setAttribute("id", i)
      elementImg.setAttribute("width", "100")
      elementImg.setAttribute("height", "100")
      elementImg.setAttribute("height", "100")
      elementImg.setAttribute("class", "current-img")
      target.appendChild(elementImg)
    }
  }
}

input_multiple_img.addEventListener('change', function(){
  Mutiplepreview(this, img)
})