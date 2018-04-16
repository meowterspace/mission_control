// This is the graphing script. It currently isn't correctly implimented.


window.onload = function () { // when the window is loaded
	var chart = new CanvasJS.Chart("chartContainer", {  // creat a new cavas

		data: [ // graph starting data. needs to be empty
		{
			type: "spline",
			dataPoints: [
				{ y: 10 },
				{ y:  4 },
				{ y: 18 },
				{ y:  8 }	
			]
		}
		]
	});
	chart.render();	// render the graph in the scene


	// This function will be connected to the websocket recieve message function.
	// It adds a new point to the graph defined by {}. Very easy to impliment.
	
	$("#addDataPoint").click(function () {

	var length = chart.options.data[0].dataPoints.length;
	chart.options.data[0].dataPoints.push({ y: 25 - Math.random() * 10});
	chart.render();

	});


}