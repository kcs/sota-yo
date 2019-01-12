#!/usr/bin/env python3

import csv
from datetime import date

regions = ( ( 'EC', 'ff00ff55' ),
            ( 'MC', 'ffffaaaa' ),
            ( 'WC', 'ffffaa55' ),
            ( 'MM', 'ff0055ff' ) )

points = [ '1', '2', '4', '6', '8', '10']

ayear = str(date.today().year)

#<href>http://maps.google.com/mapfiles/kml/pal5/icon6.png</href>
#<href>http://maps.google.com/mapfiles/kml/paddle/{}.png</href>
header = """<?xml version="1.0" encoding="UTF-8" ?>

<!--KML file created by KCs-->
<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2">
  <Document xmlns:xlink="http://www.w3/org/1999/xlink">
    <name>SOTA-YO</name>"""

styles = "".join( """
    <Style id="pm-{}">
      <IconStyle>
        <color>{}</color>
        <scale>0.8</scale>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/pal5/icon6.png</href>
        </Icon>
      </IconStyle>
      <LabelStyle>
        <color>{}</color>
      </LabelStyle>
    </Style>""".format( r[0].lower(), r[1], r[1] ) for r in regions )

styles += """
    <Style id="pm-a">
      <IconStyle>
        <color>ff00aaff</color>
        <scale>0.8</scale>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/pal5/icon6.png</href>
        </Icon>
      </IconStyle>
      <LabelStyle>
        <color>ff00aaff</color>
      </LabelStyle>
    </Style>
    <Style id="pm-o">
      <IconStyle>
        <color>aa00aaff</color>
        <scale>0.8</scale>
        <Icon>
          <href>http://maps.google.com/mapfiles/kml/pal5/icon6.png</href>
        </Icon>
      </IconStyle>
      <LabelStyle>
        <color>aa00aaff</color>
      </LabelStyle>
    </Style>"""

folder_begin = """
    <Folder>
       <name>{}</name>"""

placemark = """
      <Placemark>
        <name>{} {}</name>
        <description>{}Alt.: {}m, Prom.: {}m, Key col: {},{}, Locator: {}{}</description>
        <styleUrl>#pm-{}</styleUrl>
        <Point>
          <coordinates>{},{},0</coordinates>
        </Point>
      </Placemark>"""

folder_end = """
    </Folder>"""

footer = """
  </Document>
</kml>
"""




gpx_header = """<?xml version="1.0" encoding="UTF-8" ?>
<gpx version="1.1"
     creator="YO6PIB"
     xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"
     xmlns="http://www.topografix.com/GPX/1/1"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <metadata>
    <name>SOTA YO summit list</name>
  </metadata>
"""

gpx_placemark = """
  <wpt lat="{}" lon="{}">
    <ele>{}</ele>
    <name>{} {}</name>{}
    <sym>Summit</sym>
  </wpt>"""

yoff_comment =  """
    <cmt>{}</cmt>"""

gpx_footer = """
</gpx>
"""

gpx = gpx_header


roman_nevek = (
  'Ciuha Mare',
  'La Balaur'
)

kml = header + styles

for region in regions:
    rname = region[0]

    with open( '../../Work/%s.csv' % rname, 'r', encoding='utf-8', newline='' ) as f:
        reader = csv.DictReader( f )

        # start a new folder
        kml = kml + folder_begin.format( rname )
        for row in reader:
            if row[ 'Reference' ]:
                if row[ 'To' ] == '' and row[ 'From' ]:

                    alt_name = row[ 'Alternative Name' ]
                    if alt_name and alt_name not in roman_nevek:
                        name = alt_name
                        alt_name = row[ 'Name' ] + ', '
                    else:
                        name = row[ 'Name' ]

                    yoff = row['YOFF']
                    if yoff:
                        yoff = ', inside ' + yoff

                    if row['Last activated'].endswith(ayear):
                      activ = 'a'
                    elif row['Last activated']:
                      activ = 'o'
                    else:
                      activ = rname.lower()

                    kml = kml + placemark.format( row[ 'Reference' ],
                                                  name,
                                                  alt_name,
                                                  row[ 'Altitude' ],
                                                  row[ 'Prominence' ],
                                                  row[ 'Col Longitude' ],
                                                  row[ 'Col_Latitude' ],
                                                  row[ 'Locator' ],
                                                  yoff,
                                                  activ,
                                                  row[ 'Longitude' ],
                                                  row[ 'Latitude' ] )

                    yoff = row[ 'YOFF' ]
                    if yoff:
                        yoff = yoff_comment.format( yoff )

                    gpx = gpx + gpx_placemark.format( row[ 'Latitude' ],
                                                      row[ 'Longitude' ],
                                                      row[ 'Altitude' ],
                                                      row[ 'Reference' ],
                                                      name, yoff )

        kml = kml + folder_end

kml = kml + footer

with open( '../summits/sota-yo.kml', 'w', encoding='utf-8' ) as kml_file:
    kml_file.write( kml )

gpx = gpx + gpx_footer

# replace romanian character, GPSMAP does not recognize them
cced = {
    0x218: 'Ş',
    0x219: 'ş',
    0x21A: 'Ţ',
    0x21B: 'ţ'
}
gpx = gpx.translate( cced )

with open( '../summits/sota-yo.gpx', 'w', encoding='utf-8' ) as gpx_file:
    gpx_file.write( gpx )


