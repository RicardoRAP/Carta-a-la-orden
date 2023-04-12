/*function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("contact-form__block")
  y = x[currentTab].getElementsByTagName("input")
  if(currentTab == 0){
    z = x[currentTab].getElementsByTagName("select")
  }
  // A loop that checks every input field in the current tab:
  for (i = 0; i <= y.length; i++) {
    if(i < y.length){
      if (y[i].value == "") {
        // add an "invalid" class to the field:
        y[i].className += " invalid"
        // and set the current valid status to false:
        valid = false
      }
    }else{
      if (z[0].value == "") {
        // add an "invalid" class to the field:
        z[0].className += " invalid"
        // and set the current valid status to false:
        valid = false
      }
    } 
  }
  return valid // return the valid status
}*/
var input_profile_img = document.querySelector('#formProfile_img')
var img = document.querySelector('.form-profile-img .current-img')

const readURL = file => {
  return new Promise((res, rej) => {
      const reader = new FileReader();
      reader.onload = e => res(e.target.result);
      reader.onerror = e => rej(e);
      reader.readAsDataURL(file);
  });
};

const preview = async event => {
  const file = event.target.files[0];
  const url = await readURL(file);
  img.src = url;
};

input_profile_img.addEventListener('change', preview);

var address = document.querySelectorAll('input.address')
var full = document.querySelector('input#saveFull_address')
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

var others_serv = document.querySelectorAll('input.others-serv')
var others_s = document.querySelector('input#saveDelivery')

others_serv[0].addEventListener('click', function(e){
  if(this.checked || others_serv[1].checked){
    others_s.parentElement.classList.remove("d-none")
  }
  else{
    others_s.parentElement.classList.add("d-none")
    others_s.value = ''
  }
})
others_serv[1].addEventListener('click', function(e){
  if(this.checked || others_serv[0].checked){
    others_s.parentElement.classList.remove("d-none")
  }
  else{
    others_s.parentElement.classList.add("d-none")
    others_s.value = ''
  }
})
window.addEventListener('load', function(e){
  var dir = FullAddress()
  show_full.value = dir

  if(others_serv[1].checked || others_serv[0].checked){
    others_s.parentElement.classList.remove("d-none")
  }
  else{
    others_s.parentElement.classList.add("d-none")
    others_s.value = ''
  }
})
