const myModalEl = document.querySelector('#DishModal')
const namesMenus = document.querySelector('#Names')
const btnSubmit = document.querySelector('#Pay') 
myModalEl.addEventListener('hidden.bs.modal', event => {
  var actives = document.querySelectorAll(".item-dish.active")
  actives.forEach(ele => {
    ele.classList.remove("active")
  })
})
async function Remove(){
  var container = document.querySelector("#carouselIndicators")
  var indicator = container.querySelector(".carousel-indicators")
  var inner = container.querySelector(".carousel-inner")
  var modal_price = document.querySelector("#ModalPrice")
  var addcart = document.querySelector("#AddCart")
  var removecart = document.querySelector("#RemoveCart")
  try{
    modal_price.removeChild(modal_price.firstChild)
  }catch{}
  while (indicator.hasChildNodes()) {
    indicator.removeChild(indicator.firstChild)
  }
  while (inner.hasChildNodes()) {
    inner.removeChild(inner.firstChild)
  }
  addcart.removeAttribute("hidden")
  addcart.removeAttribute("onclick")
  removecart.setAttribute("hidden","")
  removecart.removeAttribute("onclick")
  myModalEl.removeEventListener('hidden.bs.modal', Remove)
}
async function AddCart(item, addcart, modal, menu_dish){
  return function(){
    addcart.removeEventListener('click', AddCart)
    namesMenus.value += menu_dish + ";"
    var btn = btnSubmit.querySelector("#Count_dishes")
    var total = parseInt(btn.textContent)
    btn.textContent = total + 1
    btnSubmit.removeAttribute("hidden")
    item.parentNode.classList.remove("active")
    item.parentNode.classList.add("active_select")
    modal.hide()
    addcart.setAttribute("hidden","")
  }
}
async function RemoveCart(item, removecart, modal, menu_dish){
  return function(){
    removecart.removeEventListener('click', RemoveCart)
    var names_values = namesMenus.value.split(";")
    var price_values = priceDish.value.split(";")
    var btn = btnSubmit.querySelector("#Count_dishes")
    var total = parseInt(btn.textContent)
    names_values.splice(names_values.indexOf(menu_dish),1)
    namesMenus.value = names_values.join(";")
    if (names_values.length == 0 || total - 1 == 0){
      btn.textContent = 0
      btnSubmit.setAttribute("hidden","")
    }else{
      total = total - 1
      btn.textContent = total
    }
    item.parentNode.classList.remove("active")
    item.parentNode.classList.remove("active_select")
    modal.hide()
    removecart.setAttribute("hidden","")
  }
}
async function ShowModal(item, name, tags, descrition, discount, price, gallery, offer, menu_dish){
  var modal = new bootstrap.Modal(document.querySelector('#DishModal'))
  modal.show()
  var addcart = document.querySelector("#AddCart")
  var removecart = document.querySelector("#RemoveCart")
  if(item.parentNode.classList.contains("active_select")){
    addcart.setAttribute("hidden","")
    removecart.removeAttribute("hidden")
    removecart.onclick = await RemoveCart.call(this,item,removecart,modal,menu_dish)
  }else{
    addcart.onclick = await AddCart.call(this,item,addcart,modal,menu_dish)
  }
  item.parentNode.classList.add("active")
  var title = document.querySelector("#DishModalLabel")
  title.textContent = name
  let edit = gallery.replace(' ','').substring(1).slice(0, -1)
  let array_imgs = edit.split(",")
  let carousel = array_imgs.map(function(item){
    return item.replace(' ','').substring(1).slice(0,-1)
  })
  var container = document.querySelector("#carouselIndicators")
  var indicator = container.querySelector(".carousel-indicators")
  var inner = container.querySelector(".carousel-inner")
  var size_carousel = carousel.length
  for (var i = 0; i < size_carousel; i++){
    var index = i.toString()
    var createimg = document.createElement("img")
    createimg.setAttribute("src","/static/" + carousel[i])
    createimg.setAttribute("class","d-block w-100")
    createimg.setAttribute("alt","Platillo " + index)
    var creatediv = document.createElement("div")
    var createbutton = document.createElement("button")
    createbutton.setAttribute("type","button")
    createbutton.setAttribute("data-bs-target","#carouselIndicators")
    createbutton.setAttribute("data-bs-slide-to",i)
    createbutton.setAttribute("aria-label","Slide " + index)
    if (i == 0){
      createbutton.setAttribute("class","active")
      createbutton.setAttribute("aria-current","true")
      creatediv.setAttribute("class","carousel-item active")
    }else{
      creatediv.setAttribute("class","carousel-item")
    }
    indicator.appendChild(createbutton)
    creatediv.appendChild(createimg)
    inner.appendChild(creatediv)
  }
  var modal_offer = document.querySelector("#Carousel_imgs .offer span")
  if(offer != "None"){
    document.querySelector("#Carousel_imgs .offer").classList.remove("d-none")
    modal_offer.textContent = parseFloat(offer.replace(",",".")).toString().replace(".",",") + "% de descuento"
  }else{
    document.querySelector("#Carousel_imgs .offer").classList.add("d-none")
    modal_offer.textContent = ""
  }
  var modal_price = document.querySelector("#ModalPrice")
  if (discount != "None"){
    modal_price.textContent = parseFloat(discount.replace(",",".")).toString().replace(".",",") + "$" + " - "
    var createspan = document.createElement("span")
    createspan.setAttribute("class", "discount")
    createspan.textContent = parseFloat(price.replace(",",".")).toString().replace(".",",") + "$"
    modal_price.appendChild(createspan)
  }else{
    modal_price.textContent = parseFloat(price.replace(",",".")).toString().replace(".",",") + "$"
  }
  var modal_descrip = document.querySelector("#ModalDescription")
  modal_descrip.textContent = descrition
  var modal_tags = document.querySelector("#ModalTags")
  modal_tags.textContent = tags
  myModalEl.addEventListener('hidden.bs.modal', Remove)
}