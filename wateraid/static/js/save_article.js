function saveFunction() {
var form1 = document.getElementById('save_form');
var form2 = document.getElementById('unsave_form');
form1.save.classList.add('hide');
form2.unsave.classList.remove('hide');
}

function unsaveFunction() {
var form1 = document.getElementById('save_form');
var form2 = document.getElementById('unsave_form');
form2.unsave.classList.add('hide');
form1.save.classList.remove('hide');
}