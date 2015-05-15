var Stats = function () {

    return {


        initDashboardDaterange: function () {

            if (!jQuery().daterangepicker) {
                return;
            }

            $('#dashboard-report-range').daterangepicker({
                    opens: (Metronic.isRTL() ? 'right' : 'left'),
                    startDate: moment().subtract('days', 29),
                    endDate: moment(),
                    minDate: '01/01/2012',
                    maxDate: '12/31/2015',
                    dateLimit: {
                        days: 60
                    },
                    showDropdowns: false,
                    showWeekNumbers: true,
                    timePicker: false,
                    timePickerIncrement: 1,
                    timePicker12Hour: true,
                    ranges: {
                        'Today': [moment(), moment()],
                        'Yesterday': [moment().subtract('days', 1), moment().subtract('days', 1)],
                        'Last 7 Days': [moment().subtract('days', 6), moment()],
                        'Last 30 Days': [moment().subtract('days', 29), moment()],
                        'This Month': [moment().startOf('month'), moment().endOf('month')],
                        'Last Month': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')]
                    },
                    buttonClasses: ['btn btn-sm'],
                    applyClass: ' blue',
                    cancelClass: 'default',
                    format: 'MM/DD/YYYY',
                    separator: ' to ',
                    locale: {
                        applyLabel: 'Apply',
                        fromLabel: 'From',
                        toLabel: 'To',
                        customRangeLabel: 'Custom Range',
                        daysOfWeek: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
                        monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                        firstDay: 1
                    }
                },
                function (start, end) {
                    $('#dashboard-report-range span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));

                    // Change URl
                    window.history.pushState({}, "", "/dashboard/stats/?start_date=" + start.format('YYYY-MM-DD') + "&end_date=" + end.format('YYYY-MM-DD') + "");
                    // Update html
                    $("#stats_content").html('<div id="site_statistics_loading"><img src="/static/admin/layout/img/loading.gif" alt="loading"/></div>');
                    // Query data
                    $.ajax({
                        url: "/dashboard/stats/",
                        data: { start_date: start.format('YYYY-MM-DD'), end_date: end.format('YYYY-MM-DD') },
                        context: document.body
                    }).done(function( data  ) {
                        if($(data).find("#stats_content").length > 0) {
                          $("#stats_content").html($(data).find("#stats_content").html());
                        } else {
                            window.location.href = "/dashboard/";
                        }
                    });
                }
            );


            $('#dashboard-report-range span').html(moment().subtract('days', 29).format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY'));
            $('#dashboard-report-range').show();




        }

    };

}();