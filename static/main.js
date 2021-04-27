ymaps.ready(init);

geoObjects = [];

var placemarks = [
    {
        'latitude': 55.75,
        'longitude': 37.61,
        'hintContent': 'Дело №1',
        'balloonContent': [
            '<a href="/crimes/1">',
            'Перейти в дело',
            '</a>'
        ]
    },
    {
        'latitude': 55.7632,
        'longitude': 37.5766,
        'hintContent': 'Дело №2',
        'balloonContent': [
            '<a href="/crimes/2">',
            'Перейти в дело',
            '</a>'
        ]
    },
    {
        'latitude': 55.8446027,
        'longitude': 37.557993044107964,
        'hintContent': 'Дело №11',
        'balloonContent': [
            '<a href="/crimes/11">',
            'Перейти в дело',
            '</a>'
        ]
    },
    {
        'latitude': 55.6675926,
        'longitude': 37.415446,
        'hintContent': 'Дело №4',
        'balloonContent': [
            '<a href="/crimes/4">',
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