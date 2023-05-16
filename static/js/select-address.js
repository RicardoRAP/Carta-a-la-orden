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
  var btn_submit = document.querySelector(".btn-search")
  btn_submit.removeAttribute("hidden")
  btn_submit.removeAttribute("disabled")
}