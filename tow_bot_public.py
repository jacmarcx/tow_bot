#################################################################
### Notes:
#################################################################


import pandas as pd
import geopandas as gpd
import numpy as np
import requests
import json
import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.transforms import offset_copy
import twitter
import math
import re
import csv
import datetime
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.ops import transform
import pyproj
import cartopy
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
# import geoplot as gplt
# import geoplot.crs as gcrs
import time
import pytz
from PIL import Image
import creds


# list has grown out of control... move to csv.
words = ["Uh oh... someone parked on {} is about to get towed!",
         "If you're parked on {}, your car may have already been towed away.",
         "Dear Winnipeg scofflaw parked illegally on {}... you're about to get a $100 rush hour parking fine.",
         "Person blocking rush-hour traffic on {} with their parked car: the tow truck is coming for you!",
         "Fun fact: someone parked illegally on {} is about to get a $100 rush hour fine and a $120 towing bill. Ouch!",
         "Tow truck is on its way! Someone parked on {} is about to have a bad day.",
         "City: By-Law No. 86/2016 says you can't park on main roads during rush hours.\r\n\r\nPerson about to get towed on {}:\r\n¯\_(ツ)_/¯",
         "Yikes! If you're parked on {} a tow truck is coming for you this very moment!!!",
         "Hey person parked illegally on {}... drop what you're doing an run to your car, cuz the tow truck is coming for you!",
         "To the person parked on {} during rush hour, the tow truck is on it's way. Thank you for generously donating to the city's general revenues!",
         "Looks like a tow truck is about to do the owner of that illegally parked PT Cruiser on {} a favour. Maybe bring it straight to the auto wreckers?",
         "Dr. Hook thanks the owner of the car illegally parked on {}. You have just partially subsidized their staff's next team building outing.",
         "The tow about to happen to the illegally parked car on {} is dedicated to all Winnipeg motorists trying to get to work/home on time.",
         "+1 car about to get towed on {} by the city = +1 rider for Winnipeg transit... conspiracy?",
         "Clap for the Towman, he gon' make your tow bill high (...if you're parked on {}... right this instant)",
         "Thank you to the car parked on {} right now. Your contribution to the city's general revenues will help patch a single pothole.",
         "Take a shot each time a car parked on {} during rush hour gets towed. (*takes shot*)",
         "Dear Trans AM owner parked on {}: your car is about to get towed. Thank you for funding road improvements in Transcona.",
         "To the confused car owner on {}: your car was not stolen, it was towed away just right now.",
         "To the sad looking guy on {}: your car was just towed, so you'll have to pick up your date in St. Norbert with your bicycle. BMX pegs 50% off at Royal Sports.",
         "Took the restrictor plate off to give the Red Dragon a little more juice, but it's not exactly street legal... and neither is the parking job by the driver parked on {}... tow truck on its way!",
         "Roses are red, violets are blue, the guy parked on {} is getting towed, all commuters say 'Yahoo!'.",
         "Alouette, gentille alouette. Aloutette, je te remorquerai ..... right now on {}",
         "Life is a highway, I want to ride it all night long.... are not lyrics being sung by the dude on {} about to get towed."
         "Will the owner of a 1995 Buick LeSabre please see the front desk? Your car parked on {} is about to be towed.",
         "Person parked on {}: hope you wore your running shoes today...cuz your car is about to get towed.",
         "Con: person parked on {} is about to have their car towed.\r\nPro: person parked on {} will definitely get their 10,000 steps in today.",
         "The person parked on {} who is about to get towed may have thus far avoided paying for pot-hole related damage to their car, but they won't be escaping the parking and tow fine!",
         "Better call an Uber if you're currently parked on {}... your car will be towed away shortly.",
         """"I have your car towed all the way from {} to the impound lot and all you've got for me is lite beer?" -Biff Tannen""",
         "Oh, about that car parked on {}..... yeah.... it's been towed away.",
         "The person currently parked on {} is about to get towed away.... unless, of course, they are part of the Trucker Convoy.",
         """The person parked on {}: Tua currus est ad adepto puppibus !\r\n\r\nThat's Latin for "your car is about to get towed!" """,
         "It's a bird!\r\nIt's a plane!\r\n.... nope: its a tow truck coming for the car parked on {}",
         "Word on the street is the tow truck driver coming for the car illegally parked on {} has an extra Nickleback ticket.",
         """"Yo my guy parked on {}: you're about to get your Prius yeeted by a tow truck any minute now!" - Louis Riel""",
         "To be towed on {}, or not to be towed on {}: that is the question.",
         "If the car illegally parked on {} gets towed and no one is around to see it... does Dr. Hook have it in its gated lot?",
         "There are only two guarantees in life: Paying taxes, and getting your car towed on {} during rush hour by virtue of City of Winnipeg By-Law No. 86/2016.",
         "The person parked on {}: 10 minutes ago would have been a good time to not park illegally on the street during rush hour.",
         "My crystal ball tells me the dude wearing an Ed Hardy shirt on {} is about to get his car towed.",
         "Did you hear the one about the tow truck headed for the car illegally parked on {}? Wedding is this weekend, the truck and car are getting hitched.",
         "Car blocking rush hour traffic parked on {} is about to get towed! It's tow-tally amazing!",
         "To the podiatrist whose car is parked illegally on {}: I hear the toe truck is on it's way...",
         "Twinkle twinkle little car (on {}) you're about to get towed far.",
         "...and on the Eigth Day, thou shalt tow the dude parked on {}",
         "The Gods of free-flowing motor vehicle traffic shall banish the chariot parked illegally on {} to the purgatory that is Dr. Hook's compound.",
         "Ye who parks illegally during rush hour in Winnipeg on {} will be towed momentarily.",
         "A tow truck driver pounding back a Monster Energy drink is coming for the car parked illegally on {}.",
         "Person parked illegally on {} during rush hour: I just have to run into the store quick... my car is safe for this short moment.\r\n\r\nTow truck driver: Hold my beer.",
         "Superman never made any money.... cause he kept getting his Dodge Neon towed while parked illegally on {}",
         "I've got a fever, and the only prescription is towing the car illegally parked on {} this very moment.",
         "The car currently parked on {} during rush hour is sooooo tow-worthy.",
         "You better watch out, you better not cry, you better not pout I'm telling you why: Santa Tow is coming to {}",
         "On this day in 1933, scientists split an atom for the very first time in history. Also on this day: Keith from Point Douglas got his car towed while parked on {} during rush hour.",
         "Did you know that Venus is the only planet that spins clockwise? Did you also know the PT Cruiser parked on {} is about to get towed?",
         "The dad with the Dodge Caravan currently parked on {}, heads up, you will have to pick your kids up from daycare on foot today.",
         """"I wish the city had more revenues to repair our crumbling roads" - Lady having a conversation, unaware of the fact that she's got a hefty parking ticket and her Prius is currently being towed away on {}.""",
         """"Jeanne's Cakes are the best cakes ever." - says a grandmother while looking at the car currently being towed away on {} from the comfort of her personal care home balcony.""",
         """"I hate Winnipeg" is what the driver currently stuck behind the illegally parked car about to get towed on {} is saying during his rush hour commute.""",
         "The Golden Boy has a perfect vantage point from which he can see the imminent towing of the beater currently parked illegally on {}",
         "Deep into the darkness, peering...long I stood there wondering, fearing, doubting, dreaming dreams no mortal ever dared to dream before...oh wait. Yep. that dude parked on {} is getting towed.",
         "Oh damn! Dr. Hook is out for blood today! The car currently parked on {} is a goner.",
         "Tow trucks are circling the block like a shiver of sharks. That car parked illegally on {} is fish bait any second now.",
         "To the owner of the '93 Ford Taurus getting towed on {} right this instant: Just let it go. It's a write off anyway.",
         """"Today is the greatest day to be alive!" - guy currently parked in a no stopping zone during rush hour on {}, unaware his car is getting towed.""",
         "Not sure if a sinkhole has swallowed your vehicle or if it was towed, but it's no longer parked on {}",
         "Have you ever wanted to see what an impound lot looks like? Good news if your car was illegally parked on {} just right now.",
         """Heard recently on {}: "Mr. Tow, that's my name! That name again is Mr. Tow!" """,
         "A very low-tech self-driving demonstration happening right now on {} thanks to an illegally parked vehicle and a tow truck.",
         "Why did Dr. Hook cross the road? To tow the Volkswagen Cabriolet parked illegally on {}",
         "Keith, the driver at Taran Towing has been dreaming about towing the 2001 Pontiac Sunfire currently parked illegally on {} his whole life.",
         "Now you see the car parked illegally on {}, now you don't see the car parked illegally on {}",
         "Rumour has it the T-Bird belonging to @ralphmurlax currently parked illegally on {} is about to get a fine and tow!",
         """ "More curb lanes should be converted into dedicated cycling routes" - @brent_bellamy as his illegally parked F-250 is getting towed away on {} one block over.""",
         "Maroon Chevy Lumina about to get towed on {}... not that there's anything wrong with that.",
         "Councillor @mathieuallard just tweeted that he's riding the bus, so his car is probably not the one on {} currently being towed away.",
         """ "Dude, where's my car?" - Brock from St. Vital with a stunned look on his face, holding a protein shake while standing on {}""",
         "This isn't the height of Winnipeg's 2007 auto theft crisis... so that missing car with an immobilizer that was parked on {} was probably just towed away.",
         "To the infidel atheist with the '98 Suzuki Swift illegally parked on {}: pray to God that you get to your car before Dr. Hook does.",
         "Safe to assume the car that just towed away on {} belongs to someone in North River Heights since it had a garbage bag duct taped over the broken passenger side window.",
         "The guy whose car was just towed away from {} apparently lives in South Waverley West: A fact that made this among the better days of this difficult week.",
         "Head for the hills! Tow truck driver headed for the car parked illegally on {} has been crushing Red Bulls all day!",
         "Oooh Look! A state-of-the-art driverless electric vehicle in Winnipeg. So cool!\r\n\r\nOh wait, never mind: It's a car on {} being towed away.",
         "Another tow, another dollar... {} is cleared of cars blocking traffic.",
         "Shirley is too distracted, wondering when the city will finally pull the trigger on an indoor waterpark, to realize her car parked illegally on {} is about to get towed away.",
         "Aww look, CAA is helping boost that car parked on {} with a dead battery. Oh wait, never mind, that's Dr. Hook about to haul it back to its secret compound.",
         "The oblivious owner of the car blocking rush hour traffic on {} thinks he's having a great day so far because his neighbour just confirmed for him that his basement is still water free.",
         "Is that large statue thingy in front of the Court House supposed to be an elephant or something? Oh, also a car on {} is getting towed as we speak.",
         "Driver parked on {} just got towed for no-stopping during rush hour. Crummy luck. He was just trying to find the old Palomino Club.",
         "Maybe the tow truck that just got the car on {} will also need to call for a tow truck after it destroys a wheel bearing in any number of pot holes en route to the compound.",
         "Legally speaking, if the owner of the '93 Honda Civic about to get towed on {} just sits in her car, the truck driver can't haul it away. #BadLegalTakes",
         "Heads up to the guy parked on {}: The no-stopping By-Law has just been amended by EPC. Illegally parked car owners can now choose between getting towed or having their catalytic converter torn out by a parking officer.",
         "To the lady whose car was just towed away on {}, know that the tow truck driver on shift takes each tow job very personally.",
         "Tow truck guy on {} is making vehicular traffic great again.",
         "If there's a silver lining for the owner of the car being towed away on {}, it's that only 50% of his vehicle's wheels are at risk of pot hole damage",
         "The person whose car just got towed away on {} better get in touch with WiseUp Winnipeg to launch a Charter challenge.",
         "At long last, Dr. Hook found its White Whale parked illegally on {}",
         """The person parked on {}: Malapit nang mahatak ang sasakyan mo !\r\n\r\nThat's Tagalog for "your car is about to get towed!" """,
         "Hey Winnipeg Free Press, got some breaking news to report: Maroon Pontiac Aztek getting towed away on {} this very moment. Story writes itself.",
         "The owner of the Dodge Caravan with wood paneling and stick shift getting towed on {} is such a Legend.",
         "OBVIOUSLY that Escalade getting towed on {} has Winnipeg Jets plates.",
         "Little Lucy Smith from White Ridge will definitely be missing gymnastics tonight since her mom just the family Audi towed on {}",
         "Apparently Obama was in town to register for mayoral race, but just changed his mind and left town after his car was towed on {} Thanks Winnipeg Parking Authority.",
         "Tow truck is making off with Dodge Ram illegally parked on {}\r\n\r\nThanks Trudeau.",
         "Hey Winnipeg, this is Steve Boychuk, the tow truck operator on call right now. If you're currently parked on {} you've got about five minutes before I'm towing your sedan off to the yard.",
         "Hey Winnipeg, this is Steve Boychuk, the tow trcuk operator on call right now. Just finished boosting a dead car battery downtown, but I've just been dispatched to tow away the pick up on {}.\r\n\r\nFair warning.",
         "Steve Boychuk here. Just starting my tow shift and the parking authority already radioed in for a tow on {} just right now. If that's your car, it's your lucky day, cause lineup at the Tim's drive thru is just the craps.",
         "Steve Boychuk again. Just wrapping up my tow truck shift here, and there's a cute beige Subaru Crosstek parked illegally on {}.\r\n\r\nMaybe I'll tow it, maybe I won't.",
         "The guy whose Dodge Charger has just been hitched by the tow truck on {} is currently laying on the street blocking the tow truck from driving off. Gotta run, so I'll just read the Winnipeg Sun in the morning to see how this ended.",
         "Found my coat and grabbed my hat, made the bus in seconds flat... because my illegally parked car just got towed from {}",
         "Did the no-parking-during-rush-hour By-Laws change or something? Just saw @brent_bellamy get his bicycle towed on {}",
         "Just witnessed the most meta towing ever on {}: Dr. Hook just towed away a Titan Towing truck that was boosting a CAA truck.",
         "Steve Boychuk on tow shift here. Car owner was literally just chasing after me after I towed his Taurus from {}. Guy tripped on the curb and lost his shoe. So unreal. Anyway, sorry bud but cars in the lot now.",
         "The unwitting Chevy Impala enjoys the bountiful sunshine on {}, unaware as yet of the dangers lurking in the shadows of a nearby building. Rush hour commences. The mighty tow truck springs into action. The ritualistic carnage is over; the Impala is no more."
         ]


def extent_calculator(locations):
    """
    Function to determine the extents in cases of
    multiple points on a map to maintain a
    lng_diff/lat_diff ratio of 1.33 at all time.
    Also adds a padding for margins.
    Key is to adjust the coordinate value to adjust bounding box... not the pad

    Note: this is sketch, consider using a Projected CRS.
    """
    # pads that ensure lng_diff/lat_diff ratio of 1.333
    # get actual min and max values for lat and lngs from entire list of locations
    # these are only final if dealing with a single image

    # max width = 25,000

    min_lng, max_lng = min([pair[0]  for pair in locations]), max([pair[0]  for pair in locations])
    min_lat, max_lat = min([pair[1]  for pair in locations]), max([pair[1]  for pair in locations])

    # diffs provide length of smallest bounding box edges
    diff_lng = (max_lng - min_lng)
    diff_lat = (max_lat - min_lat)

    #determine whether  lats or lngs need adjustment to maintain 2.0 aspect ratio.
    if diff_lat > diff_lng:
        # when lat edge is longest, then must adjust the lng coords
        y0, y1 = min_lat, max_lat # keep original lats

        # caclute new coords
        diff_lng_new = 1.333*diff_lat # get needed edge length

        # get increase to add to min and max
        addx = (diff_lng_new/2)-(diff_lng/2)
        x0, x1 = min_lng-addx, max_lng+addx

    else:
        # when Lng edge is longest, then must adjust the lat coords
        x0, x1 = min_lng, max_lng # keep original

         # caclute new coords
        diff_lat_new = diff_lng/1.333 # get needed edge length

        addy = (diff_lat_new/2)-(diff_lat/2)
        y0, y1 = min_lat-addy, max_lat+addy

    ####  now add appropriate padding ###
    longest = x1-x0 # based on longest edge

    # default for zero is 4000 and 3000
    lng_pad = 800 + (longest/15) # x
    lat_pad = 600.15 + ((longest/1.33)/15) # y

    x0, x1, y0, y1 = x0-lng_pad, x1+lng_pad, y0-lat_pad, y1+lat_pad # add pads

    return [x0, x1, y0, y1]


def tweet_selector(pool):
    """Chooses a random tweet from the list"""
    return random.choice(pool)


def send_tweet(tweet_text, image=''):
    """
    Publish tweet (without or without media)
    If image value left as empty string, tweet without media.
    """
    consumer_key = creds.consumer_key
    consumer_secret = creds.consumer_secret
    access_token = creds.access_token
    access_secret = creds.access_secret

    t = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token,
                      access_token_secret=access_secret)

    t.PostUpdate(status=tweet_text,
                 media=image)


def geocode_intersection(street, cross):
    """
    Function for geocoding approximate locations of tow records.
    Does not accept a list of items.
    Searches for matches in street name against city's road network data.
    Attempts to geocode intersection of street and cross using geocoder.ca
    If confidence falls below 0.9 returns None.
    """
    # dirty strings from tow data
    on_street_dirty = street
    cross_street_dirty = cross

    # find street name matches against city's roadnetwork inventory using
    # network file saved as csv
    with open('/root/towscripts/streets.csv', 'r', newline="") as f:
        csvreader = csv.reader(f)

        # set variables
        on_street_clean, cross_street_clean = None, None

        # find matching street
        for street in csvreader:
            if on_street_clean is None:
                if bool(re.search(street[0], on_street_dirty, flags=re.IGNORECASE)):
                    on_street_clean = street[0]

            if cross_street_clean is None:
                if bool(re.search(street[0], cross_street_dirty, flags=re.IGNORECASE)):
                    cross_street_clean = street[0]

            # check for matches found for both variables....
            if (on_street_clean and cross_street_clean) is not None:
                break
    try:
        # geocode using free tool at geocoder.ca
        r = requests.get(f'https://geocoder.ca/?locate={on_street_clean}+AT+{cross_street_clean}+winnipeg+mb&geoit=XML&json=1')
        data = json.loads(r.text)
        # test for error when no match is found
        try:
            # test for confidence level in geocode when match is found
            # reject all results under 0.9
            try:
                if float(data['standard']['confidence']) < 0.9:
                    coords = None
                else:
                    lat, lng = float(data['latt']), float(data['longt'])
                    coords = [lng, lat]
            except:
                if float(data['confidence']) < 0.9:
                    coords = None
                else:
                    lat, lng = float(data['latt']), float(data['longt'])
                    coords = [lng, lat]
        except:
            coords = None
    except:
        coords = None # if no matching street is found during loop

    return coords # returns either coords or nothing


def determine_coords_logic(data, geocoding=True):
    """
    Function for organizing the collected coordinates,either
    through available POINT data or via geocoding.
    Append all records (single or array) to list of lists.
    Accept list of data features from the JSON.
    """
    # build transformer
    wgs84 = pyproj.CRS('EPSG:4326')
    utm = pyproj.CRS('EPSG:26914')
    crs_convert = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform

    coords_list = [] # list of lists

    for d in data:
        # get geo if available
        try:
            coords = d['geometry']['coordinates']
            #set as point
            wgs84_pt = Point(coords)
            #convert CRS
            utm_point = transform(crs_convert, wgs84_pt)
            coords_list.append([utm_point.x, utm_point.y])
        except:
            if geocoding:
                # geocode location
                # get street strings
                street = d['properties']['location_pickup']
                street_cross = d['properties']['cross_streets_pickup']

                # error handling built into geocode func. Upon error return None
                geo_coords = geocode_intersection(street, street_cross) # geocode

                if geo_coords is None:
                    pass
                else:
                    # convert CRS
                    wgs84_pt = Point(geo_coords)
                    utm_point = transform(crs_convert, wgs84_pt)
                    coords_list.append([utm_point.x, utm_point.y])
            else:
                pass

    return coords_list



def crop_map(img):
    """
    Function for cropping out weird GoogleSatellite frame and
    the whitespace.
    """
    im = Image.open(img)

    # set pixel coordinate box values
    if 'roundup' in img:
        # city wide snap shot
        (left, upper, right, lower) = (25, 20, 940, 750)
    else:
        # 4:3 aspect ratios
        (left, upper, right, lower) = (28, 46, 953, 740)

    im1 = im.crop(box=(left, upper, right, lower))
    im1.save(img) # overwrite original with newly cropped image


def make_point_map(locations, map_type):
    """
    Function for generating map image for tweeting.
    Auto scales markers and zoom based on extent of map.
    Also uses the extent calculator function to ensure
    map aspect ratio (4:3) is consistent no matter the distributin of markers.
    """
    locations = [l for l in locations if l is not None] # ditch None values, otherwise throws error

    # reject any coodinates that fall outside of bounding box around city
    # rough set of nodes drawing towing territory
    city_coords = [[620397,5521833],[627701,5522320],[628523,5512399],[634031,5511760],
                    [635644,5516964],[642339,5520798],[642095,5527798],[646843,5528194],
                    [645078,5533671],[634366,5539362],[619241,5528498]]

    city = Polygon(city_coords)

    locs = []

    for c in locations:
        if c is None: # redundant
            continue
        elif Point(c).within(city): # check if geo is inside the city
            locs.append(c)

    googlesat = cimgt.GoogleTiles(style='satellite')
    fig = plt.figure(figsize=(10, 8))

    # Create a GeoAxes in the tile's projection.
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.UTM(zone=14, southern_hemisphere=False))

    # get extents for setting map limits
    exts = extent_calculator(locs)

    # get marker scale,  zoom level and marker circle diamter
    scaling = (exts[1]-exts[0]) - 2000 # subtract buffer added from extents
    # get marker scale, marker circle diamter and zoom level (int)
    ms, s, z = 30-(scaling*0.0005), 180-(scaling*0.005), int(round(16-(scaling*0.0002),0))

    #pass output of extent calculator function # x0, x1, y0, y1

    ax.set_extent(exts, crs=ccrs.UTM(zone=14, southern_hemisphere=False))

    # Add the google sat data at zoom level 8.
    ax.add_image(googlesat, z)

    # generate map markers and plot
    for lng, lat in locs:
        ax.plot(lng, lat, marker='.', markerfacecolor='#E40017', markeredgecolor='#EEEEEE', markersize=ms,
                alpha=1.0, transform=ccrs.UTM(zone=14, southern_hemisphere=False), zorder=100)

        if map_type == 'single': # ditch big circle around marker is multiple dots
            ax.plot(lng, lat, marker='o', markersize=s, markerfacecolor='#E40017', markeredgecolor='#E40017',
                    alpha=0.1, transform=ccrs.UTM(zone=14, southern_hemisphere=False), zorder=100)
            ax.plot(lng, lat, marker='o', markersize=s, markerfacecolor='None', markeredgecolor='#E40017',
                    alpha=1, transform=ccrs.UTM(zone=14, southern_hemisphere=False), zorder=100)
        else:
            pass

    ax.text(x=0.808, y=0.135, s='@TowAlertWpg', fontsize=20,
            verticalalignment='center', horizontalalignment='center',
            transform=fig.transFigure,
            bbox=dict(facecolor='white', alpha=0.7, boxstyle='square'))

    plt.tight_layout()
    fname = '/root/towscripts/map_point.png'
    plt.savefig(fname, dpi=100)
    plt.close()
    crop_map(fname) # crop to remove whitespace and frame



def make_roundup_point_map(locations):
    """
    Backup function to tweet multi dot events for rounds up,
    since heat map is not workable in linux
    """
    locations = [l for l in locations if l is not None] # ditch None values, otherwise throws error

    # reject any coodinates that fall outside of bounding box around city
    # rough set of nodes drawing towing territory
    city_coords = [[620397,5521833],[627701,5522320],[628523,5512399],[634031,5511760],
                    [635644,5516964],[642339,5520798],[642095,5527798],[646843,5528194],
                    [645078,5533671],[634366,5539362],[619241,5528498]]

    city = Polygon(city_coords)

    locs = []

    for c in locations:
        if c is None: # redundant
            continue
        elif Point(c).within(city): # check if geo is inside the city
            locs.append(c)

    googlesat = cimgt.GoogleTiles(style='satellite')
    fig = plt.figure(figsize=(10, 8))

    # Create a GeoAxes in the tile's projection.
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.UTM(zone=14, southern_hemisphere=False))

    # fixed extents in
    exts = [-97.32079, -96.97935, 49.78732, 49.96385]

    #pass output of extent calculator function # x0, x1, y0, y1
    ax.set_extent(exts, crs=ccrs.Geodetic())

    # Add the google sat data at zoom level 8.
    ax.add_image(googlesat, 13)

    # generate map markers and plot
    for lng, lat in locs:
        ax.plot(lng, lat, marker='.', markerfacecolor='#E40017', markeredgecolor='#EEEEEE', linewidth=0.5, markersize=14,
                alpha=0.65, transform=ccrs.UTM(zone=14, southern_hemisphere=False), zorder=100)

    ax.text(x=0.80, y=0.12, s='@TowAlertWpg', fontsize=20,
            verticalalignment='center', horizontalalignment='center',
            transform=fig.transFigure,
            bbox=dict(facecolor='white', alpha=0.7, boxstyle='square'))

    plt.tight_layout()
    fname = '/root/towscripts/map_roundup_point.png'
    plt.savefig(fname, dpi=100)
    plt.close()
    crop_map(fname) # crop to remove whitespace and frame


# def make_heat_map(locations):
#     """
#     Requires funcs for this (Geoplot) won't install in Droplet
#     Function for generating a weekly or historic roundup image for tweeting.
#     Extent is fixed for all Winnipeg.
#     Does not respect map aspect ratio.
#     No clear understanding of the projections and crs
#     """
#     locations = [l for l in locations if l is not None] # ditch None values, otherwise throws error
#
#     # reject any coodinates that fall outside of bounding box around city
#     # rough set of nodes drawing towing territory
#     city_coords = [[620397,5521833],[627701,5522320],[628523,5512399],[634031,5511760],
#                     [635644,5516964],[642339,5520798],[642095,5527798],[646843,5528194],
#                     [645078,5533671],[634366,5539362],[619241,5528498]]
#
#     city = Polygon(city_coords)
#
#     locs = []
#
#     for c in locations:
#         if c is None: # redundant
#             continue
#         elif Point(c).within(city): # check if geo is inside the city
#             locs.append(c)
#
#     googlesat = cimgt.GoogleTiles(desired_tile_form="L", style='satellite')
#     fig = plt.figure(figsize=(10,8))
#
#     # Create a GeoAxes in the tile's projection.
#     ax = fig.add_subplot(1, 1, 1, projection=googlesat.crs)
#
#     # fixed extents in
#     exts = [-97.32079, -96.97935, 49.78732, 49.96385]
#     extskdeplot = [-97.32079, 49.78732, -96.97935, 49.96385] #min_longitude, min_latitude, max_longitude, max_latitude
#     ax.set_extent(exts, crs=ccrs.Geodetic()) ## problem is extents! , crs=ccrs.Geodetic()
#
#     # Add the google sat data at zoom level 8.
#     ax.add_image(googlesat, 12, cmap="gray")
#
#     # generate map markers and plot
#     pts = gpd.GeoSeries([Point(l) for l in locs], crs='EPSG:26914').to_crs("EPSG:4326")
#
#     gplt.kdeplot(pts, cmap='Greys',shade=False, alpha=1, thresh=0.0, n_levels=20, ax=ax, extent=extskdeplot, projection=gcrs.Mercator()) # , projection=gcrs.Mercator()
#
#     # ax.scatter(pts.x, pts.y, marker='o', c='Red', edgecolor='Red', s=20, zorder=1000, transform=ccrs.Geodetic()) # #FF3333 , transform=ccrs.Geodetic() , transform=ccrs.Mercator()
#     # ax.axis('on')
#     # ax.axes.get_xaxis().set_visible(True)
#     # ax.axes.get_yaxis().set_visible(True)
#
#     ax.text(x=0.80, y=0.12, s='@TowAlertWpg', fontsize=20,
#             verticalalignment='center', alpha=0.7, horizontalalignment='center',
#             transform=fig.transFigure,
#             bbox=dict(facecolor='white', boxstyle='square'))
#
#     plt.tight_layout()
#     fname = 'roundup_map_heat.png'
#     plt.savefig(fname, dpi=100)
#     plt.close()
#     crop_map(fname)

########### tweet schedule ###############

# base url for API
url_base = 'https://data.winnipeg.ca/resource/8phf-9kb6.geojson{}'

def eod_roundup(timestamp):
    """
    Operates: weekdays at 18am
    Provide a round up for the weekday morning.
    Include heat map and basic stats at 11am each weekday.
    """
    query = f"?$query=SELECT * WHERE (status = 'Cleared') and (request_date BETWEEN '{timestamp}T06:59:00' and '{timestamp}T17:31:00')"
    r = requests.get(url_base.format(query))
    data = json.loads(r.text)

    # get list of records
    records = [d for d in data['features']]

    try:
    # loop over each entry and geocode or if geom avail, add to list of coords
        coordinates = determine_coords_logic(data=records)

        text = ("A total of {} vehicles were towed for parking illegally "
                "during the morning and afternoon rush hour today. "
                "Here's where those pesky parkers were towed from (note: some dots may overlap):")
        # check if list if full of Nones
        if all(x is None for x in coordinates):
            # has nothing to map
            send_tweet(words.format(street), image='')
        else:
            make_point_map(coordinates, 'multiple') # make the map
            send_tweet(text.format(len(records)), image='/root/towscripts/map_point.png')

    # if no records or reponses..
    except:
        pass


def week_roundup(timestamp):
    """
    Operates: Saturday at 11am
    Provide a round up of the past week.
    Include heat map and basic stats each 11am Saturday.
    """
    # get monday and friday
    mon = (datetime.datetime.strptime(timestamp, '%Y-%m-%d') - datetime.timedelta(days=5)).strftime('%Y-%m-%d')
    fri = (datetime.datetime.strptime(timestamp, '%Y-%m-%d') - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    query = f"?$query=SELECT * WHERE (status = 'Cleared') and (request_date BETWEEN '{mon}T06:59:00' and '{fri}T17:31:00')"
    r = requests.get(url_base.format(query))
    data = json.loads(r.text)

    # get list of records
    records = [d for d in data['features']]

    try:
    # loop over each entry and geocode or if geom avail, add to list of coords
        coordinates = determine_coords_logic(data=records)
        # check if list if full of Nones
        text = ("A total of {} vehicles were towed for parking illegally "
                "during rush hour over the past week. "
                "Here is where they were primarly located (note: many dots overlap):")

        if all(x is None for x in coordinates):
            # has nothing to map
            send_tweet(text.format(len(records)), image='')
        else:
            make_roundup_point_map(coordinates) # make the map
            send_tweet(text.format(len(records)), image='/root/towscripts/map_roundup_point.png')


    # if no records or reponses..
    except:
        pass


def historical(timestamp):
    """
    Not currently in use. Ideally use Geoplot for heatmap...but bugs to work out.
    Operates: Saturday at 11am
    Provide a round up of the past week.
    Include heat map and basic stats each 11am Saturday.
    """
    # get monday and friday
    mon = (datetime.datetime.strptime('2022-01-03', '%Y-%m-%d') - datetime.timedelta(days=5)).strftime('%Y-%m-%d')
    fri = (datetime.datetime.strptime(timestamp, '%Y-%m-%d') - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    query = f"?$query=SELECT * WHERE (status = 'Cleared') and (request_date BETWEEN '{mon}T06:59:00' and '{fri}T17:31:00')"
    r = requests.get(url_base.format(query))
    data = json.loads(r.text)

    # get list of records
    records = [d for d in data['features']]

    try:
    # loop over each entry and geocode or if geom avail, add to list of coords
        coordinates = determine_coords_logic(data=records, geocoding=False)
        # check if list if full of Nones

        text = ("Here is where the last 1,000 vehicles towed for illegally "
                "parking during Winnipeg's morning rush hour located (note: many dots overlap):")

        if all(x is None for x in coordinates):
            # has nothing to map
            send_tweet(text.format(len(records)), image='')
        else:
            make_roundup_point_map(coordinates) # make the map
            send_tweet(text.format(len(records)), image='/root/towscripts/map_roundup_point.png')

    # if no records or reponses..
    except:
        pass


def tow_warning(timestamp):
    """
    Operates: 7am to 9am and 3:30pm to 5:30pm on weekdays

    Grab the most recent pending tow request
    Note: swap "Cleared" with "Waiting" in api call when done
    testing and deployed.

    Query may bring in several records, but this function is
    currently designed to handle only a single coordinate plot.
    Need to loop over records to plot multiple.
    """
    query = f"?$query=SELECT * WHERE (status = 'Waiting') and (request_date BETWEEN '{timestamp}T06:50:00' and '{timestamp}T17:40:00') ORDER BY request_date"
    r = requests.get(url_base.format(query))
    data = json.loads(r.text) # get list of latest data for the day

    # determine if there is a new record to tweet.
    # if so, get index from API call and add to csv
    with open('/root/towscripts/tweets.csv', 'r', newline="") as f: # get previously tweeted records
        csvreader = list(csv.reader(f))[::-1] # reverse to start from bottom

        fresh_record_index = None # index for record that has not yet been tweeted
        add_timeval = None

        for i, d in enumerate(data['features']):

            checkpoint = d['properties']['request_date']

            if checkpoint in [row[0] for row in csvreader if len(row) != 0]:
                pass
            else:
                fresh_record_index = i
                add_timeval = checkpoint
    print(f"fresh_record_index={fresh_record_index}")
    print(f"add_timeval={add_timeval}")
    if (fresh_record_index and add_timeval) is None:
        print("no new tows to notify about")
        return
    else:
        # write new record timeval to csv
        with open('/root/towscripts/tweets.csv', 'a') as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow([add_timeval])

    try:
        # selected record to map
        record = [data['features'][fresh_record_index]]
        # get some record details
        street = data['features'][fresh_record_index]['properties']['location_pickup']

        # get coords
        coordinates = determine_coords_logic(data=record)
        print(f"street: {street}")
        # check if list if full of Nones
        if all(x is None for x in coordinates):
            # has nothing to map
            print("sending tweet with no map")
            send_tweet(tweet_selector(words).format(street), image='')
        else:
            print("sending tweet with map")
            make_point_map(coordinates, 'single') # make the map
            send_tweet(tweet_selector(words).format(street), image='/root/towscripts/map_point.png')

    # if no records exist or response failed do nothing
    except Exception as e:
        print(f"caught exception: {e}")
        pass

#################################################
### note Droplet surver time is set to UTC+0 ###
### must offset times by UTC -5 hours CDT    ###
### starting in March and -6 hours CST       ###
### starting in Nov. Using pytz lib          ###
################################################

# set timezone to convert server time to Winnipeg time
wpg = pytz.timezone('America/Winnipeg')

def is_time_between(start_time, end_time, check_time=None):
    """
    Function to check if current time (now) is in between a
    given start and and end time. Returns Bool.
    eg. is_time_between(datetime.time(7,0), datetime.time(9,30))
     between 7am and 9:30 am on any day.
    Note: must offset since server set to UTC+0
    """
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.datetime.now(wpg).time()
    if start_time < end_time:
        return check_time >= start_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= start_time or check_time <= end_time


def weekday_checker(check_day=None):
    """
    Get day of week string.
    eg. weekday_checker(datetime.date(2022,3,29))
    Note: must offset since server set to UTC+0
    """
    day_to_check = check_day or datetime.datetime.now(wpg)
    # get day of week
    dayofweek = day_to_check.strftime('%a')
    return dayofweek


def master_trigger():
    """
    Decides which function to run based on timestamp provided.
    This function can run on an endless while loop
    """
    if weekday_checker() in ['Mon','Tue','Wed','Thu','Fri']:

        # morning or afternoon rush hour test
        if is_time_between(datetime.time(6,55), datetime.time(9,5)) or is_time_between(datetime.time(15,25), datetime.time(17,35)):
            # run basic warning
            print("tow warning")
            tow_warning(datetime.datetime.now(wpg).strftime('%Y-%m-%d'))
        elif is_time_between(datetime.time(19,0), datetime.time(19,30)):
            # run end of day roundup
            print("eod_roundup")
            eod_roundup(datetime.datetime.now(wpg).strftime('%Y-%m-%d'))
        else:
            # do nothing
            print("Weekday but not during towing hours: do nothing")
            pass
    # end of week roundup
    elif (weekday_checker() == 'Sat') and (is_time_between(datetime.time(11,0), datetime.time(11,30))):
        print("running weekday roundup")
        week_roundup(datetime.datetime.now(wpg).strftime('%Y-%m-%d'))
    elif (weekday_checker() == 'Sun') and (is_time_between(datetime.time(11,0), datetime.time(11,30))):
        # historic roundup
        # print("running historic")
        # historic(datetime.datetime.now(wpg).strftime('%Y-%m-%d'))
    else:
        print("Doing nothing...")
        pass # do nothing if none of the above conditions are met.

##########################
######## testing #########
##########################

# historical('2022-04-15')
# week_roundup('2022-04-23')
# tow_warning('2022-04-07')

############################
####### Run trigger ########
############################
master_trigger()

print('Script ran successfully at: ' + datetime.datetime.now(wpg).strftime('%Y-%m-%d %H:%M:%S'))
print('****************')
print('')
