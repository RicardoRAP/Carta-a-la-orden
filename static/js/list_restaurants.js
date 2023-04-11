window.addEventListener('load',function(){
  var select_address = document.querySelector("#SelectState").value
  var btn_address = document.querySelector("#BtnState span")
  btn_address.textContent = select_address
})

function SelectAddress(e){
  var btn_address = document.querySelector("#BtnState span")
  var btn_item = e.target
  btn_address.textContent = btn_item.textContent
  var select_address = document.querySelector("#SelectState")
  select_address.value = btn_item.textContent
  var text_address = document.querySelector("#TextAddress")
  text_address.setAttribute("autocomplete",true)
  text_address.removeAttribute("disabled")
  text_address.classList.add("active")
}