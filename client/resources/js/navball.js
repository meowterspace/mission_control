

// ------------------------------------------------
// BASIC SETUP
// ------------------------------------------------

var renderer;
var scene;
var camera;
var cube;

function setup() {

	// Create an empty scene
	scene = new THREE.Scene();

	// Create a basic perspective camera
	camera = new THREE.PerspectiveCamera(50, 400 / 400, 0.1, 1000);

	camera.position.z = 10;

	// Create a renderer with Antialiasing
	renderer = new THREE.WebGLRenderer();

	// Configure renderer clear color
	//renderer.setClearColor("#000000");

	// Configure renderer size
	renderer.setSize( 400, 400 );

	// Append Renderer to DOM
	var canvas = document.getElementById('canvas');
	canvas.appendChild( renderer.domElement );

};
// ------------------------------------------------
// FUN STARTS HERE
// ------------------------------------------------


function draw(){


	// Create a Cube Mesh with basic material 40=50
	var geometry = new THREE.SphereGeometry(3, 32, 32);

	// instantiate a loader
	var loader = new THREE.TextureLoader();

	// load a resource
	loader.load(
		// resource URL
		'resources/img/nav-ball/map.png',

		// onLoad callback
		function ( texture ) {
			// in this example we create the material when the texture is loaded
			var material = new THREE.MeshBasicMaterial( {
				map: texture
			 } );

			cube = new THREE.Mesh( geometry, material );

	// Add cube to Scene
	scene.add( cube );

		},

		// onProgress callback currently not supported
		undefined,

		// onError callback
		function ( err ) {
			console.error( 'An error happened.' );
		}

	);

	var pgeometry = new THREE.PlaneGeometry(9, 9, 32)

	loader.load(
		'resources/img/nav-ball/shader.png',
		function (texture) {
			var pmaterial = new THREE.MeshBasicMaterial({
				map: texture });
			plane = new THREE.Mesh( pgeometry, pmaterial );
	scene.add( plane );
	plane.position.set(0, 0, 0);
	plane.transparent = true;
	});

};

// Render Loop
var render = function () {
  requestAnimationFrame( render );

  //cube.rotation.x = Math.PI/2;
  //cube.rotation.y = 90;
  // Render the scene
  renderer.render(scene, camera);
};

//var move_to = function() {

function render_navball() {
	setup();
	draw();
	render();
};

