function decode(cSharpString) {
    return $('<textarea/>').html(cSharpString).text();
}



function HeatMapChart(id, title, imageUrl, legendUrl, legendMin, legendMax) {
    var imageWidth = 530;
    var imageHeight = 140;
    id = decode(id);
    imageUrl = decode(imageUrl);
    var legendWidth = 60;
    var legendHeight = imageHeight;
    var legendImageWidth = legendWidth / 3;
    var legendMargin = 5;

    var xAxisHeight = 50;
    var yAxisWidth = 70;

    var marginX = 10;
    var marginY = 35;
    var width = imageWidth + legendWidth + yAxisWidth + 2 * marginX;
    var height = imageHeight + xAxisHeight + 2 * marginY;

    var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    var x = d3.scaleBand().domain(months).range([0, imageWidth - 1]).paddingInner(1.00).paddingOuter(0.0);
    var y = d3.scaleLinear().domain([24, 0]).range([0, imageHeight]);

    var svg = d3.select(id).append("svg")
        .attr("width", width).attr("height", height);
    var svgG = svg.append("g")
        .attr("width", "100%").attr("height", "100%")
        .attr("transform", "translate(" + marginX + "," + marginY + ")");

    var imageG = svgG.append("g").attr("width", imageWidth).attr("height", imageHeight);
    imageG.append("svg:image")
        .attr("xlink:href", imageUrl)
        .attr("x", yAxisWidth).attr("y", 0)
        .attr("width", imageWidth).attr("height", imageHeight)
        .attr("preserveAspectRatio", "none");
    imageG.append("g")
        .attr("transform", "translate(" + yAxisWidth + "," + imageHeight + ")")
        .call(d3.axisBottom(x));
    var yAxisG = imageG.append("g")
        .attr("transform", "translate(" + yAxisWidth + ",0)")
        .call(d3.axisLeft(y).tickValues([0, 6, 12, 18, 24]));

    svgG.append("text").text(title)
        .attr("x", yAxisWidth + imageWidth / 2).attr("y", -5)
        .attr("text-anchor", "middle").attr("class", "graph-text");

    svgG.append("text").text("Hour of Day")
        .attr("x", 0 - imageHeight / 2).attr("y", marginY).attr("text-anchor", "middle")
        .attr("transform", "rotate(-90)")
        .style("font-size", "12px");

    // legend
    var legendG = svgG.append("g")
        .attr("width", legendWidth)
        .attr("height", legendHeight)
        .attr("transform", "translate(" + (yAxisWidth + imageWidth + legendMargin) + "," + 0 + ")");
    // // key
    legendG.append("svg:image")
        .attr("xlink:href", legendUrl)
        .attr("x", 0).attr("y", 0)
        .attr("width", legendImageWidth).attr("height", legendHeight)
        .attr("preserveAspectRatio", "none");
    // min
    legendG.append("text").text(legendMin)
        .attr("x", legendImageWidth + 3).attr("y", legendHeight + 2).style("text-anchor", "start")
        .style("font-size", "10px").style("font-weight", "bold");
    // // max
    legendG.append("text").text(legendMax)
        .attr("x", legendImageWidth + 3).attr("y", 5).style("text-anchor", "start")
        .style("font-size", "10px").style("font-weight", "bold");

}

function ElectricalProductionBarChart(id, title, text) {
    var svg = dimple.newSvg(id, 590, 430);// changed from 400 to 430
    var data = d3.csvParse(text);
    var chart = new dimple.chart(svg, data);
    chart.setBounds(75, 30, 480, 330);
    var x = chart.addCategoryAxis("x", "Month");
    x.addOrderRule(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]);
    var y = chart.addMeasureAxis("y", "Value");
    y.overrideMin = 0;
    y.title = "Power (kW)";
    chart.addSeries("Component", dimple.plot.bar);
    chart.addLegend(60, 10, 510, 20, "right");
    chart.draw();
}

function MonthlyCategorizedBarChart(id, title, text, yAxis) {
    var svg = dimple.newSvg(id, 590, 440);// changed from 410 to 440
    var data = d3.csvParse(text);
    var chart = new dimple.chart(svg, data);
    chart.setBounds(75, 30, 480, 330);
    var x = chart.addCategoryAxis("x", "Month");
    x.addOrderRule(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]);
    var y = chart.addMeasureAxis("y", "Value");
    y.overrideMin = 0;
    y.title = yAxis;
    chart.addSeries("Category", dimple.plot.bar);
    chart.addLegend(60, 10, 510, 20, "right");
    chart.draw();
    x.shapes.selectAll("text").attr("transform", function (d) {
        return d3.select(this).attr("transform") + " translate(0, 20) rotate(-45)";
    });
}

function AnnualSavingsOverviewBarChart(id, title, text, currency) {
    var svg = dimple.newSvg(id, 590, 560); // changed from 450 to 560
    text = decode(text);
    var data = d3.csvParse(text);
    var chart = new dimple.chart(svg, data);
    chart.setBounds(75, 30, 480, 310);
    var x = chart.addCategoryAxis("x", "Architecture");
    x.title = "";
    let archSet = new Set();
    data.forEach(function (d) {
        archSet.add(d["Architecture"]);
    });
    x.addOrderRule([...archSet]);
    var y = chart.addMeasureAxis("y", "Value");
    y.title = currency + "/year";
    chart.addSeries("Energy", dimple.plot.bar);
    chart.addLegend(60, 10, 510, 20, "right");
    chart.draw();
    x.shapes.selectAll("text").attr("transform", function (d) {
        var value = d3.select(this).attr('transform');
        if (value) {
            value = value.replace('rotate(90,', 'rotate(45,');
        }
        return value;
    });
}

function CostOverviewBarChart(id, title, text, currency) {
    var svg = dimple.newSvg(id, 590, 560); // changed from 470 to 560
    var data = d3.csvParse(text);
    var chart = new dimple.chart(svg, data);
    chart.setBounds(50, 30, 480, 330);
    var x = chart.addCategoryAxis("x", "Architecture");
    x.title = "";
    let archSet = new Set();
    data.forEach(function (d) {
        archSet.add(d["Architecture"]);
    });
    x.addOrderRule([...archSet]);
    var y = chart.addMeasureAxis("y", "Value");
    y.title = "";
    chart.addSeries("Energy", dimple.plot.bar);
    chart.addLegend(60, 10, 510, 20, "right");
    chart.draw();
    x.shapes.selectAll("text").attr("transform", function (d) {
        var value = d3.select(this).attr('transform');
        if (value) {
            value = value.replace('rotate(90,', 'rotate(45,');
        }
        return value;
    });
    // prepend currency symbol to Y axis labels
    y.shapes.selectAll("text").text(function (d) {
        return currency + " " + d;
    });
}

function CashFlowSummaryBarChart(id, title, text, currency) {
    var svg = dimple.newSvg(id, 590, 430); // changed from  400 to 430
    text = decode(text);
    var data = d3.csvParse(text);
    var chart = new dimple.chart(svg, data);
    chart.setBounds(75, 30, 480, 330);
    var x = chart.addCategoryAxis("x", "Category");
    x.addOrderRule("Category");
    var y = chart.addMeasureAxis("y", "Value");
    y.title = "Net Present Cost (" + currency + ")";
    chart.addSeries("Component", dimple.plot.bar);
    chart.addLegend(60, 10, 510, 20, "right");
    chart.draw();
}


function CashFlowBarChart(id, title, text, currency) {
    var svg = dimple.newSvg(id, 590, 430); // changed from  400 to 430
    var data = d3.csvParse(text);
    var chart = new dimple.chart(svg, data);
    chart.setBounds(75, 30, 480, 330);
    var x = chart.addCategoryAxis("x", "Year");
    x.addOrderRule("Year");
    var y = chart.addMeasureAxis("y", "Value");
    y.title = "Nominal Cash Flow (" + currency + ")";
    chart.addSeries("Category", dimple.plot.bar);
    chart.addLegend(60, 10, 510, 20, "right");
    chart.draw();
}


function ResourceBarChart(id, title, text, axis) {
    var svg = dimple.newSvg(id, 590, 430); // changed from  400 to 430
    var data = d3.csvParse(text);
    var chart = new dimple.chart(svg, data);
    chart.setBounds(75, 30, 480, 330);
    var x = chart.addCategoryAxis("x", "Month");
    x.addOrderRule(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]);
    var y = chart.addMeasureAxis("y", "Value");
    y.overrideMin = 0;
    y.title = axis;
    chart.addSeries(null, dimple.plot.bar);
    chart.addLegend(60, 10, 510, 20, "right");
    chart.draw();
}


function LoadBarChart(id, title, text) {
    var data = d3.csvParse(text);
    for (var i = 0; i < data.length; i += 1) {
        data[i]["TimeSeries"] = new Date(2017, 0, 1, Math.floor(data[i]["Hour"]), Math.round(data[i]["Hour"] * 60 % 60));
    }
    var svg = dimple.newSvg(id, 590, 430); // changed from  400 to 430
    var chart = new dimple.chart(svg);
    chart.setBounds(0, 30, 480, 330);

    var x = chart.addTimeAxis("x", "TimeSeries");
    x.timePeriod = d3.timeHour;
    x.timeInterval = 2;
    x.tickFormat = "%I%p";
    x.title = "Hour";

    var y = chart.addMeasureAxis("y", "Value");
    y.overrideMin = 0;
    y.title = "Demand (kW)";

    var s = chart.addSeries(null, dimple.plot.area);
    s.data = data;
    chart.draw();
}


function PeakShavingTimeSeries(id, title, text) {
    var data = d3.csvParse(text);
    var pvData = [];
    var windData = [];
    var renewableData = [];
    var gridData = [];
    var socData = [];
    var baselineData = [];
    var genData = [];
    for (var i = 1; i < data.length; i += 1) {
        data[i]["TimeSeries"] = new Date(2017, 0, 1, Math.floor(data[i]["Hour"]), Math.round(data[i]["Hour"]*60 % 60));
        if (data[i]["Category"] === "PV") {
            pvData.push(data[i]);
        } else if (data[i]["Category"] === "Wind") {
            windData.push(data[i]);
        } else if (data[i]["Category"] === "Soc") {
            socData.push(data[i]);
        } else if (data[i]["Category"] === "Baseline") {
            baselineData.push(data[i]);
        } else if (data[i]["Category"] === "Grid") {
            gridData.push(data[i]);
        } else {
            console.log(data[i]["Category"]);
            genData.push(data[i]);
        }
    }
    if (Object.keys(pvData).length > 0 || Object.keys(windData).length > 0) {
        for (var i = 0; i < Math.max(pvData.length, windData.length); i++) {
            var hour = i * 24 / Math.max(pvData.length, windData.length);
            renewableData.push({
                Value: 0,
                Hour: hour,
                Category: "Total Renewable Output",
                TimeSeries: new Date(2017, 0, 1, Math.floor(hour), Math.round(hour*60%60))
            });
            if (Object.keys(pvData).length > 0) {
                renewableData[i].Value += +pvData[i].Value;
            }
            if (Object.keys(windData).length > 0) {
                renewableData[i].Value += +windData[i].Value;
            }
        }
    }
    var hasBaselineData = Object.keys(baselineData).length > 0;
    var hasSocData = Object.keys(socData).length > 0;
    var height = 250;
	if (hasBaselineData) {
		height += 203;
	}
	if (hasSocData) {
		height += 187;
	}
    var width = 300;
    var svg = dimple.newSvg(id, width, height);

    svg.append("text")
        .attr("x", (width / 2) + 10)
        .attr("y", 15)
        .style("text-anchor", "middle")
        .attr("class", "production_plot_month_title")
        .text(title);

    var productionChartY = 30;
    var productionChartTitle = "Plot of peak day ";
    productionChartTitle += Object.keys(pvData).length > 0 ? "PV, " : "";
    productionChartTitle += Object.keys(windData).length > 0 ? "Wind, " : "";
    productionChartTitle += Object.keys(genData).length > 0 ? "Generator, " : "";
    productionChartTitle += Object.keys(genData).length > 0 || Object.keys(pvData).length > 0 ? "and " : "";
    productionChartTitle += "Grid Purchases";
    svg.append("text")
        .attr("x", width / 2)
        .attr("y", productionChartY)
        .style("text-anchor", "middle")
        .attr("class", "production_plot_title")
        .text(productionChartTitle);

    var productionChart = new dimple.chart(svg);

    productionChart.setBounds(30, productionChartY + 25, width - 25, 150);

    var xAxis = productionChart.addTimeAxis("x", "TimeSeries");
    xAxis.timePeriod = d3.timeHour;
    xAxis.timeInterval = 3;
    xAxis.tickFormat = "%I%p";
    xAxis.title = "Hour";
    var yAxis = productionChart.addMeasureAxis("y", "Value");
    xAxis.showGridlines = true;
    yAxis.title = "kW";
    var gridPurchases = productionChart.addSeries("Category", dimple.plot.line);
    for (var i = 0; i < gridData.length; i++) {
        gridData[i]["Category"] = "Grid Purchases";
    }
    for (var i = 0; i < pvData.length; i++) {
        pvData[i]["Category"] = "PV Power Output";
    }
    for (var i = 0; i < windData.length; i++) {
        windData[i]["Category"] = "Wind Power Output";
    }
    for (var i = 0; i < renewableData.length; i++) {
        renewableData[i]["Category"] = "Total Renewable Output";
    }
    for (var i = 0; i < genData.length; i++) {
        genData[i]["Category"] = "Generator Power Output";
    }
    var totalPlotData = [...genData, ...gridData];
    gridPurchases.data = totalPlotData;
    var renewableOutput = productionChart.addSeries("Category", dimple.plot.area);
    renewableOutput.data = renewableData;
    var pvOutput = productionChart.addSeries("Category", dimple.plot.line);
    pvOutput.data = pvData;
    var windOutput = productionChart.addSeries("Category", dimple.plot.line);
    windOutput.data = windData;
    productionChart.assignColor("PV Power Output", "#ffff00");
    productionChart.assignColor("Wind Power Output", "#8fbcda");
    productionChart.assignColor("Total Renewable Output", "#66cc66", "#66cc66", 0.6);
    productionChart.assignColor("Grid Purchases", "#oe153d");
    productionChart.assignColor("Generator Power Output", "#fb9a99");
    productionChart.addLegend(20, productionChartY + 13, width - 5, 40, "right");
    productionChart.draw();
    if (hasBaselineData) {
        var baselineChartY = 253;
        var baselineChart = new dimple.chart(svg);
        baselineChart.setBounds(47, baselineChartY + 25, width - 50, 130);

        svg.append("text")
            .attr("x", width / 2)
            .attr("y", baselineChartY)
            .style("text-anchor", "middle")
            .attr("class", "production_plot_title")
            .text("System Grid Purchases Compared with Base Case");

        var xAxis = baselineChart.addTimeAxis("x", "TimeSeries");
        xAxis.timePeriod = d3.timeHour;
        xAxis.timeInterval = 3;
        xAxis.tickFormat = "%I%p";
        xAxis.title = "Hour";
        var yAxis = baselineChart.addMeasureAxis("y", "Value");
        xAxis.showGridlines = true;
        yAxis.title = "Grid Purchases (kW)";

        for (var i = 0; i < gridData.length; i++) {
            gridData[i]["Category"] = "System Grid Purchases";
        }
        for (var i = 0; i < baselineData.length; i++) {
            baselineData[i]["Category"] = "Baseline Grid Purchases";
        }

        var gridPurchaseData = baselineChart.addSeries("Category", dimple.plot.line);
        gridPurchaseData.data = gridData;
        var gridBaselineData = baselineChart.addSeries("Category", dimple.plot.line);
        gridBaselineData.data = baselineData;
        baselineChart.assignColor("System Grid Purchases", "#000000");
        baselineChart.assignColor("Baseline Grid Purchases", "#e31a1c");
        baselineChart.addLegend(20, baselineChartY + 9, width - 5, 40, "right");
        baselineChart.draw();
    }
    if (hasSocData) {
        var socChartY = 253;
		if (hasBaselineData)
			socChartY += 203;
        svg.append("text")
            .attr("x", width / 2)
            .attr("y", socChartY)
            .style("text-anchor", "middle")
            .attr("class", "production_plot_title")
            .text("Battery State of Charge Versus Time");
        var socChart = new dimple.chart(svg);
        var xAxis = socChart.addTimeAxis("x", "TimeSeries");
        xAxis.timePeriod = d3.timeHour;
        xAxis.timeInterval = 3;
        xAxis.tickFormat = "%I%p";
        xAxis.title = "Hour";
        var yAxis = socChart.addMeasureAxis("y", "Value");
        xAxis.showGridlines = true;
        yAxis.title = "State of Charge (%)";
        yAxis.overrideMax = 100.0;
        var socState = socChart.addSeries("Category", dimple.plot.line);
        socState.data = socData;
        socState.interpolation = "step";
        socChart.setBounds(45, socChartY + 10, width - 50, 130);
        socChart.assignColor("Soc", "#33a02c");
        socChart.draw();
    }
}
