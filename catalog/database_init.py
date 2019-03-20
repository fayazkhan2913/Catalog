from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from Data_Setup import *

engine = create_engine('sqlite:///movies.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Delete MovieGenre if exisitng.
session.query(MovieGenre).delete()
# Delete MovieName if exisitng.
session.query(MovieName).delete()
# Delete User if exisitng.
session.query(User).delete()

# Create sample users data
User1 = User(name="Fayaz Khan",
             email="fayazkhan2913@gmail.com",
             picture='http://content.gulte.com/'
             'content/2018/05/news/1525341947-1390.jpg')
session.add(User1)
session.commit()
print ("Successfully Added First User")
# Create moviegenres
MovieGenre1 = MovieGenre(name="ACTION",
                         user_id=1)
session.add(MovieGenre1)
session.commit()

MovieGenre2 = MovieGenre(name="HORROR",
                         user_id=1)
session.add(MovieGenre2)
session.commit()

MovieGenre3 = MovieGenre(name="ROMANCE",
                         user_id=1)
session.add(MovieGenre3)
session.commit()

MovieGenre4 = MovieGenre(name="SCI-FI",
                         user_id=1)
session.add(MovieGenre4)
session.commit()

MovieGenre5 = MovieGenre(name="COMEDY",
                         user_id=1)
session.add(MovieGenre5)
session.commit()

MovieGenre6 = MovieGenre(name="THRILLER",
                         user_id=1)
session.add(MovieGenre6)
session.commit()

# Enter Movie Name related to the Movie Genres
# Give The Details as per the columns in the 'moviename' table
Movie1 = MovieName(poster="https://www.glamsham.com/Uploads/"
                   "article/kgf-0976139001542969729.jpeg",
                   name="KGF",
                   year="2018",
                   rating="8.6",
                   budget="50-80cr",
                   gross="250cr",
                   date=datetime.datetime.now(),
                   moviegenreid=1,
                   user_id=1)
session.add(Movie1)
session.commit()

Movie2 = MovieName(poster="https://m.media-amazon.com/images/M/"
                   "MV5BZmJiZTIwYzktZDQyMi00OWYzLTliZDEtOTAzYmNjNjZjNTl"
                   "lXkEyXkFqcGdeQXVyMjMyNjkwMTY@._V1_"
                   "UY268_CR2,0,182,268_AL_.jpg",
                   name="OKKADU",
                   year="2003",
                   rating="8.1",
                   budget="8cr",
                   gross="32cr",
                   date=datetime.datetime.now(),
                   moviegenreid=1,
                   user_id=1)
session.add(Movie2)
session.commit()

Movie3 = MovieName(poster="https://upload.wikimedia.org/"
                   "wikipedia/en/thumb/0/07/"
                   "Raju_Gari_Gadhi_Telugu_Posters.jpg/"
                   "220px-Raju_Gari_Gadhi_Telugu_Posters.jpg",
                   name="RAJU GARI GADHI",
                   year="2015",
                   rating="6.6",
                   budget="3cr",
                   gross="25cr",
                   date=datetime.datetime.now(),
                   moviegenreid=2,
                   user_id=1)
session.add(Movie3)
session.commit()

Movie4 = MovieName(poster="https://upload.wikimedia.org/wikipedia/en/e/eb/"
                   "Prema_Katha_Chithram_Poster.jpg",
                   name="PREMA KATHA CHITRAM",
                   year="2013",
                   rating="7.4",
                   budget="5cr",
                   gross="29cr",
                   date=datetime.datetime.now(),
                   moviegenreid=2,
                   user_id=1)
session.add(Movie4)
session.commit()

Movie5 = MovieName(poster="https://images-na.ssl-images-amazon.com/"
                   "images/I/91X1PmwPjkL._RI_.jpg",
                   name="ARJUN REDDY",
                   year="2017",
                   rating="8.5",
                   budget="12cr",
                   gross="51cr",
                   date=datetime.datetime.now(),
                   moviegenreid=3,
                   user_id=1)
session.add(Movie5)
session.commit()

Movie6 = MovieName(poster="http://datastore04.rediff.com/h1500-w1500/thumb/"
                   "69586A645B6D2A2E3131/"
                   "c018gvx97vrg5mww.D.0.Tholi-Prema-Movie-Poster--3-.jpg",
                   name="THOLI PREMA",
                   year="2018",
                   rating="7.4",
                   budget="15cr",
                   gross="40cr",
                   date=datetime.datetime.now(),
                   moviegenreid=3,
                   user_id=1)
session.add(Movie6)
session.commit()

Movie7 = MovieName(poster="https://smedia2.intoday.in/btmt/images/"
                   "stories/20gjhgj-660_112918050831_112918072052.jpg",
                   name="ROBO 2.0",
                   year="2018",
                   rating="7",
                   budget="543cr",
                   gross="800cr",
                   date=datetime.datetime.now(),
                   moviegenreid=4,
                   user_id=1)
session.add(Movie7)
session.commit()

Movie8 = MovieName(poster="https://www.filmibeat.com/img/220x100x275/popcorn/"
                   "movie_posters/24-20160502145124-15027.jpg",
                   name="24",
                   year="2016",
                   rating="7.9",
                   budget="70cr",
                   gross="100cr",
                   date=datetime.datetime.now(),
                   moviegenreid=4,
                   user_id=1)
session.add(Movie8)
session.commit()

Movie9 = MovieName(poster="http://media.webdunia.com/_media/te/img/"
                   "photo-gallery/cinema-hero-s/f2-movie-new-poster-and-photo/"
                   "full/f2-movie-new-poster-and-photo-15441740358161.jpg",
                   name="F2: FUN AND FRUSTRATION",
                   year="2019",
                   rating="6.6",
                   budget="24cr",
                   gross="140cr",
                   date=datetime.datetime.now(),
                   moviegenreid=5,
                   user_id=1)
session.add(Movie9)
session.commit()

Movie10 = MovieName(poster="https://upload.wikimedia.org/wikipedia/en/thumb/"
                    "1/13/Raja_the_Great.jpg/220px-Raja_the_Great.jpg",
                    name="RAJA THE GREAT",
                    year="2016",
                    rating="7.8",
                    budget="23cr",
                    gross="45cr",
                    date=datetime.datetime.now(),
                    moviegenreid=5,
                    user_id=1)
session.add(Movie10)
session.commit()

Movie11 = MovieName(poster="https://content.gulte.com/content/2018/08/"
                    "moviereviews/Movie-Review--Goodachari--1099.jpg",
                    name="GOODACHARI",
                    year="2018",
                    rating="7.9",
                    budget="6cr",
                    gross="35cr",
                    date=datetime.datetime.now(),
                    moviegenreid=6,
                    user_id=1)
session.add(Movie11)
session.commit()

Movie12 = MovieName(poster="http://2.bp.blogspot.com/-NO4a1F7oyi0/UsA29LpuBLI/"
                    "AAAAAAAAAzs/-j5m__HXRxE/s1600/"
                    "ONE+NENOKKADINE+LATEST+POSTERS+BFA+(1).jpg",
                    name="1 NENOKKADINE",
                    year="2014",
                    rating="8.3",
                    budget="70cr",
                    gross="72cr",
                    date=datetime.datetime.now(),
                    moviegenreid=6,
                    user_id=1)
session.add(Movie12)
session.commit()

print("Your details in the movies database has been successfully inserted!!!")
