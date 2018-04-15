window.onload = function () {
	var chart = new CanvasJS.Chart("chartContainer", { 
		title: {
			//text: "Adding & Updating dataPoints"
		},
		data: [
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
	chart.render();	

	$("#addDataPoint").click(function () {

	var length = chart.options.data[0].dataPoints.length;
	//chart.options.title.text = "New DataPoint Added at the end";
	chart.options.data[0].dataPoints.push({ y: 25 - Math.random() * 10});
	chart.render();

	});

	$("#updateDataPoint").click(function () {

	var length = chart.options.data[0].dataPoints.length;
	//chart.options.title.text = "Last DataPoint Updated";
	chart.options.data[0].dataPoints[length-1].y = 15 - Math.random() * 10;
	chart.render();

	});
}