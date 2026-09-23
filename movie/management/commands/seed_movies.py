from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from movie.models import Movie, Genre, MovieCast, MovieWatchLink, Review


class Command(BaseCommand):
    help = 'Seeds the database with high-quality blockbuster movies, genres, cast, watch links, and reviews'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Seeding database with modern streaming movie data...'))

        # Ensure demo user exists
        user, _ = User.objects.get_or_create(
            username='ati',
            defaults={'email': 'ati@cinecine.test', 'is_staff': True, 'is_superuser': True}
        )
        if not user.has_usable_password():
            user.set_password('admin123')
            user.save()

        user2, _ = User.objects.get_or_create(
            username='sarah_cinéphile',
            defaults={'email': 'sarah@cinecine.test'}
        )
        user3, _ = User.objects.get_or_create(
            username='alex_filmfan',
            defaults={'email': 'alex@cinecine.test'}
        )

        # Genres
        genre_data = [
            'Action', 'Sci-Fi', 'Drama', 'Thriller', 'Adventure', 
            'Crime', 'Fantasy', 'Animation', 'Mystery'
        ]
        genres = {}
        for gname in genre_data:
            genre, _ = Genre.objects.get_or_create(name=gname)
            genres[gname] = genre

        # Movies Data
        movies_data = [
            {
                'title': 'Dune: Part Two',
                'overview': 'Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family. Facing a choice between the love of his life and the fate of the known universe, he endeavors to prevent a terrible future only he can foresee.',
                'release_year': 2024,
                'rating': 8.6,
                'runtime_minutes': 166,
                'language': 'en',
                'director': 'Denis Villeneuve',
                'poster_url': 'https://image.tmdb.org/t/p/w780/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg',
                'trailer_youtube_id': 'Way9Dexny3w',
                'genres': ['Sci-Fi', 'Adventure', 'Drama', 'Action'],
                'cast': [
                    ('Timothée Chalamet', 'Paul Atreides', 1),
                    ('Zendaya', 'Chani', 2),
                    ('Rebecca Ferguson', 'Lady Jessica', 3),
                    ('Javier Bardem', 'Stilgar', 4),
                    ('Austin Butler', 'Feyd-Rautha Harkonnen', 5),
                ],
                'watch_links': [
                    ('Max', 'https://www.max.com'),
                    ('Prime Video', 'https://www.amazon.com/primevideo'),
                    ('Apple TV+', 'https://tv.apple.com'),
                ],
                'reviews': [
                    (user, 5, 'An absolute masterpiece of modern cinema. The sound design, visuals, and score are peerless.'),
                    (user2, 5, 'Denis Villeneuve has crafted the greatest sci-fi epic since the original Star Wars trilogy.'),
                ]
            },
            {
                'title': 'Oppenheimer',
                'overview': 'The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb during World War II, exploring the moral and political turmoil that followed.',
                'release_year': 2023,
                'rating': 8.9,
                'runtime_minutes': 180,
                'language': 'en',
                'director': 'Christopher Nolan',
                'poster_url': 'https://image.tmdb.org/t/p/w780/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg',
                'trailer_youtube_id': 'uYPbbksJxIg',
                'genres': ['Drama', 'Thriller'],
                'cast': [
                    ('Cillian Murphy', 'J. Robert Oppenheimer', 1),
                    ('Emily Blunt', 'Katherine "Kitty" Oppenheimer', 2),
                    ('Matt Damon', 'Leslie Groves', 3),
                    ('Robert Downey Jr.', 'Lewis Strauss', 4),
                    ('Florence Pugh', 'Jean Tatlock', 5),
                ],
                'watch_links': [
                    ('Prime Video', 'https://www.amazon.com/primevideo'),
                    ('Apple TV+', 'https://tv.apple.com'),
                ],
                'reviews': [
                    (user3, 5, 'Cillian Murphy gives the performance of a lifetime. A haunting, breathtaking biographical drama.'),
                ]
            },
            {
                'title': 'Interstellar',
                'overview': 'When Earth becomes uninhabitable in the future, a farmer and ex-NASA pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team of researchers, to find a new planet for humans.',
                'release_year': 2014,
                'rating': 8.7,
                'runtime_minutes': 169,
                'language': 'en',
                'director': 'Christopher Nolan',
                'poster_url': 'https://image.tmdb.org/t/p/w780/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg',
                'trailer_youtube_id': 'zSWdZVtXT7E',
                'genres': ['Sci-Fi', 'Drama', 'Adventure'],
                'cast': [
                    ('Matthew McConaughey', 'Cooper', 1),
                    ('Anne Hathaway', 'Brand', 2),
                    ('Jessica Chastain', 'Murph', 3),
                    ('Michael Caine', 'Professor Brand', 4),
                ],
                'watch_links': [
                    ('Paramount+', 'https://www.paramountplus.com'),
                    ('Prime Video', 'https://www.amazon.com/primevideo'),
                ],
                'reviews': [
                    (user, 5, 'Hans Zimmer score paired with this emotional space journey brings me to tears every single viewing.'),
                ]
            },
            {
                'title': 'Inception',
                'overview': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O., but his tragic past may doom the project and his team to disaster.',
                'release_year': 2010,
                'rating': 8.8,
                'runtime_minutes': 148,
                'language': 'en',
                'director': 'Christopher Nolan',
                'poster_url': 'https://image.tmdb.org/t/p/w780/ljsZTbVsrQSqZgWeep2B1QiDKuh.jpg',
                'trailer_youtube_id': 'YoHD9XEInc0',
                'genres': ['Action', 'Sci-Fi', 'Thriller', 'Adventure'],
                'cast': [
                    ('Leonardo DiCaprio', 'Cobb', 1),
                    ('Joseph Gordon-Levitt', 'Arthur', 2),
                    ('Elliot Page', 'Ariadne', 3),
                    ('Tom Hardy', 'Eames', 4),
                    ('Ken Watanabe', 'Saito', 5),
                ],
                'watch_links': [
                    ('Netflix', 'https://www.netflix.com'),
                    ('Apple TV+', 'https://tv.apple.com'),
                ],
                'reviews': [
                    (user2, 5, 'One of the most inventive and flawlessly executed concept films in Hollywood history.'),
                ]
            },
            {
                'title': 'The Dark Knight',
                'overview': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'release_year': 2008,
                'rating': 9.0,
                'runtime_minutes': 152,
                'language': 'en',
                'director': 'Christopher Nolan',
                'poster_url': 'https://image.tmdb.org/t/p/w780/qJ2tW6WMUDux911r6m7haRef0WH.jpg',
                'trailer_youtube_id': 'EXeTwQWrcwY',
                'genres': ['Action', 'Crime', 'Drama', 'Thriller'],
                'cast': [
                    ('Christian Bale', 'Bruce Wayne / Batman', 1),
                    ('Heath Ledger', 'Joker', 2),
                    ('Aaron Eckhart', 'Harvey Dent', 3),
                    ('Michael Caine', 'Alfred', 4),
                    ('Gary Oldman', 'Jim Gordon', 5),
                ],
                'watch_links': [
                    ('Max', 'https://www.max.com'),
                    ('Prime Video', 'https://www.amazon.com/primevideo'),
                ],
                'reviews': [
                    (user, 5, 'Heath Ledger gives the greatest villain performance of all time. Still the pinnacle of comic book films.'),
                ]
            },
            {
                'title': 'Blade Runner 2049',
                'overview': 'Young Blade Runner K discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard, who has been missing for thirty years.',
                'release_year': 2017,
                'rating': 8.0,
                'runtime_minutes': 164,
                'language': 'en',
                'director': 'Denis Villeneuve',
                'poster_url': 'https://image.tmdb.org/t/p/w780/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg',
                'trailer_youtube_id': 'gCcx85zbxz4',
                'genres': ['Sci-Fi', 'Mystery', 'Drama', 'Thriller'],
                'cast': [
                    ('Ryan Gosling', 'K', 1),
                    ('Harrison Ford', 'Rick Deckard', 2),
                    ('Ana de Armas', 'Joi', 3),
                    ('Sylvia Hoeks', 'Luv', 4),
                ],
                'watch_links': [
                    ('Netflix', 'https://www.netflix.com'),
                    ('Apple TV+', 'https://tv.apple.com'),
                ],
                'reviews': [
                    (user3, 5, 'Roger Deakins cinematography in this film is pure art. A worthy successor to Ridley Scott classic.'),
                ]
            },
            {
                'title': 'Spider-Man: Across the Spider-Verse',
                'overview': 'Miles Morales catapults across the Multiverse, where he encounters a team of Spider-People charged with protecting its very existence. When the heroes clash on how to handle a new threat, Miles must redefine what it means to be a hero.',
                'release_year': 2023,
                'rating': 8.7,
                'runtime_minutes': 140,
                'language': 'en',
                'director': 'Joaquim Dos Santos, Kemp Powers',
                'poster_url': 'https://image.tmdb.org/t/p/w780/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg',
                'trailer_youtube_id': 'cqGjhVJWtEg',
                'genres': ['Animation', 'Action', 'Adventure', 'Sci-Fi'],
                'cast': [
                    ('Shameik Moore', 'Miles Morales', 1),
                    ('Hailee Steinfeld', 'Gwen Stacy', 2),
                    ('Oscar Isaac', 'Miguel O\'Hara', 3),
                    ('Daniel Kaluuya', 'Hobart "Hobie" Brown', 4),
                ],
                'watch_links': [
                    ('Netflix', 'https://www.netflix.com'),
                ],
                'reviews': [
                    (user2, 5, 'Visual animation revolution! Every single frame is rich with incredible artistic detail.'),
                ]
            },
            {
                'title': 'Parasite',
                'overview': 'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.',
                'release_year': 2019,
                'rating': 8.5,
                'runtime_minutes': 132,
                'language': 'ko',
                'director': 'Bong Joon Ho',
                'poster_url': 'https://image.tmdb.org/t/p/w780/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg',
                'trailer_youtube_id': '5xH0R_qt8BI',
                'genres': ['Drama', 'Thriller', 'Mystery'],
                'cast': [
                    ('Song Kang-ho', 'Kim Ki-taek', 1),
                    ('Lee Sun-kyun', 'Park Dong-ik', 2),
                    ('Cho Yeo-jeong', 'Choi Yeon-gyo', 3),
                    ('Choi Woo-shik', 'Kim Ki-woo', 4),
                ],
                'watch_links': [
                    ('Max', 'https://www.max.com'),
                    ('Prime Video', 'https://www.amazon.com/primevideo'),
                ],
                'reviews': [
                    (user, 5, 'Masterful pacing, sharp social commentary, and unexpected twists. Fully deserved all its Oscars.'),
                ]
            }
        ]

        created_count = 0
        for m in movies_data:
            movie, created = Movie.objects.update_or_create(
                title=m['title'],
                defaults={
                    'overview': m['overview'],
                    'release_year': m['release_year'],
                    'rating': m['rating'],
                    'runtime_minutes': m['runtime_minutes'],
                    'language': m['language'],
                    'director': m['director'],
                    'poster_url': m['poster_url'],
                    'trailer_youtube_id': m['trailer_youtube_id'],
                }
            )
            if created:
                created_count += 1

            # Assign genres
            movie.genres.clear()
            for gname in m['genres']:
                if gname in genres:
                    movie.genres.add(genres[gname])

            # Add cast
            movie.cast.all().delete()
            for actor, char, order in m['cast']:
                MovieCast.objects.create(
                    movie=movie,
                    actor_name=actor,
                    character_name=char,
                    cast_order=order
                )

            # Add watch links
            movie.watch_links.all().delete()
            for idx, (plat, url) in enumerate(m['watch_links']):
                MovieWatchLink.objects.create(
                    movie=movie,
                    platform_name=plat,
                    url=url,
                    sort_order=idx + 1
                )

            # Add reviews
            movie.reviews.all().delete()
            for rev_user, r_rating, r_comment in m['reviews']:
                Review.objects.create(
                    movie=movie,
                    user=rev_user,
                    rating=r_rating,
                    comment=r_comment
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(movies_data)} movies ({created_count} newly created).'))
