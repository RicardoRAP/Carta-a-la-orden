try{
  var others_serv = document.querySelectorAll('input.others-serv')
  var others_s = document.querySelector('input#registerDelivery')
  others_s.parentElement.classList.add('d-none')

  others_serv[0].addEventListener('click', function(e){
    if(this.checked || others_serv[1].checked){
      others_s.parentElement.classList.remove("d-none")
    }
    else{
      others_s.parentElement.classList.add("d-none")
    }
  })
  others_serv[1].addEventListener('click', function(e){
    if(this.checked || others_serv[0].checked){
      others_s.parentElement.classList.remove("d-none")
    }
    else{
      others_s.parentElement.classList.add("d-none")
    }
  })
}catch{
  console.log("Actualize su plan")
}