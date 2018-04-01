var value = 25.3;


function make(value){
	value = value.toString();
	value = value.split('');
	document.getElementById('thm1').innerHTML = value[0];
	document.getElementById('thm2').innerHTML = value[1];
	document.getElementById('thm3').innerHTML = value[2];
	document.getElementById('thm4').innerHTML = value[3];
};

function change(power, direction){
  value = value + (1*power*direction);
  console.log(value);
  make(value);
};