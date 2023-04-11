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