function ValidateBefore() {
  var valid = validateForm()
  if (!valid[0]) return showMessage(valid[1])
  try{
    var p = document.querySelector(".message-error")
    p.remove()
  }catch{}
  document.getElementById("PromoForm").submit()
  return false;
}

function validateForm() {
  var x, y, z, i, j, img
  x = document.getElementById("PromoForm")
  y = x.getElementsByTagName("input")
  z = x.getElementsByTagName("select")
  img = document.querySelectorAll(".icon-upload-imgs img")
  try{
    var p = document.querySelector(".message-error")
    p.remove()
  }catch{}
  for(j = 0; j < y.length; j++){
    y[j].classList.remove("invalid")
    if(y[j].type == "file"){
      img[1].parentNode.classList.remove("invalid")
    }
  }
  z[0].classList.remove("invalid")
  z[1].classList.remove("invalid")
  // valida los input por cada pestaña del formulario
  for (i = 0; i <= y.length; i++) {
    if(i < y.length){
      if (y[i].value == "" || y[i].value == " ") {
        if(y[i].type == "file"){
          if (y[i].id == "Menu_promo_img"){
            img[1].parentNode.className += " invalid"
            return [false,"Ingrese la imagen de la promoción que veran los comensales."]
          }
        }else if (y[i].type != "checkbox" && y[i].name != "discount"){
          y[i].className += " invalid"
          return [false,"Uno de los campos está vacío."]
        }
      }
    }else{
      if (z[0].value == "") {
        z[0].className += " invalid"
        return [false, "Seleccione por lo menos un platillo."]
      }
      if (z[1].value == "") {
        z[1].className += " invalid"
        return [false, "Selecione por lo menos una sucursal o la sede principal."]
      }
    } 
  }
  return [true, "Se ha guardado con exito."]
}

function showMessage(message){
  var form = document.querySelector("#PromoForm")
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

var input_front_img = document.querySelector('#Menu_img')
var input_promo_img = document.querySelector('#Menu_promo_img')
var target1 = document.querySelector('.front-img .form-promo-img .icon-upload-imgs')
var target2 = document.querySelector('.promo_img .form-promo-img .icon-upload-imgs')

const readURL = file => {
  return new Promise((res, rej) => {
      const reader = new FileReader()
      reader.onload = e => res(e.target.result)
      reader.onerror = e => rej(e)
      reader.readAsDataURL(file)
  });
};

async function preview(input,target){
  try{
    var reset_div = target.querySelectorAll(".current-img") 
    if (reset_div != []){
      reset_div.forEach(element =>{
        element.remove()
      })
    }
  }catch{}
  const file = input.files[0]
  if (file != null){
    const url = await readURL(file)
    var elementImg = document.createElement("img")
    elementImg.setAttribute("src", url)
    elementImg.setAttribute("width", "100")
    elementImg.setAttribute("height", "100")
    elementImg.setAttribute("style", "position: absolute;background-color: #fff;")
    elementImg.setAttribute("class", "current-img")
    target.appendChild(elementImg)
    var elementImgEdit = document.createElement("img")
    elementImgEdit.setAttribute("src", "/static/img/icon/edit.png")
    elementImgEdit.setAttribute("width", "20")
    elementImgEdit.setAttribute("height", "20")
    var elementDivEdit = document.createElement("div")
    elementDivEdit.setAttribute("class","edit-img")
    elementDivEdit.appendChild(elementImgEdit)
    target.appendChild(elementDivEdit)
  }
}

input_front_img.addEventListener('change', async function(){
  await preview(this, target1) 
})
input_promo_img.addEventListener('change', async function(){
  await preview(this, target2) 
})

function SelectAll(id_select){
  document.querySelectorAll(id_select + " option").forEach(elem =>{
    elem.selected = true;
  })
}
function ResetAll(id_select){
  document.querySelectorAll(id_select + " option").forEach(elem =>{
    elem.selected = false;
  })
}

function validateFormAfter() {
  let form = document.forms[0]
  let brands = form['brands']
  let brands_value = brands.selectedOptions
  if (brands_value.length <= 0) {
    try{
      document.querySelectorAll(".text-error").forEach(elem => {
        elem.remove()
      })
    }catch{}
    brands.classList.add("invalid")
    error = document.createElement("p")
    error.setAttribute("class","text-error")
    error.innerText  = "Selecione por lo menos una sucursal o la sede principal"
    brands.parentNode.append(error)
    return false;
  }
  
}

async function ChangeInvalid(item_self){
  if(item_self.value != "" || item_self.value != " "){
    item_self.classList.remove("invalid")
    item_self.parentNode.querySelector(".text-error").remove()
  }
}
var i_invalid = document.querySelectorAll(".invalid")
i_invalid.forEach(element =>{
  element.addEventListener("change",async function(){
    await ChangeInvalid(element)
  })
})