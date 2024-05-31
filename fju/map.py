import folium
import json
import os




def renderMap():

    # 設定顯示的地圖邊界
    min_lon, max_lon = 121.4282, 121.4362
    min_lat, max_lat = 25.0322, 25.0408


    # 建立地圖
    map = folium.Map(
        location=[(min_lat + max_lat) / 2, (min_lon + max_lon) / 2], # 中心位置
        zoom_start=17, # 預設縮放大小
        max_bounds=True, # 啟用最大邊界，避免使用者拉到輔大外的地圖
        min_lat=min_lat,
        max_lat=max_lat,
        min_lon=min_lon,
        max_lon=max_lon,
        min_zoom=17,max_zoom=20, # 可縮放大小
        attribution_control=False, # 關閉右下提供者訊息
        font_size='25px'
    )

    
    # 繪製地圖範圍資料
    map_geojson = os.path.join('map', 'map.geojson')
    with open(map_geojson, 'r', encoding='utf-8') as f:
        mapData = json.load(f)

    area = folium.GeoJson(
        mapData,
        style_function=lambda x: {
            'fillColor': '#000000',  
            'color': '#000000',    
            'weight': 0,             
            'fillOpacity': 0.7       
        }
    ).add_to(map)




    
    # 繪製地標資料
    
    ## 設定地標點樣式
    def style_function(feature):
        markup = """
                <div style="font-size: 0.8em;">
                <div style="width: 10px;
                            height: 10px;
                            border: 1px solid #303F9F;
                            border-radius: 5px;
                            background-color: #29B6F6;">
                </div>
                 </div>
        """
        return {"html": markup}

    # 讀取地標資料
    locateGeojson = os.path.join('map', 'location.geojson')
    with open(locateGeojson, 'r', encoding='utf-8') as f:
        locationData = json.load(f)
    
    # 加入地標資料
    fjuGeo = folium.GeoJson(
        locationData,
        name="fju_location",
        tooltip=folium.GeoJsonTooltip(
            fields=["name"], aliases=["地點"], localize=True
        ),
        marker=folium.Marker(icon=folium.DivIcon()),
        style_function=style_function
    ).add_to(map)

    


    # 將縮放按鍵移至右下角(使用JS將leaflet-control-zoom移動到leaflet-bottom.leaflet-right)
    zoomControl = '<script>document.addEventListener("DOMContentLoaded", function() {\
        document.querySelector("div.leaflet-bottom.leaflet-right").insertBefore(\
            document.querySelector("div.leaflet-control-zoom"), document.querySelector("div.leaflet-control-attribution")\
        );\
    });</script>'
    map.get_root().html.add_child(folium.Element(zoomControl))

    
    # 自訂搜尋欄
    searchBox = '''
    <style>
        .form {
            position: relative;
        }
        .form .fa-search {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            left: 20px;
            color: #9ca3af;
        }
        .form-input {
            height: 45px;
            text-indent: 33px;
            border-radius: 100px;
            width: 100%;
            font-size: 15px;
            
        }
        .form-input:focus {
            box-shadow: none;
        
        }
        .suggestions {
            max-height: 150px;
            overflow-y: auto;
            position: absolute;
            width: 100%;
            z-index: 1000;
            background-color: #fff;
            margin-top: 5px;
            display: none; /* 默认隐藏 */
            font-size: 15px;
        }
        @media (min-width: 576px) {
            .form-container {
                width: 300px;
            }
        }
        @media (max-width: 575.98px) {
            .form-container {
                width: 80%;
            }
        }
    </style>

    <div class="container" style="position: absolute; top: 10px; z-index: 9999; max-width: 400px;">
        <div class="row height d-flex justify-content-start align-items-center">
            <div class="col form-container">
                <div class="form">
                    <i class="fa fa-search"></i>
                    <input id="searchBox" type="text" class="form-control form-input" placeholder="查詢地點" autocomplete="off">
                    <ul id="suggestions" class="list-group suggestions"></ul>
                </div>
            </div>
        </div>
    </div>
    <script>
        // 塞入地標資料
        var geoJSONData = {{ geo_json_str }};
        // 從地標資料獲取搜尋範圍
        var places = geoJSONData.features.map(function(feature) {
        return feature.properties.name;
    }).filter(function(name) {
        return name !== null && name.trim() !== '';
    });

    var currentIndex = -1; // 當前選擇的建議索引

    document.getElementById('searchBox').addEventListener('input', function () {
        var query = this.value.trim().toLowerCase();
        var suggestions = document.getElementById('suggestions');
        suggestions.innerHTML = '';
        currentIndex = -1; // 重製索引
        if (query) {
            var filteredPlaces = places.filter(function (place) {
                return place.toLowerCase().includes(query);
            });
            filteredPlaces.forEach(function (place) {
                var li = document.createElement('li');
                li.textContent = place;
                li.className = 'list-group-item list-group-item-action';
                li.addEventListener('click', function () {
                    document.getElementById('searchBox').value = place;
                    suggestions.innerHTML = '';
                    suggestions.style.display = 'none';
                    moveToPlace(place);
                });
                suggestions.appendChild(li);
            });
            suggestions.style.display = 'block';
        } else {
            suggestions.style.display = 'none';
        }
    });

    //搜尋欄動作
    document.getElementById('searchBox').addEventListener('keydown', function (event) {
        var suggestions = document.getElementById('suggestions');
        var items = suggestions.getElementsByTagName('li');
        // 按下Enter時執行搜尋
        if (event.key === 'Enter') {
            event.preventDefault();
            selectPlace();
        // 往下選擇建議的選單
        } else if (event.key === 'ArrowDown') {
            event.preventDefault();
            if (currentIndex < items.length - 1) {
                currentIndex++;
                highlightSuggestion(items, currentIndex);
            }
        // 往上選擇建議選單
        } else if (event.key === 'ArrowUp') {
            event.preventDefault();
            if (currentIndex > 0) {
                currentIndex--;
                highlightSuggestion(items, currentIndex);
            }
        }
    });

    
    document.getElementById('searchBox').addEventListener('focusout', function () {
        selectPlace();
    });

    // 選擇建議選單的項目
    function selectPlace() {
        var suggestions = document.getElementById('suggestions');
        var items = suggestions.getElementsByTagName('li');
        if (currentIndex >= 0 && currentIndex < items.length) {
            var place = items[currentIndex].textContent;
            document.getElementById('searchBox').value = place;
            suggestions.innerHTML = '';
            suggestions.style.display = 'none';
            moveToPlace(place);
        } else {
            var query = document.getElementById('searchBox').value.trim();
            if (query) {
                var place = places.find(function (p) {
                    return p.toLowerCase() === query.toLowerCase();
                });
                if (place) {
                    document.getElementById('searchBox').value = place;
                    suggestions.innerHTML = '';
                    suggestions.style.display = 'none';
                    moveToPlace(place);
                }
            }
        }
    }

    // 反白被選擇的建議項目
    function highlightSuggestion(items, index) {
        for (var i = 0; i < items.length; i++) {
            if (i === index) {
                items[i].classList.add('active');
                items[i].scrollIntoView({ block: 'nearest' });
            } else {
                items[i].classList.remove('active');
            }
        }
    }

    //移動到搜尋欄選擇的目標
       function moveToPlace(place) {
        var selectedFeature = geoJSONData.features.find(function (feature) {
            return feature.properties.name === place;
        });
        
        if (selectedFeature) {
            var coordinates = selectedFeature.geometry.coordinates;
            var name = selectedFeature.properties.name;
            var alias = selectedFeature.properties.alias?selectedFeature.properties.alias:'Null';
            {{map}}.flyTo([coordinates[1], coordinates[0]], 19);
            L.popup([coordinates[1], coordinates[0]],{content:name}).openOn({{map}});
        }
    }
</script>
    '''
    # 加入搜尋欄到地圖中
    searchBox = searchBox.replace('{{map}}', map.get_name())
    searchBox = searchBox.replace('{{ geo_json_str }}', json.dumps(fjuGeo.data))
    map.get_root().html.add_child(folium.Element(searchBox))


    
    return map.get_root().render()
