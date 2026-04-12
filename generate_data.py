"""
generate_data.py — Generates 10,000 clean, realistic YouTube training samples.
Descriptions are long and realistic (3-6 sentences), matching real YouTube videos.

Constructive (label=1): Education, Music, News, Science
Non-constructive (label=0): Entertainment/Vlogs, Gaming, Pranks/Drama, Clickbait/Gossip
"""

import csv, os, random
random.seed(42)

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def pick(lst): return random.choice(lst)
def pick_n(lst, n): return random.sample(lst, min(n, len(lst)))

YEARS = ["2022", "2023", "2024", "2025", "2026"]
NUMS = ["3", "5", "7", "10", "15", "20", "25", "50"]

def build_desc(sentences_pool, n_min=3, n_max=6):
    """Build a description by combining sentences. 20% short (1-2), 80% long (n_min-n_max)."""
    if random.random() < 0.20:
        n = random.randint(1, 2)
    else:
        n = random.randint(n_min, n_max)
    chosen = pick_n(sentences_pool, n)
    return " ".join(chosen)

# ─── EDUCATION ────────────────────────────────────────────────────────────────

EDU_CHANNELS = [
    "Khan Academy", "MIT OpenCourseWare", "3Blue1Brown", "CrashCourse",
    "Professor Dave Explains", "Veritasium", "TED-Ed", "FreeCodeCamp",
    "Organic Chemistry Tutor", "Numberphile", "Bozeman Science",
    "Dr. Trefor Bazett", "CS Dojo", "Socratica", "The Coding Train",
    "Fireship", "Ben Eater", "Computerphile", "MinutePhysics",
    "Real Engineering", "Practical Engineering", "Technology Connections",
    "SmarterEveryDay", "ElectroBOOM", "Harvard CS50", "StatQuest",
    "Sentdex", "Corey Schafer", "Tech With Tim", "Simplilearn",
    "Edureka", "Great Learning", "Unacademy", "BYJU'S", "Physics Wallah",
    "Abdul Bari", "Jenny's Lectures", "Gate Smashers", "Neso Academy",
    "CodeWithHarry", "Apna College", "Love Babbar", "Striver",
    "William Fiset", "NeetCode", "Greg Hogg", "Reducible", "Spanning Tree",
    "Sebastian Lague", "Brackeys"
]

EDU_TOPICS = [
    "Calculus", "Linear Algebra", "Quantum Mechanics", "Organic Chemistry",
    "Machine Learning", "Data Structures", "Neural Networks", "Python Programming",
    "Statistics", "Differential Equations", "Graph Theory", "Thermodynamics",
    "Electromagnetism", "Microeconomics", "World History", "Molecular Biology",
    "Genetics", "Compiler Design", "Operating Systems", "Computer Networks",
    "Discrete Mathematics", "Probability Theory", "Number Theory", "Cryptography",
    "Database Systems", "Algorithm Design", "Artificial Intelligence",
    "Digital Electronics", "Signal Processing", "Control Systems",
    "Web Development", "Cybersecurity", "Cloud Computing", "DevOps",
    "React Framework", "Node.js", "System Design", "Object Oriented Programming",
    "Dynamic Programming", "Binary Trees", "Sorting Algorithms", "Recursion",
    "Pointers in C", "SQL Databases", "MongoDB", "Docker Containers",
    "Kubernetes", "REST APIs", "GraphQL", "TypeScript"
]

def gen_edu():
    topic = pick(EDU_TOPICS)
    ch = pick(EDU_CHANNELS)
    yr = pick(YEARS)
    titles = [
        f"Understanding {topic} — Complete Guide for Beginners",
        f"{topic}: A Visual and Intuitive Introduction",
        f"How {topic} Actually Works — Explained from Scratch",
        f"Learn {topic} in One Video — Full Course {yr}",
        f"{topic} Tutorial for Beginners — Step by Step",
        f"{topic} Explained Simply with Real World Examples",
        f"The Mathematics Behind {topic} — Deep Dive",
        f"Introduction to {topic} — University Lecture Series",
        f"Why Every Student Should Learn {topic} in {yr}",
        f"Mastering {topic}: From Basics to Advanced",
        f"{topic} — Everything You Need to Know for Exams",
        f"What is {topic}? Complete Explanation with Examples",
        f"The Fundamentals of {topic} — Core Concepts",
        f"{topic} Full Course — Beginner to Advanced {yr}",
        f"How to Learn {topic} Effectively — Study Tips and Roadmap",
        f"Deep Dive into {topic} — Lecture {pick(NUMS)}",
        f"{topic} Made Easy — No Prerequisites Needed",
        f"{topic} Crash Course for Computer Science Students",
        f"Solving {topic} Problems Step by Step — Practice Session",
        f"Advanced {topic} Concepts Every Engineer Must Know",
    ]
    desc_parts = [
        f"In this comprehensive video, we explore the fundamental concepts of {topic} from the ground up, starting with the basic principles and gradually building toward more advanced ideas.",
        f"This lecture is part of our complete {topic} series designed for university students and self-learners who want a thorough understanding of the subject.",
        f"We begin by reviewing the prerequisites and then systematically work through each concept with detailed explanations, diagrams, and worked-out examples.",
        f"By the end of this video, you will have a solid grasp of {topic} and be well-prepared for exams, interviews, or real-world applications.",
        f"All the notes, slides, and practice problems mentioned in this video are available for free download in the link below.",
        f"If you find this helpful, please consider subscribing to the channel for more educational content on computer science, mathematics, and engineering topics.",
        f"Timestamps are provided in the comments section so you can jump to any specific topic that interests you.",
        f"This video covers the core theory of {topic} along with practical demonstrations that help solidify your understanding.",
        f"We also discuss common mistakes students make when learning {topic} and how to avoid them in your studies and projects.",
        f"References and textbook recommendations for further reading on {topic} are listed at the end of the description.",
        f"Special thanks to our patrons who make these free educational videos possible. Support us on Patreon to help us create more content.",
        f"Whether you are preparing for competitive exams like GATE, GRE, or technical interviews at top companies, this {topic} tutorial will give you the edge you need.",
    ]
    return ch, pick(titles), build_desc(desc_parts, 4, 6)

# ─── MUSIC ────────────────────────────────────────────────────────────────────

MUSIC_CHANNELS = [
    "VEVO", "T-Series", "Sony Music", "Universal Music", "NPR Music",
    "Tiny Desk Concerts", "Colors Studios", "Lofi Girl", "Majestic Casual",
    "MrSuicideSheep", "Proximity", "Classical Music Only", "Halidon Music",
    "Audio Library", "NoCopyrightSounds", "Monstercat", "Rick Beato",
    "Adam Neely", "Andrew Huang", "Charles Cornell", "Jacob Collier",
    "Berklee Online", "Berlin Philharmoniker", "London Symphony Orchestra",
    "Deutsche Grammophon", "Drumeo", "Polyphonic", "Sideways",
    "Sound Field", "Vinyl Rewind", "Reverb", "Produce Like A Pro",
    "Saregama Music", "Zee Music Company", "Speed Records", "Desi Music Factory",
    "Shemaroo", "Arijit Singh", "FilmyBox", "Yuki Music",
    "Wave Music", "Bhojpuri Hits", "Rajshri", "Ultra Bollywood",
    "Tips Official", "Venus", "Eros Now Music", "Sony Music India",
    "Warner Music India", "Gaana"
]

ARTISTS = [
    "Beethoven", "Mozart", "Bach", "Chopin", "Debussy", "Adele", "Coldplay",
    "Pink Floyd", "Miles Davis", "Hans Zimmer", "Ludovico Einaudi", "Yiruma",
    "Joe Hisaishi", "Jacob Collier", "Daft Punk", "Norah Jones",
    "Arijit Singh", "A.R. Rahman", "Shreya Ghoshal", "Lata Mangeshkar"
]
SONGS = [
    "Moonlight Sonata", "Clair de Lune", "Bohemian Rhapsody", "Nocturne Op 9",
    "Fur Elise", "River Flows in You", "Experience", "Time",
    "Gymnopedie No 1", "Canon in D", "Nuvole Bianche", "Comptine",
    "Summer", "Cello Suite No 1", "Rhapsody in Blue", "Take Five"
]
GENRES = [
    "Classical", "Jazz", "Lo-fi", "Ambient", "Indie", "Folk", "R&B", "Soul",
    "Blues", "Electronic", "Orchestral", "Acoustic", "Piano", "Instrumental",
    "Bollywood", "Sufi", "Ghazal", "Devotional", "Carnatic", "Hindustani"
]
INSTRUMENTS = ["Piano", "Guitar", "Violin", "Cello", "Drums", "Saxophone", "Sitar", "Flute", "Tabla"]
VENUES = ["Carnegie Hall", "Royal Albert Hall", "Sydney Opera House", "Red Rocks", "Madison Square Garden", "Wembley Stadium"]

def gen_music():
    ch = pick(MUSIC_CHANNELS)
    artist, song, genre, inst = pick(ARTISTS), pick(SONGS), pick(GENRES), pick(INSTRUMENTS)
    yr, venue = pick(YEARS), pick(VENUES)
    titles = [
        f"{artist} — {song} (Official Music Video)",
        f"Best {genre} Playlist {yr} — {pick(NUMS)} Hours of Pure Music",
        f"{artist} Live at {venue} — Full Concert",
        f"{genre} Mix — Relaxing Music for Study and Focus",
        f"How to Play {song} on {inst} — Complete Tutorial",
        f"{artist} — {song} (Acoustic Session)",
        f"Top {genre} Songs of All Time — Curated Playlist",
        f"{artist} Greatest Hits — Full Album Stream",
        f"{song} | Beautiful {inst} Cover",
        f"Relaxing {genre} for Sleep, Study, and Meditation — {yr}",
        f"Orchestra Performs {song} — Breathtaking Performance",
        f"{artist} Unplugged — Intimate Live Session",
        f"Music Theory Analysis: Why {song} is a Masterpiece",
        f"{genre} Lofi Beats — Chill Vibes All Day",
        f"Learning {inst}: {song} Step by Step for Beginners",
    ]
    desc_parts = [
        f"Listen to the beautiful rendition of {song} by {artist}, one of the most iconic pieces in {genre} music history.",
        f"This curated {genre} playlist features over {pick(NUMS)} carefully selected tracks perfect for studying, working, relaxing, or simply enjoying great music.",
        f"Recorded live at {venue}, this performance captures the raw emotion and technical brilliance of {artist} at their absolute best.",
        f"Whether you are a longtime fan of {genre} music or discovering it for the first time, this collection offers something truly special for every listener.",
        f"Our {inst} tutorial breaks down {song} note by note, making it accessible for beginners while still offering valuable insights for intermediate players.",
        f"Subscribe to our channel for weekly uploads of the finest {genre} music, curated playlists, artist spotlights, and music theory deep dives.",
        f"This album features remastered audio in high fidelity, bringing out every subtle nuance and detail in the original recording.",
        f"Timestamps for each track are available in the pinned comment below so you can easily navigate to your favorite pieces in this compilation.",
        f"Support the artists by streaming their music on Spotify, Apple Music, and other platforms — links are provided in the description below.",
        f"This video is part of our ongoing series exploring the greatest works in {genre} music, analyzing what makes each piece timeless and universally beloved.",
    ]
    return ch, pick(titles), build_desc(desc_parts, 3, 6)

# ─── NEWS ─────────────────────────────────────────────────────────────────────

NEWS_CHANNELS = [
    "BBC News", "CNN", "Reuters", "Al Jazeera English", "DW News",
    "France 24", "NDTV", "Sky News", "PBS NewsHour", "The Guardian",
    "The New York Times", "CNBC", "Bloomberg", "Vox", "Vice News",
    "ABC News", "NBC News", "NPR", "WION", "India Today",
    "The Hindu", "Hindustan Times", "TRT World", "NHK World",
    "South China Morning Post", "The Print", "Firstpost", "Times Now",
    "CNBC TV18", "Moneycontrol", "Mint", "The Quint", "Newslaundry",
    "Rajya Sabha TV", "Lok Sabha TV", "Republic World", "News18",
    "ET Now", "Business Standard", "Scroll.in", "The Wire",
    "Channel 4 News", "CBS News", "MSNBC", "Financial Times",
    "The Economist", "AP Archive", "CNA", "Euro News", "RT", "CGTN"
]
EVENTS = [
    "Climate Change Summit", "G20 Summit", "UN General Assembly",
    "Trade Agreement", "Peace Negotiations", "Election Results",
    "Economic Sanctions", "Refugee Crisis", "Healthcare Reform",
    "Infrastructure Bill", "Defense Budget", "Tech Regulation",
    "Central Bank Policy", "Housing Crisis", "Energy Transition",
    "Education Reform", "Tax Reform", "Labor Market Report",
    "Supply Chain Disruption", "Cybersecurity Threat", "Immigration Reform",
    "Data Privacy Law", "Anti-Trust Case", "GDP Growth Report",
    "Inflation Data", "Interest Rate Decision", "Stock Market Crash",
    "Oil Price Surge", "Water Crisis", "Food Security Summit",
    "Digital Currency Regulation", "Border Dispute", "Nuclear Deal",
    "Ceasefire Agreement", "Pandemic Response", "Vaccine Rollout",
    "Space Mission Launch", "Technology Ban", "Tariff War",
    "Constitutional Amendment", "Supreme Court Ruling"
]
LEADERS = ["Prime Minister", "President", "Chancellor", "Secretary General", "Finance Minister", "Foreign Minister"]
COUNTRIES = ["India", "United States", "China", "European Union", "United Kingdom", "Japan", "Germany", "France", "Brazil", "Australia", "Canada", "Russia", "Indonesia", "South Africa"]
ORGS = ["United Nations", "WHO", "WTO", "IMF", "World Bank", "NATO", "BRICS", "G7", "OPEC", "EU Parliament"]
SECTORS = ["Global Economy", "Public Health", "Technology Sector", "Energy Markets", "Agriculture", "Financial Markets", "Education Sector", "Defense Industry"]

def gen_news():
    ch = pick(NEWS_CHANNELS)
    event, country, leader = pick(EVENTS), pick(COUNTRIES), pick(LEADERS)
    org, sector, yr = pick(ORGS), pick(SECTORS), pick(YEARS)
    titles = [
        f"Breaking: {event} — Full Coverage and Analysis",
        f"{event}: What You Need to Know Right Now",
        f"{leader} Addresses {event} at {org} Summit",
        f"{country} {event}: Impact Analysis and Expert Opinion",
        f"Latest Update: {event} — Developments in {yr}",
        f"{org} Report on {event} Raises Concerns for {sector}",
        f"{event} Explained: Background, Context, and Implications",
        f"How {event} Affects {sector} and What Comes Next",
        f"{country}'s Response to {event}: A Detailed Analysis",
        f"Top Stories Today: {event} | {country} | {sector}",
        f"Global Markets React to {event} — Expert Analysis",
        f"Daily Briefing: {event} and Other Key Developments {yr}",
        f"Inside the {event}: Investigative Report by {ch}",
        f"The {event} Crisis: Causes, Consequences, and Solutions",
        f"{country} Elections {yr}: Polls, Candidates, and Key Issues",
    ]
    desc_parts = [
        f"In this report, we provide comprehensive coverage of the {event}, examining its causes, the key players involved, and the potential consequences for {country} and the international community.",
        f"Our team of correspondents on the ground brings you the latest developments on the {event}, with live updates, expert interviews, and in-depth analysis from our editorial team.",
        f"The {leader} of {country} addressed the {org} today regarding the {event}, outlining a series of policy measures aimed at addressing the immediate challenges facing {sector}.",
        f"Economic analysts warn that the {event} could have far-reaching consequences for {sector}, with potential ripple effects across global supply chains and international trade agreements.",
        f"This segment features interviews with leading experts in {sector} who share their perspectives on how the {event} will shape policy decisions in the coming months and years.",
        f"For the latest news updates, breaking stories, and expert analysis, subscribe to {ch} and turn on notifications to stay informed about developments that matter to you.",
        f"We also examine the historical context behind the {event}, tracing its roots and explaining why it has become one of the most significant geopolitical developments of {yr}.",
        f"A panel of political analysts, economists, and security experts discusses the broader implications of the {event} for regional stability and international relations.",
        f"This report includes exclusive footage and documents obtained by our investigative journalism team, shedding new light on the factors driving the {event}.",
        f"Follow our live blog for real-time updates on the {event}, including official statements, press conferences, and reactions from world leaders and international organizations.",
    ]
    return ch, pick(titles), build_desc(desc_parts, 4, 6)

# ─── SCIENCE ──────────────────────────────────────────────────────────────────

SCI_CHANNELS = [
    "NASA", "SpaceX", "National Geographic", "Nature Video", "SciShow",
    "Kurzgesagt", "PBS Space Time", "Veritasium", "SmarterEveryDay",
    "MinutePhysics", "MinuteEarth", "Deep Look", "Sabine Hossenfelder",
    "Dr. Becky", "Anton Petrov", "Scott Manley", "Everyday Astronaut",
    "NileRed", "The Action Lab", "Applied Science", "CERN",
    "Fermilab", "Royal Institution", "World Science Festival",
    "Science Friday", "Two Minute Papers", "Arvin Ash",
    "Cool Worlds", "Astrum", "Periodic Videos", "Fraser Cain",
    "Isaac Arthur", "SEA", "Thought Emporium", "Brainiac75",
    "Science Magazine", "New Scientist", "Scientific American",
    "It's Okay To Be Smart", "Physics Girl", "Up and Atom",
    "Looking Glass Universe", "Mark Rober", "Stuff Made Here",
    "Steve Mould", "Primer", "Science Asylum", "Domain of Science",
    "Tibees", "Dr. Physics A"
]
SCI_TOPICS = [
    "Black Holes", "Dark Matter", "CRISPR Gene Editing", "Quantum Computing",
    "Gravitational Waves", "Exoplanets", "Fusion Energy", "Higgs Boson",
    "Mars Exploration", "James Webb Telescope", "mRNA Vaccines",
    "Protein Folding", "Climate Modeling", "Ocean Acidification",
    "Stem Cell Therapy", "Neuroplasticity", "Microbiome Research",
    "Superconductors", "Nuclear Fusion", "Quantum Entanglement",
    "Antimatter", "Deep Sea Exploration", "Gene Therapy", "Immunotherapy",
    "Nanotechnology", "Battery Technology", "Carbon Capture",
    "Brain-Computer Interface", "Metamaterials", "Holography",
    "Asteroid Mining", "Solar Sail Technology", "Bioluminescence",
    "Room Temperature Superconductivity", "Graphene Applications",
    "Synthetic Biology", "Aging Research", "Photosynthesis Efficiency",
    "Coral Reef Restoration", "Earthquake Prediction", "Volcanic Activity",
    "Europa Mission", "Titan Exploration", "Lunar Base Construction",
    "Space Debris Cleanup", "Gravitational Lensing", "Cosmic Microwave Background",
    "Neutrino Astronomy", "Topological Insulators", "Dark Energy"
]
SCI_FIELDS = ["Physics", "Biology", "Medicine", "Space Exploration", "Climate Science", "Neuroscience", "Chemistry", "Materials Science", "Astronomy", "Genetics", "Oceanography", "Cosmology"]
SCI_ORGS = ["NASA", "CERN", "ESA", "MIT", "Caltech", "Stanford", "NIH", "ISRO", "Max Planck Institute", "JAXA"]
JOURNALS = ["Nature", "Science", "Physical Review Letters", "The Lancet", "Cell", "PNAS"]

def gen_science():
    ch = pick(SCI_CHANNELS)
    topic, field = pick(SCI_TOPICS), pick(SCI_FIELDS)
    org, journal, yr = pick(SCI_ORGS), pick(JOURNALS), pick(YEARS)
    titles = [
        f"New Discovery: {topic} Could Change Everything We Know About {field}",
        f"How {topic} Is Transforming {field} — Latest Research {yr}",
        f"{org} Announces Major Breakthrough in {topic}",
        f"The Science Behind {topic} — Explained with Animations",
        f"What We Just Learned About {topic} — Published in {journal}",
        f"Why {topic} Is More Important Than Anyone Realized",
        f"{topic} Experiment Yields Incredible Results at {org}",
        f"Scientists Discover New Evidence of {topic}",
        f"The Future of {field}: How {topic} Changes the Game",
        f"Understanding {topic}: A Scientific Deep Dive",
        f"Could {topic} Solve the Biggest Problem in {field}?",
        f"Visualizing {topic} Like Never Before — {yr} Update",
        f"Inside the Lab: How Researchers Study {topic}",
        f"Breakthrough: {topic} Confirmed by Independent Teams at {org}",
        f"What {topic} Reveals About the Nature of {field}",
    ]
    desc_parts = [
        f"Scientists have made a groundbreaking discovery in {topic} that could fundamentally reshape our understanding of {field} and open up entirely new avenues for research and technological development.",
        f"This new research on {topic}, published in {journal}, presents compelling evidence that challenges several long-held assumptions in the field of {field} and has generated significant excitement in the scientific community.",
        f"In this video, we break down the complex science behind {topic} using clear visuals, animations, and analogies, making cutting-edge {field} research accessible to everyone regardless of their scientific background.",
        f"The team at {org} spent over three years conducting experiments and analyzing data before reaching these conclusions about {topic}, employing state-of-the-art instrumentation and novel analytical techniques.",
        f"We explore what these findings about {topic} mean for the future of {field}, including potential applications in medicine, technology, energy, and our fundamental understanding of the natural world.",
        f"Independent research groups around the world have begun replicating the {topic} experiments, and early results appear to corroborate the original findings, lending strong support to the conclusions.",
        f"This video is part of our ongoing series covering the latest and most significant developments in {field}, bringing you peer-reviewed science explained in an engaging and accessible format.",
        f"All sources, research papers, and references cited in this video are linked in the description below for those who want to explore the original {topic} research in greater detail.",
        f"Support scientific education by subscribing to our channel and sharing this video — together we can make {field} knowledge accessible to millions of curious minds around the world.",
        f"The implications of this {topic} discovery extend beyond {field} itself, potentially influencing policy decisions, funding priorities, and the direction of scientific research for decades to come.",
    ]
    return ch, pick(titles), build_desc(desc_parts, 4, 6)

# ─── ENTERTAINMENT/VLOGS ─────────────────────────────────────────────────────

VLOG_CHANNELS = [
    "MrBeast", "PewDiePie", "Dude Perfect", "David Dobrik", "Emma Chamberlain",
    "Jake Paul", "Logan Paul", "KSI", "Lilly Singh", "Danny Gonzalez",
    "Drew Gooden", "Cody Ko", "Noel Miller", "Brent Rivera", "SSSniperwolf",
    "Collins Key", "Guava Juice", "Ryan's World", "FGTeeV",
    "Azzyland", "LaurDIY", "Safiya Nygaard", "Zach King",
    "Tana Mongeau", "Trisha Paytas", "Jeffree Star", "James Charles",
    "Charli D'Amelio", "Addison Rae", "Stokes Twins", "Unspeakable",
    "SIS vs BRO", "Like Nastya", "Ben Azelart", "Lexi Rivera",
    "Bhuvan Bam", "Ashish Chanchlani", "CarryMinati", "Triggered Insaan",
    "Harsh Beniwal", "Round2Hell", "Elvish Yadav", "Amit Bhadana",
    "Gaurav Taneja", "Sourav Joshi", "Fukra Insaan", "Mythpat",
    "Live Insaan", "Slayy Point", "Tanmay Bhat"
]
CITIES = ["NYC", "LA", "Dubai", "London", "Tokyo", "Miami", "Paris", "Bali", "Seoul", "Mumbai", "Delhi", "Bangalore"]

def gen_vlog():
    ch = pick(VLOG_CHANNELS)
    city = pick(CITIES)
    yr = pick(YEARS)
    titles = [
        f"A Day in My Life in {city} — You Won't Believe This!",
        f"I Spent 24 Hours in the World's Most Expensive Hotel",
        f"My Morning Routine {yr} — Get Ready With Me",
        f"Room Tour: My Insane New Setup",
        f"What I Got for My Birthday — Unboxing Haul",
        f"Reacting to My Old Videos — So Embarrassing",
        f"10 Things You Didn't Know About Me — Q&A",
        f"I Tried Living on $1 for 24 Hours — It Was Hard",
        f"Life Update: Big Changes Are Coming",
        f"Unboxing the Most Expensive Thing I Own",
        f"Rating My Subscribers' Outfits — Fashion Review",
        f"I Let My Best Friend Control My Life for a Day",
        f"Surprising My Mom with Her Dream Car — Emotional",
        f"We Tried Every Item at McDonald's — Food Challenge",
        f"Moving to {city}! Apartment Tour and Life Update Vlog",
        f"My Aesthetic Apartment Tour in {city}",
        f"Storytime: The Craziest Thing That Happened to Me",
        f"Day in My Life as a YouTuber — Behind the Scenes",
        f"I Only Ate Food from 7-Eleven for 24 Hours",
        f"My Honest Life Update — I've Been Hiding Something",
    ]
    desc_parts = [
        f"Hey guys welcome back to my channel! In today's video I'm taking you along on the craziest adventure of my life here in {city} and trust me you do NOT want to miss what happened at the end!",
        f"Don't forget to smash that like button, hit subscribe, and turn on the notification bell so you never miss a new upload — I post new videos every single week without fail!",
        f"Follow me on all my socials for behind-the-scenes content, stories, and exclusive updates! Links to my Instagram, Twitter, TikTok, and Snapchat are all in the bio below.",
        f"Use code CREATOR at checkout for a special discount on my merch! New collection just dropped and it's selling out fast — link in the description to grab yours before it's gone!",
        f"This was honestly one of the most fun videos I've ever filmed and I had an absolute blast making it with the entire crew — let me know in the comments what you want to see next!",
        f"Huge shoutout to my sponsor for making this video possible! Check them out using my link below for an exclusive offer that's only available to my subscribers.",
        f"If this video hits {pick(NUMS)}K likes I'll do an even crazier challenge next week so make sure to like and share this video with all your friends and family!",
        f"Business inquiries only please email my management team at the address listed below — for fan mail and PR packages the PO box address is also in the description.",
        f"Thank you so much for {pick(NUMS)} million subscribers! This community means absolutely everything to me and I wouldn't be here without each and every one of you watching and supporting.",
        f"Watch my last video if you haven't seen it yet — it was absolutely insane and it's linked right here at the end of this video or in the description below!",
    ]
    return ch, pick(titles), build_desc(desc_parts, 4, 6)

# ─── GAMING ───────────────────────────────────────────────────────────────────

GAMING_CHANNELS = [
    "PewDiePie Gaming", "Ninja", "Shroud", "xQc", "Ludwig",
    "Pokimane", "Valkyrae", "Sykkuno", "Summit1G", "Tyler1",
    "Typical Gamer", "Lazarbeam", "Fresh", "Ali-A", "Lachlan",
    "Jelly", "Kwebbelkop", "DanTDM", "Dream", "GeorgeNotFound",
    "TommyInnit", "Technoblade", "Wilbur Soot", "MrBeast Gaming",
    "Sidemen", "W2S", "Miniminter", "IShowSpeed", "Kai Cenat",
    "Total Gaming", "Dynamo Gaming", "Mortal", "Scout", "Jonathan Gaming",
    "GamerFleet", "Techno Gamerz", "Chapati Hindustani Gamer",
    "Triggered Insaan Gaming", "Ujjwal", "BeastBoyShub",
    "Mythpat Gaming", "Live Insaan Gaming", "Alpha Clasher",
    "Navi Gaming", "2B Gamer", "Desi Gamers", "UnGraduate Gamer",
    "AS Gaming", "Lokesh Gamer", "Tonde Gamer"
]
GAMES = [
    "Minecraft", "Fortnite", "GTA V", "Valorant", "Apex Legends",
    "Call of Duty", "League of Legends", "Roblox", "Among Us", "Elden Ring",
    "FIFA", "Rocket League", "CS2", "Overwatch 2", "PUBG Mobile",
    "Free Fire", "BGMI", "Clash Royale", "Genshin Impact", "Fall Guys"
]
MODES = ["Ranked", "Battle Royale", "Survival", "Creative", "Competitive", "Hardcore", "Solo", "Squad"]

def gen_gaming():
    ch = pick(GAMING_CHANNELS)
    game, mode = pick(GAMES), pick(MODES)
    yr = pick(YEARS)
    titles = [
        f"I Played {game} and THIS Happened — Unbelievable Ending",
        f"{game} but Everything is Randomized — Chaos Mode",
        f"{pick(NUMS)} Kill Game in {game}! New Personal Record",
        f"Trolling Random Players in {game} — Their Reactions Were Priceless",
        f"{game} {mode} is COMPLETELY BROKEN Right Now",
        f"My Best {game} Moments of {yr} — Highlights Compilation",
        f"First Time Playing {game} — It Was INSANE",
        f"{game} {mode} Challenge with My Friends — Who Wins?",
        f"This {game} Glitch is Absolutely Game-Breaking",
        f"I Became the Number One {game} Player — Road to Top",
        f"Can I Win {game} Using Only a Pistol?",
        f"{game} Speedrun Attempt — New Strategy Discovered",
        f"Playing {game} Until I Finally Win — No Quitting",
        f"Destroying Everyone in {game} {mode} — Easy Wins",
        f"{game} is BACK and Better Than Ever — {yr} Update Review",
        f"Teaching My Mom How to Play {game} — Hilarious Reactions",
        f"Rating Viewers' {game} Clips — Best and Worst Plays",
        f"We Broke {game} with This Overpowered Strategy",
        f"New {game} Season {pick(NUMS)} is HERE — First Impressions",
        f"I Got DESTROYED in {game} {mode} — Rage Moments Compilation",
    ]
    desc_parts = [
        f"What's up everyone! In today's video we're diving back into {game} and I promise you this is one of the wildest gaming sessions I've ever recorded — the ending is absolutely ridiculous!",
        f"If you enjoyed this {game} gameplay, make sure to leave a like on the video and subscribe with notifications on so you never miss a new upload — I post daily {game} content!",
        f"Drop a comment below telling me what {game} challenge you want me to try next and I'll pick the best suggestion for next week's video — I read every single comment!",
        f"Use my creator code in the {game} store to support the channel at no extra cost to you! It really helps me keep making these videos and I appreciate every single one of you.",
        f"Follow my Twitch channel where I stream {game} live every weekday evening — come hang out, chat with me in real time, and watch the chaos unfold as it happens live!",
        f"Join our Discord server to play {game} with other fans, share your best clips, participate in community gaming tournaments, and get early access to video announcements!",
        f"My {game} settings, keybinds, sensitivity, crosshair, and complete gaming PC setup specs are all listed in the pinned comment below for anyone who's been asking about them!",
        f"This {game} session was recorded live on stream and edited down to the best highlights and funniest rage moments — the full unedited stream VOD is available on my Twitch channel.",
        f"Shoutout to everyone in the {game} community who sent in their gameplay clips for this video — keep sending them in through Discord and I'll feature the best ones every week!",
        f"Don't miss my other {game} videos including funny compilations, rage moments, epic wins, and insane clutch plays — all linked in the playlist at the end of this video!",
    ]
    return ch, pick(titles), build_desc(desc_parts, 4, 6)

# ─── PRANKS / DRAMA ──────────────────────────────────────────────────────────

PRANK_CHANNELS = [
    "BigDawsTV", "NELK", "Ross Creations", "Roman Atwood", "FouseyTUBE",
    "Drama Alert", "Keemstar", "Tea Spill", "Spill Sesh", "Anna Oop",
    "Def Noodles", "H3H3 Productions", "ImJayStation", "Morgz",
    "Ben Azelart Pranks", "Stokes Twins Pranks", "Carter Sharer",
    "Chad Wild Clay", "Vy Qwaint", "Spy Ninja", "Infinite Lists",
    "Jack Vale Films", "Alan Chikin Chow", "Daniel LaBelle",
    "Lele Pons", "Anwar Jibawi", "Twan Kuyper",
    "Lakshay Chaudhary", "Thugesh", "Dhruv Rathee Vlogs",
    "Puneet Superstar", "UK07 Rider", "Maxtern", "Samrat Bhai",
    "The Rawknee Show", "Ocus Focus", "Crazy XYZ",
    "MR. INDIAN HACKER", "Crazy Deep", "YPM Vlogs",
    "Ankur Warikoo Shorts", "Beer Biceps Drama", "Flying Beast Drama",
    "Manoj Dey", "Technical Guruji Vlogs", "Elvish Army",
    "Lakshay vs Everyone", "Roast King", "Controversy Central",
    "Drama Hub India"
]
PERSONS = ["Girlfriend", "Boyfriend", "Best Friend", "Mom", "Dad", "Roommate", "Sister", "Wife", "Husband"]
TARGETS = ["This Creator", "Jake Paul", "This Influencer", "This TikToker", "This Couple"]
CONFESSIONS = ["Moving Away", "Dropping Out", "Breaking Up", "Quitting YouTube", "Getting Married"]
CELEBS = ["Logan Paul", "KSI", "Tana Mongeau", "Jeffree Star", "James Charles", "CarryMinati", "Elvish Yadav"]

def gen_prank():
    ch = pick(PRANK_CHANNELS)
    person, target = pick(PERSONS), pick(TARGETS)
    confession, celeb = pick(CONFESSIONS), pick(CELEBS)
    titles = [
        f"PRANKING My {person} and It WENT COMPLETELY WRONG",
        f"I Told My {person} I'm {confession} — Emotional Reaction",
        f"EXPOSING {target} — The Truth They Don't Want You to Know",
        f"{person} Caught on Camera Doing Something Shocking!",
        f"I Faked My Own Breakup to See Their Reaction",
        f"This YouTuber SCAMMED Everyone — Full Exposed Video",
        f"{celeb} vs {pick(CELEBS)}: The Complete Drama Breakdown",
        f"Why {target} Is Getting CANCELLED by Everyone",
        f"Scary Ouija Board Challenge at 3AM — DON'T TRY THIS",
        f"{person} Had the WORST Reaction to This Prank Ever",
        f"The {target} Situation Just Got Way Worse",
        f"Calling {celeb} at 3AM and They Actually Answered!",
        f"I Put Hot Sauce in My {person}'s Food — Epic Prank",
        f"Breaking Down the {target} Controversy — All the Receipts",
        f"ROASTING My {person}'s Fashion Choices — No Mercy",
        f"{celeb} Finally Responds to All the Hate",
        f"The REAL Reason {target} Disappeared from YouTube",
        f"we need to talk about {target}... this is serious",
        f"Dressing as Spider-Man in Public — People's Reactions Were WILD",
        f"I Spent 24 Hours Saying YES to Everything My {person} Said",
    ]
    desc_parts = [
        f"I absolutely cannot believe this prank went THIS far — the reaction was way more intense than anything I expected and you need to watch the entire video to see how it all played out!",
        f"EXPOSING all the truth and receipts that nobody else is willing to talk about right now — like and share this video if you want me to keep making these accountability videos!",
        f"This was hands down the most INSANE prank I have ever pulled off on my channel and I genuinely thought I was going to get in serious trouble for it — the reaction was priceless though!",
        f"The internet drama is getting completely out of hand so here is the full unbiased breakdown with every piece of evidence, screenshots, and context that you need to form your own opinion.",
        f"YOU WILL NOT BELIEVE what happened when I tried this prank on my {person}! This is easily top 3 craziest videos on this entire channel — make sure you watch until the very end!",
        f"Drop your thoughts and opinions about this whole drama situation in the comments below because I genuinely want to know what you all think — I read every single comment on these videos!",
        f"This situation has gone WAY too far and honestly someone needed to speak up about it so here is literally everything you need to know about what's really going on behind the scenes.",
        f"Subscribe and hit the notification bell because the drama content and prank videos just keep getting crazier every week and you definitely don't want to miss what I have planned next!",
        f"The tea is absolutely SCALDING right now so grab your snacks, get comfortable, and let me give you the complete breakdown of this entire situation from the very beginning to the latest developments.",
        f"Prank went completely and utterly wrong — I almost got kicked out and banned for life! But honestly it was so worth it for the reactions and I would totally do it all over again!",
    ]
    return ch, pick(titles), build_desc(desc_parts, 4, 6)

# ─── CLICKBAIT / GOSSIP ──────────────────────────────────────────────────────

CLICKBAIT_CHANNELS = [
    "Bright Side", "5-Minute Crafts", "Troom Troom", "7-Second Riddles",
    "BE AMAZED", "TheRichest", "Top Trending", "WatchMojo", "TheThings",
    "Screen Rant", "Looper", "Nicki Swift", "BuzzFeed Multiplayer",
    "E! News", "TMZ", "Access Hollywood", "Hollywood Life",
    "The Shade Room", "Bossip", "Page Six", "Perez Hilton",
    "The Infographics Show", "MostAmazingTop10", "Chills", "Top15s",
    "Mind Warehouse", "FactVerse", "Mashed", "BabbleTop",
    "Clevver News", "Entertainment Tonight", "Daily Pop",
    "Bollywood Hungama", "Lehren TV", "PinkVilla", "Bollywood Bubble",
    "SpotboyE", "BollywoodNow", "Filmibeat", "Koimoi",
    "Bollywood Spy", "Viral Bollywood", "Instant Bollywood",
    "B4U Entertainment", "Bollywood Aajkal", "FactTechz Hindi",
    "Top 10 Hindi", "Unknown Facts Hindi", "HollyBolly",
    "Gossip Central India"
]
CB_CELEBS = [
    "Kim Kardashian", "Kanye", "Drake", "Rihanna", "Selena Gomez",
    "Justin Bieber", "Elon Musk", "Kylie Jenner", "Beyonce", "Ariana Grande",
    "Dua Lipa", "Zendaya", "Tom Holland", "Bad Bunny", "Cardi B",
    "Deepika Padukone", "Ranveer Singh", "Alia Bhatt", "Shah Rukh Khan", "Salman Khan"
]
THINGS = ["Secret", "Trick", "Hack", "Signal", "Sign", "Discovery", "Photo", "Detail", "Pattern", "Feature"]
NOUNS = ["Past", "Relationship", "Fortune", "Surgery", "Diet", "Mansion", "Scandal", "Breakdown"]

def gen_clickbait():
    ch = pick(CLICKBAIT_CHANNELS)
    celeb, thing, noun = pick(CB_CELEBS), pick(THINGS), pick(NOUNS)
    titles = [
        f"You Won't BELIEVE What {celeb} Just Did — Shocking Reveal",
        f"{pick(NUMS)} {thing}s That Will Absolutely BLOW Your Mind",
        f"Why You Should NEVER Do This — The Shocking Truth Revealed",
        f"{celeb}'s Secret {noun} Has Finally Been Revealed to the Public",
        f"This Simple {thing} Will Completely Change Your Life Forever",
        f"Scientists Literally Cannot Explain This {thing}!",
        f"Doctors Are BEGGING Everyone to Stop Doing This Immediately",
        f"I Found Something Terrifying in My Backyard — SCARY",
        f"{celeb} BREAKS SILENCE on {noun} for the First Time",
        f"The Dark Truth About {thing}s That Nobody Ever Tells You",
        f"Only 3% of People Can Solve This — Are You One of Them?",
        f"If You See This {thing}, RUN Immediately and Don't Look Back!",
        f"{pick(NUMS)} Life Hacks That Are Actually GENIUS — Must Try",
        f"The Internet Is Going CRAZY Over This {thing} Right Now",
        f"{celeb} Spotted with {pick(CB_CELEBS)} — What's Really Going On?",
        f"Stop Doing THIS Right Now — Experts Issue Urgent Warning",
        f"What {celeb} Looks Like Without Makeup SHOCKED the Entire World",
        f"I Wish Everyone Knew This {thing} Much Sooner — Life Changing",
        f"Things You've Been Doing WRONG Your Entire Life",
        f"The Untold Story of {celeb}'s {noun} — Full Exclusive",
    ]
    desc_parts = [
        f"You absolutely will not believe what happened in this video — make sure to watch the FULL thing all the way to the very end to find out the shocking truth that everyone is talking about!",
        f"This is the most INSANE content we have ever produced on this channel! Like, subscribe, and share with everyone you know for mind-blowing content uploaded every single day without exception!",
        f"Celebrity gossip, shocking revelations, and exclusive behind-the-scenes information that nobody else is covering right now — don't miss a single video by subscribing and turning on all notifications!",
        f"These incredible facts will leave you completely and utterly SPEECHLESS! Comment below and tell me if number 3 surprised you because it absolutely blew my mind when I discovered it!",
        f"SHARE this video before it gets taken down! They really don't want this information getting out to the public but we believe everyone deserves to know the truth about what's really going on!",
        f"97 percent of people watching this video will get this completely WRONG! Are you in the top 3 percent? Watch the full video to find out and prove you're smarter than everyone else!",
        f"The entire internet is going absolutely CRAZY over this incredible discovery and honestly I completely understand why — once you see it you will never be able to look at things the same way again!",
        f"Subscribe RIGHT NOW for daily uploads featuring the most shocking, unbelievable, and mind-blowing content on all of YouTube — we work tirelessly to bring you the content you deserve!",
        f"This one single piece of information changes absolutely EVERYTHING about what you thought you knew! Most people have literally no idea about this shocking fact that experts have been hiding!",
        f"Watch until the END for the biggest and most unexpected reveal we have ever done on this channel — I guarantee you will be left completely speechless and you will want to tell everyone about it!",
    ]
    return ch, pick(titles), build_desc(desc_parts, 4, 6)

# ─── GENERATE ALL DATA ───────────────────────────────────────────────────────

GENERATORS = {
    "Education":           (gen_edu,       1, 2500),
    "Music":               (gen_music,     1, 2500),
    "News":                (gen_news,      1, 2500),
    "Science":             (gen_science,   1, 2500),
    "Entertainment/Vlogs": (gen_vlog,      0, 2500),
    "Gaming":              (gen_gaming,    0, 2500),
    "Pranks/Drama":        (gen_prank,     0, 2500),
    "Clickbait/Gossip":    (gen_clickbait, 0, 2500),
}

def main():
    os.makedirs("data", exist_ok=True)
    print("🔄 Generating training data...\n")

    all_samples = []

    for name, (gen_fn, label, count) in GENERATORS.items():
        seen = set()
        samples = []
        attempts = 0
        while len(samples) < count and attempts < count * 15:
            attempts += 1
            ch, title, desc = gen_fn()
            key = (ch, title[:80])  # dedup key
            if key not in seen:
                seen.add(key)
                samples.append({
                    "channel_name": ch,
                    "title": title,
                    "description": desc,
                    "label": label,
                })
        icon = "✅" if label == 1 else "❌"
        avg_desc = sum(len(s["description"]) for s in samples) / max(len(samples), 1)
        print(f"  {icon} {name}: {len(samples)} samples (avg desc: {avg_desc:.0f} chars)")
        all_samples.extend(samples)

    random.shuffle(all_samples)

    output_path = "data/training_data.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["channel_name", "title", "description", "label"])
        writer.writeheader()
        writer.writerows(all_samples)

    pos = sum(1 for s in all_samples if s["label"] == 1)
    neg = len(all_samples) - pos
    print(f"\n✅ Generated {len(all_samples)} samples → {output_path}")
    print(f"   Constructive: {pos} | Non-constructive: {neg}")
    print(f"   Balance: {pos/len(all_samples)*100:.1f}% / {neg/len(all_samples)*100:.1f}%")

if __name__ == "__main__":
    main()
