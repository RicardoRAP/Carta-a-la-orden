var input_menu_img = document.querySelector('#Menu_img')
var target = document.querySelector('.form-menu-img .icon-upload-imgs')

const readURL = file => {
  return new Promise((res, rej) => {
      const reader = new FileReader()
      reader.onload = e => res(e.target.result)
      reader.onerror = e => rej(e)
      reader.readAsDataURL(file)
  });
};

const preview = async event => {
  try{
    var reset_div = target.querySelectorAll(".current-img") 
    if (reset_div != []){
      reset_div.forEach(element =>{
        element.remove()
      })
    }
  }catch{}
  const file = event.target.files[0]
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

input_menu_img.addEventListener('change', preview)

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

function validateForm() {
  let form = document.forms[0]
  let brands = form['brands']
  let brands_value = brands.selectedOptions
  let in_principal = form['in_principal']
  let in_principal_value = in_principal.checked
  console.log(in_principal_value, brands_value.length)
  if (in_principal_value == false && brands_value.length <= 0) {
    try{
      document.querySelectorAll(".text-error").forEach(elem => {
        elem.remove()
      })
    }catch{}
    if (brands_value.length <= 0){
      brands.classList.add("invalid")
      error = document.createElement("p")
      error.setAttribute("class","text-error")
      error.innerText  = "Seleccione una sucursal"
      brands.parentNode.append(error)
    }
    if (in_principal_value == false){
      in_principal.classList.add("invalid")
      error = document.createElement("p")
      error.setAttribute("class","text-error")
      error.innerText  = "Active la sede principal"
      in_principal.parentNode.append(error)
    }
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