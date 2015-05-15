var ChartsAmcharts = function() {

    var initChartSample2 = function() {
        var chart;
           var chartData = [];
           //AmCharts.ready(function () {
               // generate some random data first
               generateChartData();
               // SERIAL CHART
               chart = new AmCharts.AmSerialChart();
               chart.pathToImages = "/static/global/plugins/amcharts/amcharts/images/";
               chart.dataProvider = chartData;
               chart.categoryField = "date";

               // listen for "dataUpdated" event (fired when chart is inited) and call zoomChart method when it happens
               //chart.addListener("dataUpdated", zoomChart);

               // AXES
               // category
               var categoryAxis = chart.categoryAxis;
               categoryAxis.parseDates = true; // as our data is date-based, we set parseDates to true
               categoryAxis.minPeriod = "DD"; // our data is daily, so we set minPeriod to DD
               categoryAxis.minorGridEnabled = true;
               categoryAxis.axisColor = "#DADADA";
               categoryAxis.twoLineMode = true;
               categoryAxis.dateFormats = [{
                    period: 'fff',
                    format: 'JJ:NN:SS'
                }, {
                    period: 'ss',
                    format: 'JJ:NN:SS'
                }, {
                    period: 'mm',
                    format: 'JJ:NN'
                }, {
                    period: 'hh',
                    format: 'JJ:NN'
                }, {
                    period: 'DD',
                    format: 'DD'
                }, {
                    period: 'WW',
                    format: 'DD'
                }, {
                    period: 'MM',
                    format: 'MMM'
                }, {
                    period: 'YYYY',
                    format: 'YYYY'
                }];

               // first value axis (on the left)
               var valueAxis1 = new AmCharts.ValueAxis();
               valueAxis1.axisColor = "#FF6600";
               valueAxis1.axisThickness = 2;
               valueAxis1.gridAlpha = 0;
               chart.addValueAxis(valueAxis1);

               // third value axis (on the left, detached)
               valueAxis3 = new AmCharts.ValueAxis();
               valueAxis3.offset = 5; // this line makes the axis to appear detached from plot area
               valueAxis3.gridAlpha = 0;
               valueAxis3.axisColor = "#B0DE09";
               valueAxis3.axisThickness = 2;
               chart.addValueAxis(valueAxis3);

               // GRAPHS
               // first graph
               var graph1 = new AmCharts.AmGraph();
               graph1.valueAxis = valueAxis1; // we have to indicate which value axis should be used
               graph1.title = "Active users";
               graph1.valueField = "active";
               graph1.bullet = "round";
               graph1.hideBulletsCount = 30;
               graph1.bulletBorderThickness = 1;
               chart.addGraph(graph1);

               // second graph
               var graph2 = new AmCharts.AmGraph();
               graph2.valueAxis = valueAxis1; // we have to indicate which value axis should be used
               graph2.title = "Total users";
               graph2.valueField = "total";
               graph2.bullet = "square";
               graph2.hideBulletsCount = 30;
               graph2.bulletBorderThickness = 1;
               chart.addGraph(graph2);

               // CURSOR
               var chartCursor = new AmCharts.ChartCursor();
               chartCursor.cursorAlpha = 0.1;
               chartCursor.fullWidth = true;
               chart.addChartCursor(chartCursor);

               // SCROLLBAR
               var chartScrollbar = new AmCharts.ChartScrollbar();
               chart.addChartScrollbar(chartScrollbar);

               // LEGEND
               var legend = new AmCharts.AmLegend();
               legend.marginLeft = 110;
               legend.useGraphSettings = true;
               chart.addLegend(legend);

               // WRITE
               chart.write("chart_2");
           //});

           // generate some random data, quite different range
           function generateChartData() {
               data=LINE_CHART_DATA;//$.parseJSON(document.getElementById('charts').value);
               $.each(data, function(key, item){                   // we create date objects here. In your data, you can have date strings
                   // and then set format of your dates using chart.dataDateFormat property,
                   // however when possible, use date objects, as this will speed up chart rendering.
                   var newDate = new Date(item['cur_date']);
                   var total = item['total_user'];
                   var active = item['total_active_user'];
//                   var views = Math.round(Math.random() * 6000);

                   chartData.push({
                       date: newDate,
                       active: active,
                       total: total
//                       views: views
                   });
               })
           }

           // this method is called when chart is first inited as we listen for "dataUpdated" event
           function zoomChart() {
               // different zoom methods can be used - zoomToIndexes, zoomToDates, zoomToCategoryValues
               chart.zoomToIndexes(8, 12);
           }
    }

    var initChartSample4 = function() {
            var chart;
            var chartData = [];
            data=STACK_CHART_DATA;
            $.each(data, function(key, item){                   // we create date objects here. In your data, you can have date strings
                // and then set format of your dates using chart.dataDateFormat property,
                   // however when possible, use date objects, as this will speed up chart rendering.
                var newDate = new Date(item['cur_date']);
                var text = item['total_msg_text'];
                var voice = item['total_msg_voice'];
                var other = item['total_msg_other']
                   chartData.push({
                       "date": newDate,
                       "text": text,
                       "voice": voice,
                       "other": other
                   });
               })

            //AmCharts.ready(function () {
                // SERIAL CHART
                chart = new AmCharts.AmSerialChart();
                chart.dataProvider = chartData;
                chart.categoryField = "date";
                chart.plotAreaBorderAlpha = 0.2;
                chart.pathToImages = "/static/global/plugins/amcharts/amcharts/images/";

                // AXES
                // category
                //chart.addListener("dataUpdated", zoomChart);
                var categoryAxis = chart.categoryAxis;
                categoryAxis.gridAlpha = 0.1;
                categoryAxis.axisAlpha = 0;
                categoryAxis.gridPosition = "start";
                categoryAxis.parseDates = true; // as our data is date-based, we set parseDates to true
                categoryAxis.minPeriod = "DD"; // our data is daily, so we set minPeriod to DD
                categoryAxis.minorGridEnabled = true;
                categoryAxis.axisColor = "#DADADA";
                categoryAxis.twoLineMode = true;
                categoryAxis.dateFormats = [{
                    period: 'fff',
                    format: 'JJ:NN:SS'
                }, {
                    period: 'ss',
                    format: 'JJ:NN:SS'
                }, {
                    period: 'mm',
                    format: 'JJ:NN'
                }, {
                    period: 'hh',
                    format: 'JJ:NN'
                }, {
                    period: 'DD',
                    format: 'DD'
                }, {
                    period: 'WW',
                    format: 'DD'
                }, {
                    period: 'MM',
                    format: 'MMM'
                }, {
                    period: 'YYYY',
                    format: 'YYYY'
                }];

                // value
                var valueAxis = new AmCharts.ValueAxis();
                valueAxis.stackType = "regular";
                valueAxis.gridAlpha = 0.1;
                valueAxis.axisAlpha = 0;
                chart.addValueAxis(valueAxis);

                // GRAPHS
                // first graph
                var graph = new AmCharts.AmGraph();
                graph.title = "Text Messages";
                graph.labelText = "[[value]]";
                graph.valueField = "text";
                graph.type = "column";
                graph.lineAlpha = 0;
                graph.fillAlphas = 1;
                graph.lineColor = "#C72C95";
                graph.balloonText = "<span style='color:#555555;'>[[category]]</span><br><span style='font-size:14px'>[[title]]:<b>[[value]]</b></span>";
                chart.addGraph(graph);

                // second graph
                graph = new AmCharts.AmGraph();
                graph.title = "Voice Messages";
                graph.labelText = "[[value]]";
                graph.valueField = "voice";
                graph.type = "column";
                graph.lineAlpha = 0;
                graph.fillAlphas = 1;
                graph.lineColor = "#D8E0BD";
                graph.balloonText = "<span style='color:#555555;'>[[category]]</span><br><span style='font-size:14px'>[[title]]:<b>[[value]]</b></span>";
                chart.addGraph(graph);

                // third graph
                graph = new AmCharts.AmGraph();
                graph.title = "Other Messages";
                graph.labelText = "[[value]]";
                graph.valueField = "other";
                graph.type = "column";
                graph.lineAlpha = 0;
                graph.fillAlphas = 1;
                graph.lineColor = "#B3DBD4";
                graph.balloonText = "<span style='color:#555555;'>[[category]]</span><br><span style='font-size:14px'>[[title]]:<b>[[value]]</b></span>";
                chart.addGraph(graph);
               // SCROLLBAR
               var chartScrollbar = new AmCharts.ChartScrollbar();
               chart.addChartScrollbar(chartScrollbar);

                // LEGEND
                var legend = new AmCharts.AmLegend();
                legend.borderAlpha = 0.2;
                legend.horizontalGap = 10;
                legend.marginLeft = 110;
                legend.useGraphSettings = true;
                chart.addLegend(legend);
//                console.log(STACK_CHART_DATA);
                // WRITE
                chart.write("chart_4");
            //});

            function zoomChart() {
               // different zoom methods can be used - zoomToIndexes, zoomToDates, zoomToCategoryValues
               chart.zoomToIndexes(5, 12);
            }
    }

    return {
        //main function to initiate the module

        init: function() {
            initChartSample2();
            initChartSample4();
        }

    };

}();