ymaps.ready(init);

var placemarks = [
    {
        latitude: 55.75,
        longitude: 37.61,
        hintContent: 'Емае',
        balloonContent: [
            '<a href="/crimes/1">',
            'Перейти в дело',
            '</a>'
        ]
    }
],
    geoObjects = [];

function init() {
    var map = new ymaps.Map('map', {
        center: [55.7520, 37.6175],
        zoom: 10,
        controls: ['zoomControl'],
    });

    for (var i = 0; i < placemarks.length; i++) {
        geoObjects[i] = new ymaps.Placemark([placemarks[i].latitude, placemarks[i].longitude],
            {
                hintContent: placemarks[i].hintContent,
                balloonContent: placemarks[i].balloonContent.join('')
            }
        )
    }
    var clusterer = new ymaps.Clusterer({
        clusterIcons: [
            {
                href: 'img/marker.png',
                size: [100, 100],
                offset: [-50, -50]
            }
        ],
        clusterIconContentLayout: null
    });
    map.geoObjects.add(clusterer);
    clusterer.add(geoObjects);
}