from assets_console import *

### DEFINE TERRITORIES ###

# north america #
nAmerican_terr: dict[str: Territory] = {
    "alaska": Territory("Alaska", ["kamchatka", "nw territory", "alberta"]),
    "nw territory": Territory("Northwest Territory", ["alaska", "alberta", "ontario", "greenland"]),
    "greenland": Territory("Greenland", ["nw territory", "ontario", "quebec", "iceland"]),
    "alberta": Territory("Alberta", ["alaska", "nw territory", "ontario", "w us"]),
    "ontario": Territory("Ontario", ["alberta", "nw territory", "greenland", "quebec", "w us", "e us"]),
    "quebec": Territory("Quebec", ["ontario", "greenland", "e us"]),
    "w us": Territory("Western United States", ["alberta", "ontario", "e us", "central america"]),
    "e us": Territory("Eastern United States", ["w us", "ontario", "quebec", "central america"]),
    "central america": Territory("Central America", ["w us", "e us", "venezuela"])
}

# south america #
sAmerican_terr: dict[str: Territory] = {
    "venezuela": Territory("Venezuela", ["central america", "peru", "brazil"]),
    "peru": Territory("Peru", ["venezuela", "brazil", "argentina"]),
    "brazil": Territory("Brazil", ["peru", "venezuela", "n africa", "argentina"]),
    "argentina": Territory("Argentina", ["peru", "brazil"])
}

# europe #
european_terr: dict[str: Territory] = {
    "iceland": Territory("Iceland", ["greenland"]),
    "scandinavia": Territory("Scandinavia"),
    "ukraine": Territory("Ukaraine"),
    "gb": Territory("Great Britain"),
    "n europe": Territory("Northern Europe"),
    "w europe": Territory("Western Europe"),
    "s europe": Territory("Southern Europe")
}

# africa #
african_terr: dict[str: Territory] = {
    "n africa": Territory("North Africa", ["brazil"]),
    "egypt": Territory("Egypt"),
    "e africa": Territory("East Africa"),
    "congo": Territory("Congo"),
    "s africa": Territory("South Africa"),
    "madagascar": Territory("Madagascar")
}

# asia #
asian_terr: dict[str: Territory] = {
    "ural": Territory("Ural"),
    "siberia": Territory("Siberia"),
    "yakutsk": Territory("Yakutsk"),
    "irkutsk": Territory("Irkutsk"),
    "mongolia": Territory("Mongolia"),
    "kamchatka": Territory("Kamchatka", ["alaska"]),
    "japan": Territory("Japan"),
    "afghanistan": Territory("Afghanistan"),
    "china": Territory("China"),
    "middle e": Territory("Middle East"),
    "india": Territory("India"),
    "siam": Territory("Siam")
}

# australia #
aussie_terr: dict[str: Territory] = {
    "indonesia": Territory("Indonesia"),
    "new guinea": Territory("New Guinea"),
    "w australia": Territory("Western Australia"),
    "e australia": Territory("Eastern Australia")
}



### <------------------------------------------> ###



### DEFINE CONTINENTS ###

classic_continents: dict[str: Continent] = {
    "n america": Continent("North America", nAmerican_terr, 5),
    "s america": Continent("South America", sAmerican_terr, 2),
    "europe": Continent("Europe", european_terr, 5),
    "africa": Continent("Africa", african_terr, 3),
    "asia": Continent("Asia", asian_terr, 7),
    "australia": Continent("Australia", aussie_terr, 2)
}