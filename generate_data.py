"""
generate_data.py — Generates 10,000 clean, realistic YouTube training samples.

Categories:
  Constructive (label=1): Education, Music, News, Science
  Non-constructive (label=0): Entertainment/Vlogs, Gaming, Pranks/Drama, Clickbait/Gossip

Each sample: channel_name, title, description, label
"""

import csv
import os
import random
import itertools

random.seed(42)

# ─── CONSTRUCTIVE CATEGORIES (label=1) ───────────────────────────────────────

EDUCATION = {
    "channels": [
        "Khan Academy", "MIT OpenCourseWare", "3Blue1Brown", "CrashCourse",
        "Professor Dave Explains", "Veritasium", "TED-Ed", "FreeCodeCamp",
        "Organic Chemistry Tutor", "Kurzgesagt", "Numberphile", "Bozeman Science",
        "PatrickJMT", "Eddie Woo", "Neso Academy", "Dr. Trefor Bazett",
        "Mathologer", "CS Dojo", "Socratica", "LearnCode.academy",
        "The Coding Train", "Fireship", "Ben Eater", "Computerphile",
        "Two Minute Papers", "Primer", "MinutePhysics", "Up and Atom",
        "Looking Glass Universe", "Physics Girl", "Real Engineering",
        "Practical Engineering", "Technology Connections", "Steve Mould",
        "SmarterEveryDay", "Mark Rober", "Stuff Made Here", "ElectroBOOM",
        "EEVblog", "GreatScott!", "Codecademy", "Harvard CS50",
        "Google Developers", "Microsoft Developer", "AWS Training",
        "DataCamp", "StatQuest", "Sentdex", "Corey Schafer", "Tech With Tim"
    ],
    "title_templates": [
        "Understanding {topic} — Complete Guide",
        "{topic}: A Visual Introduction",
        "How {topic} Actually Works",
        "Learn {topic} in {duration}",
        "{topic} Tutorial for Beginners",
        "{topic} Explained Simply",
        "The Mathematics Behind {topic}",
        "Introduction to {topic} — Lecture {num}",
        "Why {topic} Matters in {year}",
        "Mastering {topic}: Step by Step",
        "{topic} — Everything You Need to Know",
        "What is {topic}? Complete Explanation",
        "The Fundamentals of {topic}",
        "{topic} Course — Part {num}",
        "How to Learn {topic} Effectively",
        "Deep Dive into {topic}",
        "{topic} Made Easy",
        "A Beginner's Guide to {topic}",
        "{topic} From Scratch — Full Course",
        "The History and Evolution of {topic}",
        "Advanced {topic} Concepts Explained",
        "{topic} Crash Course for Students",
        "Solving {topic} Problems Step by Step",
        "The Science of {topic}",
        "{topic}: Theory and Practice"
    ],
    "topics": [
        "Calculus", "Linear Algebra", "Quantum Mechanics", "Organic Chemistry",
        "Machine Learning", "Data Structures", "Neural Networks", "Python Programming",
        "Statistics", "Differential Equations", "Graph Theory", "Thermodynamics",
        "Electromagnetism", "Microeconomics", "World History", "Molecular Biology",
        "Genetics", "Compiler Design", "Operating Systems", "Computer Networks",
        "Discrete Mathematics", "Probability Theory", "Number Theory", "Relativity",
        "Cryptography", "Database Systems", "Algorithm Design", "Artificial Intelligence",
        "Digital Electronics", "Signal Processing", "Control Systems", "Fluid Mechanics",
        "Astrophysics", "Cell Biology", "Biochemistry", "Abstract Algebra",
        "Real Analysis", "Complex Analysis", "Topology", "Philosophy of Science",
        "Cognitive Science", "Linguistics", "Game Theory", "Information Theory",
        "Robotics", "Embedded Systems", "Cloud Computing", "Web Development",
        "Cybersecurity", "Blockchain Technology"
    ],
    "desc_templates": [
        "In this video, we explore the fundamental concepts of {topic}. Perfect for students and lifelong learners.",
        "A comprehensive lecture covering {topic} from the basics to advanced applications.",
        "This tutorial walks you through {topic} with clear examples and visual explanations.",
        "Learn {topic} with hands-on examples. Ideal for self-study and exam preparation.",
        "We break down {topic} into digestible pieces so anyone can understand it.",
        "Join us as we dive deep into {topic}. References and resources in the description below.",
        "This is part of our series on {topic}. Watch the full playlist for the complete course.",
        "A visual and intuitive explanation of {topic} that goes beyond the textbook.",
        "Everything you need to know about {topic} explained clearly with diagrams and examples.",
        "An in-depth look at {topic} covering theory, applications, and practice problems."
    ]
}

MUSIC = {
    "channels": [
        "VEVO", "T-Series", "Sony Music", "Warner Music", "Universal Music",
        "NPR Music", "Tiny Desk Concerts", "Colors Studios", "Majestic Casual",
        "MrSuicideSheep", "Proximity", "Trap Nation", "ChilledCow",
        "Lofi Girl", "Classical Music Only", "Berlin Philharmoniker",
        "London Symphony Orchestra", "Deutsche Grammophon", "Halidon Music",
        "Audio Library", "NoCopyrightSounds", "Monstercat", "Spinnin Records",
        "Armada Music", "Anjunabeats", "Drumeo", "Rick Beato", "Adam Neely",
        "12tone", "David Bruce Composer", "Andrew Huang", "Polyphonic",
        "Sideways", "Listening In", "Charles Cornell", "Tantacrul",
        "Early Music Sources", "Tonal", "Music Matters", "Sound Field",
        "Jacob Collier", "Berklee Online", "Musicology", "Vinyl Rewind",
        "Reverb", "Signal Path", "Produce Like A Pro", "Pensado's Place",
        "Recording Revolution", "SpectreSoundStudios"
    ],
    "title_templates": [
        "{artist} — {song} (Official Music Video)",
        "{song} | {genre} Playlist {year}",
        "{artist} Live at {venue}",
        "{genre} Mix — Best of {year}",
        "How to Play {song} on {instrument}",
        "{artist} — {song} (Acoustic Version)",
        "{genre} for Studying and Focus",
        "Top {num} {genre} Songs of All Time",
        "{artist} Full Album — {song}",
        "{song} | {instrument} Cover",
        "The Best of {artist} — Greatest Hits",
        "{genre} Compilation — {duration} of Pure Music",
        "{artist} — {song} (Lyric Video)",
        "Relaxing {genre} for Sleep and Meditation",
        "{instrument} Tutorial: How to Play {song}",
        "{genre} Chill Vibes — {year} Mix",
        "Orchestra Performs {song} by {artist}",
        "{artist} Unplugged — Live Session",
        "Understanding Music Theory: {song} Analysis",
        "Why {artist}'s {song} is a Masterpiece"
    ],
    "artists": [
        "Beethoven", "Mozart", "Bach", "Chopin", "Debussy", "Adele",
        "Ed Sheeran", "Taylor Swift", "Coldplay", "Radiohead", "Pink Floyd",
        "The Beatles", "Miles Davis", "John Coltrane", "Billie Eilish",
        "Kendrick Lamar", "Hans Zimmer", "Yo-Yo Ma", "Itzhak Perlman",
        "Lang Lang", "Norah Jones", "Bon Iver", "Sigur Ros", "Explosions in the Sky",
        "Max Richter", "Olafur Arnalds", "Ludovico Einaudi", "Yiruma",
        "Joe Hisaishi", "Ryuichi Sakamoto", "Jacob Collier", "Snarky Puppy",
        "Herbie Hancock", "Chick Corea", "Pat Metheny", "Tame Impala",
        "Khruangbin", "Daft Punk", "Aphex Twin", "Boards of Canada"
    ],
    "songs": [
        "Moonlight Sonata", "Clair de Lune", "Bohemian Rhapsody", "Stairway to Heaven",
        "Imagine", "Yesterday", "Nocturne Op. 9 No. 2", "Fur Elise",
        "River Flows in You", "Experience", "Time", "Interstellar Theme",
        "Gymnopedie No. 1", "Canon in D", "Four Seasons", "Swan Lake",
        "Nuvole Bianche", "Comptine d'un autre ete", "Merry Christmas Mr. Lawrence",
        "Summer", "Divenire", "Una Mattina", "Metamorphosis", "The Planets",
        "Cello Suite No. 1", "Air on the G String", "Rhapsody in Blue",
        "Take Five", "So What", "My Favorite Things"
    ],
    "genres": [
        "Classical", "Jazz", "Lo-fi", "Ambient", "Indie", "Folk",
        "R&B", "Soul", "Blues", "Electronic", "Orchestral", "Acoustic",
        "Piano", "Chill", "Instrumental", "World Music", "Baroque",
        "Romantic Era", "Contemporary Classical", "Post-Rock"
    ],
    "instruments": ["Piano", "Guitar", "Violin", "Cello", "Drums", "Bass", "Saxophone", "Flute"],
    "venues": ["Carnegie Hall", "Royal Albert Hall", "Sydney Opera House", "Coachella", "Glastonbury", "Montreux Jazz Festival", "Red Rocks", "Madison Square Garden"],
    "desc_templates": [
        "Listen to {song} by {artist}. A beautiful piece of {genre} music.",
        "Enjoy this curated {genre} playlist for relaxation, study, or work.",
        "Live performance of {song} recorded at {venue}. Pure musical excellence.",
        "{artist} performs {song} in this stunning live session.",
        "A {genre} compilation featuring the best tracks for focus and calm.",
        "Learn how to play {song} on {instrument} with this step-by-step tutorial.",
        "Album stream: {artist} — featuring {song} and other timeless tracks.",
        "The definitive collection of {genre} music. Subscribe for weekly playlists.",
        "Breaking down the music theory behind {song} by {artist}.",
        "A deep exploration of {genre} and why it stands the test of time."
    ]
}

NEWS = {
    "channels": [
        "BBC News", "CNN", "Reuters", "Al Jazeera English", "DW News",
        "France 24", "NDTV", "Sky News", "PBS NewsHour", "AP Archive",
        "The Guardian", "The New York Times", "Washington Post", "CNBC",
        "Bloomberg", "Financial Times", "The Economist", "Vox",
        "Vice News", "Channel 4 News", "ABC News", "NBC News",
        "CBS News", "MSNBC", "NPR", "The Wire", "Scroll.in",
        "India Today", "The Hindu", "Hindustan Times", "WION",
        "TRT World", "NHK World", "CNA", "South China Morning Post",
        "The Print", "Firstpost", "News18", "Republic World",
        "Rajya Sabha TV", "Lok Sabha TV", "Doordarshan", "Times Now",
        "CNBC TV18", "ET Now", "Mint", "Moneycontrol", "Business Standard",
        "LiveMint", "The Quint", "Newslaundry"
    ],
    "title_templates": [
        "Breaking: {event} — Full Coverage",
        "{event}: What You Need to Know",
        "{leader} Addresses {event} at {org}",
        "{country} {policy}: Impact and Analysis",
        "Latest Update: {event} — {year}",
        "{org} Report on {event}",
        "{event} Explained in {duration}",
        "How {event} Affects {sector}",
        "{country}'s Response to {event}",
        "Analysis: {event} and Its Global Impact",
        "Top Stories: {event} | {date} News",
        "{leader} on {event}: Key Takeaways",
        "The {event} Crisis Explained",
        "{country} Elections {year}: Complete Coverage",
        "World Economic Forum: {leader} on {event}",
        "Inside the {event}: An Investigative Report",
        "{org} Summit: Key Decisions on {event}",
        "{event}: Facts vs Fiction",
        "Global Markets React to {event}",
        "Daily Briefing: {event} Updates"
    ],
    "events": [
        "Climate Change Summit", "G20 Summit", "UN General Assembly", "Trade Agreement",
        "Peace Negotiations", "Election Results", "Economic Sanctions", "Refugee Crisis",
        "Healthcare Reform", "Infrastructure Bill", "Defense Budget", "Tech Regulation",
        "Central Bank Policy", "Housing Crisis", "Energy Transition", "Space Program",
        "Education Reform", "Tax Reform", "Labor Market Report", "Supply Chain Disruption",
        "Diplomatic Talks", "Cybersecurity Threat", "Border Security", "Water Crisis",
        "Food Security", "Digital Currency Regulation", "Minimum Wage Debate",
        "Public Health Emergency", "Environmental Policy", "Transportation Bill",
        "Immigration Reform", "Data Privacy Law", "Anti-Trust Case", "Climate Accord",
        "Trade Deficit Report", "Manufacturing Output", "GDP Growth Report",
        "Inflation Data", "Employment Numbers", "Interest Rate Decision"
    ],
    "leaders": [
        "Prime Minister", "President", "Chancellor", "Secretary General",
        "Foreign Minister", "Finance Minister", "Chief Justice", "Governor",
        "Ambassador", "Chairman", "Commissioner", "Director General"
    ],
    "countries": [
        "India", "United States", "China", "European Union", "United Kingdom",
        "Japan", "Germany", "France", "Brazil", "Australia", "Canada", "South Korea",
        "Russia", "Indonesia", "South Africa", "Mexico", "Saudi Arabia", "Turkey"
    ],
    "orgs": ["United Nations", "WHO", "WTO", "IMF", "World Bank", "NATO", "ASEAN", "BRICS", "G7", "OPEC", "EU Parliament", "African Union"],
    "sectors": ["Global Economy", "Public Health", "Technology Sector", "Energy Markets", "Agriculture", "Financial Markets", "Real Estate", "Education Sector"],
    "desc_templates": [
        "Full coverage of {event}. Stay informed with the latest developments.",
        "Our correspondents report on {event} and its implications for {sector}.",
        "Analysis of {event} by our expert panel. Subscribe for daily news updates.",
        "Breaking news: {event}. We bring you live updates and expert commentary.",
        "What does {event} mean for {country}? Our in-depth analysis explains.",
        "Today's top story: {event}. Get the facts and context you need.",
        "A comprehensive look at {event} and what it means going forward.",
        "Our investigative team reports on {event}. Watch the full segment.",
        "Expert analysis on {event} covering all angles and perspectives.",
        "Daily news roundup featuring {event} and other important stories."
    ]
}

SCIENCE = {
    "channels": [
        "NASA", "SpaceX", "ESA", "National Geographic", "Nature Video",
        "Science Magazine", "New Scientist", "Scientific American",
        "Kurzgesagt", "PBS Space Time", "Veritasium", "SmarterEveryDay",
        "MinutePhysics", "MinuteEarth", "Deep Look", "SciShow",
        "SciShow Space", "It's Okay To Be Smart", "Physics Girl",
        "Looking Glass Universe", "Up and Atom", "Sabine Hossenfelder",
        "Arvin Ash", "Dr. Becky", "Fraser Cain", "Anton Petrov",
        "Isaac Arthur", "Cool Worlds", "SEA", "Astrum",
        "Periodic Videos", "NileRed", "NileBlue", "Cody's Lab",
        "Applied Science", "Thought Emporium", "Brainiac75",
        "The Action Lab", "Thunderf00t", "Scott Manley",
        "Everyday Astronaut", "TMRO", "NASA Goddard", "JPL",
        "Fermilab", "CERN", "Royal Institution", "World Science Festival",
        "Breakthrough", "Science Friday"
    ],
    "title_templates": [
        "New Discovery: {topic} Changes Everything",
        "How {topic} Could Transform {field}",
        "{org} Announces Breakthrough in {topic}",
        "The Science Behind {topic}",
        "What We Just Learned About {topic}",
        "Exploring {topic}: Latest Research {year}",
        "Why {topic} Is More Important Than You Think",
        "{topic} Experiment: Incredible Results",
        "Scientists Discover {topic} in {location}",
        "The Future of {field}: {topic}",
        "New Research on {topic} Published in {journal}",
        "Understanding {topic}: A Scientific Perspective",
        "{topic}: From Theory to Reality",
        "How Scientists Study {topic}",
        "The Mystery of {topic} — Finally Solved?",
        "Visualizing {topic} Like Never Before",
        "Could {topic} Change Our Understanding of {field}?",
        "Inside the Lab: {topic} Research",
        "What {topic} Tells Us About {field}",
        "Breakthrough: {topic} Confirmed by {org}"
    ],
    "topics": [
        "Black Holes", "Dark Matter", "Dark Energy", "CRISPR Gene Editing",
        "Quantum Computing", "Gravitational Waves", "Exoplanets", "Fusion Energy",
        "Neutrino Detection", "Higgs Boson", "Mars Exploration", "James Webb Telescope",
        "mRNA Vaccines", "Protein Folding", "Climate Modeling", "Ocean Acidification",
        "Coral Reef Restoration", "Stem Cell Therapy", "Neuroplasticity",
        "Microbiome Research", "Superconductors", "Graphene Applications",
        "Nuclear Fusion", "Asteroid Mining", "Solar Sail Technology",
        "Quantum Entanglement", "Antimatter", "Bioluminescence",
        "Deep Sea Exploration", "Volcanic Activity", "Earthquake Prediction",
        "Gene Therapy", "Immunotherapy", "Nanotechnology", "Battery Technology",
        "Carbon Capture", "Reforestation", "Biodiversity", "Synthetic Biology",
        "Space Debris", "Lunar Base", "Titan Exploration", "Europa Mission",
        "Photosynthesis Efficiency", "Aging Research", "Brain-Computer Interface",
        "Metamaterials", "Topological Insulators", "Room Temperature Superconductivity",
        "Holography"
    ],
    "fields": [
        "Physics", "Biology", "Medicine", "Space Exploration", "Climate Science",
        "Neuroscience", "Chemistry", "Materials Science", "Astronomy", "Ecology",
        "Genetics", "Oceanography", "Geology", "Paleontology", "Cosmology"
    ],
    "orgs": ["NASA", "CERN", "ESA", "MIT", "Caltech", "Stanford", "NIH", "Max Planck Institute", "ISRO", "JAXA", "CSIRO"],
    "journals": ["Nature", "Science", "Physical Review Letters", "The Lancet", "Cell", "PNAS", "New England Journal of Medicine"],
    "locations": ["Deep Space", "Mars", "the Arctic", "the Ocean Floor", "the Amazon", "Antarctica", "the Moon", "Yellowstone", "the Mariana Trench", "the ISS"],
    "desc_templates": [
        "Scientists have made a groundbreaking discovery in {topic} that could reshape our understanding of {field}.",
        "New research on {topic} has been published in {journal}. Here's what it means.",
        "We explore the latest findings on {topic} and what they mean for the future of {field}.",
        "A visual journey through the science of {topic}. Sources and references linked below.",
        "Breaking science news: {topic} research yields surprising results.",
        "In this video, we explain {topic} and its significance for {field}.",
        "Join us as we explore the cutting-edge research on {topic}.",
        "From the lab to the cosmos: understanding {topic} and its applications.",
        "A comprehensive look at {topic} research and its implications for {field}.",
        "New data from {org} reveals fascinating insights about {topic}."
    ]
}


# ─── NON-CONSTRUCTIVE CATEGORIES (label=0) ────────────────────────────────────

ENTERTAINMENT_VLOGS = {
    "channels": [
        "MrBeast", "PewDiePie", "Dude Perfect", "Liza Koshy", "David Dobrik",
        "Emma Chamberlain", "Casey Neistat", "Jake Paul", "Logan Paul",
        "KSI", "Markiplier", "Jacksepticeye", "Lilly Singh", "Zach King",
        "Danny Gonzalez", "Drew Gooden", "Cody Ko", "Noel Miller",
        "Jenna Marbles", "Shane Dawson", "Tana Mongeau", "Trisha Paytas",
        "Jeffree Star", "James Charles", "Charli D'Amelio", "Addison Rae",
        "Brent Rivera", "Lexi Rivera", "Stokes Twins", "Unspeakable",
        "SSSniperwolf", "SIS vs BRO", "Collins Key", "Guava Juice",
        "Ryan's World", "Like Nastya", "Kids Diana Show", "Vlad and Niki",
        "CKN Toys", "Blippi", "FGTeeV", "EvanTubeHD",
        "MattyBRaps", "JoJo Siwa", "Azzyland", "LaurDIY",
        "Rosanna Pansino", "Simply Nailogical", "Safiya Nygaard", "Jojo's Juice"
    ],
    "title_templates": [
        "A Day in My Life in {city} 🌆",
        "I Spent 24 Hours in {location}",
        "My Morning Routine {year} ☀️",
        "Room Tour! My New {adj} Setup 🏠",
        "What I Got for My Birthday 🎂",
        "Reacting to My Old Videos 😂",
        "{num} Things You Didn't Know About Me",
        "Q&A: Answering Your Questions!",
        "I Tried {challenge} for a Week",
        "Things I Wish I Knew at {age}",
        "Life Update: {update} 😱",
        "Unboxing My {item} Haul!",
        "Rating My Subscribers' {thing}",
        "I Let My {person} Control My Day",
        "Surprising My {person} with {item}!",
        "We Tried Every {food} at {restaurant}",
        "Moving to {city}! Life Update Vlog",
        "My {adj} Apartment Tour 🏡",
        "Storytime: {story} (NOT CLICKBAIT)",
        "Day in My Life as a {job}"
    ],
    "cities": ["NYC", "LA", "Dubai", "London", "Tokyo", "Miami", "Paris", "Bali", "Barcelona", "Seoul", "Singapore", "Mumbai"],
    "locations": ["a Haunted House", "a Private Island", "an Abandoned Mall", "a Mansion", "the World's Largest Waterpark", "a Desert", "a Jungle"],
    "challenges": ["Living on $1", "Not Eating", "Not Sleeping", "Speaking Only Spanish", "Being Vegan", "No Phone"],
    "items": ["iPhone", "Tesla", "Designer Bags", "Sneakers", "Laptop", "PS5", "Custom PC"],
    "adj": ["Aesthetic", "Minimalist", "Luxury", "Cozy", "Dream", "Ultimate"],
    "persons": ["Best Friend", "Mom", "Girlfriend", "Boyfriend", "Sister", "Brother", "Dog"],
    "foods": ["Burger", "Pizza", "Sushi", "Taco", "Donut", "Ice Cream"],
    "restaurants": ["McDonald's", "Starbucks", "Taco Bell", "Chipotle", "Five Guys", "Chick-fil-A"],
    "stories": ["How I Almost Died", "My Worst Date Ever", "I Got Scammed", "The Craziest Thing That Happened"],
    "jobs": ["YouTuber", "College Student", "CEO", "Model", "Influencer"],
    "updates": ["Big Changes Coming", "Moving Out", "New Relationship", "I Quit My Job"],
    "things": ["Outfits", "Rooms", "Pets", "Art"],
    "desc_templates": [
        "Hey guys! In today's video, I'm sharing my crazy adventure. Don't forget to like and subscribe! 💕",
        "WATCH TILL THE END for a huge surprise! Links to everything mentioned below.",
        "Today's vlog is INSANE. I can't believe this happened. Smash that like button!",
        "New vlog dropping every week! Follow me on Instagram for behind-the-scenes content.",
        "Life has been crazy lately. Here's what's been going on! Merch link in bio 🔥",
        "This was honestly the best day of my life! Turn on notifications so you never miss an upload.",
        "Enjoy this vlog! Let me know in the comments what you want to see next!",
        "The craziest experience ever! If you enjoyed this video, give it a thumbs up 👍",
        "Welcome back to my channel! Today's video is a special one — stay tuned!",
        "Subscribe and join the family! New content every single day."
    ]
}

GAMING = {
    "channels": [
        "PewDiePie Gaming", "Ninja", "Shroud", "DrDisRespect", "Tfue",
        "TimTheTatman", "xQc", "Ludwig", "Pokimane", "Valkyrae",
        "Sykkuno", "CourageJD", "Summit1G", "Tyler1", "Myth",
        "Typical Gamer", "Lazarbeam", "Fresh", "Muselk", "Ali-A",
        "Lachlan", "BCC Trolling", "Jelly", "Kwebbelkop", "Slogoman",
        "DanTDM", "Stampylonghead", "CaptainSparklez", "Dream", "GeorgeNotFound",
        "Sapnap", "TommyInnit", "Tubbo", "Technoblade", "Ph1LzA",
        "Wilbur Soot", "Ranboo", "Karl Jacobs", "MrBeast Gaming",
        "Sidemen", "W2S", "Miniminter", "TBJZL", "Behzinga",
        "Vikkstar123", "Zerkaa", "ChrisMD", "Speed", "IShowSpeed",
        "Kai Cenat"
    ],
    "title_templates": [
        "I Played {game} and THIS Happened 😂",
        "{game} but {modifier}",
        "{num} Kill Game in {game}! (World Record?)",
        "Trolling {person} in {game}",
        "{game} {mode} is BROKEN 💀",
        "My Best {game} Moments of {year}",
        "First Time Playing {game} — It Was INSANE",
        "{game} {mode} Challenge with {person}",
        "Reacting to {game} Clips That Break Reality",
        "This {game} Glitch is Game-Breaking!",
        "I Became the BEST {game} Player",
        "Can I Win {game} Using Only {weapon}?",
        "{game} Speedrun in {duration} — New Strategy!",
        "Playing {game} Until I Win",
        "Destroying Sweats in {game} {mode}",
        "{game} is BACK and Better Than Ever",
        "Rating Viewers' {game} Clips",
        "Teaching My {person} How to Play {game}",
        "The ULTIMATE {game} Guide for Beginners",
        "We Broke {game} with This Strategy 🤯"
    ],
    "games": [
        "Minecraft", "Fortnite", "GTA V", "Valorant", "Apex Legends",
        "Call of Duty", "League of Legends", "Roblox", "Among Us", "Elden Ring",
        "FIFA", "Rocket League", "CS2", "Overwatch 2", "Warzone",
        "Rust", "ARK", "Terraria", "Stardew Valley", "Fall Guys"
    ],
    "modes": ["Ranked", "Battle Royale", "Survival", "Creative", "Competitive", "Hardcore", "Solo", "Duo", "Squad"],
    "modifiers": [
        "I Can Only Use a Pistol", "Everything is Randomized", "My Screen is Upside Down",
        "I Can't Stop Running", "Using a Steering Wheel", "Voice Controls Only",
        "Blindfolded", "One Hand Only", "Playing with My Feet", "Using a Trackpad"
    ],
    "weapons": ["Pistol", "Melee", "Crossbow", "Fists", "Worst Gun", "Random Weapon"],
    "persons": ["Noobs", "My Mom", "Random Strangers", "My Little Brother", "Streamers", "My Girlfriend"],
    "desc_templates": [
        "Today we're playing {game} and it was absolutely wild! Drop a like if you enjoyed!",
        "NEW {game} video! Can we hit {num} likes? Subscribe for daily gaming content!",
        "Playing {game} with the squad. This was hilarious 😂 Leave a comment with your best moment!",
        "I tried the most insane challenge in {game}. You won't believe what happened!",
        "Watch me dominate in {game}! Use code CREATOR in the item shop!",
        "Best {game} gameplay you'll see today. Merch available at the link below!",
        "Grinding {game} ranked — can we reach the top? Let me know your rank in the comments!",
        "New {game} update is insane! Here's everything you need to know.",
        "Epic {game} moments compilation. Share this with your gaming buddy!",
        "Stream highlights from last night's {game} session. Follow on Twitch for live gameplay!"
    ]
}

PRANKS_DRAMA = {
    "channels": [
        "Prank Nation", "Just For Laughs Gags", "BigDawsTV", "VitalyzdTv",
        "NELK", "Ross Creations", "Jack Vale Films", "Roman Atwood",
        "Dennis Roady", "FouseyTUBE", "Pranksters In Love", "Amelia Dimz",
        "Drama Alert", "Keemstar", "The Drama Channel", "Tea Spill",
        "Spill Sesh", "Anna Oop", "Sebastian Sallow", "Def Noodles",
        "H3H3 Productions", "Ethan Klein", "ImJayStation", "N&A Productions",
        "3AM Challenge", "Guava Juice Pranks", "ChandlersFunHouse",
        "MoeAndET", "Twan Kuyper", "Lele Pons", "Anwar Jibawi",
        "Brent Rivera Pranks", "Alan Chikin Chow", "Caleb City",
        "Daniel LaBelle", "The McCartys", "The Pun Guys", "Ben Azelart",
        "Stokes Twins Pranks", "Carter Sharer", "Lizzy Sharer",
        "Stephen Sharer", "Grace Sharer", "Matt and Rebecca",
        "Chad Wild Clay", "Vy Qwaint", "Project Zorgo", "Spy Ninja",
        "Morgz", "Infinite Lists"
    ],
    "title_templates": [
        "PRANKING My {person} (GONE WRONG!) 😱",
        "I Told My {person} I'm {confession} 😂",
        "EXPOSING {target} — The Truth Revealed",
        "{person} Caught {action} On Camera!",
        "I Faked {event} to See Their Reaction",
        "This YouTuber SCAMMED Everyone — Exposed!",
        "{celeb} vs {celeb}: The Full Story",
        "Why {target} Is CANCELLED ❌",
        "I Pretended to be {character} in Public",
        "Scary {challenge} at 3AM (DON'T TRY THIS)",
        "{person} Had the WORST Reaction to This Prank",
        "The {target} Situation Just Got Worse",
        "Calling {celeb} at 3AM! (THEY ANSWERED!) 📞",
        "I Put {item} in My {person}'s {thing} — PRANK",
        "Breaking Down the {target} Controversy",
        "ROASTING My {person}'s {thing} 🔥",
        "{celeb} Responds to the HATE",
        "The REAL Reason {target} Is Over",
        "Dressing as {character} in Public Reactions",
        "we need to talk about {target}..."
    ],
    "persons": ["Girlfriend", "Boyfriend", "Best Friend", "Mom", "Dad", "Roommate", "Sister", "Brother", "Wife", "Husband"],
    "targets": ["This Creator", "Jake Paul", "The Situation", "Drama Alert", "This Influencer", "This TikToker", "This Couple", "This Brand"],
    "confessions": ["Moving Away", "Pregnant", "Dropping Out", "Breaking Up", "Quitting YouTube", "Getting Married"],
    "actions": ["Lying", "Cheating", "Stealing", "Sneaking Out", "Being Fake"],
    "events": ["My Own Death", "A Breakup", "A Fight", "Being Arrested", "Winning the Lottery"],
    "celebs": ["Logan Paul", "KSI", "Tana Mongeau", "Jeffree Star", "James Charles", "Trisha Paytas"],
    "characters": ["Spider-Man", "a Cop", "a Celebrity", "a Robot", "a Zombie"],
    "items": ["a Spider", "Hot Sauce", "Slime", "Glitter", "Fake Bug"],
    "things": ["Food", "Bed", "Car", "Shower", "Backpack"],
    "challenges": ["Ouija Board", "One Man Hide and Seek", "Bloody Mary", "Charlie Charlie"],
    "desc_templates": [
        "I can't believe this prank went THIS far! Watch till the end for the craziest reaction ever!",
        "EXPOSING the truth that nobody is talking about. Like and share if you agree!",
        "This prank was INSANE! Don't forget to subscribe for more crazy content every week!",
        "The drama is getting out of hand. Here's the full breakdown with receipts.",
        "YOU WON'T BELIEVE WHAT HAPPENED! This is my craziest prank yet!",
        "Full story breakdown with all the evidence. Drop your thoughts in the comments!",
        "This has gone TOO FAR. Here's everything you need to know about the situation.",
        "Prank went completely wrong! I almost got in serious trouble 😂 Like if you want more!",
        "The tea is SCALDING ☕ Full breakdown of what's happening.",
        "Subscribe and turn on notifications for the latest drama updates!"
    ]
}

CLICKBAIT_GOSSIP = {
    "channels": [
        "Bright Side", "ACTUALLY HAPPENED", "5-Minute Crafts", "Troom Troom",
        "7-Second Riddles", "BE AMAZED", "Incredible Facts", "Mind Warehouse",
        "TheRichest", "Luxury Zone", "FactVerse", "Top Trending",
        "Talltanic", "The Infographics Show", "Matt's Off Road Recovery",
        "Chills", "Top15s", "MostAmazingTop10", "WatchMojo", "TheThings",
        "Screen Rant", "Looper", "Nicki Swift", "The List", "Mashed",
        "BabbleTop", "BuzzFeed Multiplayer", "Clevver News", "E! News",
        "Entertainment Tonight", "TMZ", "Access Hollywood", "Hollywood Life",
        "Just Jared", "Perez Hilton", "Pop Culture", "CelebGossip",
        "Daily Pop", "The Shade Room", "Bossip", "MediaTakeOut",
        "Star Magazine", "US Weekly", "People Magazine", "InTouch Weekly",
        "OK! Magazine", "Life & Style", "Radar Online", "Page Six",
        "Gossip Mill"
    ],
    "title_templates": [
        "You Won't BELIEVE What {celeb} Did! 😱",
        "{num} {thing} That Will BLOW Your Mind",
        "Why You Should NEVER {action} (Shocking Truth)",
        "{celeb}'s Secret {noun} Revealed!",
        "This {thing} Will Change Your Life Forever",
        "Scientists Can't Explain This {thing}!",
        "Doctors Are BEGGING People to Stop {action}",
        "I Found a {thing} in My {place} (SCARY!)",
        "{celeb} BREAKS SILENCE on {noun}",
        "The Dark Truth About {thing} Nobody Tells You",
        "Only {percent}% of People Can {challenge}",
        "If You See This {thing}, RUN!",
        "{num} Life Hacks That Are Actually GENIUS",
        "People Are Going CRAZY Over This {thing}",
        "{celeb} Spotted with {celeb2} — What's Going On?",
        "Stop Doing THIS Right Now — Doctors Warn",
        "This Simple Trick Will {benefit}",
        "What {celeb} Looks Like Without Makeup SHOCKED Everyone",
        "I Wish I Knew This {thing} Sooner",
        "Things You're Doing WRONG Every Day"
    ],
    "celebs": [
        "Kim Kardashian", "Kanye West", "Drake", "Rihanna", "Selena Gomez",
        "Justin Bieber", "Elon Musk", "Kylie Jenner", "Beyonce", "Ariana Grande",
        "Dua Lipa", "Zendaya", "Tom Holland", "Chris Hemsworth", "Scarlett Johansson",
        "Bad Bunny", "Post Malone", "Cardi B", "Megan Thee Stallion", "Travis Scott"
    ],
    "things": [
        "Secret", "Trick", "Hack", "Signal", "Sign", "Discovery", "Photo",
        "Coincidence", "Detail", "Object", "Pattern", "Message", "Symbol",
        "Feature", "Invention"
    ],
    "nouns": ["Past", "Relationship", "Fortune", "Surgery", "Diet", "Mansion", "Breakdown", "Scandal"],
    "actions": [
        "Eat Before Bed", "Use Your Phone at Night", "Drink Tap Water",
        "Sit Like This", "Sleep on Your Back", "Skip Breakfast",
        "Charge Your Phone Overnight", "Mix These Foods"
    ],
    "places": ["Backyard", "Attic", "Basement", "Wall", "Old House", "Garden"],
    "challenges": ["Solve This", "Pass This Test", "See the Difference", "Answer This"],
    "benefits": ["Save You Thousands", "Make You Rich", "Change Everything", "Fix Your Life"],
    "desc_templates": [
        "You won't believe what happened! Watch the FULL video to find out the shocking truth!",
        "This is INSANE! Like, subscribe, and share for more mind-blowing content every day!",
        "Celebrity gossip and shocking revelations! Don't miss a single video — subscribe now!",
        "These facts will leave you SPEECHLESS! Comment below if #3 surprised you!",
        "SHARE before it gets taken down! The truth they don't want you to know!",
        "97% of people get this WRONG! Are you in the top 3%? Find out now!",
        "The internet is going CRAZY over this discovery! Like if you're shocked!",
        "Unlock the secrets they don't want you to know! Subscribe for daily uploads!",
        "This changes EVERYTHING! Most people have no idea about this shocking fact!",
        "Watch till the END for the biggest reveal! You'll be speechless!"
    ]
}


# ─── DATA GENERATION ──────────────────────────────────────────────────────────

def fill_template(template: str, data: dict) -> str:
    """Fill a template string with random values from data dict, plus common values."""
    filled = template
    max_attempts = 20
    attempt = 0

    while "{" in filled and attempt < max_attempts:
        attempt += 1
        for key in list(data.keys()) + ["year", "num", "duration", "date", "age", "percent"]:
            placeholder = "{" + key + "}"
            if placeholder in filled:
                if key == "year":
                    val = str(random.choice([2022, 2023, 2024, 2025, 2026]))
                elif key == "num":
                    val = str(random.choice([3, 5, 7, 10, 15, 20, 25, 50, 100]))
                elif key == "duration":
                    val = random.choice(["5 Minutes", "10 Minutes", "15 Minutes", "30 Minutes", "1 Hour", "2 Hours"])
                elif key == "date":
                    val = random.choice(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]) + f" {random.randint(1,28)}"
                elif key == "age":
                    val = str(random.choice([16, 18, 20, 21, 25, 30]))
                elif key == "percent":
                    val = str(random.choice([1, 2, 3, 5, 10]))
                elif key == "celeb2":
                    val = random.choice(data.get("celebs", ["Someone"]))
                elif key in data:
                    val_source = data[key]
                    if isinstance(val_source, list):
                        val = random.choice(val_source)
                    else:
                        val = str(val_source)
                else:
                    continue
                filled = filled.replace(placeholder, val, 1)

    return filled


def generate_samples(category_data: dict, label: int, count: int) -> list:
    """Generate `count` unique samples for a category."""
    samples = set()
    attempts = 0
    max_attempts = count * 10

    # Build lookup for fill_template
    fill_data = {}
    for key, val in category_data.items():
        if key not in ("title_templates", "desc_templates", "channels"):
            fill_data[key] = val

    # Handle singular/plural key aliases for template compatibility
    # e.g. "topics" list needs to match "{topic}" placeholder
    singular_map = {}
    for key in list(fill_data.keys()):
        if key.endswith("s") and key != "news":
            singular = key[:-1]
            if singular not in fill_data:
                singular_map[singular] = fill_data[key]
        if key.endswith("ies"):
            singular = key[:-3] + "y"
            if singular not in fill_data:
                singular_map[singular] = fill_data[key]
        if key.endswith("es") and key not in singular_map and key != "venues":
            singular = key[:-2]
            if singular not in fill_data:
                singular_map[singular] = fill_data[key]

    fill_data.update(singular_map)

    while len(samples) < count and attempts < max_attempts:
        attempts += 1
        channel = random.choice(category_data["channels"])
        title = fill_template(random.choice(category_data["title_templates"]), fill_data)
        desc = fill_template(random.choice(category_data["desc_templates"]), fill_data)

        key = (channel, title)
        if key not in samples:
            samples.add(key)

    result = []
    for channel, title in samples:
        desc = fill_template(random.choice(category_data["desc_templates"]), fill_data)
        result.append({
            "channel_name": channel,
            "title": title,
            "description": desc,
            "label": label
        })

    return result[:count]


def main():
    os.makedirs("data", exist_ok=True)

    print("🔄 Generating training data...")

    constructive_categories = [
        ("Education", EDUCATION),
        ("Music", MUSIC),
        ("News", NEWS),
        ("Science", SCIENCE),
    ]

    non_constructive_categories = [
        ("Entertainment/Vlogs", ENTERTAINMENT_VLOGS),
        ("Gaming", GAMING),
        ("Pranks/Drama", PRANKS_DRAMA),
        ("Clickbait/Gossip", CLICKBAIT_GOSSIP),
    ]

    all_samples = []

    # 5000 constructive (1250 each)
    for name, data in constructive_categories:
        samples = generate_samples(data, label=1, count=1250)
        print(f"  ✅ {name}: {len(samples)} samples")
        all_samples.extend(samples)

    # 5000 non-constructive (1250 each)
    for name, data in non_constructive_categories:
        samples = generate_samples(data, label=0, count=1250)
        print(f"  ❌ {name}: {len(samples)} samples")
        all_samples.extend(samples)

    random.shuffle(all_samples)

    # Write CSV
    output_path = "data/training_data.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["channel_name", "title", "description", "label"])
        writer.writeheader()
        writer.writerows(all_samples)

    print(f"\n✅ Generated {len(all_samples)} samples → {output_path}")

    # Print distribution summary
    pos = sum(1 for s in all_samples if s["label"] == 1)
    neg = sum(1 for s in all_samples if s["label"] == 0)
    print(f"   Constructive: {pos} | Non-constructive: {neg}")
    print(f"   Balance: {pos / len(all_samples) * 100:.1f}% / {neg / len(all_samples) * 100:.1f}%")


if __name__ == "__main__":
    main()
