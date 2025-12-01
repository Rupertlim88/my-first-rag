#!/usr/bin/env python3
"""
Generate 1000 unique attractions in CSV format matching attractions_seed.csv structure.
"""

import csv
import random
from typing import List, Dict

# Diverse set of cities with their countries and currencies
CITIES = [
    ("Paris", "France", "EUR"),
    ("London", "UK", "GBP"),
    ("New York", "USA", "USD"),
    ("Tokyo", "Japan", "JPY"),
    ("Barcelona", "Spain", "EUR"),
    ("Rome", "Italy", "EUR"),
    ("Berlin", "Germany", "EUR"),
    ("Amsterdam", "Netherlands", "EUR"),
    ("Vienna", "Austria", "EUR"),
    ("Prague", "Czech Republic", "CZK"),
    ("Budapest", "Hungary", "HUF"),
    ("Warsaw", "Poland", "PLN"),
    ("Stockholm", "Sweden", "SEK"),
    ("Copenhagen", "Denmark", "DKK"),
    ("Oslo", "Norway", "NOK"),
    ("Dublin", "Ireland", "EUR"),
    ("Edinburgh", "UK", "GBP"),
    ("Madrid", "Spain", "EUR"),
    ("Lisbon", "Portugal", "EUR"),
    ("Athens", "Greece", "EUR"),
    ("Istanbul", "Turkey", "TRY"),
    ("Dubai", "UAE", "AED"),
    ("Singapore", "Singapore", "SGD"),
    ("Hong Kong", "China", "HKD"),
    ("Shanghai", "China", "CNY"),
    ("Beijing", "China", "CNY"),
    ("Seoul", "South Korea", "KRW"),
    ("Bangkok", "Thailand", "THB"),
    ("Kuala Lumpur", "Malaysia", "MYR"),
    ("Jakarta", "Indonesia", "IDR"),
    ("Manila", "Philippines", "PHP"),
    ("Ho Chi Minh City", "Vietnam", "VND"),
    ("Sydney", "Australia", "AUD"),
    ("Melbourne", "Australia", "AUD"),
    ("Auckland", "New Zealand", "NZD"),
    ("Mumbai", "India", "INR"),
    ("Delhi", "India", "INR"),
    ("Bangalore", "India", "INR"),
    ("Cairo", "Egypt", "EGP"),
    ("Cape Town", "South Africa", "ZAR"),
    ("Johannesburg", "South Africa", "ZAR"),
    ("Nairobi", "Kenya", "KES"),
    ("Lagos", "Nigeria", "NGN"),
    ("São Paulo", "Brazil", "BRL"),
    ("Rio de Janeiro", "Brazil", "BRL"),
    ("Buenos Aires", "Argentina", "ARS"),
    ("Mexico City", "Mexico", "MXN"),
    ("Toronto", "Canada", "CAD"),
    ("Vancouver", "Canada", "CAD"),
    ("Montreal", "Canada", "CAD"),
    ("Chicago", "USA", "USD"),
    ("Los Angeles", "USA", "USD"),
    ("San Francisco", "USA", "USD"),
    ("Miami", "USA", "USD"),
    ("Boston", "USA", "USD"),
    ("Seattle", "USA", "USD"),
    ("Las Vegas", "USA", "USD"),
    ("Orlando", "USA", "USD"),
    ("Washington DC", "USA", "USD"),
    ("Philadelphia", "USA", "USD"),
    ("Atlanta", "USA", "USD"),
]

# Attraction types
ATTRACTION_TYPES = [
    "landmark",
    "museum",
    "park",
    "theme_park",
    "gallery",
    "monument",
    "cathedral",
    "temple",
    "palace",
    "castle",
    "tower",
    "bridge",
    "market",
    "beach",
    "garden",
    "zoo",
    "aquarium",
    "theater",
    "opera_house",
    "stadium",
    "library",
    "observatory",
    "botanical_garden",
    "ruins",
    "fortress",
]

# Templates for generating realistic data
LANDMARK_NAMES = [
    "Tower", "Bridge", "Square", "Plaza", "Monument", "Memorial", "Gate", "Arch",
    "Cathedral", "Basilica", "Church", "Temple", "Shrine", "Pagoda", "Mosque",
    "Palace", "Castle", "Fortress", "Citadel", "Acropolis", "Colosseum", "Arena",
    "Observatory", "Lighthouse", "Clock Tower", "City Hall", "Parliament", "Opera House"
]

MUSEUM_NAMES = [
    "Museum", "Gallery", "Art Museum", "History Museum", "Science Museum",
    "Natural History Museum", "Maritime Museum", "Aviation Museum", "War Museum",
    "Cultural Museum", "Ethnographic Museum", "Archaeological Museum", "Modern Art Museum"
]

PARK_NAMES = [
    "Park", "Garden", "Botanical Garden", "National Park", "Memorial Park",
    "Central Park", "City Park", "Riverside Park", "Waterfront Park", "Beach Park"
]

THEME_PARK_NAMES = [
    "Theme Park", "Adventure Park", "Amusement Park", "Water Park", "Entertainment Park"
]

# Generate unique attraction names
def generate_attraction_name(city: str, attraction_type: str, index: int) -> str:
    """Generate a unique attraction name based on type and city."""
    city_short = city.split()[0] if " " in city else city
    
    if attraction_type == "landmark":
        landmark = random.choice(LANDMARK_NAMES)
        prefixes = [city_short, "Historic", "Grand", "Royal", "National", "Central", "Old", "New", "Ancient"]
        if random.random() < 0.3:
            return f"{random.choice(prefixes)} {landmark}"
        else:
            return f"{landmark} of {city_short}"
    
    elif attraction_type == "museum":
        museum = random.choice(MUSEUM_NAMES)
        prefixes = [city_short, "National", "City", "Royal", "Grand", "Historic"]
        return f"{random.choice(prefixes)} {museum}"
    
    elif attraction_type == "park":
        park = random.choice(PARK_NAMES)
        prefixes = [city_short, "Central", "Riverside", "Memorial", "National", "City"]
        return f"{random.choice(prefixes)} {park}"
    
    elif attraction_type == "theme_park":
        park = random.choice(THEME_PARK_NAMES)
        return f"{city_short} {park}"
    
    elif attraction_type == "gallery":
        return f"{city_short} Art Gallery" if random.random() < 0.5 else f"Modern Art Gallery of {city_short}"
    
    elif attraction_type == "cathedral":
        return f"{city_short} Cathedral" if random.random() < 0.5 else f"Cathedral of {city_short}"
    
    elif attraction_type == "temple":
        return f"{city_short} Temple" if random.random() < 0.5 else f"Temple of {city_short}"
    
    elif attraction_type == "palace":
        return f"{city_short} Palace" if random.random() < 0.5 else f"Royal Palace of {city_short}"
    
    elif attraction_type == "castle":
        return f"{city_short} Castle" if random.random() < 0.5 else f"Castle of {city_short}"
    
    elif attraction_type == "tower":
        return f"{city_short} Tower" if random.random() < 0.5 else f"Tower of {city_short}"
    
    elif attraction_type == "bridge":
        return f"{city_short} Bridge" if random.random() < 0.5 else f"Historic Bridge of {city_short}"
    
    elif attraction_type == "market":
        return f"{city_short} Market" if random.random() < 0.5 else f"Central Market of {city_short}"
    
    elif attraction_type == "beach":
        return f"{city_short} Beach" if random.random() < 0.5 else f"Golden Beach of {city_short}"
    
    elif attraction_type == "garden":
        return f"{city_short} Botanical Garden" if random.random() < 0.5 else f"Botanical Gardens of {city_short}"
    
    elif attraction_type == "zoo":
        return f"{city_short} Zoo" if random.random() < 0.5 else f"Zoo of {city_short}"
    
    elif attraction_type == "aquarium":
        return f"{city_short} Aquarium" if random.random() < 0.5 else f"Marine Aquarium of {city_short}"
    
    elif attraction_type == "theater":
        return f"{city_short} Theater" if random.random() < 0.5 else f"Grand Theater of {city_short}"
    
    elif attraction_type == "opera_house":
        return f"{city_short} Opera House" if random.random() < 0.5 else f"Opera House of {city_short}"
    
    elif attraction_type == "stadium":
        return f"{city_short} Stadium" if random.random() < 0.5 else f"National Stadium of {city_short}"
    
    elif attraction_type == "library":
        return f"{city_short} Library" if random.random() < 0.5 else f"National Library of {city_short}"
    
    elif attraction_type == "observatory":
        return f"{city_short} Observatory" if random.random() < 0.5 else f"Astronomical Observatory of {city_short}"
    
    elif attraction_type == "botanical_garden":
        return f"{city_short} Botanical Garden" if random.random() < 0.5 else f"Botanical Gardens of {city_short}"
    
    elif attraction_type == "ruins":
        return f"Ancient Ruins of {city_short}" if random.random() < 0.5 else f"{city_short} Archaeological Site"
    
    elif attraction_type == "fortress":
        return f"{city_short} Fortress" if random.random() < 0.5 else f"Historic Fortress of {city_short}"
    
    else:
        return f"{city_short} {attraction_type.replace('_', ' ').title()}"


def generate_address(city: str, country: str, attraction_name: str) -> str:
    """Generate a realistic address."""
    street_types = ["Street", "Avenue", "Boulevard", "Road", "Lane", "Square", "Plaza", "Park"]
    street_names = ["Main", "Central", "Royal", "Grand", "Historic", "Park", "Riverside", "Waterfront", 
                   "Market", "Church", "Cathedral", "Palace", "Castle", "Tower", "Bridge"]
    
    street_num = random.randint(1, 9999)
    street_name = random.choice(street_names)
    street_type = random.choice(street_types)
    
    # Generate postal code (varies by country)
    postal_codes = {
        "USA": f"{random.randint(10000, 99999)}",
        "UK": f"{random.choice(['SW', 'NW', 'SE', 'NE', 'W', 'E', 'N', 'S'])}{random.randint(1, 20)} {random.randint(1, 9)}{random.choice('ABCDEFGHJKLMNOPQRSTUVWXYZ')}{random.choice('ABCDEFGHJKLMNOPQRSTUVWXYZ')}",
        "France": f"{random.randint(10000, 99999)}",
        "Japan": f"{random.randint(100, 999)}-{random.randint(1000, 9999)}",
    }
    
    postal_code = postal_codes.get(country, f"{random.randint(10000, 99999)}")
    
    return f"{street_num} {street_name} {street_type}, {city}, {postal_code}, {country}"


def generate_price(attraction_type: str, currency: str) -> float:
    """Generate realistic price based on attraction type and currency."""
    # Base prices in USD, then convert
    base_prices = {
        "landmark": (0, 35),
        "museum": (0, 25),
        "park": (0, 15),
        "theme_park": (50, 150),
        "gallery": (0, 20),
        "monument": (0, 15),
        "cathedral": (0, 12),
        "temple": (0, 10),
        "palace": (10, 30),
        "castle": (8, 25),
        "tower": (15, 35),
        "bridge": (0, 5),
        "market": (0, 0),
        "beach": (0, 10),
        "garden": (0, 15),
        "zoo": (10, 30),
        "aquarium": (15, 40),
        "theater": (20, 100),
        "opera_house": (30, 150),
        "stadium": (10, 80),
        "library": (0, 5),
        "observatory": (5, 20),
        "botanical_garden": (0, 15),
        "ruins": (5, 20),
        "fortress": (8, 20),
    }
    
    min_price, max_price = base_prices.get(attraction_type, (0, 20))
    
    # Many attractions are free (30% chance for free types)
    if min_price == 0 and random.random() < 0.3:
        return 0.00
    
    price = round(random.uniform(min_price, max_price), 2)
    
    # Currency conversion (simplified)
    conversions = {
        "EUR": 0.92,
        "GBP": 0.79,
        "JPY": 150.0,
        "AUD": 1.52,
        "CAD": 1.35,
        "CNY": 7.2,
        "HKD": 7.8,
        "SGD": 1.34,
        "KRW": 1300.0,
        "THB": 35.0,
        "MYR": 4.7,
        "IDR": 15700.0,
        "PHP": 56.0,
        "VND": 24500.0,
        "INR": 83.0,
        "BRL": 5.0,
        "MXN": 17.0,
        "ARS": 850.0,
        "TRY": 32.0,
        "AED": 3.67,
        "EGP": 31.0,
        "ZAR": 18.5,
        "KES": 130.0,
        "NGN": 1500.0,
        "CZK": 23.0,
        "HUF": 360.0,
        "PLN": 4.0,
        "SEK": 10.5,
        "DKK": 6.9,
        "NOK": 10.5,
        "NZD": 1.64,
    }
    
    if currency in conversions:
        price = price * conversions[currency]
    
    return round(price, 2)


def generate_open_hours(attraction_type: str) -> str:
    """Generate realistic opening hours."""
    patterns = [
        "Daily: 9:00-18:00",
        "Daily: 8:00-20:00",
        "Daily: 10:00-17:00",
        "Daily: 9:00-17:00",
        "Daily: 8:00-22:00",
        "Daily: 6:00-22:00",
        "Mon-Sat: 9:00-18:00; Sun: 10:00-17:00",
        "Tue-Sun: 9:00-18:00; Mon: Closed",
        "Daily: 9:00-20:00 (varies by season)",
        "Daily: 8:00-20:30 (varies by season)",
        "Daily: 10:00-18:00 (last entry 17:00)",
        "Mon-Fri: 9:00-17:00; Sat-Sun: 10:00-18:00",
        "Daily: 24 hours",
        "Daily: 6:00-1:00",
    ]
    
    if attraction_type == "park":
        return random.choice(["Daily: 6:00-22:00", "Daily: 24 hours", "Daily: 8:00-20:00"])
    elif attraction_type == "beach":
        return "Daily: 24 hours"
    elif attraction_type == "theme_park":
        return random.choice(["Daily: 9:00-20:00 (varies by season)", "Daily: 10:00-22:00 (varies by season)"])
    elif attraction_type == "temple" or attraction_type == "cathedral":
        return random.choice(["Daily: 6:00-18:00", "Daily: 8:00-17:00", "Daily: 7:00-19:00"])
    else:
        return random.choice(patterns)


def generate_things_to_do(attraction_name: str, attraction_type: str, city: str) -> str:
    """Generate detailed things to do description."""
    activities = {
        "landmark": [
            "Climb to the top for panoramic city views and enjoy breathtaking scenery.",
            "Explore the historic architecture and learn about the landmark's significance.",
            "Take guided tours to discover hidden stories and architectural details.",
            "Visit during sunset for spectacular lighting and photo opportunities.",
            "Attend special events and exhibitions held throughout the year.",
        ],
        "museum": [
            "Explore world-class collections featuring art, history, and culture from around the world.",
            "Join guided tours led by expert curators to gain deeper insights into the exhibits.",
            "Attend special exhibitions, workshops, and educational programs for all ages.",
            "Use audio guides available in multiple languages for a self-paced experience.",
            "Visit the museum shop and café for souvenirs and refreshments.",
        ],
        "park": [
            "Stroll through beautifully landscaped gardens and enjoy peaceful nature walks.",
            "Have a picnic on the lawns, rent bicycles, or enjoy outdoor recreational activities.",
            "Visit seasonal flower displays, fountains, and sculptures throughout the park.",
            "Attend outdoor concerts, festivals, and cultural events held in the park.",
            "Explore walking trails, playgrounds, and designated areas for sports and relaxation.",
        ],
        "theme_park": [
            "Experience thrilling rides and attractions based on popular themes and stories.",
            "Watch live shows, parades, and character meet-and-greets throughout the day.",
            "Enjoy themed dining experiences and shopping for exclusive merchandise.",
            "Visit during special events and seasonal celebrations for unique experiences.",
            "Explore multiple themed areas, each offering different adventures and entertainment.",
        ],
        "gallery": [
            "View rotating exhibitions of contemporary and classical art from renowned artists.",
            "Attend gallery talks, artist workshops, and special opening events.",
            "Explore permanent collections showcasing local and international artworks.",
            "Participate in educational programs and guided tours for art enthusiasts.",
            "Visit the gallery shop for art books, prints, and unique gifts.",
        ],
        "cathedral": [
            "Admire stunning Gothic architecture, stained glass windows, and intricate details.",
            "Attend religious services, concerts, and special ceremonies held in the cathedral.",
            "Climb the towers for panoramic views of the city and surrounding areas.",
            "Explore the crypt, chapels, and historical artifacts on display.",
            "Join guided tours to learn about the cathedral's history and architectural significance.",
        ],
        "temple": [
            "Participate in traditional rituals and ceremonies open to visitors.",
            "Explore the temple grounds, gardens, and architectural features.",
            "Shop at nearby markets for traditional crafts, souvenirs, and local specialties.",
            "Attend seasonal festivals and cultural events celebrated at the temple.",
            "Learn about the temple's history and spiritual significance through guided tours.",
        ],
        "palace": [
            "Tour opulent royal chambers, grand halls, and beautifully decorated rooms.",
            "Explore the palace gardens, courtyards, and surrounding grounds.",
            "View collections of royal artifacts, paintings, and historical treasures.",
            "Attend special exhibitions and cultural events held in the palace.",
            "Learn about the royal history and architectural evolution of the palace.",
        ],
        "castle": [
            "Explore medieval fortifications, towers, and historic battlements.",
            "Visit the castle museum to see armor, weapons, and historical artifacts.",
            "Climb the towers for panoramic views and enjoy scenic walks along the ramparts.",
            "Attend reenactments, medieval festivals, and special events.",
            "Learn about the castle's history through guided tours and interactive exhibits.",
        ],
        "tower": [
            "Ascend to observation decks for 360-degree panoramic city views.",
            "Visit restaurants, cafes, and shops located within the tower.",
            "Experience glass floors, skywalks, and thrilling observation experiences.",
            "Attend special events, exhibitions, and seasonal celebrations.",
            "Enjoy sunset and evening visits for spectacular lighting and cityscapes.",
        ],
        "bridge": [
            "Walk across the historic bridge and admire architectural details and city views.",
            "Learn about the bridge's engineering and historical significance.",
            "Take photographs of iconic cityscapes and river views from the bridge.",
            "Visit during special events and festivals that take place on the bridge.",
            "Explore nearby attractions and waterfront areas accessible from the bridge.",
        ],
        "market": [
            "Shop for fresh produce, local crafts, souvenirs, and unique gifts.",
            "Sample local street food, traditional dishes, and regional specialties.",
            "Experience the vibrant atmosphere and interact with local vendors.",
            "Find unique handmade items, antiques, and cultural artifacts.",
            "Attend market festivals, food events, and cultural celebrations.",
        ],
        "beach": [
            "Relax on sandy shores, swim in clear waters, and enjoy water sports.",
            "Rent beach equipment, join water activities, or take boat tours.",
            "Enjoy beachside dining, cafes, and sunset views over the ocean.",
            "Explore nearby coastal trails, viewpoints, and natural attractions.",
            "Participate in beach activities, volleyball, and recreational sports.",
        ],
        "garden": [
            "Stroll through themed gardens showcasing diverse plant collections.",
            "Attend seasonal flower shows, garden tours, and horticultural events.",
            "Learn about plant species, conservation, and botanical research.",
            "Enjoy peaceful walks, photography, and nature observation.",
            "Visit the garden shop, café, and educational facilities.",
        ],
        "zoo": [
            "Observe diverse animal species in naturalistic habitats and enclosures.",
            "Attend animal feeding sessions, keeper talks, and educational presentations.",
            "Explore themed areas representing different ecosystems and continents.",
            "Participate in behind-the-scenes tours and interactive animal encounters.",
            "Visit conservation exhibits and learn about wildlife protection efforts.",
        ],
        "aquarium": [
            "Explore underwater worlds featuring marine life from around the globe.",
            "Watch feeding demonstrations, dive shows, and educational presentations.",
            "Walk through tunnel exhibits for immersive underwater experiences.",
            "Learn about marine conservation, ecosystems, and ocean science.",
            "Visit interactive touch pools and special exhibits for hands-on learning.",
        ],
        "theater": [
            "Attend world-class performances including plays, musicals, and concerts.",
            "Take guided tours of the historic theater and learn about its architecture.",
            "Enjoy pre-show dining and drinks at the theater's restaurant and bars.",
            "Experience the opulent interior, grand stages, and acoustic excellence.",
            "Attend special events, galas, and cultural celebrations.",
        ],
        "opera_house": [
            "Attend opera performances, ballets, and classical music concerts.",
            "Take architectural tours to explore the stunning design and history.",
            "Dine at the opera house restaurant and enjoy pre-show experiences.",
            "Learn about the venue's acoustics, stage technology, and artistic heritage.",
            "Attend special events, opening nights, and cultural galas.",
        ],
        "stadium": [
            "Attend major sporting events, concerts, and entertainment shows.",
            "Take stadium tours to explore behind-the-scenes areas and facilities.",
            "Visit the stadium museum to learn about sports history and achievements.",
            "Enjoy dining options, shops, and interactive experiences at the venue.",
            "Attend special events, exhibitions, and community activities.",
        ],
        "library": [
            "Browse extensive collections of books, manuscripts, and historical documents.",
            "Attend author talks, literary events, and educational programs.",
            "Use reading rooms, research facilities, and digital resources.",
            "Explore special exhibitions and rare book collections.",
            "Participate in workshops, book clubs, and community activities.",
        ],
        "observatory": [
            "Observe celestial objects through powerful telescopes during evening sessions.",
            "Attend astronomy talks, planetarium shows, and educational programs.",
            "Learn about space, planets, stars, and the universe through interactive exhibits.",
            "Participate in stargazing events and special astronomical observations.",
            "Explore the observatory's history and contributions to astronomy.",
        ],
        "botanical_garden": [
            "Explore diverse plant collections from around the world in themed gardens.",
            "Attend seasonal flower displays, garden tours, and horticultural workshops.",
            "Learn about plant conservation, biodiversity, and botanical research.",
            "Enjoy peaceful walks, photography, and nature observation.",
            "Visit the garden shop, greenhouse, and educational facilities.",
        ],
        "ruins": [
            "Explore ancient archaeological sites and learn about historical civilizations.",
            "Take guided tours to understand the ruins' historical significance.",
            "Photograph impressive structures, carvings, and architectural remains.",
            "Visit the on-site museum to see artifacts and learn about the site's history.",
            "Attend special events, reenactments, and cultural celebrations.",
        ],
        "fortress": [
            "Explore historic fortifications, battlements, and military architecture.",
            "Visit the fortress museum to see weapons, armor, and historical artifacts.",
            "Climb towers and ramparts for panoramic views of the surrounding area.",
            "Learn about the fortress's military history and strategic importance.",
            "Attend reenactments, historical events, and special exhibitions.",
        ],
    }
    
    base_activities = activities.get(attraction_type, [
        f"Explore {attraction_name} and discover its unique features and history.",
        f"Take guided tours to learn about the attraction's significance and stories.",
        f"Enjoy the beautiful surroundings and take photographs of memorable moments.",
        f"Attend special events and exhibitions held throughout the year.",
        f"Visit nearby attractions and explore the surrounding area.",
    ])
    
    # Combine 2-3 activities for a detailed description
    selected = random.sample(base_activities, min(2, len(base_activities)))
    return " ".join(selected)


def generate_attractions(count: int = 1000) -> List[Dict[str, str]]:
    """Generate list of unique attractions."""
    attractions = []
    used_names = set()
    
    # Ensure we have enough unique combinations
    max_attempts = count * 10
    attempts = 0
    
    while len(attractions) < count and attempts < max_attempts:
        attempts += 1
        
        city, country, currency = random.choice(CITIES)
        attraction_type = random.choice(ATTRACTION_TYPES)
        
        # Generate unique name
        name = generate_attraction_name(city, attraction_type, len(attractions))
        if name in used_names:
            continue
        
        used_names.add(name)
        
        location = f"{city}, {country}"
        address = generate_address(city, country, name)
        price = generate_price(attraction_type, currency)
        open_hours = generate_open_hours(attraction_type)
        things_to_do = generate_things_to_do(name, attraction_type, city)
        
        attraction = {
            "city_name": city,
            "attraction_name": name,
            "attraction_type": attraction_type,
            "location": location,
            "address": address,
            "price": f"{price:.2f}",
            "currency": currency,
            "open_hours": open_hours,
            "things_to_do": things_to_do,
        }
        
        attractions.append(attraction)
    
    return attractions


def write_csv(attractions: List[Dict[str, str]], filename: str):
    """Write attractions to CSV file."""
    fieldnames = [
        "city_name",
        "attraction_name",
        "attraction_type",
        "location",
        "address",
        "price",
        "currency",
        "open_hours",
        "things_to_do",
    ]
    
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(attractions)
    
    print(f"Generated {len(attractions)} attractions in {filename}")


if __name__ == "__main__":
    print("Generating 1000 unique attractions...")
    attractions = generate_attractions(1000)
    
    # Write to CSV
    script_dir = __file__.rsplit("/", 1)[0] if "/" in __file__ else "."
    output_file = f"{script_dir}/attractions_1000.csv"
    write_csv(attractions, output_file)
    
    print(f"\nSummary:")
    print(f"- Total attractions: {len(attractions)}")
    print(f"- Unique cities: {len(set(a['city_name'] for a in attractions))}")
    print(f"- Unique types: {len(set(a['attraction_type'] for a in attractions))}")
    print(f"- Free attractions: {sum(1 for a in attractions if float(a['price']) == 0.0)}")
    print(f"\nFile saved to: {output_file}")

