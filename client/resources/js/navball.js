
var renderer;
var scene;
var camera;
var cube;

function setup() { // This just sets up the 3D scene and canvas to be the right size.

	// Create an empty scene
	scene = new THREE.Scene();
	// Create a basic camera
	camera = new THREE.PerspectiveCamera(50, 400 / 400, 0.1, 1000);
	camera.position.z = 10;
	// Create a renderer with Antialiasing
	renderer = new THREE.WebGLRenderer();
	// Configure renderer size
	renderer.setSize( 400, 400 );
	// Append Renderer to DOM
	var canvas = document.getElementById('canvas');
	canvas.appendChild( renderer.domElement );

};


function draw(){ // This creates 3D objects within the scene


	var geometry = new THREE.SphereGeometry(3, 32, 32); // create a sphere
	var loader = new THREE.TextureLoader();

	loader.load( // This loads the map.png image to put on the ball. 
		'resources/img/nav-ball/map.png',

		function ( texture ) { // This function sets the texture of the ball
							   // to be the map when the ball has loaded into 
							   // the game
			var material = new THREE.MeshBasicMaterial( {
				map: texture
			 } );
			// defines the ball as 'cube'
			cube = new THREE.Mesh( geometry, material );

	// Adds the ball with the texture to the scene
	scene.add( cube );

		},
		undefined,
		// error logging
		function ( err ) {
			console.error( 'An error happened.' );
		}

	);
	// This creates a new 2D plane in the 3D scene
	var pgeometry = new THREE.PlaneGeometry(9, 9, 32)

	loader.load( // agian, this loads the shader.png texture and applies it to the plane.
		'resources/img/nav-ball/shader.png',
		function (texture) {
			var pmaterial = new THREE.MeshBasicMaterial({
				map: texture });
			plane = new THREE.Mesh( pgeometry, pmaterial );
	scene.add( plane ); // add the plane to the 3d scene
	plane.position.set(0, 0, 0); // set the position of the plane
	plane.transparent = true;
	});

};

// This renderes the scene
var render = function () {
  requestAnimationFrame( render );

  renderer.render(scene, camera);
};

// This function pulls all the above functions together to render the entire navball at once.
// it is called when the FDAI/Navball modal/window is opened in the UI
function render_navball() {
	setup();
	draw();
	render();
};

