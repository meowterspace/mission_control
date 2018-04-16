var menu_flag = 0; // stores if the Press any key to continue function has already been activated

$(document).on('keyup',function(evt) { // if a keyup event occours
  if (menu_flag == 0){ // and if it hasn't occoured before
  	if (evt.keyCode == 8||evt.keyCode == 9||evt.keyCode == 13||evt.keyCode == 16||evt.keyCode == 17||evt.keyCode == 18||evt.keyCode == 19||evt.keyCode == 20||evt.keyCode == 27||evt.keyCode == 33||evt.keyCode == 34||evt.keyCode == 35||evt.keyCode == 36||evt.keyCode == 37||evt.keyCode == 38||evt.keyCode == 39||evt.keyCode == 40||evt.keyCode == 45||evt.keyCode == 46||evt.keyCode == 48||evt.keyCode == 49||evt.keyCode == 50||evt.keyCode == 51||evt.keyCode == 52||evt.keyCode == 53||evt.keyCode == 54||evt.keyCode == 55||evt.keyCode == 56||evt.keyCode == 57||evt.keyCode == 65||evt.keyCode == 66||evt.keyCode == 67||evt.keyCode == 68||evt.keyCode == 69||evt.keyCode == 70||evt.keyCode == 71||evt.keyCode == 72||evt.keyCode == 73||evt.keyCode == 74||evt.keyCode == 75||evt.keyCode == 76||evt.keyCode == 77||evt.keyCode == 78||evt.keyCode == 79||evt.keyCode == 80||evt.keyCode == 81||evt.keyCode == 82||evt.keyCode == 83||evt.keyCode == 84||evt.keyCode == 85||evt.keyCode == 86||evt.keyCode == 87||evt.keyCode == 88||evt.keyCode == 89||evt.keyCode == 90||evt.keyCode == 91||evt.keyCode == 92||evt.keyCode == 93||evt.keyCode == 96||evt.keyCode == 97||evt.keyCode == 98||evt.keyCode == 99||evt.keyCode == 100||evt.keyCode == 101||evt.keyCode == 102||evt.keyCode == 103||evt.keyCode == 104||evt.keyCode == 105||evt.keyCode == 016||evt.keyCode == 107||evt.keyCode == 109||evt.keyCode == 110||evt.keyCode == 111||evt.keyCode == 112||evt.keyCode == 113||evt.keyCode == 114||evt.keyCode == 115||evt.keyCode == 116||evt.keyCode == 117||evt.keyCode == 118||evt.keyCode == 119||evt.keyCode == 120||evt.keyCode == 121||evt.keyCode == 122||evt.keyCode == 123||evt.keyCode == 144||evt.keyCode == 145||evt.keyCode == 186||evt.keyCode == 187||evt.keyCode == 188||evt.keyCode == 189||evt.keyCode == 190||evt.keyCode == 191||evt.keyCode == 192||evt.keyCode == 219||evt.keyCode == 220||evt.keyCode == 221||evt.keyCode == 222) {
  		// ^ if it is a standard ascii keyboard key,
    	$('#menu').show();  // show the menu
 		$('#PAKTC').hide(); // and hide the press any key to continue text
 		menu_flag = 1; // set the menu flag so it can't happen again.
  	};
  };
});

// This function is called by the join button. It hides the menu and shows the join menu.
function join() {
	$('#menu').hide();
	$('#join-menu').show();
};
// this function is called by the host button. It displays some text then redirects the user to the github
// repo so they can look into hosting their own game.
function host() {
	alert('You will now be redirected to the GitHub repo for MCS 3000'); // displays redirect alert
	window.location.replace('http://github.com/meowterspace/mission_control') // redirects to repo
};
// This function is called by the about button. It displays some very basic about text.
function about() {
	alert('This is the mission control similator 3000. A multiplayer simulation that allows you to take a seat in mission control! \n Click join to join a game or host to learn how to host your own');
};