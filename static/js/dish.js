var input_multiple_img = document.querySelector('#multipleImg')
var img = document.querySelector('.form-multiple-img')

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
      elementImg.setAttribute("style", "object-fit: contain;")
      elementImg.setAttribute("class", "current-img")
      target.appendChild(elementImg)
    }
  }
}

input_multiple_img.addEventListener('change', function(){
  Mutiplepreview(this, img)

})

async function ChangeInput(item_self){
  if(item_self.value != "" || item_self.value != " "){
    try{
      if(item_self.id == "multipleImg"){
        item_self.parentNode.querySelector(".icon-upload-imgs").classList.remove("error-multi-imgs")
        item_self.parentNode.querySelector(".text-error").remove()
      }else{
        item_self.classList.remove("invalid")
      }
    }catch{}
  }
}

var inputs_invalid = document.querySelectorAll("input")
var textarea_invalid = document.querySelector("textarea")
inputs_invalid.forEach(element =>{
  element.addEventListener("input",async function(){
    await ChangeInput(element)
  })
  if(element.id == "multipleImg"){
    element.addEventListener("change",async function(){
      await ChangeInput(element)
    })
  }
})
textarea_invalid.addEventListener("input",async function(){
  await ChangeInput(textarea_invalid)
})

var form = document.querySelector("form")
form.noValidate = true
form.onsubmit = async function(e) {
  try{
    this.querySelectorAll(".text-error").forEach(elem => {
      elem.remove()
    })
  }catch{}
  e.preventDefault()
  try{
    this.reportValidity()
  }catch{}
  
  if (this.checkValidity()) return form.submit();

  var inputs = document.querySelectorAll("input")
  textarea = document.querySelector("textarea")
  first = true
  var error
  inputs.forEach(element =>{
    if (element.validity.valueMissing && element.id == "registerPrice" && (textarea.value == "" || textarea.value == " ")){
      textarea.classList.add("invalid")
      error = document.createElement("p")
      error.setAttribute("class","text-error")
      error.innerText  = "Campo requerido"
      textarea.parentNode.append(error)
    }
    if (element.validity.valueMissing == true){
      if(element.id == "multipleImg"){
        element.parentNode.setAttribute("data-toggle","tooltip")
        element.parentNode.setAttribute("data-placement","bottom")
        element.parentNode.setAttribute("title","Seleccione al menos 2 imagenes")
        document.querySelector(".icon-upload-imgs").classList.add("error-multi-imgs")
      }
      else{
        element.classList.add("invalid")
      }
      error = document.createElement("p")
      error.setAttribute("class","text-error")
      error.innerText  = "Campo requerido"
      element.parentNode.append(error)
    }
  })
}