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

var address = document.querySelectorAll('input.address')
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