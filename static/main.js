ymaps.ready(init);

geoObjects = [];

var placemarks = [
    {
        'latitude': 55.8446027,
        'longitude': 37.55799304410796,
        'hintContent': 'Дело №1',
        'balloonContent': [
            '<a href="/crimes/1">',
            'Перейти в дело',
            '</a>'
        ]
    }
];

console.log(placemarks);
function init() {
    var map = new ymaps.Map('map', {
        center: [55.7520, 37.6175],
        zoom: 10,
        controls: ['zoomControl'],
    });

    for (var i = 0; i < placemarks.length; i++) {
        geoObjects[i] = new ymaps.Placemark([placemarks[i]['latitude'], placemarks[i]['longitude']],
            {
                hintContent: placemarks[i]['hintContent'],
                balloonContent: placemarks[i]['balloonContent'].join('')
            }
        )
    }
    var clusterer = new ymaps.Clusterer({
        clusterIcons: [
            {
                size: [100, 100],
                offset: [-50, -50]
            }
        ],
        clusterIconContentLayout: null
    });
    map.geoObjects.add(clusterer);
    clusterer.add(geoObjects);
}