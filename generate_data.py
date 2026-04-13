"""
generate_data.py — Generates 100,000 clean, diverse, unique YouTube training samples.
Uses combinatorial expansion to create truly unique titles and descriptions.

Constructive (label=1): Education, Music, News, Science
Non-constructive (label=0): Entertainment/Vlogs, Gaming, Pranks/Drama, Clickbait/Gossip
"""

import csv, os, random, hashlib
random.seed(42)

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def pick(lst): return random.choice(lst)
def pick_n(lst, n): return random.sample(lst, min(n, len(lst)))

YEARS = ["2022", "2023", "2024", "2025", "2026"]
NUMS = ["3", "5", "7", "8", "10", "12", "15", "20", "25", "30", "50", "100"]
PARTS = ["Part 1", "Part 2", "Part 3", "Part 4", "Part 5"]
EPISODES = ["Ep 1", "Ep 2", "Ep 3", "Ep 5", "Ep 7", "Ep 10", "Ep 12", "Ep 15"]

def build_desc(sentences_pool, n_min=3, n_max=6):
    """Build a description by combining sentences. 20% short (1-2), 80% long (n_min-n_max)."""
    if random.random() < 0.20:
        n = random.randint(1, 2)
    else:
        n = random.randint(n_min, n_max)
    chosen = pick_n(sentences_pool, n)
    return " ".join(chosen)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── EDUCATION (MASSIVELY EXPANDED) ──────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

EDU_CHANNELS = [
    # International
    "Khan Academy", "MIT OpenCourseWare", "3Blue1Brown", "CrashCourse",
    "Professor Dave Explains", "Veritasium", "TED-Ed", "FreeCodeCamp",
    "Organic Chemistry Tutor", "Numberphile", "Bozeman Science",
    "Dr. Trefor Bazett", "CS Dojo", "Socratica", "The Coding Train",
    "Fireship", "Ben Eater", "Computerphile", "MinutePhysics",
    "Real Engineering", "Practical Engineering", "Technology Connections",
    "SmarterEveryDay", "ElectroBOOM", "Harvard CS50", "StatQuest",
    "Sentdex", "Corey Schafer", "Tech With Tim", "Traversy Media",
    "The Net Ninja", "Programming with Mosh", "Academind",
    "Web Dev Simplified", "Kevin Powell", "Bro Code", "thenewboston",
    "Derek Banas", "CalebCurry", "Clever Programmer",
    # Indian tech/education
    "Simplilearn", "Edureka", "Great Learning", "Unacademy", "BYJU'S",
    "Physics Wallah", "Abdul Bari", "Jenny's Lectures", "Gate Smashers",
    "Neso Academy", "CodeWithHarry", "Apna College", "Love Babbar",
    "Striver", "Pepcoding", "Kunal Kushwaha", "Telusko",
    "Intellipaat", "Krish Naik", "CampusX", "5 Minutes Engineering",
    "Knowledge Gate", "Last Moment Tuitions", "Ekeeda", "NPTEL",
    "IIT Bombay", "IIT Madras", "Indian School of Business",
    # Specific tool/platform educators
    "Sheryians Coding School", "WsCube Tech", "Colt Steele",
    "Angela Yu", "Jonas Schmedtmann", "Maximilian Schwarzmuller",
    "Stephen Grider", "Brad Traversy", "Wes Bos", "Scott Hanselman",
    "Chandler Bing Codes", "Alex The Analyst", "Luke Barousse",
    "Maven Analytics", "Guy in a Cube", "Curbal", "Patrick LeBlanc",
    "Adam Finer", "Leila Gharani", "ExcelIsFun", "MrExcel",
    "MyOnlineTrainingHub", "Teacher's Tech", "Kevin Stratvert",
    "Mike Dane", "David Bombal", "NetworkChuck", "John Hammond",
    "Professor Messer", "PowerCert", "freeCodeCamp.org",
    "William Fiset", "NeetCode", "Greg Hogg", "Reducible",
    "Spanning Tree", "Sebastian Lague", "Brackeys",
    "TechWorld with Nana", "Amigoscode", "Java Brains", "Durgasoft",
    "Hitesh Choudhary", "Chai aur Code", "The Organic Chemistry Tutor",
    "Khan Academy India", "Vedantu", "Doubtnut", "Magnet Brains",
    "PW Foundation", "Mohit Tyagi", "Mathongo", "Allen Career Institute",
    "Motion Education", "Etoos Education", "Competishun",
]

# Massively expanded EDU topics — covers programming, data, tools, academics
EDU_TOPICS = [
    # Programming languages
    "Python Programming", "Java Programming", "JavaScript", "C Programming",
    "C++ Programming", "Go Programming", "Rust Programming", "TypeScript",
    "Kotlin Programming", "Swift Programming", "Ruby Programming", "PHP Development",
    "R Programming", "Scala Programming", "Dart Programming", "Perl Scripting",
    "Shell Scripting", "Bash Scripting", "PowerShell", "Assembly Language",
    # Web development
    "HTML and CSS", "React.js", "Angular Framework", "Vue.js", "Next.js",
    "Node.js", "Express.js", "Django Framework", "Flask Framework",
    "Spring Boot", "FastAPI", "REST APIs", "GraphQL",
    "Tailwind CSS", "Bootstrap Framework", "SASS and SCSS", "Web Components",
    "Progressive Web Apps", "Server Side Rendering", "WebSocket Programming",
    "Frontend Development", "Backend Development", "Full Stack Development",
    # Data & BI tools (KEY ADDITIONS)
    "Power BI", "DAX Formulas", "Power Query", "Data Modeling in Power BI",
    "Tableau", "Tableau Desktop", "Tableau Server", "Looker Studio",
    "Google Data Studio", "Microsoft Excel", "Advanced Excel", "Excel VBA",
    "Excel Pivot Tables", "Excel VLOOKUP and XLOOKUP", "Google Sheets",
    "Data Visualization", "Business Intelligence", "Data Analytics",
    "Data Warehousing", "ETL Pipeline", "Data Engineering",
    "Apache Spark", "Apache Kafka", "Apache Airflow", "Snowflake",
    "BigQuery", "Redshift", "Databricks", "Azure Data Factory",
    "SSIS Packages", "SSRS Reports", "Azure Synapse Analytics",
    # Data Science & ML
    "Machine Learning", "Deep Learning", "Neural Networks",
    "Natural Language Processing", "Computer Vision", "Reinforcement Learning",
    "TensorFlow", "PyTorch", "Scikit-Learn", "Pandas Library",
    "NumPy", "Matplotlib", "Seaborn Visualization", "Keras",
    "Random Forest", "Decision Trees", "Gradient Boosting",
    "Logistic Regression", "Support Vector Machines", "K-Means Clustering",
    "Principal Component Analysis", "Feature Engineering",
    "Model Evaluation", "Hyperparameter Tuning", "Transfer Learning",
    "Generative AI", "Large Language Models", "Prompt Engineering",
    "ChatGPT API", "OpenAI API", "LangChain", "Vector Databases",
    "Hugging Face Transformers", "Stable Diffusion", "DALL-E",
    # DevOps & Cloud
    "Docker Containers", "Kubernetes", "CI/CD Pipeline",
    "Jenkins", "GitHub Actions", "GitLab CI", "Terraform",
    "Ansible", "AWS Cloud", "Azure Cloud", "Google Cloud Platform",
    "Linux Administration", "Nginx", "Apache Server",
    "Microservices Architecture", "Serverless Computing",
    "AWS Lambda", "AWS EC2", "AWS S3", "Azure Functions",
    # Databases
    "SQL Databases", "MySQL", "PostgreSQL", "MongoDB", "Redis",
    "Cassandra", "DynamoDB", "Firebase", "SQLite", "Oracle Database",
    "Microsoft SQL Server", "Neo4j Graph Database", "Elasticsearch",
    "Database Design", "Database Normalization", "Stored Procedures",
    "Database Indexing", "Query Optimization",
    # CS fundamentals
    "Data Structures", "Algorithm Design", "Dynamic Programming",
    "Graph Algorithms", "Sorting Algorithms", "Binary Trees",
    "Linked Lists", "Hash Tables", "Stacks and Queues", "Heaps",
    "Recursion", "Backtracking", "Greedy Algorithms", "Divide and Conquer",
    "Object Oriented Programming", "Design Patterns", "SOLID Principles",
    "System Design", "API Design", "Software Architecture",
    "Operating Systems", "Computer Networks", "Compiler Design",
    "Database Management Systems", "Theory of Computation",
    "Digital Electronics", "Computer Organization",
    "Discrete Mathematics", "Automata Theory",
    # Mathematics
    "Calculus", "Linear Algebra", "Differential Equations",
    "Probability Theory", "Statistics", "Number Theory",
    "Abstract Algebra", "Real Analysis", "Complex Analysis",
    "Graph Theory", "Combinatorics", "Mathematical Logic",
    "Numerical Methods", "Optimization Theory", "Game Theory",
    "Trigonometry", "Coordinate Geometry", "Vectors and 3D Geometry",
    "Matrices and Determinants", "Sequences and Series",
    # Science subjects
    "Quantum Mechanics", "Thermodynamics", "Electromagnetism",
    "Classical Mechanics", "Optics", "Fluid Mechanics",
    "Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry",
    "Molecular Biology", "Genetics", "Biochemistry",
    "Microbiology", "Ecology", "Evolution", "Anatomy and Physiology",
    "Cell Biology", "Immunology", "Pharmacology",
    # Engineering
    "Signal Processing", "Control Systems", "Embedded Systems",
    "VLSI Design", "Power Systems", "Communication Systems",
    "Structural Engineering", "Fluid Dynamics", "Heat Transfer",
    "Manufacturing Processes", "Engineering Drawing",
    "Finite Element Analysis", "CAD Design", "3D Modeling",
    # Cybersecurity
    "Cybersecurity", "Ethical Hacking", "Penetration Testing",
    "Network Security", "Cryptography", "Malware Analysis",
    "Bug Bounty Hunting", "Web Application Security", "OWASP Top 10",
    "Security Operations", "Incident Response", "Digital Forensics",
    # Mobile development
    "Android Development", "iOS Development", "Flutter",
    "React Native", "SwiftUI", "Jetpack Compose",
    # Other professional skills
    "Project Management", "Agile Methodology", "Scrum Framework",
    "Product Management", "UX Design", "UI Design",
    "Figma Tutorial", "Adobe Photoshop", "Adobe Illustrator",
    "Video Editing", "Motion Graphics", "After Effects",
    "Technical Writing", "Communication Skills", "Public Speaking",
    "Resume Building", "Interview Preparation", "Aptitude and Reasoning",
    # Competitive exams
    "JEE Main Preparation", "JEE Advanced Preparation", "NEET Preparation",
    "GATE Preparation", "UPSC Preparation", "CAT Preparation",
    "GRE Preparation", "GMAT Preparation", "TOEFL Preparation", "IELTS Preparation",
    "SAT Preparation", "ACT Preparation", "AP Exams", "IB Curriculum",
    "CBSE Board Exams", "ICSE Board Exams", "State Board Exams",
    "SSC Exam Preparation", "Banking Exam Preparation", "CUET Preparation",
    # Finance & Business
    "Stock Market", "Investment Strategies", "Personal Finance",
    "Financial Accounting", "Cost Accounting", "Taxation",
    "GST Filing", "Income Tax Return", "Mutual Funds",
    "Cryptocurrency Basics", "Blockchain Technology",
    "Startup Funding", "Business Strategy", "Marketing Analytics",
    "Digital Marketing", "SEO Optimization", "Google Analytics",
    "Facebook Ads", "Email Marketing", "Content Marketing",
]

EDU_FORMATS = [
    "Complete Guide for Beginners", "Full Course", "Tutorial",
    "Step by Step Guide", "Crash Course", "Masterclass",
    "Deep Dive", "Explained Simply", "From Scratch",
    "Hands On Tutorial", "Practical Guide", "Complete Roadmap",
    "Beginner to Advanced", "Made Easy", "In One Video",
    "Zero to Hero", "Quick Start Guide", "Bootcamp",
    "Workshop", "Live Session", "Lecture Series",
    "Study Guide", "Essential Concepts", "Core Fundamentals",
    "Interview Prep", "Practice Problems", "Project Based Learning",
    "Real World Examples", "With Projects", "Complete Walkthrough",
]

EDU_VERBS = [
    "Understanding", "Learning", "Mastering", "Exploring",
    "Introduction to", "Getting Started with", "How to Learn",
    "The Complete", "Everything About", "The Fundamentals of",
    "Deep Dive into", "A Visual Guide to", "Building with",
    "Working with", "Implementing", "Designing with",
    "Solving Problems in", "Hands On", "Practical",
]

def gen_edu():
    ch = pick(EDU_CHANNELS)
    topic = pick(EDU_TOPICS)
    fmt = pick(EDU_FORMATS)
    verb = pick(EDU_VERBS)
    yr = pick(YEARS)
    part = pick(PARTS)
    ep = pick(EPISODES)

    titles = [
        f"{verb} {topic} — {fmt}",
        f"{topic}: {fmt} ({part})",
        f"{topic} {fmt} | {yr}",
        f"Learn {topic} in One Video — {fmt} {yr}",
        f"{topic} Tutorial for Beginners — {fmt}",
        f"{topic} {fmt} with {pick(EDU_VERBS).rstrip()} Examples",
        f"The Mathematics Behind {topic} — {fmt}",
        f"Why Every Student Should Learn {topic} in {yr}",
        f"{topic} — Everything You Need to Know for Exams",
        f"What is {topic}? {fmt}",
        f"{topic} Full Course — Beginner to Advanced {yr}",
        f"How to Learn {topic} Effectively — Study Tips and Roadmap",
        f"{topic} Made Easy — No Prerequisites Needed",
        f"{topic} Crash Course for Students",
        f"Solving {topic} Problems — Practice Session {ep}",
        f"Advanced {topic} Concepts Every Student Must Know",
        f"{topic} {fmt} — {ch} {yr}",
        f"{topic}: Master the Fundamentals | {fmt} ({part})",
        f"{topic} for Data Analysts — {fmt}",
        f"{topic} for Absolute Beginners — {yr} Edition",
        f"Complete {topic} Course — Free Certification {yr}",
        f"{topic} Interview Questions and Answers {yr}",
        f"{topic} Project Tutorial — Build From Scratch",
        f"How {topic} Actually Works — Explained from Scratch",
        f"{topic} Roadmap {yr} — How to Get Started",
        f"Best Way to Learn {topic} — Complete Guide",
        f"{topic} Tips and Tricks Every Developer Should Know",
        f"{topic} Course {ep} — {fmt}",
        f"Master {topic} in {pick(NUMS)} Hours — {fmt}",
        f"{topic} for Working Professionals — Career Guide {yr}",
    ]

    desc_parts = [
        f"In this comprehensive video, we explore the fundamental concepts of {topic} from the ground up, starting with basic principles and gradually building toward more advanced ideas.",
        f"This lecture is part of our complete {topic} series designed for university students and self-learners who want a thorough understanding of the subject.",
        f"We begin by reviewing the prerequisites and then systematically work through each concept with detailed explanations, diagrams, and worked-out examples.",
        f"By the end of this video, you will have a solid grasp of {topic} and be well-prepared for exams, interviews, or real-world applications.",
        f"All the notes, slides, and practice problems mentioned in this video are available for free download in the link below.",
        f"If you find this helpful, please consider subscribing to the channel for more educational content on technology, programming, and engineering topics.",
        f"Timestamps are provided in the comments section so you can jump to any specific topic that interests you.",
        f"This video covers the core theory of {topic} along with practical demonstrations that help solidify your understanding.",
        f"We also discuss common mistakes students make when learning {topic} and how to avoid them in your studies and projects.",
        f"References and textbook recommendations for further reading on {topic} are listed at the end of the description.",
        f"Whether you are preparing for competitive exams like GATE, GRE, or technical interviews at top companies, this {topic} tutorial will give you the edge you need.",
        f"This session is designed for beginners who want to start their journey in {topic} from scratch without any prior experience.",
        f"Instead of just theory, we break down concepts in a simple and practical way so you can actually start using {topic} in real projects.",
        f"By the end of this video, you will clearly understand how {topic} works and how to apply it effectively in your daily work.",
        f"This is a hands-on tutorial where we build a real project using {topic} step by step, explaining every decision along the way.",
        f"We cover everything from installation and setup to advanced features of {topic}, making this a complete reference for learners at all levels.",
        f"Our instructor has over 10 years of industry experience working with {topic} and brings practical insights that you won't find in textbooks.",
        f"This course is completely free and covers {topic} in depth, with quizzes and assignments to test your understanding at each stage.",
        f"Join thousands of students who have already completed this {topic} course and landed jobs at top tech companies.",
        f"The concepts of {topic} covered in this video are frequently asked in technical interviews at companies like Google, Amazon, Microsoft, and Meta.",
    ]
    return ch, pick(titles), build_desc(desc_parts, 4, 7)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── MUSIC ────────────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

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
    "Wave Music", "Rajshri", "Ultra Bollywood",
    "Tips Official", "Venus", "Eros Now Music", "Sony Music India",
    "Warner Music India", "Gaana", "JioSaavn", "Spotify India",
    "Apple Music", "Tidal", "Deezer Sessions", "BBC Radio 1",
    "KEXP", "Mahogany Sessions", "Sofar Sounds", "Paste Magazine",
    "La Blogotheque", "Genius", "Lyrical Lemonade",
    "Trap Nation", "Bass Nation", "Chill Nation", "Selected.",
    "Mr Deep Sense", "Fluidified", "The Vibe Guide", "Chill Plug",
    "EDM Sauce", "Spinnin Records", "Armada Music", "Ultra Music",
    "Anjunabeats", "Defected Records", "Black Butter Records",
]

ARTISTS = [
    "Beethoven", "Mozart", "Bach", "Chopin", "Debussy", "Adele", "Coldplay",
    "Pink Floyd", "Miles Davis", "Hans Zimmer", "Ludovico Einaudi", "Yiruma",
    "Joe Hisaishi", "Jacob Collier", "Daft Punk", "Norah Jones",
    "Arijit Singh", "A.R. Rahman", "Shreya Ghoshal", "Lata Mangeshkar",
    "Kishore Kumar", "Sonu Nigam", "Neha Kakkar", "Atif Aslam",
    "Ed Sheeran", "Taylor Swift", "Billie Eilish", "The Weeknd",
    "Kendrick Lamar", "Post Malone", "Dua Lipa", "Harry Styles",
    "BTS", "BLACKPINK", "Imagine Dragons", "Arctic Monkeys",
    "Radiohead", "The Beatles", "Queen", "Led Zeppelin",
    "Vivaldi", "Tchaikovsky", "Liszt", "Rachmaninoff", "Schubert",
]
SONGS = [
    "Moonlight Sonata", "Clair de Lune", "Bohemian Rhapsody", "Nocturne Op 9",
    "Fur Elise", "River Flows in You", "Experience", "Time",
    "Gymnopedie No 1", "Canon in D", "Nuvole Bianche", "Comptine",
    "Summer", "Cello Suite No 1", "Rhapsody in Blue", "Take Five",
    "Tum Hi Ho", "Kun Faya Kun", "Chaiyya Chaiyya", "Kal Ho Naa Ho",
    "Raabta", "Channa Mereya", "Ae Dil Hai Mushkil", "Kesariya",
    "Shape of You", "Blinding Lights", "Someone Like You", "Dynamite",
]
GENRES = [
    "Classical", "Jazz", "Lo-fi", "Ambient", "Indie", "Folk", "R&B", "Soul",
    "Blues", "Electronic", "Orchestral", "Acoustic", "Piano", "Instrumental",
    "Bollywood", "Sufi", "Ghazal", "Devotional", "Carnatic", "Hindustani",
    "Hip Hop", "Pop", "Rock", "Metal", "Country", "Reggae", "Latin",
    "K-Pop", "EDM", "House", "Techno", "Trance", "Drum and Bass",
]
INSTRUMENTS = ["Piano", "Guitar", "Violin", "Cello", "Drums", "Saxophone", "Sitar", "Flute", "Tabla", "Harmonium", "Veena", "Sarangi"]
VENUES = ["Carnegie Hall", "Royal Albert Hall", "Sydney Opera House", "Red Rocks", "Madison Square Garden", "Wembley Stadium", "Hollywood Bowl", "Blue Note", "Montreux Jazz Festival"]
MOODS = ["Relaxing", "Uplifting", "Melancholic", "Energetic", "Peaceful", "Romantic", "Nostalgic", "Dreamy", "Soulful", "Calming"]

def gen_music():
    ch = pick(MUSIC_CHANNELS)
    artist, song, genre = pick(ARTISTS), pick(SONGS), pick(GENRES)
    inst, yr, venue = pick(INSTRUMENTS), pick(YEARS), pick(VENUES)
    mood = pick(MOODS)
    titles = [
        f"{artist} — {song} (Official Music Video)",
        f"Best {genre} Playlist {yr} — {pick(NUMS)} Hours of Pure Music",
        f"{artist} Live at {venue} — Full Concert",
        f"{genre} Mix — {mood} Music for Study and Focus",
        f"How to Play {song} on {inst} — Complete Tutorial",
        f"{artist} — {song} (Acoustic Session)",
        f"Top {genre} Songs of All Time — Curated Playlist",
        f"{artist} Greatest Hits — Full Album Stream",
        f"{song} | Beautiful {inst} Cover",
        f"{mood} {genre} for Sleep, Study, and Meditation — {yr}",
        f"Orchestra Performs {song} — Breathtaking Performance",
        f"{artist} Unplugged — Intimate Live Session",
        f"Music Theory Analysis: Why {song} is a Masterpiece",
        f"{genre} Lofi Beats — Chill Vibes All Day",
        f"Learning {inst}: {song} Step by Step for Beginners",
        f"{mood} {genre} Music — {pick(NUMS)} Hour Playlist {yr}",
        f"{artist} {song} Slowed and Reverb — {mood} Vibes",
        f"Best of {artist} — Top {pick(NUMS)} Songs Collection",
        f"{genre} Radio — Live Stream 24/7",
        f"{inst} Music for {mood} Moments — {yr} Compilation",
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
        f"This video is part of our ongoing series exploring the greatest works in {genre} music, analyzing what makes each piece timeless.",
        f"This {mood} {genre} mix is perfect for background listening while you work, study, read, or simply unwind after a long day.",
        f"Featuring {pick(NUMS)} handpicked tracks from the best {genre} artists, this compilation is designed to create the perfect {mood} atmosphere.",
    ]
    return ch, pick(titles), build_desc(desc_parts, 3, 6)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── NEWS ─────────────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

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
    "The Economist", "AP Archive", "CNA", "Euro News",
    "Gravitas WION", "Palki Sharma", "Dhruv Rathee",
    "Think School", "Soch by Mohak Mangal", "Newsthink",
    "RealLifeLore", "PolyMatter", "CaspianReport", "TLDR News",
    "Wendover Productions", "Half as Interesting",
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
    "Inflation Data", "Interest Rate Decision", "Stock Market Movement",
    "Oil Price Surge", "Water Crisis", "Food Security Summit",
    "Digital Currency Regulation", "Border Dispute", "Nuclear Deal",
    "Ceasefire Agreement", "Pandemic Response", "Vaccine Rollout",
    "Space Mission Launch", "Technology Ban", "Tariff War",
    "Constitutional Amendment", "Supreme Court Ruling",
    "Budget Announcement", "Foreign Policy Shift", "Climate Accord",
    "Semiconductor Crisis", "AI Regulation", "Tech Layoffs",
    "Union Budget Analysis", "RBI Policy Review", "SEBI Regulation",
    "Trade Deficit Report", "Agricultural Reform", "Labor Code",
]
LEADERS = ["Prime Minister", "President", "Chancellor", "Secretary General", "Finance Minister", "Foreign Minister", "Chief Justice", "Governor"]
COUNTRIES = ["India", "United States", "China", "European Union", "United Kingdom", "Japan", "Germany", "France", "Brazil", "Australia", "Canada", "Russia", "Indonesia", "South Africa", "South Korea", "Mexico", "Saudi Arabia", "Turkey"]
ORGS = ["United Nations", "WHO", "WTO", "IMF", "World Bank", "NATO", "BRICS", "G7", "OPEC", "EU Parliament", "ASEAN", "African Union", "SCO"]
SECTORS = ["Global Economy", "Public Health", "Technology Sector", "Energy Markets", "Agriculture", "Financial Markets", "Education Sector", "Defense Industry", "Housing Sector", "Manufacturing"]

def gen_news():
    ch = pick(NEWS_CHANNELS)
    event, country, leader = pick(EVENTS), pick(COUNTRIES), pick(LEADERS)
    org, sector, yr = pick(ORGS), pick(SECTORS), pick(YEARS)
    titles = [
        f"Breaking: {event} — Full Coverage and Analysis",
        f"{event}: What You Need to Know Right Now",
        f"{leader} Addresses {event} at {org} Summit",
        f"{country} {event}: Impact Analysis and Expert Opinion",
        f"Latest Update: {event} — Key Developments in {yr}",
        f"{org} Report on {event} Raises Concerns for {sector}",
        f"{event} Explained: Background, Context, and Implications",
        f"How {event} Affects {sector} and What Comes Next",
        f"{country}'s Response to {event}: A Detailed Analysis",
        f"Top Stories Today: {event} | {country} | {sector}",
        f"Global Markets React to {event} — Expert Analysis",
        f"Daily Briefing: {event} and Other Key Developments {yr}",
        f"Inside the {event}: Investigative Report",
        f"The {event}: Causes, Consequences, and Solutions",
        f"{country} {yr}: Analysis of {event} and Its Impact on {sector}",
        f"What the {event} Means for {country} — Deep Analysis",
        f"{event} Timeline: Everything That Happened So Far",
        f"Expert Panel Discusses {event} and {sector} Outlook",
        f"Why {event} Matters More Than You Think — {yr} Analysis",
        f"Geopolitical Analysis: {event} and {country}'s Role in {org}",
    ]
    desc_parts = [
        f"In this report, we provide comprehensive coverage of the {event}, examining its causes, the key players involved, and the potential consequences for {country} and the international community.",
        f"Our team of correspondents on the ground brings you the latest developments on the {event}, with live updates, expert interviews, and in-depth analysis from our editorial team.",
        f"The {leader} of {country} addressed the {org} today regarding the {event}, outlining a series of policy measures aimed at addressing the immediate challenges facing {sector}.",
        f"Economic analysts warn that the {event} could have far-reaching consequences for {sector}, with potential ripple effects across global supply chains and international trade agreements.",
        f"This segment features interviews with leading experts in {sector} who share their perspectives on how the {event} will shape policy decisions in the coming months and years.",
        f"For the latest news updates, breaking stories, and expert analysis, subscribe to {ch} and turn on notifications to stay informed about developments that matter to you.",
        f"We examine the historical context behind the {event}, tracing its roots and explaining why it has become one of the most significant developments of {yr}.",
        f"A panel of political analysts, economists, and security experts discusses the broader implications of the {event} for regional stability and international relations.",
        f"This report includes exclusive footage and documents obtained by our investigative journalism team, shedding new light on the factors driving the {event}.",
        f"Follow our live coverage for real-time updates on the {event}, including official statements, press conferences, and reactions from world leaders.",
        f"We analyze how the {event} is connected to broader trends in {sector} and what it reveals about the changing geopolitical landscape in {yr}.",
        f"This analysis breaks down the complex dynamics of the {event}, making it accessible and understandable for viewers who want to stay informed about global affairs.",
    ]
    return ch, pick(titles), build_desc(desc_parts, 4, 6)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── SCIENCE ──────────────────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

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
    "Tibees", "Dr. Physics A", "Dianna Cowern", "Practical Engineering",
    "Real Science", "Answers With Joe", "Joe Scott", "Kyle Hill",
    "BrainCraft", "Vsauce", "Vsauce2", "Vsauce3",
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
    "Neutrino Astronomy", "Topological Insulators", "Dark Energy",
    "Artificial Photosynthesis", "Quantum Teleportation", "String Theory",
    "Particle Physics", "Plasma Physics", "Quantum Biology",
    "Astrobiology", "Terraforming", "Dyson Sphere", "Anti-Aging Research",
]
SCI_FIELDS = ["Physics", "Biology", "Medicine", "Space Exploration", "Climate Science", "Neuroscience", "Chemistry", "Materials Science", "Astronomy", "Genetics", "Oceanography", "Cosmology", "Earth Science", "Ecology"]
SCI_ORGS = ["NASA", "CERN", "ESA", "MIT", "Caltech", "Stanford", "NIH", "ISRO", "Max Planck Institute", "JAXA", "SpaceX", "ITER", "Fermilab"]
JOURNALS = ["Nature", "Science", "Physical Review Letters", "The Lancet", "Cell", "PNAS", "New England Journal of Medicine", "Annual Review"]

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
        f"The Complete Story of {topic} — From Theory to Discovery",
        f"How {topic} Works — {field} Explained for Everyone",
        f"{yr} Nobel Prize: {topic} and Its Impact on {field}",
        f"Documentary: The Quest for {topic} at {org}",
        f"Why Scientists Are Excited About {topic} — {journal} Paper Review",
    ]
    desc_parts = [
        f"Scientists have made a groundbreaking discovery in {topic} that could fundamentally reshape our understanding of {field} and open up entirely new avenues for research.",
        f"This new research on {topic}, published in {journal}, presents compelling evidence that challenges several long-held assumptions in {field}.",
        f"In this video, we break down the complex science behind {topic} using clear visuals, animations, and analogies, making cutting-edge {field} research accessible to everyone.",
        f"The team at {org} spent over three years conducting experiments and analyzing data before reaching these conclusions about {topic}.",
        f"We explore what these findings about {topic} mean for the future of {field}, including potential applications in medicine, technology, and energy.",
        f"Independent research groups around the world have begun replicating the {topic} experiments, and early results corroborate the original findings.",
        f"This video is part of our ongoing series covering the latest developments in {field}, bringing you peer-reviewed science explained in an engaging format.",
        f"All sources, research papers, and references cited in this video are linked in the description below for those who want to explore the original {topic} research.",
        f"Support scientific education by subscribing to our channel and sharing this video.",
        f"The implications of this {topic} discovery extend beyond {field} itself, potentially influencing policy decisions and the direction of scientific research for decades.",
        f"We interview leading researchers working on {topic} at {org}, who share their insights on how this discovery was made and what comes next.",
        f"This documentary explores the full history of {topic} research, from early theoretical predictions to the latest experimental confirmations.",
    ]
    return ch, pick(titles), build_desc(desc_parts, 4, 7)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── ENTERTAINMENT / VLOGS (NON-CONSTRUCTIVE) ────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

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
    "Live Insaan", "Slayy Point", "Tanmay Bhat",
    "Jordan Matter", "Yes Theory", "Airrack", "Danny Duncan",
    "Vitaly", "Lance Stewart", "Liza Koshy", "King Bach",
    "Lele Pons", "Hannah Stocking", "Alisha Marie",
    "Superwoman", "JeromeASF", "SSSniperWolf Reacts",
]
CITIES = ["NYC", "LA", "Dubai", "London", "Tokyo", "Miami", "Paris", "Bali", "Seoul", "Mumbai", "Delhi", "Bangalore", "Las Vegas", "Berlin", "Bangkok", "Singapore"]
CHALLENGES = ["24 hours in", "eating only", "spending $10000 at", "living in", "surviving", "buying everything at", "saying yes to everything at"]

def gen_vlog():
    ch = pick(VLOG_CHANNELS)
    city = pick(CITIES)
    yr = pick(YEARS)
    challenge = pick(CHALLENGES)
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
        f"{challenge} {city} — INSANE Experience",
        f"Buying Everything in One Color for 24 Hours Challenge",
        f"I Gave Away $100000 to Random Strangers on the Street",
        f"Extreme Hide and Seek in my Mansion — Winner Gets Prize",
        f"Testing VIRAL TikTok Life Hacks — Do They Actually Work?",
        f"Last to Leave {city} Wins $10000 Challenge",
        f"Reacting to my Subscribers' Rooms — Rating Tour",
        f"I Built a Treehouse and Lived in It for 24 Hours",
        f"Trying {city}'s Cheapest vs Most Expensive Restaurant",
        f"My Weekly Reset Routine — Cleaning, Organization, Self Care Vlog",
    ]
    desc_parts = [
        f"Hey guys welcome back to my channel! In today's video I'm taking you along on the craziest adventure of my life here in {city} and trust me you do NOT want to miss what happened!",
        f"Don't forget to smash that like button, hit subscribe, and turn on the notification bell so you never miss a new upload — I post new videos every single week!",
        f"Follow me on all my socials for behind-the-scenes content! Links to my Instagram, Twitter, TikTok, and Snapchat are all in the bio below.",
        f"Use code CREATOR at checkout for a special discount on my merch! New collection just dropped and it's selling out fast — link in the description!",
        f"This was honestly one of the most fun videos I've ever filmed and I had an absolute blast making it with the entire crew!",
        f"Huge shoutout to my sponsor for making this video possible! Check them out using my link below for an exclusive offer.",
        f"If this video hits {pick(NUMS)}K likes I'll do an even crazier challenge next week so make sure to like and share!",
        f"Business inquiries only please email my management team at the address listed below.",
        f"Thank you so much for {pick(NUMS)} million subscribers! This community means absolutely everything to me!",
        f"Watch my last video if you haven't seen it yet — it was absolutely insane and it's linked right here!",
        f"Comment below what challenge you want me to try next in {city}! I read every single comment and pick the best ones.",
        f"This trip to {city} was absolutely wild and I can't wait to show you everything that happened — stay tuned for the full series!",
    ]
    return ch, pick(titles), build_desc(desc_parts, 4, 6)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── GAMING (NON-CONSTRUCTIVE) ───────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

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
    "AS Gaming", "Lokesh Gamer", "Tonde Gamer",
    "Markiplier", "Jacksepticeye", "CoryxKenshin", "SSundee",
    "Ldshadowlady", "Aphmau", "PrestonPlayz", "BriannaPlayz",
]
GAMES = [
    "Minecraft", "Fortnite", "GTA V", "Valorant", "Apex Legends",
    "Call of Duty", "League of Legends", "Roblox", "Among Us", "Elden Ring",
    "FIFA", "Rocket League", "CS2", "Overwatch 2", "PUBG Mobile",
    "Free Fire", "BGMI", "Clash Royale", "Genshin Impact", "Fall Guys",
    "Hogwarts Legacy", "Starfield", "Palworld", "Lethal Company",
    "Baldur's Gate 3", "GTA Online", "Helldivers 2", "The Finals",
]
MODES = ["Ranked", "Battle Royale", "Survival", "Creative", "Competitive", "Hardcore", "Solo", "Squad", "Duos", "Custom"]

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
        f"Why I'm QUITTING {game} Forever — The Truth",
        f"{game} Pro vs Noob Challenge — Who Will Win?",
        f"This {game} {mode} Strategy is UNFAIR — Easy Wins Every Time",
        f"Building the ULTIMATE Base in {game} — Insane Design",
        f"I Spent {pick(NUMS)} Hours in {game} — Here's What Happened",
        f"{game} Funny Moments Compilation — Try Not to Laugh",
        f"REACTING to the Best {game} Plays of {yr}",
        f"LIVE — Playing {game} {mode} with Subscribers — Join Now!",
        f"The WORST {game} Player You've Ever Seen — Fail Compilation",
        f"Hacking in {game}? I Found Something Suspicious",
    ]
    desc_parts = [
        f"What's up everyone! In today's video we're diving back into {game} and I promise you this is one of the wildest gaming sessions I've ever recorded!",
        f"If you enjoyed this {game} gameplay, make sure to leave a like and subscribe with notifications on — I post daily {game} content!",
        f"Drop a comment below telling me what {game} challenge you want me to try next!",
        f"Use my creator code in the {game} store to support the channel at no extra cost to you!",
        f"Follow my Twitch channel where I stream {game} live every weekday evening — come hang out and chat!",
        f"Join our Discord server to play {game} with other fans and participate in community tournaments!",
        f"My {game} settings, keybinds, sensitivity, and complete PC setup specs are all listed in the pinned comment below!",
        f"This {game} session was recorded live on stream and edited down to the best highlights and funniest moments.",
        f"Shoutout to everyone who sent in their {game} clips — keep sending them through Discord!",
        f"Don't miss my other {game} videos including funny compilations, rage moments, and epic wins — all in the playlist!",
        f"The new {game} update completely changed the meta and we're testing out all the new strategies in {mode} mode today.",
        f"This {game} challenge was suggested by a subscriber and it was way harder than I expected — wait until you see what happened!",
    ]
    return ch, pick(titles), build_desc(desc_parts, 4, 6)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── PRANKS / DRAMA (NON-CONSTRUCTIVE) ───────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

PRANK_CHANNELS = [
    "BigDawsTV", "NELK", "Ross Creations", "Roman Atwood", "FouseyTUBE",
    "Drama Alert", "Keemstar", "Tea Spill", "Spill Sesh", "Anna Oop",
    "Def Noodles", "H3H3 Productions", "ImJayStation", "Morgz",
    "Ben Azelart Pranks", "Stokes Twins Pranks", "Carter Sharer",
    "Chad Wild Clay", "Vy Qwaint", "Spy Ninja", "Infinite Lists",
    "Jack Vale Films", "Alan Chikin Chow", "Daniel LaBelle",
    "Lele Pons", "Anwar Jibawi", "Twan Kuyper",
    "Lakshay Chaudhary", "Thugesh", "Puneet Superstar", "UK07 Rider",
    "Maxtern", "The Rawknee Show", "Ocus Focus", "Crazy XYZ",
    "MR. INDIAN HACKER", "Crazy Deep", "YPM Vlogs",
    "Roast King", "Controversy Central", "Drama Hub India",
    "Just For Laughs Gags", "TrollStation", "VitalyzdTV",
    "RackaRacka", "Marlon Webb", "King Vader",
    "Dhar Mann", "Jay Shetty Drama", "SunnyV2",
    "Penguinz0", "Turkey Tom", "Kavos",
]
PERSONS = ["Girlfriend", "Boyfriend", "Best Friend", "Mom", "Dad", "Roommate", "Sister", "Wife", "Husband", "Brother", "Grandma"]
TARGETS = ["This Creator", "Jake Paul", "This Influencer", "This TikToker", "This Couple", "This Celebrity", "This Streamer"]
CONFESSIONS = ["Moving Away", "Dropping Out", "Breaking Up", "Quitting YouTube", "Getting Married", "Getting Arrested", "Losing Everything"]
CELEBS = ["Logan Paul", "KSI", "Tana Mongeau", "Jeffree Star", "James Charles", "CarryMinati", "Elvish Yadav", "Mr Beast", "Dream"]

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
        f"CONFRONTING {target} Face to Face — It Got Heated",
        f"The ENTIRE {celeb} Drama Explained in {pick(NUMS)} Minutes",
        f"I Hired a Private Investigator to Follow My {person}",
        f"Destroying My {person}'s Phone and Surprising Them With a New One",
        f"Caught My {person} LYING — Hidden Camera Footage",
        f"ROAST Battle: Me vs {person} — Who Wins?",
        f"Filling My {person}'s Room With {pick(NUMS)}000 Balloons Prank",
        f"Reading My {person}'s Text Messages — EXPOSED",
        f"I Pretended to be INVISIBLE for 24 Hours — Prank",
        f"Extreme Truth or Dare with My {person} — GONE WRONG",
    ]
    desc_parts = [
        f"I absolutely cannot believe this prank went THIS far — the reaction was way more intense than anything I expected!",
        f"EXPOSING all the truth and receipts that nobody else is willing to talk about — like and share if you want more!",
        f"This was hands down the most INSANE prank I have ever pulled off on my channel and I genuinely thought I was going to get in trouble!",
        f"The internet drama is getting completely out of hand so here is the full unbiased breakdown with every piece of evidence you need.",
        f"YOU WILL NOT BELIEVE what happened when I tried this on my {person}! Make sure you watch until the very end!",
        f"Drop your thoughts about this whole drama in the comments below because I genuinely want to know what you all think!",
        f"This situation has gone WAY too far and honestly someone needed to speak up about it.",
        f"Subscribe and hit the notification bell because the prank videos just keep getting crazier every week!",
        f"The tea is absolutely SCALDING right now so grab your snacks and let me give you the complete breakdown!",
        f"Prank went completely wrong — I almost got kicked out and banned for life! But it was so worth it for the reactions!",
        f"This is not clickbait — everything in this video actually happened and I have the evidence to prove it.",
        f"Make sure to follow all my socials for behind-the-scenes of these pranks — the bloopers are even funnier!",
    ]
    return ch, pick(titles), build_desc(desc_parts, 4, 6)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── CLICKBAIT / GOSSIP (NON-CONSTRUCTIVE) ───────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

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
    "Gossip Central India", "Did You Know Facts", "Ridddle",
    "MatPat", "Film Theory", "Talltanic",
]
CB_CELEBS = [
    "Kim Kardashian", "Kanye", "Drake", "Rihanna", "Selena Gomez",
    "Justin Bieber", "Elon Musk", "Kylie Jenner", "Beyonce", "Ariana Grande",
    "Dua Lipa", "Zendaya", "Tom Holland", "Bad Bunny", "Cardi B",
    "Deepika Padukone", "Ranveer Singh", "Alia Bhatt", "Shah Rukh Khan", "Salman Khan",
    "Taylor Swift", "Travis Kelce", "Margot Robbie", "Timothee Chalamet",
]
THINGS = ["Secret", "Trick", "Hack", "Signal", "Sign", "Discovery", "Photo", "Detail", "Pattern", "Feature", "Fact", "Method"]
NOUNS = ["Past", "Relationship", "Fortune", "Surgery", "Diet", "Mansion", "Scandal", "Breakdown", "Transformation", "Lifestyle"]

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
        f"Top {pick(NUMS)} CRAZIEST {thing}s Ever Caught on Camera",
        f"Why Everyone Is WRONG About {celeb} — The Real Story",
        f"{celeb}'s {noun} EXPOSED — This Changes Everything",
        f"Watch This Before It Gets DELETED — {thing} Revealed",
        f"The REAL Reason {celeb} Did This SHOCKED Everyone",
        f"Ranking the Most INSANE {thing}s of {pick(YEARS)}",
        f"This ONE {thing} RUINED {celeb}'s Career Forever",
        f"I Tried {celeb}'s {noun} Routine and THIS Happened",
        f"Nobody Is Talking About {celeb}'s {noun} and Here's Why",
        f"The TRUTH About {celeb} That {pick(CB_CELEBS)} Doesn't Want You to Know",
    ]
    desc_parts = [
        f"You absolutely will not believe what happened — make sure to watch the FULL thing all the way to the very end to find out the shocking truth!",
        f"This is the most INSANE content we have ever produced! Like, subscribe, and share for mind-blowing content uploaded every day!",
        f"Celebrity gossip, shocking revelations, and exclusive behind-the-scenes information that nobody else is covering right now!",
        f"These incredible facts will leave you completely SPEECHLESS! Comment below and tell me if number 3 surprised you!",
        f"SHARE this video before it gets taken down! They really don't want this information getting out to the public!",
        f"97 percent of people will get this completely WRONG! Are you in the top 3 percent?",
        f"The entire internet is going absolutely CRAZY over this incredible discovery!",
        f"Subscribe RIGHT NOW for daily uploads featuring the most shocking and unbelievable content on YouTube!",
        f"This one single piece of information changes absolutely EVERYTHING about what you thought you knew!",
        f"Watch until the END for the biggest reveal we have ever done — I guarantee you will be speechless!",
        f"Don't miss any of our shocking content — turn on all notifications and never be behind on the latest trending stories!",
        f"We spent WEEKS researching this topic and what we found is absolutely mind-blowing — you need to see this!",
    ]
    return ch, pick(titles), build_desc(desc_parts, 4, 6)

# ═══════════════════════════════════════════════════════════════════════════════
# ─── GENERATE ALL DATA ───────────────────────────────────────────────────────
# ═══════════════════════════════════════════════════════════════════════════════

GENERATORS = {
    "Education":           (gen_edu,       1, 12500),
    "Music":               (gen_music,     1, 12500),
    "News":                (gen_news,      1, 12500),
    "Science":             (gen_science,   1, 12500),
    "Entertainment/Vlogs": (gen_vlog,      0, 12500),
    "Gaming":              (gen_gaming,    0, 12500),
    "Pranks/Drama":        (gen_prank,     0, 12500),
    "Clickbait/Gossip":    (gen_clickbait, 0, 12500),
}

def main():
    os.makedirs("data", exist_ok=True)
    print("🔄 Generating 100,000 training samples...\n")

    all_samples = []

    for name, (gen_fn, label, count) in GENERATORS.items():
        seen = set()
        samples = []
        attempts = 0
        max_attempts = count * 30  # More headroom for 100k unique samples
        while len(samples) < count and attempts < max_attempts:
            attempts += 1
            ch, title, desc = gen_fn()
            # Use hash of title + desc for dedup (desc is always unique due to random combos)
            key = hashlib.md5((title + desc).encode()).hexdigest()
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
