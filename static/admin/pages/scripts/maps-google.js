String.prototype.isEmpty = function() {
    return (this.length === 0 || !this.trim());
};
var makers = [];
var MapsGoogle = function () {
    var mapMarker = function () {
        skey=$("#skey").val().trim().replace(/"/g, '?');
        SLOC_DATA=LOC_DATA
        for(var i = 0; i < SLOC_DATA.length; i++) {
            for (var prop in SLOC_DATA[i])
                if(typeof SLOC_DATA[i][prop]=='string')
                    SLOC_DATA[i][prop] = SLOC_DATA[i][prop].toLowerCase();
        }
        if(!skey.isEmpty()){
            locs1=JSON.search(SLOC_DATA, '//*[contains(username, "'+skey.toLowerCase()+'")]');
            locs2=JSON.search(SLOC_DATA, '//*[contains(first_name, "'+skey.toLowerCase()+'")]');
            locs3=JSON.search(SLOC_DATA, '//*[contains(last_name, "'+skey.toLowerCase()+'")]');
            locs4=JSON.search(SLOC_DATA, '//*[contains(phone, "'+skey.toLowerCase()+'")]');
            locs=$.merge(locs4, $.merge(locs1, $.merge(locs2,locs3)));
        }else{
            console.log('no search key');
            locs=LOC_DATA;
        }
        console.log(locs);
        if($.isEmptyObject(locs)){
            var map = new GMaps({
            div: '#gmap_marker',
            lat: 35.746512,
            lng: -95.925781,
            zoom: 4
        });
        }else{
        if(!skey.isEmpty()){
            zoomr=15;
            long=locs[0]['location']['longitude'];
        }else{
            zoomr=4;
            long=parseFloat(locs[0]['location']['longitude'])+25;
        }
        //console.log(zoomr);
        //console.log(long);
        //var map2 = new GMaps({
        //    div: '#gmap_marker',
        //    lat: locs[0]['location']['latitude'],
        //    lng: long,
        //    zoom: zoomr,
        //});
        var myLatlng = new google.maps.LatLng(locs[0]['location']['latitude'], long);
        var mapOptions = {
            zoom: zoomr,
            center: myLatlng
          }
        var map = new google.maps.Map(document.getElementById('gmap_marker'), mapOptions);

        $.each(locs, function(key, item){
            //a=map.addMarker({
            //lat: item['location']['latitude'],
            //lng: item['location']['longitude'],
            //title: item['username']
            //details: {
            //    username: item['username'],
            //    lat: item['location']['latitude'],
            //    long: item['location']['longitude'],
            //},
            //})

             var marker = new google.maps.Marker({
                  position:  new google.maps.LatLng(item['location']['latitude'], item['location']['longitude']),
                  map: map,
                  //title: item['username'],
                  draggable: false,
                  visible: true
              });

            var boxText = document.createElement("div");
                boxText.style.cssText = "border: 1px solid black; margin-top: 8px; background: yellow; padding: 5px;";
                boxText.innerHTML = item['username'];

            var myOptions = {
                 content: boxText
                ,disableAutoPan: true
                ,maxWidth: 0
                ,pixelOffset: new google.maps.Size(-70, 0)
                ,zIndex: null
                ,boxStyle: {
                  background: "url('/static/global/img/tipbox.gif') no-repeat scroll -70px 0px"
                  ,opacity: 1
                  ,width: "120px"

                 }
                ,closeBoxMargin: "10px 2px 2px 2px"
                ,closeBoxURL: "http://www.google.com/intl/en_us/mapfiles/close.gif"
                ,infoBoxClearance: new google.maps.Size(1, 1)
                ,isHidden: false
                ,pane: "floatPane"
                ,enableEventPropagation: false
		    };
            var ib = new InfoBox(myOptions);
            google.maps.event.addListener(marker, "click", function (e) {
                ib.open(map, this);
            });
		    //ib.open(map, marker);

            //makers.push(marker);
            })

        }
        map.setZoom(zoomr);
    }

    return {
        //main function to initiate map samples
        init: function () {
            mapMarker();
        }

    };

}();

var MapsGoogleProfile = function () {
    var mapMarker = function () {
        locs=jQuery.parseJSON((document.getElementById('locations').value));

        var myLatlng = new google.maps.LatLng(locs['location']['latitude'], locs['location']['longitude']);
        var mapOptions = {
            zoom: 13,
            center: myLatlng
          }
        var map = new google.maps.Map(document.getElementById('gmap_marker'), mapOptions);

        var marker = new google.maps.Marker({
              position:  new google.maps.LatLng(locs['location']['latitude'], locs['location']['longitude']),
              map: map,
              //title: item['username'],
              draggable: false,
              visible: true
          });
        var boxText = document.createElement("div");
                boxText.style.cssText = "border: 1px solid black; margin-top: 8px; background: yellow; padding: 5px;";
                boxText.innerHTML = locs['username'];

        var myOptions = {
             content: boxText
            ,disableAutoPan: true
            ,maxWidth: 0
            ,pixelOffset: new google.maps.Size(-70, 0)
            ,zIndex: null
            ,boxStyle: {
              background: "url('/static/global/img/tipbox.gif') no-repeat scroll -70px 0px"
              ,opacity: 1
              ,width: "120px"

             }
            ,closeBoxMargin: "10px 2px 2px 2px"
            ,closeBoxURL: "http://www.google.com/intl/en_us/mapfiles/close.gif"
            ,infoBoxClearance: new google.maps.Size(1, 1)
            ,isHidden: false
            ,pane: "floatPane"
            ,enableEventPropagation: false
        };
        var ib = new InfoBox(myOptions);
        google.maps.event.addListener(marker, "click", function (e) {
            ib.open(map, this);
        });
        //ib.open(map, marker);

    }

    return {
        //main function to initiate map samples
        init: function () {
            mapMarker();
        }

    };

}();

var MapsGoogleProfileDefault = function () {
    var mapMarker = function () {
        var map = new GMaps({
            div: '#gmap_marker',
            lat: 35.746512,
            lng: -78.925781,
            zoom: 12,
        });
        //map.setZoom(5);
    }

    return {
        //main function to initiate map samples
        init: function () {
            mapMarker();
        }

    };

}();