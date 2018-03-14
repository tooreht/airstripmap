"""KML airstrip components"""


import simplekml


# Region
latlonaltbox = simplekml.LatLonAltBox(
    north=-11.63011499099052,
    south=-26.04605302582592,
    east=51.58283094574556,
    west=42.72857522419672,
    minaltitude=0,
    maxaltitude=0,
)
lod = simplekml.Lod(
    minlodpixels=8192,
    maxlodpixels=-1,
    minfadeextent=0,
    maxfadeextent=0,
)
region = simplekml.Region(latlonaltbox=latlonaltbox, lod=lod)

# Styles
green = simplekml.Style()
green.iconstyle.color = simplekml.Color.green
green.iconstyle.icon.href = "http://www.gstatic.com/mapspro/images/stock/959-wht-circle-blank.png"
green.iconstyle.scale = 1.0

yellow = simplekml.Style()
yellow.iconstyle.color = simplekml.Color.yellow
yellow.iconstyle.icon.href = "http://www.gstatic.com/mapspro/images/stock/959-wht-circle-blank.png"
yellow.iconstyle.scale = 1.0

orange = simplekml.Style()
orange.iconstyle.color = simplekml.Color.orange
orange.iconstyle.icon.href = "http://www.gstatic.com/mapspro/images/stock/959-wht-circle-blank.png"
orange.iconstyle.scale = 1.0

red = simplekml.Style()
red.iconstyle.color = simplekml.Color.red
red.iconstyle.icon.href = "http://www.gstatic.com/mapspro/images/stock/959-wht-circle-blank.png"
red.iconstyle.scale = 1.0

small_airport = simplekml.Style()
small_airport.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/airports.png"
small_airport.iconstyle.scale = 1
small_airport.balloonstyle.text = "<![CDATA[<h3>$[name]</h3>]]>"
small_airport.balloonstyle.bgcolor = simplekml.Color.lightgreen
small_airport.balloonstyle.textcolor = simplekml.Color.rgb(0, 0, 255)

medium_airport = simplekml.Style()
medium_airport.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/airports.png"
medium_airport.iconstyle.scale = 1.5
medium_airport.balloonstyle.text = "<![CDATA[<h3>$[name]</h3>]]>"
medium_airport.balloonstyle.bgcolor = simplekml.Color.lightgreen
medium_airport.balloonstyle.textcolor = simplekml.Color.rgb(0, 0, 255)

big_airport = simplekml.Style()
big_airport.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/airports.png"
big_airport.iconstyle.scale = 2
big_airport.balloonstyle.text = "<![CDATA[<h3>$[name]</h3>]]>"
big_airport.balloonstyle.bgcolor = simplekml.Color.lightgreen
big_airport.balloonstyle.textcolor = simplekml.Color.rgb(0, 0, 255)
