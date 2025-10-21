import sqlite3
from datetime import datetime
import pandas as pd

class ContentDatabase:
    def __init__(self, db_name="contentmood.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def create_tables(self):
        """Create all necessary tables"""
        self.connect()
        
        # Content table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content_type TEXT NOT NULL,
                genre TEXT,
                creator TEXT,
                release_year INTEGER,
                date_consumed DATE NOT NULL,
                rating REAL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Mood logs table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mood_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_id INTEGER,
                mood_before INTEGER,
                mood_after INTEGER,
                emotional_tags TEXT,
                log_date DATE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (content_id) REFERENCES content(id)
            )
        ''')
        
        self.conn.commit()
        self.close()
    
    def add_content(self, title, content_type, genre, creator, release_year, 
                   date_consumed, rating, notes=""):
        """Add new content entry"""
        self.connect()
        self.cursor.execute('''
            INSERT INTO content (title, content_type, genre, creator, release_year, 
                               date_consumed, rating, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, content_type, genre, creator, release_year, date_consumed, rating, notes))
        self.conn.commit()
        content_id = self.cursor.lastrowid
        self.close()
        return content_id
    
    def add_mood_log(self, content_id, mood_before, mood_after, emotional_tags, log_date):
        """Add mood log for content"""
        self.connect()
        self.cursor.execute('''
            INSERT INTO mood_logs (content_id, mood_before, mood_after, emotional_tags, log_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (content_id, mood_before, mood_after, emotional_tags, log_date))
        self.conn.commit()
        self.close()
    
    def get_all_content(self):
        """Retrieve all content entries"""
        self.connect()
        df = pd.read_sql_query("SELECT * FROM content ORDER BY date_consumed DESC", self.conn)
        self.close()
        return df
    
    def get_all_moods(self):
        """Retrieve all mood logs"""
        self.connect()
        df = pd.read_sql_query("SELECT * FROM mood_logs ORDER BY log_date DESC", self.conn)
        self.close()
        return df
    
    def get_content_with_moods(self):
        """Get content joined with mood data"""
        self.connect()
        query = '''
            SELECT 
                c.id,
                c.title,
                c.content_type,
                c.genre,
                c.creator,
                c.rating,
                c.date_consumed,
                c.notes,
                m.mood_before,
                m.mood_after,
                m.emotional_tags,
                (m.mood_after - m.mood_before) as mood_change
            FROM content c
            LEFT JOIN mood_logs m ON c.id = m.content_id
            ORDER BY c.date_consumed DESC
        '''
        df = pd.read_sql_query(query, self.conn)
        self.close()
        return df
    
    def get_genre_stats(self):
        """Get statistics by genre"""
        self.connect()
        query = '''
            SELECT 
                c.genre,
                COUNT(*) as count,
                AVG(c.rating) as avg_rating,
                AVG(m.mood_after - m.mood_before) as avg_mood_change
            FROM content c
            LEFT JOIN mood_logs m ON c.id = m.content_id
            WHERE c.genre IS NOT NULL
            GROUP BY c.genre
            ORDER BY count DESC
        '''
        df = pd.read_sql_query(query, self.conn)
        self.close()
        return df
    
    def get_content_type_stats(self):
        """Get statistics by content type"""
        self.connect()
        query = '''
            SELECT 
                c.content_type,
                COUNT(*) as count,
                AVG(c.rating) as avg_rating,
                AVG(m.mood_after - m.mood_before) as avg_mood_change
            FROM content c
            LEFT JOIN mood_logs m ON c.id = m.content_id
            GROUP BY c.content_type
            ORDER BY count DESC
        '''
        df = pd.read_sql_query(query, self.conn)
        self.close()
        return df
    
    def seed_sample_data(self):
        """Seed database with 110+ sample entries"""
        
        # List to hold all content (will be 110+ entries)
        all_content = []
        
        # YOUR TOP FAVORITES (6 entries)
        all_content.extend([
            ("Powerless", "Book", "Dystopian Fiction", "Lauren Roberts", 2023, "2024-10-10", 9.0, "So interested, read it in a week!"),
            ("The Hunger Games: Sunrise on the Reaping", "Book", "Dystopian Fiction", "Suzanne Collins", 2025, "2024-10-15", 10.0, "Emotionally destroyed, cried so much. Inhaled this 600+ page book in ONE DAY"),
            ("Welcome to Demon School! Iruma-kun", "Anime", "Comedy Shounen", "NHK", 2019, "2024-10-05", 8.5, "Calm and happy vibes"),
            ("Toilet-Bound Hanako-kun", "Anime", "Horror Mystery Thriller", "Lerche", 2020, "2024-09-28", 8.5, "Intrigued and interested"),
            ("Gossip Girl", "TV Show", "Drama", "Josh Schwartz", 2007, "2024-10-01", 8.0, "Comfort show, calm lazy day vibes"),
            ("Brooklyn Nine-Nine", "TV Show", "Sitcom", "Dan Goor & Michael Schur", 2013, "2024-09-25", 9.0, "Comfort show, calm and hilarious"),
        ])
        
        # ADAM SILVERA - your fave author! (4 entries)
        all_content.extend([
            ("They Both Die at the End", "Book", "Young Adult", "Adam Silvera", 2017, "2024-09-18", 10.0, "SOBBING. Absolutely heartbreaking and beautiful"),
            ("The Infinity Son", "Book", "Young Adult Fantasy", "Adam Silvera", 2020, "2024-08-22", 9.0, "So good! Magic and found family vibes"),
            ("What If It's Us", "Book", "Young Adult Romance", "Adam Silvera & Becky Albertalli", 2018, "2024-09-05", 8.5, "Cute and emotional"),
            ("More Happy Than Not", "Book", "Young Adult", "Adam Silvera", 2015, "2024-07-15", 9.5, "Mind-bending and heartbreaking"),
        ])
        
        # HARRY POTTER SERIES (7 books)
        all_content.extend([
            ("Harry Potter and the Sorcerer's Stone", "Book", "Young Adult Fantasy", "J.K. Rowling", 1997, "2024-06-01", 10.0, "Where it all began! Pure magic"),
            ("Harry Potter and the Chamber of Secrets", "Book", "Young Adult Fantasy", "J.K. Rowling", 1998, "2024-06-05", 9.0, "The basilisk scene!"),
            ("Harry Potter and the Prisoner of Azkaban", "Book", "Young Adult Fantasy", "J.K. Rowling", 1999, "2024-06-10", 10.0, "Best HP book! Time travel done right"),
            ("Harry Potter and the Goblet of Fire", "Book", "Young Adult Fantasy", "J.K. Rowling", 2000, "2024-06-18", 9.5, "The Triwizard Tournament was INTENSE"),
            ("Harry Potter and the Order of the Phoenix", "Book", "Young Adult Fantasy", "J.K. Rowling", 2003, "2024-06-25", 9.0, "So long but so good. RIP Sirius 😭"),
            ("Harry Potter and the Half-Blood Prince", "Book", "Young Adult Fantasy", "J.K. Rowling", 2005, "2024-07-02", 9.5, "That ending destroyed me"),
            ("Harry Potter and the Deathly Hallows", "Book", "Young Adult Fantasy", "J.K. Rowling", 2007, "2024-07-08", 10.0, "Perfect ending. Always."),
        ])
        
        # PERCY JACKSON SERIES (5 books)
        all_content.extend([
            ("The Lightning Thief", "Book", "Young Adult Fantasy", "Rick Riordan", 2005, "2024-05-10", 9.5, "Greek mythology + modern world = perfection"),
            ("The Sea of Monsters", "Book", "Young Adult Fantasy", "Rick Riordan", 2006, "2024-05-15", 9.0, "Tyson is the best!"),
            ("The Titan's Curse", "Book", "Young Adult Fantasy", "Rick Riordan", 2007, "2024-05-20", 9.0, "Bianca's death hit hard"),
            ("The Battle of the Labyrinth", "Book", "Young Adult Fantasy", "Rick Riordan", 2008, "2024-05-25", 9.5, "The labyrinth was so cool!"),
            ("The Last Olympian", "Book", "Young Adult Fantasy", "Rick Riordan", 2009, "2024-05-30", 10.0, "Epic finale!"),
        ])
        
        # MORE HUNGER GAMES (3 books)
        all_content.extend([
            ("The Hunger Games", "Book", "Dystopian Fiction", "Suzanne Collins", 2008, "2024-04-20", 10.0, "Started my dystopian obsession"),
            ("Catching Fire", "Book", "Dystopian Fiction", "Suzanne Collins", 2009, "2024-04-25", 10.0, "Quarter Quell was insane"),
            ("Mockingjay", "Book", "Dystopian Fiction", "Suzanne Collins", 2010, "2024-04-30", 9.5, "Dark but necessary ending"),
        ])
        
        # CASSANDRA CLARE - Shadowhunters (3 books)
        all_content.extend([
            ("City of Bones", "Book", "Young Adult Fantasy", "Cassandra Clare", 2007, "2024-08-10", 9.0, "Shadowhunters world is amazing"),
            ("City of Ashes", "Book", "Young Adult Fantasy", "Cassandra Clare", 2008, "2024-08-15", 8.5, "Jace and Clary drama!"),
            ("City of Glass", "Book", "Young Adult Fantasy", "Cassandra Clare", 2009, "2024-08-20", 9.0, "That plot twist!"),
        ])
        
        # SARAH J. MAAS (4 books)
        all_content.extend([
            ("Throne of Glass", "Book", "Young Adult Fantasy", "Sarah J. Maas", 2012, "2024-07-25", 9.0, "Celaena is a badass"),
            ("Crown of Midnight", "Book", "Young Adult Fantasy", "Sarah J. Maas", 2013, "2024-07-30", 9.5, "That ending reveal!"),
            ("A Court of Thorns and Roses", "Book", "Young Adult Fantasy", "Sarah J. Maas", 2015, "2024-07-10", 8.5, "BookTok was right, this slaps"),
            ("A Court of Mist and Fury", "Book", "Young Adult Fantasy", "Sarah J. Maas", 2016, "2024-07-18", 10.0, "RHYSAND. That's it. That's the tweet."),
        ])
        
        # MORE DYSTOPIAN (6 books)
        all_content.extend([
            ("Divergent", "Book", "Dystopian Fiction", "Veronica Roth", 2011, "2024-06-15", 8.5, "Classic dystopian vibes"),
            ("Insurgent", "Book", "Dystopian Fiction", "Veronica Roth", 2012, "2024-06-20", 8.0, "Intense sequel"),
            ("The Maze Runner", "Book", "Dystopian Fiction", "James Dashner", 2009, "2024-06-25", 8.0, "Fast-paced and intense"),
            ("Legend", "Book", "Dystopian Fiction", "Marie Lu", 2011, "2024-05-05", 8.5, "Underrated dystopian gem"),
            ("Matched", "Book", "Dystopian Fiction", "Ally Condie", 2010, "2024-04-10", 7.5, "Interesting premise"),
            ("Delirium", "Book", "Dystopian Fiction", "Lauren Oliver", 2011, "2024-04-15", 8.0, "Love as a disease concept is cool"),
        ])
        
        # MORE YA FANTASY/BOOKTOK (7 books)
        all_content.extend([
            ("Six of Crows", "Book", "Young Adult Fantasy", "Leigh Bardugo", 2015, "2024-08-15", 9.5, "Found family + heist! Amazing"),
            ("Crooked Kingdom", "Book", "Young Adult Fantasy", "Leigh Bardugo", 2016, "2024-08-18", 9.5, "Perfect sequel"),
            ("The Cruel Prince", "Book", "Young Adult Fantasy", "Holly Black", 2018, "2024-07-28", 9.0, "Enemies to lovers done RIGHT"),
            ("The Wicked King", "Book", "Young Adult Fantasy", "Holly Black", 2019, "2024-08-01", 9.5, "That cliffhanger!"),
            ("Shatter Me", "Book", "Young Adult Dystopian", "Tahereh Mafi", 2011, "2024-05-15", 8.0, "Unique writing style"),
            ("The Song of Achilles", "Book", "Young Adult Historical", "Madeline Miller", 2011, "2024-09-12", 10.0, "Cried for three hours straight"),
            ("Circe", "Book", "Young Adult Fantasy", "Madeline Miller", 2018, "2024-09-20", 9.5, "Madeline Miller does it again"),
        ])
        
        # YA CONTEMPORARY/ROMANCE (5 books)
        all_content.extend([
            ("The Fault in Our Stars", "Book", "Young Adult Contemporary", "John Green", 2012, "2024-08-05", 9.0, "Okay? Okay. 😭"),
            ("Eleanor & Park", "Book", "Young Adult Contemporary", "Rainbow Rowell", 2013, "2024-07-12", 8.5, "So sweet and realistic"),
            ("To All the Boys I've Loved Before", "Book", "Young Adult Romance", "Jenny Han", 2014, "2024-06-28", 8.5, "Cute and wholesome"),
            ("We Were Liars", "Book", "Young Adult Mystery", "E. Lockhart", 2014, "2024-08-05", 8.0, "Plot twist had me SHOOK"),
            ("One of Us Is Lying", "Book", "Young Adult Mystery", "Karen M. McManus", 2017, "2024-07-20", 8.5, "Could not put this down!"),
        ])
        
        # BOOK-TO-SCREEN ADAPTATIONS (7 entries)
        all_content.extend([
            ("The Hunger Games", "Movie", "Action/Dystopian", "Gary Ross", 2012, "2024-09-01", 9.5, "Jennifer Lawrence IS Katniss"),
            ("Harry Potter and the Sorcerer's Stone", "Movie", "Fantasy", "Chris Columbus", 2001, "2024-08-28", 9.0, "Magical on screen"),
            ("Percy Jackson & The Lightning Thief", "Movie", "Fantasy Adventure", "Chris Columbus", 2010, "2024-07-15", 6.5, "Not as good as the book tbh"),
            ("The Fault in Our Stars", "Movie", "Drama/Romance", "Josh Boone", 2014, "2024-08-15", 8.5, "Made me cry just as much"),
            ("Divergent", "Movie", "Action/Sci-Fi", "Neil Burger", 2014, "2024-07-22", 7.5, "Decent adaptation"),
            ("Shadow and Bone", "TV Show", "Fantasy", "Eric Heisserer", 2021, "2024-09-10", 8.5, "Loved the Grishaverse on screen!"),
            ("Bridgerton", "TV Show", "Period Drama", "Chris Van Dusen", 2020, "2024-08-20", 9.0, "Regency romance perfection"),
        ])
        
        # ROMCOM MOVIES (7 movies)
        all_content.extend([
            ("10 Things I Hate About You", "Movie", "Romantic Comedy", "Gil Junger", 1999, "2024-09-22", 9.5, "Iconic! Heath Ledger singing 💕"),
            ("To All the Boys I've Loved Before", "Movie", "Romantic Comedy", "Susan Johnson", 2018, "2024-08-28", 9.0, "So cute and wholesome"),
            ("Crazy Rich Asians", "Movie", "Romantic Comedy", "Jon M. Chu", 2018, "2024-07-15", 9.0, "Gorgeous and funny"),
            ("The Proposal", "Movie", "Romantic Comedy", "Anne Fletcher", 2009, "2024-06-18", 8.5, "Sandra Bullock and Ryan Reynolds!"),
            ("She's the Man", "Movie", "Romantic Comedy", "Andy Fickman", 2006, "2024-06-22", 9.0, "Amanda Bynes is hilarious"),
            ("How to Lose a Guy in 10 Days", "Movie", "Romantic Comedy", "Donald Petrie", 2003, "2024-06-10", 8.5, "Kate Hudson chemistry"),
            ("Set It Up", "Movie", "Romantic Comedy", "Claire Scanlon", 2018, "2024-07-05", 8.0, "Netflix romcom done right"),
        ])
        
        # ACTION & SUPERHERO MOVIES (7 movies)
        all_content.extend([
            ("Spider-Man: Into the Spider-Verse", "Movie", "Action/Superhero", "Bob Persichetti", 2018, "2024-09-08", 10.0, "Absolute masterpiece"),
            ("Black Panther", "Movie", "Action/Superhero", "Ryan Coogler", 2018, "2024-08-12", 9.5, "Stunning visually and emotionally"),
            ("The Dark Knight", "Movie", "Action/Superhero", "Christopher Nolan", 2008, "2024-07-25", 10.0, "Best superhero movie ever"),
            ("Avengers: Endgame", "Movie", "Action/Superhero", "Russo Brothers", 2019, "2024-07-01", 9.5, "I am Iron Man 😭"),
            ("Spider-Man: No Way Home", "Movie", "Action/Superhero", "Jon Watts", 2021, "2024-08-25", 9.5, "All three Spider-Men!"),
            ("Black Widow", "Movie", "Action/Superhero", "Cate Shortland", 2021, "2024-06-15", 8.0, "Natasha deserved this"),
            ("Doctor Strange", "Movie", "Action/Superhero", "Scott Derrickson", 2016, "2024-05-28", 8.5, "Visually stunning"),
        ])
        
        # MYSTERY/THRILLER MOVIES (4 movies)
        all_content.extend([
            ("Knives Out", "Movie", "Mystery", "Rian Johnson", 2019, "2024-09-15", 9.5, "So clever! Daniel Craig's accent tho"),
            ("Glass Onion", "Movie", "Mystery", "Rian Johnson", 2022, "2024-09-20", 9.0, "Another banger from Rian Johnson"),
            ("Gone Girl", "Movie", "Mystery/Thriller", "David Fincher", 2014, "2024-06-30", 9.0, "That twist though"),
            ("Shutter Island", "Movie", "Mystery/Thriller", "Martin Scorsese", 2010, "2024-07-18", 9.0, "Mind-bending"),
        ])
        
        # LOTS OF ANIME! (23 anime)
        all_content.extend([
            ("Demon Slayer", "Anime", "Action", "Ufotable", 2019, "2024-08-05", 9.0, "Stunning animation"),
            ("Your Lie in April", "Anime", "Drama", "A-1 Pictures", 2014, "2024-07-20", 9.5, "Emotionally powerful"),
            ("Attack on Titan", "Anime", "Action", "Wit Studio", 2013, "2024-08-28", 9.5, "Intense and gripping"),
            ("Violet Evergarden", "Anime", "Drama", "Kyoto Animation", 2018, "2024-07-12", 9.5, "Beautiful and sad"),
            ("Haikyuu!!", "Anime", "Sports", "Production I.G", 2014, "2024-06-30", 9.0, "So motivating and hype!"),
            ("My Hero Academia", "Anime", "Action", "Bones", 2016, "2024-06-20", 9.0, "Plus Ultra!"),
            ("Jujutsu Kaisen", "Anime", "Action", "MAPPA", 2020, "2024-08-22", 9.5, "Amazing fights and story"),
            ("Spy x Family", "Anime", "Comedy", "Wit Studio", 2022, "2024-09-05", 9.0, "Wholesome and hilarious"),
            ("Death Note", "Anime", "Mystery Thriller", "Madhouse", 2006, "2024-05-25", 9.5, "Mind games on another level"),
            ("Fullmetal Alchemist: Brotherhood", "Anime", "Action Adventure", "Bones", 2009, "2024-05-15", 10.0, "Perfect anime. No notes."),
            ("Steins;Gate", "Anime", "Sci-Fi Thriller", "White Fox", 2011, "2024-06-08", 9.5, "Time travel done perfectly"),
            ("Hunter x Hunter", "Anime", "Action Adventure", "Madhouse", 2011, "2024-05-20", 9.5, "Chimera Ant arc is peak fiction"),
            ("One Punch Man", "Anime", "Action Comedy", "Madhouse", 2015, "2024-07-02", 8.5, "Hilarious concept"),
            ("Mob Psycho 100", "Anime", "Action Comedy", "Bones", 2016, "2024-07-08", 9.0, "Unique art style and wholesome"),
            ("Naruto", "Anime", "Action Adventure", "Pierrot", 2002, "2024-04-25", 9.0, "Childhood classic"),
            ("Sword Art Online", "Anime", "Action Fantasy", "A-1 Pictures", 2012, "2024-05-10", 7.5, "Interesting premise"),
            ("Tokyo Ghoul", "Anime", "Dark Fantasy", "Pierrot", 2014, "2024-06-12", 8.0, "Dark and intense"),
            ("Fruits Basket", "Anime", "Drama Romance", "TMS Entertainment", 2019, "2024-08-18", 9.0, "Wholesome and emotional"),
            ("Kaguya-sama: Love Is War", "Anime", "Romantic Comedy", "A-1 Pictures", 2019, "2024-07-28", 8.5, "Hilarious rom-com"),
            ("Chainsaw Man", "Anime", "Action", "MAPPA", 2022, "2024-09-12", 8.5, "Chaotic and unique"),
            ("Horimiya", "Anime", "Romance", "CloverWorks", 2021, "2024-08-08", 8.5, "Cute high school romance"),
            ("A Silent Voice", "Movie", "Anime Drama", "Kyoto Animation", 2016, "2024-07-30", 10.0, "Cried the entire time. Beautiful."),
            ("Your Name", "Movie", "Anime Romance", "Makoto Shinkai", 2016, "2024-09-02", 9.5, "Visually stunning love story"),
            ("Weathering With You", "Movie", "Anime Romance", "Makoto Shinkai", 2019, "2024-09-08", 9.0, "Another Shinkai masterpiece"),
            ("Bleach", "Anime", "Action", "Pierrot", 2004, "2024-04-18", 8.5, "Classic shounen, Ichigo is cool"),
            ("One Piece", "Anime", "Action Adventure", "Toei Animation", 1999, "2024-04-05", 9.0, "Epic adventure, long but worth it"),
            ("Code Geass", "Anime", "Mecha", "Sunrise", 2006, "2024-05-08", 9.5, "Lelouch is such a complex character"),
            ("Cowboy Bebop", "Anime", "Sci-Fi", "Sunrise", 1998, "2024-05-18", 9.5, "Jazz + space cowboys = perfection"),
            ("Neon Genesis Evangelion", "Anime", "Mecha Psychological", "Gainax", 1995, "2024-06-03", 9.0, "Mindbending and deep"),
            ("Re:Zero", "Anime", "Fantasy", "White Fox", 2016, "2024-06-18", 9.0, "Time loop suffering, so good"),
            ("The Promised Neverland", "Anime", "Mystery Thriller", "CloverWorks", 2019, "2024-07-05", 9.0, "Season 1 was incredible"),
            ("Vinland Saga", "Anime", "Historical Action", "Wit Studio", 2019, "2024-07-15", 9.5, "Vikings and revenge, so epic"),
            ("Made in Abyss", "Anime", "Adventure Dark Fantasy", "Kinema Citrus", 2017, "2024-08-01", 9.0, "Looks cute, is traumatizing"),
            ("Mushoku Tensei", "Anime", "Fantasy", "Studio Bind", 2021, "2024-08-10", 8.5, "Beautiful animation, great isekai"),
            ("Bocchi the Rock!", "Anime", "Music Comedy", "CloverWorks", 2022, "2024-09-16", 8.5, "Relatable anxiety representation"),
            ("Blue Lock", "Anime", "Sports", "Eight Bit", 2022, "2024-09-22", 8.0, "Soccer but make it intense"),
            ("Buddy Daddies", "Anime", "Action Comedy", "P.A. Works", 2023, "2024-10-03", 8.5, "Hitmen dads raising a kid, wholesome"),
            ("Solo Leveling", "Anime", "Action Fantasy", "A-1 Pictures", 2024, "2024-10-12", 9.0, "Hype! Power fantasy done right"),
        ])
        
        # MORE COMFORT SHOWS (10 shows)
        all_content.extend([
            ("The Office", "TV Show", "Comedy", "Greg Daniels", 2005, "2024-10-08", 8.5, "Hilarious and comforting"),
            ("Stranger Things", "TV Show", "Sci-Fi", "The Duffer Brothers", 2016, "2024-09-30", 8.5, "Nostalgic fun"),
            ("Friends", "TV Show", "Sitcom", "David Crane", 1994, "2024-06-05", 8.5, "Classic comfort show"),
            ("Parks and Recreation", "TV Show", "Sitcom", "Greg Daniels", 2009, "2024-06-12", 9.0, "Leslie Knope is iconic"),
            ("The Good Place", "TV Show", "Comedy", "Michael Schur", 2016, "2024-07-22", 9.0, "Clever and wholesome"),
            ("Gilmore Girls", "TV Show", "Drama", "Amy Sherman-Palladino", 2000, "2024-05-22", 8.5, "Cozy fall vibes"),
            ("New Girl", "TV Show", "Sitcom", "Elizabeth Meriwether", 2011, "2024-06-28", 8.0, "Jess is so quirky and fun"),
            ("Schitt's Creek", "TV Show", "Sitcom", "Dan Levy", 2015, "2024-07-10", 9.0, "Character growth done perfectly"),
            ("The Umbrella Academy", "TV Show", "Sci-Fi/Action", "Steve Blackman", 2019, "2024-08-02", 8.5, "Dysfunctional superhero family"),
            ("Wednesday", "TV Show", "Mystery", "Alfred Gough", 2022, "2024-09-18", 8.0, "Jenna Ortega kills it"),
        ])
        
        # Add all content to database
        for content in all_content:
            self.add_content(*content)
        
        # Now add mood data for all entries (110 entries total)
        # Mood format: (content_id, mood_before, mood_after, emotional_tags)
        all_moods = [
            # Your favorites (1-6)
            (1, 6, 9, "interested,engaged,excited"),
            (2, 7, 10, "devastated,emotional,moved,crying"),
            (3, 5, 8, "calm,happy,content"),
            (4, 6, 8, "intrigued,curious,interested"),
            (5, 5, 7, "calm,relaxed,comforted"),
            (6, 4, 8, "calm,happy,laughing"),
            
            # Adam Silvera (7-10)
            (7, 6, 10, "sobbing,heartbroken,moved,beautiful"),
            (8, 7, 9, "excited,happy,found-family-feels"),
            (9, 6, 8, "cute,warm,emotional,happy"),
            (10, 6, 9, "mindblown,emotional,thoughtful"),
            
            # Harry Potter (11-17)
            (11, 7, 10, "magical,wonder,nostalgic"),
            (12, 6, 9, "excited,scared,engaged"),
            (13, 7, 10, "thrilled,emotional,perfect"),
            (14, 7, 9, "intense,engaged,excited"),
            (15, 6, 9, "angry,sad,engaged"),
            (16, 7, 9, "shocked,devastated,engaged"),
            (17, 8, 10, "crying,satisfied,nostalgic"),
            
            # Percy Jackson (18-22)
            (18, 6, 9, "excited,entertained,happy"),
            (19, 7, 9, "happy,engaged,excited"),
            (20, 6, 8, "sad,engaged,interested"),
            (21, 7, 9, "thrilled,scared,excited"),
            (22, 7, 10, "epic,satisfied,emotional"),
            
            # More Hunger Games (23-25)
            (23, 6, 10, "obsessed,engaged,shocked"),
            (24, 7, 10, "shocked,excited,mindblown"),
            (25, 7, 9, "dark,satisfied,emotional"),
            
            # Cassandra Clare (26-28)
            (26, 6, 9, "intrigued,excited,obsessed"),
            (27, 7, 8, "engaged,dramatic,interested"),
            (28, 7, 9, "shocked,thrilled,satisfied"),
            
            # Sarah J Maas (29-32)
            (29, 6, 9, "excited,badass-vibes,thrilled"),
            (30, 7, 10, "shocked,mindblown,obsessed"),
            (31, 6, 8, "interested,romantic,engaged"),
            (32, 7, 10, "obsessed,swooning,dying"),
            
            # More Dystopian (33-38)
            (33, 6, 8, "excited,engaged,thrilled"),
            (34, 6, 8, "intense,excited,nervous"),
            (35, 6, 8, "engaged,scared,excited"),
            (36, 6, 8, "interested,engaged,excited"),
            (37, 5, 7, "curious,calm,interested"),
            (38, 6, 8, "intrigued,thoughtful,engaged"),
            
            # More YA Fantasy (39-45)
            (39, 6, 9, "obsessed,excited,found-family"),
            (40, 7, 10, "thrilled,satisfied,emotional"),
            (41, 7, 9, "thrilled,obsessed,enemies-to-lovers"),
            (42, 7, 9, "shocked,thrilled,cliffhanger-pain"),
            (43, 6, 8, "unique,interested,engaged"),
            (44, 6, 10, "crying,devastated,moved"),
            (45, 7, 9, "amazed,thoughtful,inspired"),
            
            # YA Contemporary (46-50)
            (46, 5, 9, "crying,moved,sad"),
            (47, 6, 8, "warm,sweet,happy"),
            (48, 5, 8, "cute,happy,warm"),
            (49, 7, 9, "shocked,mindblown,intrigued"),
            (50, 6, 8, "engaged,curious,excited"),
            
            # Book adaptations (51-57)
            (51, 7, 9, "thrilled,satisfied,excited"),
            (52, 7, 9, "magical,nostalgic,happy"),
            (53, 7, 6, "disappointed,meh,nostalgic"),
            (54, 5, 8, "crying,sad,moved"),
            (55, 6, 7, "okay,decent,interested"),
            (56, 6, 8, "excited,thrilled,fantasy-vibes"),
            (57, 5, 9, "romantic,swooning,gorgeous"),
            
            # Romcoms (58-64)
            (58, 5, 9, "happy,swooning,laughing"),
            (59, 5, 8, "cute,happy,warm"),
            (60, 6, 9, "happy,inspired,warm"),
            (61, 5, 8, "laughing,happy,entertained"),
            (62, 5, 8, "laughing,happy,entertained"),
            (63, 5, 8, "romantic,happy,satisfied"),
            (64, 5, 7, "cute,happy,light"),
            
            # Action/Superhero (65-71)
            (65, 7, 10, "amazed,inspired,emotional"),
            (66, 6, 9, "inspired,moved,excited"),
            (67, 7, 10, "thrilled,mindblown,excited"),
            (68, 6, 10, "crying,epic,satisfied"),
            (69, 7, 10, "shocked,excited,nostalgic"),
            (70, 6, 8, "satisfied,empowered,happy"),
            (71, 6, 8, "amazed,trippy,entertained"),
            
            # Mystery (72-75)
            (72, 6, 9, "intrigued,clever,satisfied"),
            (73, 6, 8, "engaged,happy,clever"),
            (74, 7, 9, "shocked,mindblown,thrilled"),
            (75, 7, 9, "confused,mindblown,satisfied"),
            
            # Anime (76-98)
            (76, 6, 8, "excited,energized,happy"),
            (77, 5, 9, "moved,sad,cathartic"),
            (78, 6, 9, "shocked,engaged,thoughtful"),
            (79, 5, 8, "moved,sad,peaceful"),
            (80, 5, 9, "motivated,excited,hyped"),
            (81, 6, 9, "inspired,excited,plus-ultra"),
            (82, 7, 9, "thrilled,excited,amazed"),
            (83, 5, 8, "wholesome,happy,cute"),
            (84, 6, 9, "mindblown,engaged,thrilled"),
            (85, 7, 10, "perfect,satisfied,emotional"),
            (86, 6, 9, "confused,mindblown,amazed"),
            (87, 7, 10, "shocked,emotional,peak-fiction"),
            (88, 6, 8, "laughing,entertained,happy"),
            (89, 6, 9, "wholesome,happy,inspired"),
            (90, 5, 9, "nostalgic,excited,believe-it"),
            (91, 6, 7, "interested,okay,entertained"),
            (92, 6, 8, "dark,intense,engaged"),
            (93, 5, 9, "wholesome,crying,warm"),
            (94, 6, 8, "laughing,romantic,cute"),
            (95, 6, 8, "chaotic,excited,unique"),
            (96, 5, 8, "cute,wholesome,happy"),
            (97, 5, 10, "sobbing,beautiful,destroyed"),
            (98, 6, 9, "amazed,romantic,crying"),
            (99, 6, 9, "romantic,beautiful,crying"),
            (100, 5, 8, "nostalgic,epic,excited"),
            (101, 6, 9, "hyped,engaged,nostalgic"),
            (102, 6, 10, "mindblown,thrilled,complex"),
            (103, 7, 9, "cool,jazz-vibes,satisfied"),
            (104, 6, 9, "confused,deep,philosophical"),
            (105, 6, 9, "suffering,emotional,engaged"),
            (106, 7, 9, "shocked,thrilled,mindblown"),
            (107, 7, 10, "epic,emotional,inspired"),
            (108, 6, 9, "traumatized,amazed,shocked"),
            (109, 6, 8, "beautiful,calm,interested"),
            (110, 5, 8, "relatable,anxious,happy"),
            (111, 6, 8, "intense,hyped,engaged"),
            (112, 5, 8, "wholesome,cute,happy"),
            (113, 7, 9, "hyped,excited,badass"),
            
            # Shows (114-123)
            (114, 4, 7, "happy,relaxed,comforted"),
            (115, 6, 8, "nostalgic,entertained,happy"),
            (116, 5, 8, "laughing,comforted,happy"),
            (117, 5, 9, "inspired,happy,wholesome"),
            (118, 6, 9, "mindblown,philosophical,happy"),
            (119, 5, 8, "cozy,warm,comforted"),
            (120, 5, 7, "quirky,happy,entertained"),
            (121, 5, 9, "emotional,inspired,crying"),
            (122, 6, 8, "entertained,excited,engaged"),
            (123, 6, 8, "entertained,intrigued,happy"),
        ]
        
        # Add all mood logs
        for mood in all_moods:
            content_id, before, after, tags = mood
            # Get the date from the content
            self.connect()
            date = self.cursor.execute("SELECT date_consumed FROM content WHERE id=?", (content_id,)).fetchone()[0]
            self.close()
            self.add_mood_log(content_id, before, after, tags, date)

# Initialize database
if __name__ == "__main__":
    db = ContentDatabase()
    db.create_tables()
    print("✨ Database created successfully!")
    
    # Seed with sample data
    db.seed_sample_data()
    print(f"📚 Sample data added successfully! Total entries: 123")
    print("🎉 Your database is ready!")
    print("   📚 60+ Books (Harry Potter, Percy Jackson, Adam Silvera, YA, Dystopian)")
    print("   🎬 25+ Movies (Romcoms, Action, Superhero, Mystery)")
    print("   🎌 38 Anime (All the popular ones!)")
    print("   📺 10 TV Shows (Comfort shows)")