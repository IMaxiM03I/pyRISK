from assets_pg import *

### DEFINE TERRITORIES ###

# north america #
nAmerican_terr: dict[str: Territory] = {
    "alaska": Territory(name="Alaska", neighbours=["kamchatka", "nw territory", "alberta"], x=56, y=80),
    "nw territory": Territory(name="Northwest Territory", neighbours=["alaska", "alberta", "ontario", "greenland"], x=146, y=75),
    "greenland": Territory(name="Greenland", neighbours=["nw territory", "ontario", "quebec", "iceland"], x=325, y=50),
    "alberta": Territory(name="Alberta", neighbours=["alaska", "nw territory", "ontario", "w us"], x=122, y=120),
    "ontario": Territory(name="Ontario", neighbours=["alberta", "nw territory", "greenland", "quebec", "w us", "e us"], x=190, y=130),
    "quebec": Territory(name="Quebec", neighbours=["ontario", "greenland", "e us"], x=250, y=135),
    "w us": Territory(name="Western United States", neighbours=["alberta", "ontario", "e us", "central america"], x=105, y=185),
    "e us": Territory(name="Eastern United States", neighbours=["w us", "ontario", "quebec", "central america"], x=178, y=204),
    "central america": Territory(name="Central America", neighbours=["w us", "e us", "venezuela"], x=102, y=270)
}

# south america #
sAmerican_terr: dict[str: Territory] = {
    "venezuela": Territory(name="Venezuela", neighbours=["central america", "peru", "brazil"], x=162, y=318),
    "peru": Territory(name="Peru", neighbours=["venezuela", "brazil", "argentina"], x=140, y=407),
    "brazil": Territory(name="Brazil", neighbours=["peru", "venezuela", "n africa", "argentina"], x=234, y=390),
    "argentina": Territory(name="Argentina", neighbours=["peru", "brazil"], x=135, y=530)
}

# europe #
european_terr: dict[str: Territory] = {
    "iceland": Territory(name="Iceland", neighbours=["greenland", "gb", "scandinavia"], x=385, y=95),
    "scandinavia": Territory(name="Scandinavia", neighbours=["iceland", "gb", "ukraine", "n europe"], x=470, y=102),
    "ukraine": Territory(name="Ukraine", neighbours=["n europe", "scandinavia", "ural", "afghanistan", "middle e", "s europe"], x=540, y=160),
    "gb": Territory(name="Great Britain", neighbours=["iceland", "scandinavia", "n europe", "w europe"], x=368, y=170),
    "n europe": Territory(name="Northern Europe", neighbours=["gb", "scandinavia", "ukraine", "s europe", "w europe"], x=456, y=178),
    "w europe": Territory(name="Western Europe", neighbours=["gb", "n europe", "s europe", "n africa"], x=383, y=250),
    "s europe": Territory(name="Southern Europe", neighbours=["w europe", "n europe", "ukraine", "middle e", "egypt", "n africa"], x=470, y=234)
}

# africa #
african_terr: dict[str: Territory] = {
    "n africa": Territory(name="North Africa", neighbours=["brazil", "w europe", "s europe", "egypt", "e africa", "congo"], x=412, y=364),
    "egypt": Territory(name="Egypt", neighbours=["n africa", "s europe", "middle e", "e africa"], x=494, y=330),
    "e africa": Territory(name="East Africa", neighbours=["n africa", "egypt", "madagascar", "middle e", "s africa", "congo"], x=558, y=426),
    "congo": Territory(name="Congo", neighbours=["n africa", "e africa", "s africa"], x=488, y=456),
    "s africa": Territory(name="South Africa", neighbours=["congo", "e africa", "madagascar"], x=492, y=555),
    "madagascar": Territory(name="Madagascar", neighbours=["s africa", "e africa"], x=608, y=552)
}

# asia #
asian_terr: dict[str: Territory] = {
    "ural": Territory(name="Ural", neighbours=["ukraine", "siberia", "china", "afghanistan"], x=648, y=130),
    "siberia": Territory(name="Siberia", neighbours=["ural", "yakutsk", "irkutsk", "mongolia", "china", "afghanistan"], x=700, y=100),
    "yakutsk": Territory(name="Yakutsk", neighbours=["siberia", "kamchatka", "irkutsk"], x=768, y=64),
    "irkutsk": Territory(name="Irkutsk", neighbours=["siberia", "yakutsk", "kamchatka", "mongolia"], x=762, y=130),
    "mongolia": Territory(name="Mongolia", neighbours=["siberia", "irkutsk", "kamchatka", "japan", "china"], x=784, y=185),
    "kamchatka": Territory(name="Kamchatka", neighbours=["irkutsk", "yakutsk", "alaska", "japan", "mongolia"], x=846, y=74),
    "japan": Territory(name="Japan", neighbours=["mongolia", "kamchatka"], x=888, y=190),
    "afghanistan": Territory(name="Afghanistan", neighbours=["ukraine", "ural", "china", "india", "middle e"], x=634, y=205),
    "china": Territory(name="China", neighbours=["afghanistan", "ural", "siberia", "mongolia", "siam", "india"], x=756, y=242),
    "middle e": Territory(name="Middle East", neighbours=["egypt", "s europe", "ukraine", "afghanistan", "india", "e africa"], x=572, y=310),
    "india": Territory(name="India", neighbours=["middle e", "afghanistan", "china", "siam"], x=700, y=300),
    "siam": Territory(name="Siam", neighbours=["india", "china", "indonesia"], x=782, y=330)
}

# australia #
aussie_terr: dict[str: Territory] = {
    "indonesia": Territory(name="Indonesia", neighbours=["siam", "new guinea", "w australia"], x=795, y=436),
    "new guinea": Territory(name="New Guinea", neighbours=["indonesia", "e australia", "w australia"], x=908, y=416),
    "w australia": Territory(name="Western Australia", neighbours=["indonesia", "new guinea", "e australia"], x=850, y=556),
    "e australia": Territory(name="Eastern Australia", neighbours=["w australia", "new guinea"], x=960, y=550)
}



### <------------------------------------------> ###



### DEFINE CONTINENTS ###

classic_continents: dict[str: Continent] = {
    "n america": Continent("North America", "n america", nAmerican_terr, 5),
    "s america": Continent("South America", "s america", sAmerican_terr, 2),
    "europe": Continent("Europe", "europe", european_terr, 5),
    "africa": Continent("Africa", "africa", african_terr, 3),
    "asia": Continent("Asia", "asia", asian_terr, 7),
    "australia": Continent("Australia", "australia", aussie_terr, 2)
}

for continent in classic_continents.values():
    for id in continent.getTerritories().keys():
        continent.getTerritories()[id].setID(id)


### MAP ###

CLASSIC_MAP = pg.image.load(r'C:\Users\20210682\Documents\risk\maps\classic_map_v1-1_resized.png')
