window.addEventListener('DOMContentLoaded',function(){
  setTimeout(showPage, 2000)
})

function showPage() {
  try{
    document.querySelector('#loader').style.display = "none"
  }catch{
    console.log("Without loader")
  }
}