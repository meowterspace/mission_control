var value = 25.3;


function make(id, value, dp){ // List of IDs for values, value, decimal point position in array
	value = Math.round(value*100)/100;
	console.log(value);
	value = value.toString();
	value = value.split('');
	for (var i=0; i<id.length; i++){
		if (value[i] == null){ value[i] = '0';};
		if (value[dp] == null){ value[dp] = '.';};
		document.getElementById(id[i]).innerHTML = value[i];
	};
};

function change(power, direction){
  value = value + (1*power*direction);
  console.log(value);
  make(['thm1', 'thm2', 'thm3', 'thm4'], value, 2); 
};