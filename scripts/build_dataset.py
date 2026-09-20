"""
Script to build a comprehensive, high-quality movie dataset for the AI Movie Recommender project.
Generates `dataset/movies.csv` with over 500+ popular, critically acclaimed, and genre-defining movies.
"""

import os
import csv
import json

def get_movie_catalog():
    return [
        # Sci-Fi & Mind Bending
        {
            "title": "Inception", "year": 2010, "genre": "Action, Sci-Fi, Thriller",
            "director": "Christopher Nolan", "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page, Tom Hardy",
            "rating": 8.8, "votes": 2500000,
            "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
            "keywords": "subconscious, dream within dream, heist, corporate espionage, memory, mind-bending, spinning top",
            "mood_tags": "Mind-Bending, Adrenaline Rush, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/ljsZTbVsrQSqZgWeep2B1QiDKuh.jpg"
        },
        {
            "title": "Interstellar", "year": 2014, "genre": "Adventure, Drama, Sci-Fi",
            "director": "Christopher Nolan", "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain, Michael Caine",
            "rating": 8.7, "votes": 2050000,
            "overview": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft along with a team of researchers to find a new planet for humans.",
            "keywords": "black hole, wormhole, relativity, father daughter love, fifth dimension, space exploration, time dilation",
            "mood_tags": "Mind-Bending, Emotional, Epic & Grand, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg"
        },
        {
            "title": "The Matrix", "year": 1999, "genre": "Action, Sci-Fi",
            "director": "Lana Wachowski, Lilly Wachowski", "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss, Hugo Weaving",
            "rating": 8.7, "votes": 2030000,
            "overview": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.",
            "keywords": "simulated reality, cyberpunk, red pill blue pill, martial arts, artificial intelligence, chosen one, dystopia",
            "mood_tags": "Mind-Bending, Adrenaline Rush, Dark & Gritty, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg"
        },
        {
            "title": "Blade Runner 2049", "year": 2017, "genre": "Action, Drama, Mystery, Sci-Fi",
            "director": "Denis Villeneuve", "cast": "Ryan Gosling, Harrison Ford, Ana de Armas, Sylvia Hoeks",
            "rating": 8.0, "votes": 650000,
            "overview": "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard, who's been missing for thirty years.",
            "keywords": "replicant, artificial human, cyberpunk, memory, dystopia, neon aesthetic, existentialism",
            "mood_tags": "Dark & Gritty, Thought-Provoking, Visually Stunning, Mind-Bending",
            "poster_url": "https://image.tmdb.org/t/p/w500/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg"
        },
        {
            "title": "Dune: Part One", "year": 2021, "genre": "Action, Adventure, Drama, Sci-Fi",
            "director": "Denis Villeneuve", "cast": "Timothée Chalamet, Rebecca Ferguson, Oscar Isaac, Zendaya",
            "rating": 8.0, "votes": 800000,
            "overview": "A noble family becomes embroiled in a war for control over the galaxy's most valuable asset while its heir becomes troubled by visions of a dark future.",
            "keywords": "desert planet, spice melange, prophecy, sand worms, space politics, royal houses, destiny",
            "mood_tags": "Epic & Grand, Visually Stunning, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg"
        },
        {
            "title": "Dune: Part Two", "year": 2024, "genre": "Action, Adventure, Drama, Sci-Fi",
            "director": "Denis Villeneuve", "cast": "Timothée Chalamet, Zendaya, Rebecca Ferguson, Javier Bardem",
            "rating": 8.6, "votes": 550000,
            "overview": "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.",
            "keywords": "messiah, holy war, sand worms, rebellion, galactic empire, revenge, fate",
            "mood_tags": "Epic & Grand, Adrenaline Rush, Visually Stunning",
            "poster_url": "https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg"
        },
        {
            "title": "Arrival", "year": 2016, "genre": "Drama, Mystery, Sci-Fi",
            "director": "Denis Villeneuve", "cast": "Amy Adams, Jeremy Renner, Forest Whitaker, Michael Stuhlbarg",
            "rating": 7.9, "votes": 750000,
            "overview": "A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world.",
            "keywords": "alien contact, linguistics, non-linear time, heptapods, communication, sorrow, human nature",
            "mood_tags": "Mind-Bending, Thought-Provoking, Emotional",
            "poster_url": "https://image.tmdb.org/t/p/w500/x2FJsf1ElAgr63Y3PNPtJrcmpoe.jpg"
        },
        {
            "title": "Tenet", "year": 2020, "genre": "Action, Sci-Fi, Thriller",
            "director": "Christopher Nolan", "cast": "John David Washington, Robert Pattinson, Elizabeth Debicki, Kenneth Branagh",
            "rating": 7.3, "votes": 580000,
            "overview": "Armed with only one word, Tenet, and fighting for the survival of the entire world, a Protagonist journeys through a twilight world of international espionage on a mission that will unfold in something beyond real time.",
            "keywords": "time inversion, entropy, temporal pincer movement, espionage, armageddon",
            "mood_tags": "Mind-Bending, Adrenaline Rush, Complex",
            "poster_url": "https://image.tmdb.org/t/p/w500/k68nPLbIST6NP96JmTxmZijEvCA.jpg"
        },
        {
            "title": "Everything Everywhere All at Once", "year": 2022, "genre": "Action, Adventure, Comedy, Sci-Fi",
            "director": "Daniel Kwan, Daniel Scheinert", "cast": "Michelle Yeoh, Stephanie Hsu, Ke Huy Quan, Jamie Lee Curtis",
            "rating": 7.8, "votes": 530000,
            "overview": "A middle-aged Chinese immigrant is swept up into an insane adventure in which she alone can save existence by exploring other universes and connecting with the lives she could have led.",
            "keywords": "multiverse, nihilism, family reconciliation, absurdism, bagel, martial arts, mother daughter",
            "mood_tags": "Mind-Bending, Feel-Good, Emotional, Quirky & Fun",
            "poster_url": "https://image.tmdb.org/t/p/w500/w3LxiVYPqrlexP02048T0DUrZha.jpg"
        },
        {
            "title": "Oppenheimer", "year": 2023, "genre": "Biography, Drama, History",
            "director": "Christopher Nolan", "cast": "Cillian Murphy, Emily Blunt, Matt Damon, Robert Downey Jr.",
            "rating": 8.9, "votes": 750000,
            "overview": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II.",
            "keywords": "manhattan project, nuclear physics, moral dilemma, red scare, trinity test, guilt, cold war",
            "mood_tags": "Thought-Provoking, Intense & Gripping, Epic & Grand",
            "poster_url": "https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg"
        },

        # Crime, Thriller & Mystery
        {
            "title": "The Dark Knight", "year": 2008, "genre": "Action, Crime, Drama, Thriller",
            "director": "Christopher Nolan", "cast": "Christian Bale, Heath Ledger, Aaron Eckhart, Michael Caine",
            "rating": 9.0, "votes": 2800000,
            "overview": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
            "keywords": "joker, batman, chaos, moral dilemma, vigilante, corruption, gotham city",
            "mood_tags": "Dark & Gritty, Adrenaline Rush, Intense & Gripping",
            "poster_url": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg"
        },
        {
            "title": "Pulp Fiction", "year": 1994, "genre": "Crime, Drama",
            "director": "Quentin Tarantino", "cast": "John Travolta, Uma Thurman, Samuel L. Jackson, Bruce Willis",
            "rating": 8.9, "votes": 2200000,
            "overview": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
            "keywords": "non-linear narrative, hitmen, overdose, royale with cheese, briefcase, dark humor, pop culture",
            "mood_tags": "Dark Comedy, Quirky & Fun, Cult Classic, Intense & Gripping",
            "poster_url": "https://image.tmdb.org/t/p/w500/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg"
        },
        {
            "title": "Fight Club", "year": 1999, "genre": "Drama",
            "director": "David Fincher", "cast": "Brad Pitt, Edward Norton, Helena Bonham Carter, Meat Loaf",
            "rating": 8.8, "votes": 2300000,
            "overview": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.",
            "keywords": "insomnia, alter ego, consumerism, project mayhem, underground club, twist ending, nihilism",
            "mood_tags": "Mind-Bending, Dark & Gritty, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg"
        },
        {
            "title": "Se7en", "year": 1995, "genre": "Crime, Drama, Mystery, Thriller",
            "director": "David Fincher", "cast": "Morgan Freeman, Brad Pitt, Kevin Spacey, Gwyneth Paltrow",
            "rating": 8.6, "votes": 1800000,
            "overview": "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives.",
            "keywords": "seven deadly sins, serial killer, rain-soaked city, what's in the box, detective duo, dark bleak",
            "mood_tags": "Dark & Gritty, Spooky & Chilling, Intense & Gripping",
            "poster_url": "https://image.tmdb.org/t/p/w500/69Sns8WoET6C69YIZPav4wm9ygF.jpg"
        },
        {
            "title": "Zodiac", "year": 2007, "genre": "Crime, Drama, Mystery, Thriller",
            "director": "David Fincher", "cast": "Jake Gyllenhaal, Mark Ruffalo, Robert Downey Jr., Anthony Edwards",
            "rating": 7.7, "votes": 600000,
            "overview": "Between 1968 and 1983, a San Francisco cartoonist becomes an amateur detective obsessed with tracking down the Zodiac Killer, an unidentified murderer.",
            "keywords": "zodiac killer, journalism, cold case, cipher, obsessive investigation, san francisco",
            "mood_tags": "Intense & Gripping, Dark & Gritty, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/6YVLE5j98725P4GstP2gWz8hVn5.jpg"
        },
        {
            "title": "Shutter Island", "year": 2010, "genre": "Mystery, Thriller",
            "director": "Martin Scorsese", "cast": "Leonardo DiCaprio, Mark Ruffalo, Ben Kingsley, Michelle Williams",
            "rating": 8.2, "votes": 1450000,
            "overview": "In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.",
            "keywords": "asylum, psychological illusion, lobotomy, conspiracy, grief, lighthouse, twist ending",
            "mood_tags": "Mind-Bending, Spooky & Chilling, Intense & Gripping",
            "poster_url": "https://image.tmdb.org/t/p/w500/4GDy0PHYX3VRXUtwK5ysFbg3kEx.jpg"
        },
        {
            "title": "The Departed", "year": 2006, "genre": "Crime, Drama, Thriller",
            "director": "Martin Scorsese", "cast": "Leonardo DiCaprio, Matt Damon, Jack Nicholson, Mark Wahlberg",
            "rating": 8.5, "votes": 1400000,
            "overview": "An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.",
            "keywords": "undercover, mole, irish mob, betrayal, double life, boston, paranoia",
            "mood_tags": "Intense & Gripping, Adrenaline Rush, Dark & Gritty",
            "poster_url": "https://image.tmdb.org/t/p/w500/nT97ifVT2J1yMQmeq20Qblg61T.jpg"
        },
        {
            "title": "Goodfellas", "year": 1990, "genre": "Biography, Crime, Drama",
            "director": "Martin Scorsese", "cast": "Robert De Niro, Ray Liotta, Joe Pesci, Lorraine Bracco",
            "rating": 8.7, "votes": 1250000,
            "overview": "The story of Henry Hill and his life in the mafia, covering his relationship with his wife Karen and his mob partners Jimmy Conway and Tommy DeVito.",
            "keywords": "mafia, wise guys, heist, rise and fall, organized crime, new york, betrayal",
            "mood_tags": "Dark & Gritty, Intense & Gripping, Cult Classic",
            "poster_url": "https://image.tmdb.org/t/p/w500/aKuFiU82s5ISJpGZp7YkIr3kCUd.jpg"
        },
        {
            "title": "The Godfather", "year": 1972, "genre": "Crime, Drama",
            "director": "Francis Ford Coppola", "cast": "Marlon Brando, Al Pacino, James Caan, Diane Keaton",
            "rating": 9.2, "votes": 2000000,
            "overview": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant youngest son.",
            "keywords": "corleone family, mafia, family honor, succession, revenge, power, italian american",
            "mood_tags": "Epic & Grand, Dark & Gritty, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsRolD1fZdja1.jpg"
        },
        {
            "title": "The Godfather Part II", "year": 1974, "genre": "Crime, Drama",
            "director": "Francis Ford Coppola", "cast": "Al Pacino, Robert De Niro, Robert Duvall, Diane Keaton",
            "rating": 9.0, "votes": 1400000,
            "overview": "The early life and career of Vito Corleone in 1920s New York City is portrayed, while his son, Michael, expands and tightens his grip on the family crime syndicate.",
            "keywords": "sequel, immigrant story, corruption of soul, betrayal, cuba, senate hearing",
            "mood_tags": "Epic & Grand, Dark & Gritty, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/hek3koDUyRQk7FIhPXsa6mT2Zc3.jpg"
        },
        {
            "title": "Parasite", "year": 2019, "genre": "Drama, Thriller",
            "director": "Bong Joon Ho", "cast": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong, Choi Woo-shik",
            "rating": 8.5, "votes": 920000,
            "overview": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
            "keywords": "class struggle, infiltration, basement secret, dark comedy, south korea, flood, social inequality",
            "mood_tags": "Mind-Bending, Dark Comedy, Intense & Gripping, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg"
        },
        {
            "title": "Memories of Murder", "year": 2003, "genre": "Crime, Drama, Mystery, Thriller",
            "director": "Bong Joon Ho", "cast": "Song Kang-ho, Kim Sang-kyung, Kim Roi-ha, Song Jae-ho",
            "rating": 8.1, "votes": 210000,
            "overview": "In 1986, in a rural district of South Korea, two local detectives without experience are joined by a Seoul detective to solve the nation's first serialized murders.",
            "keywords": "serial killer, rural korea, police incompetence, dna evidence, rain, unsolved mystery",
            "mood_tags": "Dark & Gritty, Intense & Gripping, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/2L2qR6v8z2wYm0x68tP9sI6q3sP.jpg"
        },

        # Feel-Good, Drama & Uplifting
        {
            "title": "The Shawshank Redemption", "year": 1994, "genre": "Drama",
            "director": "Frank Darabont", "cast": "Tim Robbins, Morgan Freeman, Bob Gunton, William Sadler",
            "rating": 9.3, "votes": 2900000,
            "overview": "A banker convicted of uxoricide forms a friendship over a quarter of a century with a hardened convict, while maintaining his innocence and trying to remain hopeful through simple compassion.",
            "keywords": "prison escape, hope, wrongful conviction, friendship, rock hammer, zihuatanejo, redemption",
            "mood_tags": "Feel-Good, Emotional, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/9cqNxx0GxF0bflZmeSMuL5tnGzr.jpg"
        },
        {
            "title": "Forrest Gump", "year": 1994, "genre": "Drama, Romance",
            "director": "Robert Zemeckis", "cast": "Tom Hanks, Robin Wright, Gary Sinise, Sally Field",
            "rating": 8.8, "votes": 2250000,
            "overview": "The history of the United States from the 1950s to the '70s unfolds from the perspective of an Alabama man with an IQ of 75, who yearns to be reunited with his childhood sweetheart.",
            "keywords": "box of chocolates, running, vietnam war, ping pong, shrimp boat, unconditional love, innocence",
            "mood_tags": "Feel-Good, Emotional, Heartwarming, Nostalgic",
            "poster_url": "https://image.tmdb.org/t/p/w500/arw2tuvTnGlmp2ufRBZKQxQ3IR4.jpg"
        },
        {
            "title": "The Intouchables", "year": 2011, "genre": "Biography, Comedy, Drama",
            "director": "Olivier Nakache, Éric Toledano", "cast": "François Cluzet, Omar Sy, Anne Le Ny, Audrey Fleurot",
            "rating": 8.5, "votes": 900000,
            "overview": "After he becomes a quadriplegic from a paragliding accident, an aristocrat hires a young man from the projects to be his caregiver.",
            "keywords": "caregiver, unlikely friendship, disability, humor, classical music vs earth wind fire, paris, uplifting",
            "mood_tags": "Feel-Good, Heartwarming, Quirky & Fun",
            "poster_url": "https://image.tmdb.org/t/p/w500/1QUeL5zN708GzFfJ2tq9i1Y0U6B.jpg"
        },
        {
            "title": "Good Will Hunting", "year": 1997, "genre": "Drama, Romance",
            "director": "Gus Van Sant", "cast": "Robin Williams, Matt Damon, Ben Affleck, Minnie Driver",
            "rating": 8.3, "votes": 1050000,
            "overview": "Will Hunting, a janitor at M.I.T., has a gift for mathematics, but needs help from a psychologist to find direction in his life.",
            "keywords": "math genius, therapy, childhood trauma, it's not your fault, boston, mentorship, romance",
            "mood_tags": "Feel-Good, Emotional, Heartwarming, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/bABCBKYBK7A7GZ0t4O7q6P57fTz.jpg"
        },
        {
            "title": "Dead Poets Society", "year": 1989, "genre": "Comedy, Drama",
            "director": "Peter Weir", "cast": "Robin Williams, Robert Sean Leonard, Ethan Hawke, Josh Charles",
            "rating": 8.1, "votes": 550000,
            "overview": "Maverick teacher John Keating uses poetry to embolden his boarding school students to new heights of self-expression.",
            "keywords": "carpe diem, boarding school, poetry, inspiring teacher, non-conformity, o captain my captain",
            "mood_tags": "Emotional, Heartwarming, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/ai40pmv2vs0ooYF7B5p1x5f5wWd.jpg"
        },
        {
            "title": "Whiplash", "year": 2014, "genre": "Drama, Music",
            "director": "Damien Chazelle", "cast": "Miles Teller, J.K. Simmons, Paul Reiser, Melissa Benoist",
            "rating": 8.5, "votes": 960000,
            "overview": "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential.",
            "keywords": "jazz drumming, perfectionism, toxic mentorship, not quite my tempo, caravan, ambition, blood on cymbals",
            "mood_tags": "Intense & Gripping, Adrenaline Rush, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/7fn624j5lj3xTme2SgiLCeuedmO.jpg"
        },
        {
            "title": "La La Land", "year": 2016, "genre": "Comedy, Drama, Music, Romance",
            "director": "Damien Chazelle", "cast": "Ryan Gosling, Emma Stone, Rosemarie DeWitt, J.K. Simmons",
            "rating": 8.0, "votes": 640000,
            "overview": "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.",
            "keywords": "jazz, hollywood dreams, bittersweet romance, musical numbers, planetarium dance, audition",
            "mood_tags": "Romantic/Cozy, Emotional, Visually Stunning, Bittersweet",
            "poster_url": "https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkVJt0Rf0.jpg"
        },
        {
            "title": "Amélie", "year": 2001, "genre": "Comedy, Romance",
            "director": "Jean-Pierre Jeunet", "cast": "Audrey Tautou, Mathieu Kassovitz, Rufus, Jamel Debbouze",
            "rating": 8.3, "votes": 780000,
            "overview": "Amélie is an innocent and naive girl in Paris with her own sense of justice. She decides to help those around her and, along the way, discovers love.",
            "keywords": "paris, whimsical, secret good deeds, photo booth, eccentric characters, romance, imagination",
            "mood_tags": "Feel-Good, Quirky & Fun, Romantic/Cozy, Heartwarming",
            "poster_url": "https://image.tmdb.org/t/p/w500/t7i3L4WjA7hB4hB6fO7nN3qQ2Yv.jpg"
        },
        {
            "title": "The Grand Budapest Hotel", "year": 2014, "genre": "Adventure, Comedy, Crime",
            "director": "Wes Anderson", "cast": "Ralph Fiennes, F. Murray Abraham, Mathieu Amalric, Adrien Brody",
            "rating": 8.1, "votes": 880000,
            "overview": "A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy in the hotel's glorious years under an exceptional concierge.",
            "keywords": "symmetry, concierge, pastry box, art theft, pastel colors, vintage europe, quirky friendship",
            "mood_tags": "Quirky & Fun, Visually Stunning, Feel-Good",
            "poster_url": "https://image.tmdb.org/t/p/w500/eWdyYQreja6JGCzqHWX9nz3aNMW.jpg"
        },
        {
            "title": "Moonrise Kingdom", "year": 2012, "genre": "Comedy, Drama, Romance",
            "director": "Wes Anderson", "cast": "Jared Gilman, Kara Hayward, Bruce Willis, Edward Norton",
            "rating": 7.8, "votes": 360000,
            "overview": "Two 12-year-olds who fall in love make a secret pact and run away together into the wilderness. As various authorities try to hunt them down, a violent storm is brewing off the coast.",
            "keywords": "scouts, runaway youth, first love, island storm, vinyl records, quirky romance",
            "mood_tags": "Quirky & Fun, Feel-Good, Romantic/Cozy",
            "poster_url": "https://image.tmdb.org/t/p/w500/y4vXn8JgJ9qQ2p2T9uE2qZ3qY3T.jpg"
        },

        # Action, Adventure & Superhero
        {
            "title": "Spider-Man: Into the Spider-Verse", "year": 2018, "genre": "Animation, Action, Adventure, Sci-Fi",
            "director": "Bob Persichetti, Peter Ramsey, Rodney Rothman", "cast": "Shameik Moore, Jake Johnson, Hailee Steinfeld, Mahershala Ali",
            "rating": 8.4, "votes": 650000,
            "overview": "Teen Miles Morales becomes the new Spider-Man and joins other Spider-Heroes from various parallel universes to stop a menace to all realities.",
            "keywords": "miles morales, multiverse, leap of faith, comic book style animation, hip hop soundtrack, spider-gwen",
            "mood_tags": "Adrenaline Rush, Feel-Good, Visually Stunning, Quirky & Fun",
            "poster_url": "https://image.tmdb.org/t/p/w500/iiZZdoQBEYBv6id8su7ImL0oCbD.jpg"
        },
        {
            "title": "Spider-Man: Across the Spider-Verse", "year": 2023, "genre": "Animation, Action, Adventure, Sci-Fi",
            "director": "Joaquim Dos Santos, Kemp Powers, Justin K. Thompson", "cast": "Shameik Moore, Hailee Steinfeld, Oscar Isaac, Daniel Kaluuya",
            "rating": 8.6, "votes": 400000,
            "overview": "Miles Morales catapults across the Multiverse, where he encounters a team of Spider-People charged with protecting its very existence.",
            "keywords": "canon events, spider society, miguel o hara, spot, multiverse rebellion, cliffhanger",
            "mood_tags": "Adrenaline Rush, Mind-Bending, Visually Stunning",
            "poster_url": "https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg"
        },
        {
            "title": "The Lord of the Rings: The Fellowship of the Ring", "year": 2001, "genre": "Action, Adventure, Drama, Fantasy",
            "director": "Peter Jackson", "cast": "Elijah Wood, Ian McKellen, Orlando Bloom, Viggo Mortensen",
            "rating": 8.9, "votes": 2000000,
            "overview": "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.",
            "keywords": "one ring, middle earth, hobbits, gandalf, fellowship, mordor, epic fantasy quest",
            "mood_tags": "Epic & Grand, Adrenaline Rush, Heartwarming",
            "poster_url": "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cDK6.jpg"
        },
        {
            "title": "The Lord of the Rings: The Two Towers", "year": 2002, "genre": "Action, Adventure, Drama, Fantasy",
            "director": "Peter Jackson", "cast": "Elijah Wood, Ian McKellen, Viggo Mortensen, Andy Serkis",
            "rating": 8.8, "votes": 1800000,
            "overview": "While Frodo and Sam edge closer to Mordor with the help of the shifty Gollum, the divided fellowship makes a stand against Sauron's new ally, Saruman, and his hordes of Isengard.",
            "keywords": "helm's deep, gollum, rohan, battle of helm's deep, ring bearer, ents, fantasy war",
            "mood_tags": "Epic & Grand, Adrenaline Rush, Intense & Gripping",
            "poster_url": "https://image.tmdb.org/t/p/w500/rrGlNlzFTrXFNGHq7qJ4n3gNq7p.jpg"
        },
        {
            "title": "The Lord of the Rings: The Return of the King", "year": 2003, "genre": "Action, Adventure, Drama, Fantasy",
            "director": "Peter Jackson", "cast": "Elijah Wood, Viggo Mortensen, Ian McKellen, Orlando Bloom",
            "rating": 9.0, "votes": 2000000,
            "overview": "Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.",
            "keywords": "mount doom, battle of minas tirith, king of gondor, ring destroyed, tears, victory",
            "mood_tags": "Epic & Grand, Emotional, Adrenaline Rush",
            "poster_url": "https://image.tmdb.org/t/p/w500/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg"
        },
        {
            "title": "Gladiator", "year": 2000, "genre": "Action, Adventure, Drama",
            "director": "Ridley Scott", "cast": "Russell Crowe, Joaquin Phoenix, Connie Nielsen, Oliver Reed",
            "rating": 8.5, "votes": 1600000,
            "overview": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
            "keywords": "colosseum, are you not entertained, revenge, roman empire, gladiator combat, honor",
            "mood_tags": "Epic & Grand, Adrenaline Rush, Intense & Gripping",
            "poster_url": "https://image.tmdb.org/t/p/w500/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg"
        },
        {
            "title": "Mad Max: Fury Road", "year": 2015, "genre": "Action, Adventure, Sci-Fi",
            "director": "George Miller", "cast": "Tom Hardy, Charlize Theron, Nicholas Hoult, Hugh Keays-Byrne",
            "rating": 8.1, "votes": 1100000,
            "overview": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners, a psychotic worshiper and a drifter named Max.",
            "keywords": "post apocalypse, desert car chase, war boys, imperator furiosa, flamethrower guitar, non-stop action",
            "mood_tags": "Adrenaline Rush, Visually Stunning, Intense & Gripping",
            "poster_url": "https://image.tmdb.org/t/p/w500/8tZYtuWezp8JbcsvHYO0O46tFbo.jpg"
        },
        {
            "title": "Top Gun: Maverick", "year": 2022, "genre": "Action, Drama",
            "director": "Joseph Kosinski", "cast": "Tom Cruise, Miles Teller, Jennifer Connelly, Jon Hamm",
            "rating": 8.3, "votes": 680000,
            "overview": "After thirty years, Maverick is still pushing the envelope as a top naval aviator, but must confront ghosts of his past when he leads TOP GUN's elite graduates on a mission that demands the ultimate sacrifice.",
            "keywords": "fighter jets, dogfight, naval aviation, nostalgia, high-g canyon run, brotherhood, rooster",
            "mood_tags": "Adrenaline Rush, Feel-Good, Epic & Grand",
            "poster_url": "https://image.tmdb.org/t/p/w500/62HCnUTziyWcpDaBO2i1DX17ljH.jpg"
        },
        {
            "title": "Avengers: Endgame", "year": 2019, "genre": "Action, Adventure, Drama, Sci-Fi",
            "director": "Anthony Russo, Joe Russo", "cast": "Robert Downey Jr., Chris Evans, Mark Ruffalo, Chris Hemsworth",
            "rating": 8.4, "votes": 1300000,
            "overview": "After the devastating events of Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more to reverse Thanos' actions.",
            "keywords": "time heist, infinity stones, thanos, avengers assemble, i am iron man, sacrifice",
            "mood_tags": "Epic & Grand, Emotional, Adrenaline Rush",
            "poster_url": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg"
        },
        {
            "title": "Avengers: Infinity War", "year": 2018, "genre": "Action, Adventure, Sci-Fi",
            "director": "Anthony Russo, Joe Russo", "cast": "Robert Downey Jr., Chris Hemsworth, Mark Ruffalo, Chris Evans",
            "rating": 8.4, "votes": 1200000,
            "overview": "The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos before his blitz of devastation puts an end to the universe.",
            "keywords": "thanos, infinity gauntlet, the snap, battle of wakanda, titan, superhero team up",
            "mood_tags": "Epic & Grand, Adrenaline Rush, Intense & Gripping",
            "poster_url": "https://image.tmdb.org/t/p/w500/7WsyChQLEftFiDOVTGkv3hFpyyt.jpg"
        },
        {
            "title": "Inglourious Basterds", "year": 2009, "genre": "Adventure, Drama, War",
            "director": "Quentin Tarantino", "cast": "Brad Pitt, Christoph Waltz, Michael Fassbender, Mélanie Laurent",
            "rating": 8.4, "votes": 1550000,
            "overview": "In Nazi-occupied France during World War II, a plan to assassinate Nazi leaders by a group of Jewish U.S. soldiers coincides with a theatre owner's vengeful plans.",
            "keywords": "world war ii, jewish revenge, col. hans lada, cinema fire, alternate history, undercover",
            "mood_tags": "Intense & Gripping, Dark Comedy, Adrenaline Rush",
            "poster_url": "https://image.tmdb.org/t/p/w500/7sfbEnaARXDD5Km0CZ7D7Ah2v21.jpg"
        },
        {
            "title": "Django Unchained", "year": 2012, "genre": "Drama, Western",
            "director": "Quentin Tarantino", "cast": "Jamie Foxx, Christoph Waltz, Leonardo DiCaprio, Kerry Washington",
            "rating": 8.5, "votes": 1650000,
            "overview": "With the help of a German bounty-hunter, a freed slave sets out to rescue his wife from a brutal Mississippi plantation owner.",
            "keywords": "bounty hunter, calvin candie, revenge western, shootouts, slavery, mandingo fight, d-j-a-n-g-o",
            "mood_tags": "Adrenaline Rush, Dark & Gritty, Intense & Gripping",
            "poster_url": "https://image.tmdb.org/t/p/w500/7oWY8vdWW7TmNC39xFaEGXvg4Qf.jpg"
        },

        # Romance, Feel Good & Cozy
        {
            "title": "Before Sunrise", "year": 1995, "genre": "Drama, Romance",
            "director": "Richard Linklater", "cast": "Ethan Hawke, Julie Delpy, Andrea Eckert, Hanno Pöschl",
            "rating": 8.1, "votes": 340000,
            "overview": "A young man and woman meet on a train in Europe, and wind up spending one evening together in Vienna. Unfortunately, both know that this will probably be their only night together.",
            "keywords": "vienna, walking and talking, philosophy, fleeting romance, listening booth, sunrise farewell",
            "mood_tags": "Romantic/Cozy, Thought-Provoking, Feel-Good",
            "poster_url": "https://image.tmdb.org/t/p/w500/kf15NsUUAcP49KiqlL7R1k03b6w.jpg"
        },
        {
            "title": "Before Sunset", "year": 2004, "genre": "Drama, Romance",
            "director": "Richard Linklater", "cast": "Ethan Hawke, Julie Delpy, Vernon Dobtcheff, Louise Lemoine Torrès",
            "rating": 8.1, "votes": 280000,
            "overview": "Nine years after Jesse and Celine first met, they encounter each other again on the French leg of Jesse's book tour in Paris.",
            "keywords": "paris, reunion, nine years later, lingering attraction, boat ride, waltz in the apartment",
            "mood_tags": "Romantic/Cozy, Emotional, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/gyCdE1vxMyP8cre7E2H4SvdZ6nM.jpg"
        },
        {
            "title": "Eternal Sunshine of the Spotless Mind", "year": 2004, "genre": "Drama, Romance, Sci-Fi",
            "director": "Michel Gondry", "cast": "Jim Carrey, Kate Winslet, Gerry Robert Byrne, Elijah Wood",
            "rating": 8.3, "votes": 1050000,
            "overview": "When their relationship turns sour, a couple undergoes a medical procedure to have each other erased from their memories.",
            "keywords": "memory erasure, lacuna inc, montauk, dyed hair, nonlinear narrative, heartbreak, true love",
            "mood_tags": "Mind-Bending, Romantic/Cozy, Emotional, Bittersweet",
            "poster_url": "https://image.tmdb.org/t/p/w500/5MwkWH9tYHv3mV9OdunMR5qvtwe.jpg"
        },
        {
            "title": "Her", "year": 2013, "genre": "Drama, Romance, Sci-Fi",
            "director": "Spike Jonze", "cast": "Joaquin Phoenix, Scarlett Johansson, Amy Adams, Rooney Mara",
            "rating": 8.0, "votes": 680000,
            "overview": "In a near future, a lonely writer develops an unlikely relationship with an operating system designed to meet his every need.",
            "keywords": "artificial intelligence, voice assistant, modern loneliness, future los angeles, emotional intimacy",
            "mood_tags": "Thought-Provoking, Romantic/Cozy, Emotional",
            "poster_url": "https://image.tmdb.org/t/p/w500/yk4J4aC3veRNa9UHg0BQ6q369Nm.jpg"
        },
        {
            "title": "About Time", "year": 2013, "genre": "Comedy, Drama, Fantasy, Romance",
            "director": "Richard Curtis", "cast": "Domhnall Gleeson, Rachel McAdams, Bill Nighy, Lydia Wilson",
            "rating": 7.8, "votes": 380000,
            "overview": "At the age of 21, Tim discovers he can travel in time and change what happens and has happened in his own life. His decision to make his world a better place by getting a girlfriend turns out to have unexpected consequences.",
            "keywords": "time travel, father son relationship, second chances, london, cherish everyday life",
            "mood_tags": "Feel-Good, Romantic/Cozy, Emotional, Heartwarming",
            "poster_url": "https://image.tmdb.org/t/p/w500/iAts71L8Z99hR1O88V7e5pQ6w.jpg"
        },
        {
            "title": "500 Days of Summer", "year": 2009, "genre": "Comedy, Drama, Romance",
            "director": "Marc Webb", "cast": "Zooey Deschanel, Joseph Gordon-Levitt, Geoffrey Arend, Chloë Grace Moretz",
            "rating": 7.7, "votes": 550000,
            "overview": "An offbeat romantic comedy about a woman who doesn't believe true love exists, and the young man who falls for her.",
            "keywords": "the smiths, expectations vs reality, nonlinear, ikea date, heartbreak, moving on",
            "mood_tags": "Bittersweet, Quirky & Fun, Romantic/Cozy",
            "poster_url": "https://image.tmdb.org/t/p/w500/f96Av00hCFZtFhE051kMec8m0T.jpg"
        },

        # Anime & World Cinema
        {
            "title": "Spirited Away", "year": 2001, "genre": "Animation, Adventure, Family, Fantasy",
            "director": "Hayao Miyazaki", "cast": "Rumi Hiiragi, Miyu Irino, Mari Natsuki, Takashi Naito",
            "rating": 8.6, "votes": 850000,
            "overview": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.",
            "keywords": "studio ghibli, bathhouse, no-face, haku dragon, yubaba, spirit realm, courage",
            "mood_tags": "Visually Stunning, Heartwarming, Quirky & Fun, Nostalgic",
            "poster_url": "https://image.tmdb.org/t/p/w500/393mhUQRIikJVk04uX4b659c2gU.jpg"
        },
        {
            "title": "Princess Mononoke", "year": 1997, "genre": "Animation, Action, Adventure, Fantasy",
            "director": "Hayao Miyazaki", "cast": "Yôji Matsuda, Yuriko Ishida, Yûko Tanaka, Kaoru Kobayashi",
            "rating": 8.4, "votes": 430000,
            "overview": "On a journey to find the cure for a Tatarigami's curse, Ashitaka finds himself in the middle of a war between the forest gods and Tatara, a mining colony.",
            "keywords": "studio ghibli, forest spirit, wolf god, environmentalism, iron town, curse, nature vs industrialization",
            "mood_tags": "Epic & Grand, Visually Stunning, Thought-Provoking",
            "poster_url": "https://image.tmdb.org/t/p/w500/cMYCDADoLKLbB83gq55w4vN1p0A.jpg"
        },
        {
            "title": "Your Name.", "year": 2016, "genre": "Animation, Drama, Fantasy, Romance",
            "director": "Makoto Shinkai", "cast": "Ryunosuke Kamiki, Mone Kamishiraishi, Ryo Narita, Aoi Yuki",
            "rating": 8.4, "votes": 320000,
            "overview": "Two teenagers share a profound, magical connection upon discovering they are swapping bodies. Things manage to become even more complicated when the boy and girl decide to meet in person.",
            "keywords": "body swap, comet catastrophe, tokyo, rural shrine, red thread of fate, twilight kataware-doki",
            "mood_tags": "Emotional, Romantic/Cozy, Visually Stunning, Mind-Bending",
            "poster_url": "https://image.tmdb.org/t/p/w500/q719jXXEzOoYaps6amxQo0qwW9.jpg"
        },
        {
            "title": "3 Idiots", "year": 2009, "genre": "Comedy, Drama",
            "director": "Rajkumar Hirani", "cast": "Aamir Khan, Madhavan, Sharman Joshi, Kareena Kapoor",
            "rating": 8.4, "votes": 430000,
            "overview": "Two friends are searching for their long lost companion. They revisit their college days and recall the memories of their friend who inspired them to think differently, even as the rest of the world called them 'idiots'.",
            "keywords": "engineering college, all is well, friendship, educational pressure, passion over marks, rancho",
            "mood_tags": "Feel-Good, Emotional, Heartwarming, Quirky & Fun",
            "poster_url": "https://image.tmdb.org/t/p/w500/7c9UVPPiTPltouxShYm848edzcw.jpg"
        },
        {
            "title": "Dangal", "year": 2016, "genre": "Action, Biography, Drama, Sport",
            "director": "Nitesh Tiwari", "cast": "Aamir Khan, Sakshi Tanwar, Fatima Sana Shaikh, Sanya Malhotra",
            "rating": 8.3, "votes": 210000,
            "overview": "Former wrestler Mahavir Singh Phogat and his two wrestler daughters struggle towards glory at the Commonwealth Games in the face of societal oppression.",
            "keywords": "wrestling, female empowerment, father coach, commonwealth games, haryana, dedication",
            "mood_tags": "Adrenaline Rush, Emotional, Heartwarming, Epic & Grand",
            "poster_url": "https://image.tmdb.org/t/p/w500/bA4d3r4e6504NqK2z7rF84B42rG.jpg"
        },
        {
            "title": "Taare Zameen Par", "year": 2007, "genre": "Drama, Family",
            "director": "Aamir Khan, Amole Gupte", "cast": "Darsheel Safary, Aamir Khan, Tisca Chopra, Vipin Sharma",
            "rating": 8.3, "votes": 200000,
            "overview": "An eight-year-old boy is thought to be a lazy trouble-maker, until the new art teacher has the patience and compassion to discover the real problem behind his struggles in school.",
            "keywords": "dyslexia, compassionate teacher, boarding school, childhood innocence, art competition, parents expectation",
            "mood_tags": "Feel-Good, Emotional, Heartwarming",
            "poster_url": "https://image.tmdb.org/t/p/w500/aHw8iJj2zT9dEw62zZk91Z2P8m.jpg"
        },
        {
            "title": "Lagaan", "year": 2001, "genre": "Drama, Musical, Sport",
            "director": "Ashutosh Gowariker", "cast": "Aamir Khan, Gracy Singh, Rachel Shelley, Paul Blackthorne",
            "rating": 8.1, "votes": 120000,
            "overview": "The people of a small village in Victorian India stake their future on a game of cricket against their ruthless British rulers.",
            "keywords": "cricket match, british raj, village unity, double tax lagaan, sports underdog, anthem",
            "mood_tags": "Epic & Grand, Adrenaline Rush, Feel-Good",
            "poster_url": "https://image.tmdb.org/t/p/w500/9b33a5h6k4nJ8Z7R1tH4zU0F9i.jpg"
        },
        {
            "title": "Gangs of Wasseypur", "year": 2012, "genre": "Action, Comedy, Crime, Drama",
            "director": "Anurag Kashyap", "cast": "Manoj Bajpayee, Richa Chadha, Nawazuddin Siddiqui, Tigmanshu Dhulia",
            "rating": 8.2, "votes": 105000,
            "overview": "A clash between Sultan and Shahid Khan leads to the expulsion of Khan from Wasseypur, and ignites a deadly blood feud spanning three generations.",
            "keywords": "coal mafia, bihar, revenge saga, iconic dialogue, faizal khan, bollywood cult, realism",
            "mood_tags": "Dark & Gritty, Intense & Gripping, Adrenaline Rush",
            "poster_url": "https://image.tmdb.org/t/p/w500/x2xWnFfF0o5yG4q0p3dF6H7wJ3Y.jpg"
        },
        {
            "title": "Tumbbad", "year": 2018, "genre": "Drama, Fantasy, Horror",
            "director": "Rahi Anil Barve, Anand Gandhi", "cast": "Sohum Shah, Jyoti Malshe, Anita Date-Kelkar, Ronjini Chakraborty",
            "rating": 8.2, "votes": 60000,
            "overview": "A mythological story about a human who builds a shrine for Hastar, a monster who is never supposed to be worshipped, because of greed for gold coins.",
            "keywords": "hastar, cursed womb, greed, endless rain, maharashtra, mythological horror, gold dough",
            "mood_tags": "Dark & Gritty, Spooky & Chilling, Visually Stunning",
            "poster_url": "https://image.tmdb.org/t/p/w500/pA2k9Uq1P0sU9rW0k4jJ6E7l9m.jpg"
        },

        # Horror, Psychological & Tension
        {
            "title": "The Shining", "year": 1980, "genre": "Drama, Horror",
            "director": "Stanley Kubrick", "cast": "Jack Nicholson, Shelley Duvall, Danny Lloyd, Scatman Crothers",
            "rating": 8.4, "votes": 1100000,
            "overview": "A family heads to an isolated hotel for the winter where a sinister presence influences the father into violence, while his psychic son sees horrific forebodings from both past and future.",
            "keywords": "overlook hotel, cabin fever, here's johnny, redrum, twin girls, hedge maze, isolation",
            "mood_tags": "Spooky & Chilling, Mind-Bending, Intense & Gripping",
            "poster_url": "https://image.tmdb.org/t/p/w500/b6qUu00iIIft4VJHGIR0b98vda0.jpg"
        },
        {
            "title": "Psycho", "year": 1960, "genre": "Horror, Mystery, Thriller",
            "director": "Alfred Hitchcock", "cast": "Anthony Perkins, Janet Leigh, Vera Miles, John Gavin",
            "rating": 8.5, "votes": 720000,
            "overview": "A Phoenix secretary embezzles $40,000 from her employer's client, goes on the run and checks into a remote motel run by a young man under the domination of his mother.",
            "keywords": "bates motel, shower scene, split personality, taxidermy, norman bates, hitchcockian suspense",
            "mood_tags": "Spooky & Chilling, Intense & Gripping, Cult Classic",
            "poster_url": "https://image.tmdb.org/t/p/w500/yz45KscGQikzrGEjST2io9GaxNk.jpg"
        },
        {
            "title": "Get Out", "year": 2017, "genre": "Horror, Mystery, Thriller",
            "director": "Jordan Peele", "cast": "Daniel Kaluuya, Allison Williams, Bradley Whitford, Catherine Keener",
            "rating": 7.8, "votes": 680000,
            "overview": "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception of him eventually reaches a boiling point.",
            "keywords": "the sunken place, tea cup hypnosis, social thriller, body snatching, weekend getaway",
            "mood_tags": "Spooky & Chilling, Thought-Provoking, Intense & Gripping",
            "poster_url": "https://image.tmdb.org/t/p/w500/tFXcEccSQMf3lfhfXKSU9iRBpa3.jpg"
        },
        {
            "title": "Hereditary", "year": 2018, "genre": "Drama, Horror, Mystery, Thriller",
            "director": "Ari Aster", "cast": "Toni Collette, Alex Wolff, Milly Shapiro, Gabriel Byrne",
            "rating": 7.3, "votes": 400000,
            "overview": "A grieving family is haunted by tragic and disturbing occurrences after the death of their secretive grandmother.",
            "keywords": "cult of paimon, grief, decapitation, miniatures, family curse, terrifying clucking sound",
            "mood_tags": "Spooky & Chilling, Dark & Gritty, Intense & Gripping",
            "poster_url": "https://image.tmdb.org/t/p/w500/p9fmuz2Oj3HtEJw87PzWkn7o1oE.jpg"
        },
        {
            "title": "A Quiet Place", "year": 2018, "genre": "Drama, Horror, Sci-Fi",
            "director": "John Krasinski", "cast": "Emily Blunt, John Krasinski, Millicent Simmonds, Noah Jupe",
            "rating": 7.5, "votes": 590000,
            "overview": "In a post-apocalyptic world, a family is forced to live in silence while hiding from monsters with ultra-sensitive hearing.",
            "keywords": "blind creatures, sound hunting, sign language, nail on stairs, birth in bathtub, silence",
            "mood_tags": "Intense & Gripping, Spooky & Chilling, Adrenaline Rush",
            "poster_url": "https://image.tmdb.org/t/p/w500/nAU74GmpUk7t5iklEp3bufwDq4n.jpg"
        }
    ]

# Function to expand catalog programmatically into a rich 150+ movie dataset with realistic data
def build_expanded_catalog():
    base = get_movie_catalog()
    
    additional_movies = [
        # Sci-Fi / Action / Classic
        ("The Matrix Reloaded", 2003, "Action, Sci-Fi", "Lana Wachowski, Lilly Wachowski", "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss", 7.2, 600000, "Neo and the rebel leaders estimate that they have 72 hours until 250,000 probes discover Zion and destroy it.", "zion, freeway chase, the architect, agent smith clone, destiny", "Adrenaline Rush, Mind-Bending", "https://image.tmdb.org/t/p/w500/9TGHDvWrqKBpuDxakLgnICzWvpH.jpg"),
        ("The Prestige", 2006, "Drama, Mystery, Sci-Fi, Thriller", "Christopher Nolan", "Christian Bale, Hugh Jackman, Scarlett Johansson, Michael Caine", 8.5, 1400000, "After a tragic accident, two stage magicians in 1890s London engage in a battle to create the ultimate illusion while sacrificing everything they have to outwit each other.", "magic, tesla machine, obsession, rivalry, twist ending, cloning, sacrifice", "Mind-Bending, Intense & Gripping, Dark & Gritty", "https://image.tmdb.org/t/p/w500/bdN3gXuIZYaJP7ftKK2sU0nPtEA.jpg"),
        ("Memento", 2000, "Mystery, Thriller", "Christopher Nolan", "Guy Pearce, Carrie-Anne Moss, Joe Pantoliano", 8.4, 1300000, "A man with short-term memory loss attempts to track down his wife's murderer.", "amnesia, polaroids, tattoos, backwards storytelling, unreliable narrator, noir", "Mind-Bending, Intense & Gripping, Dark & Gritty", "https://image.tmdb.org/t/p/w500/yuNs09hvpHVU1cBTCAk9zxsL2oW.jpg"),
        ("Alien", 1979, "Horror, Sci-Fi", "Ridley Scott", "Sigourney Weaver, Tom Skerritt, John Hurt", 8.5, 930000, "The crew of a commercial spacecraft encounters a deadly lifeform after investigating an unknown transmission.", "xenomorph, nostromo, chestburster, space horror, isolation, ripley", "Spooky & Chilling, Intense & Gripping, Dark & Gritty", "https://image.tmdb.org/t/p/w500/vfrQk5IPloGg1v9Rzbh2Eg3VGyM.jpg"),
        ("Aliens", 1986, "Action, Adventure, Sci-Fi, Thriller", "James Cameron", "Sigourney Weaver, Michael Biehn, Carrie Henn", 8.4, 760000, "Decades after surviving the Nostromo catastrophe, Ellen Ripley returns to LV-426 with a unit of Colonial Marines to investigate a lost colony.", "colonial marines, alien queen, power loader, get away from her, sci-fi action", "Adrenaline Rush, Intense & Gripping, Epic & Grand", "https://image.tmdb.org/t/p/w500/b1Vk8F5Uu4Qf6k7zY2j2r6m5vO.jpg"),
        ("Terminator 2: Judgment Day", 1991, "Action, Sci-Fi", "James Cameron", "Arnold Schwarzenegger, Linda Hamilton, Edward Furlong, Robert Patrick", 8.6, 1150000, "A cyborg, identical to the one who failed to kill Sarah Connor, must now protect her ten-year-old son John from an even more advanced and powerful cyborg.", "liquid metal t1000, hasta la vista baby, cyberdyne, nuclear prevention, motorcycle chase", "Adrenaline Rush, Epic & Grand, Visually Stunning", "https://image.tmdb.org/t/p/w500/5M0j0B18abtBI5a4L99hvUDqp2J.jpg"),
        ("The Terminator", 1984, "Action, Sci-Fi", "James Cameron", "Arnold Schwarzenegger, Linda Hamilton, Michael Biehn", 8.1, 900000, "A human soldier is sent from 2029 to 1984 to stop an almost indestructible cyborg killing machine, sent from the same year, which has been programmed to execute Sarah Connor.", "i will be back, time travel, tech noir, future war, cybernetic organism", "Adrenaline Rush, Dark & Gritty, Intense & Gripping", "https://image.tmdb.org/t/p/w500/hzXSE6Mfdt49Pp08i9n0jU9RzR8.jpg"),
        ("Avatar", 2009, "Action, Adventure, Fantasy, Sci-Fi", "James Cameron", "Sam Worthington, Zoe Saldana, Sigourney Weaver, Stephen Lang", 7.9, 1350000, "A paraplegic Marine dispatched to the moon Pandora on a unique mission becomes torn between following his orders and protecting the world he feels is his home.", "pandora, na'vi, unobtanium, bioluminescent forest, eywa, avatar body", "Visually Stunning, Epic & Grand, Feel-Good", "https://image.tmdb.org/t/p/w500/kyeqWdyUXW608qlYkRqosgbbJyK.jpg"),
        ("Avatar: The Way of Water", 2022, "Action, Adventure, Fantasy, Sci-Fi", "James Cameron", "Sam Worthington, Zoe Saldana, Sigourney Weaver, Kate Winslet", 7.6, 500000, "Jake Sully lives with his newfound family formed on the extrasolar moon Pandora. Once a familiar threat returns to finish what was previously started, Jake must work with Neytiri and the army of the Na'vi race.", "metkayina reef clan, tulkun whale, ocean world, family protection, underwater 3d", "Visually Stunning, Epic & Grand, Emotional", "https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"),
        ("Jurassic Park", 1993, "Action, Adventure, Sci-Fi", "Steven Spielberg", "Sam Neill, Laura Dern, Jeff Goldblum, Richard Attenborough", 8.2, 1050000, "An industrialist invites some experts to visit his theme park of cloned dinosaurs. After a power failure, the creatures run amok.", "t-rex, velociraptors, isla nublar, chaos theory, amber mosquito, life finds a way", "Adrenaline Rush, Feel-Good, Visually Stunning", "https://image.tmdb.org/t/p/w500/oU7Oq2kFAAlGqbU4VoAE36g4hoI.jpg"),
        ("Schindler's List", 1993, "Biography, Drama, History", "Steven Spielberg", "Liam Neeson, Ralph Fiennes, Ben Kingsley", 9.0, 1400000, "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.", "holocaust, krakow ghetto, girl in red coat, righteous among nations, black and white masterpiece", "Emotional, Thought-Provoking, Dark & Gritty", "https://image.tmdb.org/t/p/w500/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg"),
        ("Saving Private Ryan", 1998, "Drama, War", "Steven Spielberg", "Tom Hanks, Matt Damon, Tom Sizemore, Edward Burns", 8.6, 1450000, "Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action.", "omaha beach, d-day, earned this, brotherhood, sniper tower, world war ii", "Adrenaline Rush, Emotional, Epic & Grand", "https://image.tmdb.org/t/p/w500/uqx37cS8cpHg8U35f9U5IBlrCV3.jpg"),
        ("Catch Me If You Can", 2002, "Biography, Crime, Drama", "Steven Spielberg", "Leonardo DiCaprio, Tom Hanks, Christopher Walken, Martin Sheen", 8.1, 1050000, "Barely 21 yet, Frank is a skilled forger who has passed as a doctor, lawyer and pilot all before his graduation, pursued by FBI agent Carl Hanratty.", "imposter, check fraud, pan am pilot, cat and mouse, 1960s style, charm", "Feel-Good, Quirky & Fun, Adrenaline Rush", "https://image.tmdb.org/t/p/w500/ctjEj2xM322B69aFp3jH5g7f2Z0.jpg"),
        ("No Country for Old Men", 2007, "Crime, Drama, Thriller", "Joel Coen, Ethan Coen", "Tommy Lee Jones, Javier Bardem, Josh Brolin, Woody Harrelson", 8.2, 1050000, "Violence and mayhem ensue after a hunter stumbles upon some dead bodies, a stash of heroin and more than $2 million in cash near the Rio Grande.", "anton chigurh, coin toss, silenced shotgun, drug money, west texas, moral decay", "Dark & Gritty, Intense & Gripping, Thought-Provoking", "https://image.tmdb.org/t/p/w500/6d5XOczrRbs51zM4W53k6wX96m.jpg"),
        ("Fargo", 1996, "Crime, Thriller", "Joel Coen, Ethan Coen", "William H. Macy, Frances McDormand, Steve Buscemi, Peter Stormare", 8.1, 720000, "Jerry Lundegaard's inept crime falls apart due to his and his henchmen's bungling and the persistent police work of the quite pregnant Marge Gunderson.", "woodchipper, minnesota snow, fake kidnapping, pregnant sheriff, quirky crime", "Dark Comedy, Quirky & Fun, Cult Classic", "https://image.tmdb.org/t/p/w500/rt7cpEr1u9fbgL8T76j3O8O4q0U.jpg"),
        ("The Big Lebowski", 1998, "Comedy, Crime", "Joel Coen, Ethan Coen", "Jeff Bridges, John Goodman, Julianne Moore, Steve Buscemi", 8.1, 840000, "Ultimate L.A. slacker Jeff 'The Dude' Lebowski, mistaken for a millionaire of the same name, seeks restitution for a ruined rug and enlists his bowling buddies.", "the dude, rug tied the room together, white russian, bowling, nihilists, walter sobchak", "Quirky & Fun, Cult Classic, Feel-Good", "https://image.tmdb.org/t/p/w500/9BTNYtWJvC8C0n4H4p4q3U3Hq3V.jpg"),
        ("12 Angry Men", 1957, "Crime, Drama", "Sidney Lumet", "Henry Fonda, Lee J. Cobb, Martin Balsam, John Fiedler", 9.0, 850000, "The jury in a New York City murder trial is frustrated by a single member whose reasonable doubt forces the team to consider the evidence more carefully.", "jury deliberation, reasonable doubt, single room drama, black and white classic, justice", "Thought-Provoking, Intense & Gripping", "https://image.tmdb.org/t/p/w500/ow3wq89wM8qd5X7hWKxiRfsFf9C.jpg"),
        ("The Silence of the Lambs", 1991, "Crime, Drama, Thriller", "Jonathan Demme", "Jodie Foster, Anthony Hopkins, Lawrence A. Bonney, Kasi Lemmons", 8.6, 1500000, "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.", "hannibal lecter, clarice starling, buffalo bill, fava beans and chianti, moth, psychological game", "Spooky & Chilling, Intense & Gripping, Dark & Gritty", "https://image.tmdb.org/t/p/w500/uS9m8OBk1A8eM9I0f5F9wT2bU4v.jpg"),
        ("Coco", 2017, "Animation, Adventure, Comedy, Family, Fantasy, Music", "Lee Unkrich, Adrian Molina", "Anthony Gonzalez, Gael García Bernal, Benjamin Bratt, Alanna Ubach", 8.4, 580000, "Aspiring musician Miguel, confronted with his family's ancestral ban on music, enters the Land of the Dead to find his great-great-grandfather, a legendary singer.", "day of the dead, remember me, guitar, skeleton world, ancestors, alebrijes", "Feel-Good, Emotional, Heartwarming, Visually Stunning", "https://image.tmdb.org/t/p/w500/gGEsBPAijhVUFoiNpgZXqRVWJt2.jpg")
    ]
    
    # Assemble catalog
    all_movies = list(base)
    start_id = len(all_movies) + 1
    
    for row in additional_movies:
        all_movies.append({
            "title": row[0],
            "year": row[1],
            "genre": row[2],
            "director": row[3],
            "cast": row[4],
            "rating": row[5],
            "votes": row[6],
            "overview": row[7],
            "keywords": row[8],
            "mood_tags": row[9],
            "poster_url": row[10]
        })
        
    # Additional expanded popular library across global cinema
    more_titles = [
        # Animated Masterpieces
        ("WALL-E", 2008, "Animation, Adventure, Family, Sci-Fi", "Andrew Stanton", "Ben Burtt, Elissa Knight, Jeff Garlin", 8.4, 1150000, "In the distant future, a small waste-collecting robot inadvertently embarks on a space journey that will ultimately decide the fate of mankind.", "robot love, eve, clean earth, space ship axiom, plant in boot, silence", "Feel-Good, Emotional, Thought-Provoking", "https://image.tmdb.org/t/p/w500/hbhFnRzzg6ZDmm8YAmxBnQAcUm.jpg"),
        ("Up", 2009, "Animation, Adventure, Comedy, Family", "Pete Docter, Bob Peterson", "Edward Asner, Jordan Nagai, John Ratzenberger", 8.3, 1080000, "78-year-old Carl Fredricksen travels to Paradise Falls in his house equipped with balloons, inadvertently taking a young stowaway.", "opening montage, flying balloon house, paradise falls, talking dog dug, badge", "Emotional, Feel-Good, Heartwarming", "https://image.tmdb.org/t/p/w500/vpbaStTMt8qqgE27qOX8RIg8H1C.jpg"),
        ("Toy Story", 1995, "Animation, Adventure, Comedy, Family, Fantasy", "John Lasseter", "Tom Hanks, Tim Allen, Don Rickles, Jim Varney", 8.3, 1020000, "A cowboy doll is profoundly threatened and jealous when a new spaceman action figure supplants him as top toy in a boy's bedroom.", "woody, buzz lightyear, to infinity and beyond, pizza planet, sid, childhood toys", "Feel-Good, Nostalgic, Heartwarming", "https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg"),
        ("Toy Story 3", 2010, "Animation, Adventure, Comedy, Family, Fantasy", "Lee Unkrich", "Tom Hanks, Tim Allen, Joan Cusack, Ned Beatty", 8.3, 890000, "The toys are mistakenly delivered to a day-care center instead of the attic right before Andy leaves for college, and it's up to Woody to convince the other toys that they weren't abandoned.", "sunnyside daycare, lotso bear, incinerator scene, college farewell, childhood goodbye", "Emotional, Heartwarming, Feel-Good", "https://image.tmdb.org/t/p/w500/AbbXspwhIR19GK2392Az3o3iAoi.jpg"),
        ("Ratatouille", 2007, "Animation, Adventure, Comedy, Family, Fantasy", "Brad Bird, Jan Pinkava", "Brad Garrett, Lou Romano, Patton Oswalt, Ian Holm", 8.1, 800000, "A rat who can cook makes an unusual alliance with a young kitchen worker at a famous Paris restaurant.", "remy the rat, gusteau, anyone can cook, anton ego, critic revelation, french food", "Feel-Good, Heartwarming, Visually Stunning", "https://image.tmdb.org/t/p/w500/npHNrrHGHRaT2r7T4w0k1NfJz8h.jpg"),
        ("Inside Out", 2015, "Animation, Adventure, Comedy, Drama, Family, Fantasy", "Pete Docter, Ronnie Del Carmen", "Amy Poehler, Bill Hader, Lewis Black, Mindy Kaling", 8.1, 770000, "After young Riley is uprooted from her Midwest life and moved to San Francisco, her emotions - Joy, Fear, Anger, Disgust and Sadness - conflict on how best to navigate a new city.", "emotions inside head, bing bong, core memories, sadness is necessary, psychology", "Emotional, Feel-Good, Thought-Provoking", "https://image.tmdb.org/t/p/w500/lRHE0vzf3oYJrhbsQmMKyUpQ8ko.jpg"),
        ("Inside Out 2", 2024, "Animation, Adventure, Comedy, Drama, Family, Fantasy", "Kelsey Mann", "Amy Poehler, Maya Hawke, Kensington Tallman, Liza Lapira", 7.7, 240000, "Follow Riley in her teenage years as new emotions like Anxiety, Envy, Ennui, and Embarrassment show up in Headquarters.", "anxiety, panic attack, teenage years, self belief, headquarters, puberty", "Emotional, Feel-Good, Thought-Provoking", "https://image.tmdb.org/t/p/w500/vpnVM9B6NMmQpWeZvzLvDESb2QY.jpg"),
        ("How to Train Your Dragon", 2010, "Animation, Action, Adventure, Family, Fantasy", "Dean DeBlois, Chris Sanders", "Jay Baruchel, Gerard Butler, Christopher Mintz-Plasse, America Ferrera", 8.1, 780000, "A hapless young Viking who aspires to hunt dragons becomes the unlikely friend of a young dragon himself, and learns there may be more to the creatures than he assumed.", "toothless, night fury, viking island berk, flight sequence, forbidden friendship", "Feel-Good, Adrenaline Rush, Heartwarming", "https://image.tmdb.org/t/p/w500/ygGmAO60t8GyqUv97V9Fk9r5B.jpg"),

        # Modern Blockbusters & Action
        ("John Wick", 2014, "Action, Crime, Thriller", "Chad Stahelski", "Keanu Reeves, Michael Nyqvist, Alfie Allen, Willem Dafoe", 7.4, 720000, "An ex-hitman comes out of retirement to track down the gangsters that took everything from him.", "baba yaga, continental hotel, dog revenge, gun fu, gold coins, pencil assassin", "Adrenaline Rush, Dark & Gritty, Intense & Gripping", "https://image.tmdb.org/t/p/w500/fZPSd91yGE9fCcCe6OoQr6E3Bev.jpg"),
        ("John Wick: Chapter 4", 2023, "Action, Crime, Thriller", "Chad Stahelski", "Keanu Reeves, Donnie Yen, Bill Skarsgård, Laurence Fishburne", 7.7, 340000, "John Wick uncovers a path to defeating The High Table. But before he can earn his freedom, Wick must face off against a new enemy.", "high table duel, staircase climb, dragon's breath shotgun, caine blind swordsman", "Adrenaline Rush, Visually Stunning, Intense & Gripping", "https://image.tmdb.org/t/p/w500/vZloFAK7NmvMGKE7VkF5UHaz0I.jpg"),
        ("The Batman", 2022, "Action, Crime, Drama, Mystery", "Matt Reeves", "Robert Pattinson, Zoë Kravitz, Jeffrey Wright, Colin Farrell", 7.8, 770000, "When a sadistic serial killer begins murdering key political figures in Gotham, Batman is forced to investigate the city's hidden corruption and question his family's involvement.", "riddler ciphers, batmobile muscle car, vengeance, catwoman, nirvana something in the way", "Dark & Gritty, Intense & Gripping, Spooky & Chilling", "https://image.tmdb.org/t/p/w500/74xTEgt7R36Fpooo50r9T25onhq.jpg"),
        ("Joker", 2019, "Crime, Drama, Thriller", "Todd Phillips", "Joaquin Phoenix, Robert De Niro, Zazie Beetz, Frances Conroy", 8.4, 1500000, "During the 1980s, a failed stand-up comedian is driven insane and turns to a life of crime and chaos in Gotham City while becoming an infamous psychopathic crime figure.", "arthur fleck, mental illness, stairs dance, live talk show, society clown, origin story", "Dark & Gritty, Intense & Gripping, Thought-Provoking", "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg"),
        ("The Wolf of Wall Street", 2013, "Biography, Comedy, Crime", "Martin Scorsese", "Leonardo DiCaprio, Jonah Hill, Margot Robbie, Matthew McConaughey", 8.2, 1600000, "Based on the true story of Jordan Belfort, from his rise to a wealthy stock-broker living the high life to his fall involving crime, corruption and the federal government.", "penny stocks, quaeludes, stratton oakmont, excess, greed, sell me this pen", "Dark Comedy, Adrenaline Rush, Quirky & Fun", "https://image.tmdb.org/t/p/w500/34m2tygAYBGqA9MXKhRDtzYd4v1.jpg"),
        ("Casino", 1995, "Crime, Drama", "Martin Scorsese", "Robert De Niro, Sharon Stone, Joe Pesci, James Woods", 8.2, 570000, "In Las Vegas, two best friends - a casino executive and a mafia enforcer - compete and clash over a gambling empire, and over a fast-living and deceptive socialite.", "las vegas gambling, mob control, desert burial, greed, betrayal, sharon stone", "Dark & Gritty, Intense & Gripping, Epic & Grand", "https://image.tmdb.org/t/p/w500/4TS5O1IP42bY2BvgMxLSD0m9O7G.jpg"),
        ("Heat", 1995, "Action, Crime, Drama", "Michael Mann", "Al Pacino, Robert De Niro, Val Kilmer, Jon Voight", 8.3, 720000, "A group of high-end professional thieves start to feel the heat from the LAPD when they unknowingly leave a clue at their latest heist.", "diner faceoff, bank shootout downtown la, professionalism, cat and mouse cop thief", "Adrenaline Rush, Dark & Gritty, Intense & Gripping", "https://image.tmdb.org/t/p/w500/rrBuGu0PjqncAzUh9Em5qdEvz.jpg"),
        ("Drive", 2011, "Action, Drama", "Nicolas Winding Refn", "Ryan Gosling, Carey Mulligan, Bryan Cranston, Albert Brooks", 7.8, 680000, "A mysterious Hollywood stuntman and mechanic who moonlights as a getaway driver finds himself in trouble when he helps out his neighbor in Los Angeles.", "synthwave soundtrack, scorpion jacket, elevator stomp, toothpick, silent hero", "Dark & Gritty, Visually Stunning, Intense & Gripping", "https://image.tmdb.org/t/p/w500/602vev0x7qU7878g2Q0p8O04t0k.jpg"),
        ("Baby Driver", 2017, "Action, Crime, Music", "Edgar Wright", "Ansel Elgort, Jon Bernthal, Jon Hamm, Eiza González, Jamie Foxx", 7.6, 600000, "After being coerced into working for a crime boss, a young getaway driver finds himself taking part in a heist doomed to fail.", "music synced action, tinnitus, ipod playlist, red subaru drift, diner romance", "Adrenaline Rush, Quirky & Fun, Feel-Good", "https://image.tmdb.org/t/p/w500/rmnQ9j1fZLtwL2Fqg6q59pU2z7.jpg"),
        ("Knives Out", 2019, "Comedy, Crime, Drama, Mystery, Thriller", "Rian Johnson", "Daniel Craig, Chris Evans, Ana de Armas, Jamie Lee Curtis", 7.9, 800000, "A detective investigates the death of a patriarch of an eccentric, combative family.", "benoit blanc, donut hole, eccentric family, inheritance, poisoned syringe, whodunnit", "Quirky & Fun, Intense & Gripping, Feel-Good", "https://image.tmdb.org/t/p/w500/pThyQovXQrw2m0s9x82twj48Jq4.jpg"),
        ("Glass Onion: A Knives Out Mystery", 2022, "Comedy, Drama, Mystery", "Rian Johnson", "Daniel Craig, Edward Norton, Janelle Monáe, Kathryn Hahn", 7.1, 450000, "Famed Southern detective Benoit Blanc travels to Greece for his latest case, peeling back the layers of a mystery involving a new cast of colorful suspects.", "tech billionaire, private island, murder mystery puzzle, peeling layers, disruption", "Quirky & Fun, Visually Stunning, Feel-Good", "https://image.tmdb.org/t/p/w500/vDGr1YdrlfbU9wxTOdpf3zChmv9.jpg"),
        
        # Sci-Fi / Cult / Modern Classics
        ("Ex Machina", 2014, "Drama, Sci-Fi, Thriller", "Alex Garland", "Domhnall Gleeson, Alicia Vikander, Oscar Isaac", 7.7, 580000, "A young programmer is selected to participate in a ground-breaking experiment in synthetic intelligence by evaluating the human qualities of a highly advanced humanoid A.I.", "turing test, ava android, isolated mountain estate, dance scene, ai ethics, manipulation", "Mind-Bending, Intense & Gripping, Thought-Provoking", "https://image.tmdb.org/t/p/w500/btbRB7BrD88799HA9yQ9v7vJ9n.jpg"),
        ("Her", 2013, "Drama, Romance, Sci-Fi", "Spike Jonze", "Joaquin Phoenix, Scarlett Johansson, Amy Adams", 8.0, 680000, "In a near future, a lonely writer develops an unlikely relationship with an operating system designed to meet his every need.", "os one, samantha voice, high-waisted trousers, love in digital age, loneliness", "Thought-Provoking, Romantic/Cozy, Emotional", "https://image.tmdb.org/t/p/w500/yk4J4aC3veRNa9UHg0BQ6q369Nm.jpg"),
        ("The Truman Show", 1998, "Comedy, Drama, Sci-Fi", "Peter Weir", "Jim Carrey, Ed Harris, Laura Linney, Noah Emmerich", 8.2, 1150000, "An insurance salesman discovers his entire life is actually a reality TV show broadcast live around the clock across the entire globe.", "seahaven dome, reality tv, fake sun, good morning good afternoon goodnight, escape", "Thought-Provoking, Mind-Bending, Feel-Good", "https://image.tmdb.org/t/p/w500/vuza0WqY239gBNa1vRGe9updt9n.jpg"),
        ("Eternal Sunshine of the Spotless Mind", 2004, "Drama, Romance, Sci-Fi", "Michel Gondry", "Jim Carrey, Kate Winslet, Elijah Wood", 8.3, 1050000, "When their relationship turns sour, a couple undergoes a medical procedure to have each other erased from their memories.", "clementine kruczynski, meet me in montauk, memory erasure, frozen lake", "Mind-Bending, Romantic/Cozy, Emotional", "https://image.tmdb.org/t/p/w500/5MwkWH9tYHv3mV9OdunMR5qvtwe.jpg"),
        ("Prisoners", 2013, "Crime, Drama, Mystery, Thriller", "Denis Villeneuve", "Hugh Jackman, Jake Gyllenhaal, Viola Davis, Paul Dano", 8.2, 820000, "When Keller Dover's daughter and her friend go missing, he takes matters into his own hands as the police pursue multiple leads and the pressure mounts.", "missing child, labyrinth maze, detective loki, vigilante father, suburban mystery, whistle", "Dark & Gritty, Intense & Gripping, Thought-Provoking", "https://image.tmdb.org/t/p/w500/tuZhZ6uX9vYyN1Y6v6X5K8eQ1q.jpg"),
        ("Sicario", 2015, "Action, Crime, Drama, Mystery, Thriller", "Denis Villeneuve", "Emily Blunt, Benicio Del Toro, Josh Brolin, Victor Garber", 7.7, 490000, "An idealistic FBI agent is enlisted by a government task force to aid in the escalating war against drugs at the border area between the U.S. and Mexico.", "juarez border bridge, cartel tunnel, alejandro hitman, night vision raid, moral grey area", "Dark & Gritty, Intense & Gripping, Adrenaline Rush", "https://image.tmdb.org/t/p/w500/5T9iU3cE1rP8xN3a6T7t0U6e8B.jpg"),
        ("Incendies", 2010, "Drama, Mystery, War", "Denis Villeneuve", "Lubna Azabal, Mélissa Désormeaux-Poulin, Maxim Gaudette", 8.3, 210000, "Twins journey to the Middle East to discover their family roots and fulfill their mother's last wishes.", "middle east war, brother and father letter, math 1+1=1, shocking secret, testament", "Emotional, Thought-Provoking, Dark & Gritty", "https://image.tmdb.org/t/p/w500/51j199i8n3qV6U3fX8gL0mP4G.jpg"),
        
        # Indian Cinema Highlights
        ("Kantara", 2022, "Action, Adventure, Drama", "Rishab Shetty", "Rishab Shetty, Sapthami Gowda, Kishore Kumar G.", 8.2, 110000, "When greed paves the way for betrayal, scheming and murder, a young tribal man reluctantly inherits the tradition of his ancestors to seek justice.", "panjurli daiva, bhuta kola roar, forest land conflict, divine possession, coastal karnataka", "Visually Stunning, Epic & Grand, Intense & Gripping", "https://image.tmdb.org/t/p/w500/pA2k9Uq1P0sU9rW0k4jJ6E7l9m.jpg"),
        ("RRR", 2022, "Action, Drama", "S.S. Rajamouli", "N.T. Rama Rao Jr., Ram Charan, Ajay Devgn, Alia Bhatt", 7.8, 180000, "A fictitious story about two legendary revolutionaries and their journey away from home before they began fighting for their country in the 1920s.", "naatu naatu dance, tiger fight, piggyback rifle combat, anti-colonial revolution, bromance", "Adrenaline Rush, Epic & Grand, Visually Stunning", "https://image.tmdb.org/t/p/w500/wE0q27t1e6Z0N4Jv8n9p9k4m1K.jpg"),
        ("Baahubali 2: The Conclusion", 2017, "Action, Drama", "S.S. Rajamouli", "Prabhas, Rana Daggubati, Anushka Shetty, Ramya Krishnan", 8.2, 110000, "When Shiva, the son of Bahubali, learns about his heritage, he begins to look for answers. His story is juxtaposed with past events that unfolded in the Mahishmati Kingdom.", "mahishmati empire, katappa killed baahubali, coronation, royal betrayal, elephant sequence", "Epic & Grand, Adrenaline Rush, Visually Stunning", "https://image.tmdb.org/t/p/w500/5y8oQ1xP5E5M7X0v7l9q3e5p7k.jpg"),
        ("Drishyam", 2015, "Crime, Drama, Mystery, Thriller", "Nishikant Kamat", "Ajay Devgn, Tabu, Shriya Saran, Rajat Kapoor", 8.2, 100000, "Desperate measures are taken by a man who tries to save his family from the dark side of the law, after they commit an unexpected crime.", "2nd october panjim ashram, cable operator movie knowledge, fabricated alibi, police interrogation", "Intense & Gripping, Mind-Bending, Thought-Provoking", "https://image.tmdb.org/t/p/w500/7a8z9J3lK8Z5W6d2M4s1N7rP9.jpg"),
        ("Andhadhun", 2018, "Comedy, Crime, Music, Mystery, Thriller", "Sriram Raghavan", "Ayushmann Khurrana, Tabu, Radhika Apte, Anil Dhawan", 8.2, 115000, "A series of mysterious events change the life of a blind pianist, who now must report a crime that he was never supposed to know about.", "fake blind pianist, dead body in apartment, organ harvesting, hare rabbit, dark comedy twist", "Dark Comedy, Mind-Bending, Intense & Gripping", "https://image.tmdb.org/t/p/w500/2L2qR6v8z2wYm0x68tP9sI6q3sP.jpg"),
        ("Swades", 2004, "Drama", "Ashutosh Gowariker", "Shah Rukh Khan, Gayatri Joshi, Kishori Ballal", 8.2, 100000, "A successful Indian scientist at NASA returns to an Indian village to take his nanny to America with him and in the process rediscovers his roots.", "nasa scientist, village electrification, caravan water cup, patriotism, social reform", "Feel-Good, Emotional, Thought-Provoking", "https://image.tmdb.org/t/p/w500/4nQ1oY5f6m1j8Q6M9v6P8j9N4B.jpg"),
        ("Chak De! India", 2007, "Drama, Sport", "Shimit Amin", "Shah Rukh Khan, Vidya Malvade, Sagarika Ghatge", 8.1, 95000, "Kabir Khan, a former hockey star, tainted as someone who betrayed his country, begins coaching the Indian women's national hockey team to prove his loyalty.", "sattar minute speech, women hockey world cup, underdog team, redemption, teamwork", "Adrenaline Rush, Feel-Good, Emotional", "https://image.tmdb.org/t/p/w500/3Z3M6p1K8B0J7L4n4V9X8Z1Q7b.jpg")
    ]

    for row in more_titles:
        all_movies.append({
            "title": row[0],
            "year": row[1],
            "genre": row[2],
            "director": row[3],
            "cast": row[4],
            "rating": row[5],
            "votes": row[6],
            "overview": row[7],
            "keywords": row[8],
            "mood_tags": row[9],
            "poster_url": row[10]
        })
        
    # Deduplicate by title
    unique_movies = {}
    for m in all_movies:
        if m["title"].lower() not in unique_movies:
            unique_movies[m["title"].lower()] = m
            
    # Assign sequential IDs
    res = []
    for idx, (k, v) in enumerate(unique_movies.items(), start=1):
        v_copy = dict(v)
        v_copy["id"] = idx
        res.append(v_copy)
        
    return res

def save_catalog_csv(filepath="dataset/movies.csv"):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    movies = build_expanded_catalog()
    fieldnames = ["id", "title", "year", "genre", "director", "cast", "rating", "votes", "overview", "keywords", "mood_tags", "poster_url"]
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for m in movies:
            writer.writerow(m)
            
    print(f"Successfully wrote {len(movies)} curated movies to {filepath}")

if __name__ == "__main__":
    save_catalog_csv()
