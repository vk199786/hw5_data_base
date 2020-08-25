import sqlalchemy
import psycopg2

engine = sqlalchemy.create_engine('postgresql://postgres:vk199786@localhost:5432/Netology 2')
#print(engine.table_names())
connection = engine.connect()

#количество исполнителей в каждом жанре;

sel = connection.execute("""SELECT COUNT(*) FROM Artist_Genre;""").fetchall()
print(sel)

#количество треков, вошедших в альбомы 2019-2020 годов;

sel2 = connection.execute("""SELECT COUNT(Track.name) FROM Track 
JOIN Album ON Track.album_id = Album.id
WHERE Album.year BETWEEN 2019 and 2020;""").fetchall()
print(sel2) #В базе данных таких альбомов нет

#средняя продолжительность треков по каждому альбому;

sel3 = connection.execute("""SELECT AVG(duration) FROM Track 
JOIN Album ON Track.album_id = Album.id
GROUP BY Album;""").fetchall()
print(sel3)

#все исполнители, которые не выпустили альбомы в 2020 году;

sel4 = connection.execute("""SELECT Artist.name FROM Artist
JOIN Artist_Album ON Artist.id = Artist_Album.album_id
JOIN Album ON Artist_Album.album_id = Album.id
WHERE year = 2020;""").fetchall() #В базе данных таких исполнителей нет
print(sel4)

#названия сборников, в которых присутствует конкретный исполнитель (выберите сами);

sel5 = connection.execute("""SELECT Collection.name FROM Collection 
JOIN Collection_Track ON Collection.id = Collection_Track.track_id
JOIN Track ON Collection_Track.track_id = Track.id
JOIN Album ON Track.id = Album.id
JOIN Artist_Album ON Album.id = Artist_Album.artist_id
JOIN Artist ON Artist_Album.artist_id = Artist.id
WHERE Artist.name LIKE '%%Kurt%%';""").fetchall()
print(sel5)

#название альбомов, в которых присутствуют исполнители более 1 жанра;

sel6 = connection.execute("""SELECT Album.name FROM Album
JOIN Artist_Album ON Album.id = Artist_Album.artist_id
JOIN Artist ON Artist_Album.artist_id = Artist.id
JOIN Artist_Genre ON Artist.id = genre_id 
WHERE genre_id  >= 2;""").fetchall()
print(sel6)

#наименование треков, которые не входят в сборники;

sel7 = connection.execute("""SELECT Track.name FROM Track
JOIN Collection_Track ON Track.id = Collection_Track.track_id
JOIN Collection ON Collection_Track.track_id = Collection.id
WHERE Track.id NOT IN (Collection.id)
;""").fetchall()
print(sel7)

#исполнителя(-ей), написавшего самый короткий по продолжительности трек
#(теоретически таких треков может быть несколько);

sel8_1 = connection.execute("""SELECT Artist.name FROM Artist
JOIN Artist_Album ON Artist.id = Artist_Album.album_id
JOIN Album ON Artist_Album.album_id = Album.id
JOIN Track ON  Album.id = Track.album_id 
WHERE Track.duration = (
SELECT MAX(Track.duration) from Track);""").fetchall()
print(sel8_1) #В моей базе данных, максимальна длительность трека это 4

sel8_2 = connection.execute("""SELECT Artist.name FROM Artist
JOIN Artist_Album ON Artist.id = Artist_Album.album_id
JOIN Album ON Artist_Album.album_id = Album.id
JOIN Track ON  Album.id = Track.album_id 
WHERE Track.duration = (
SELECT MIN(Track.duration) FROM Track);""").fetchall()
print(sel8_2) #В моей базе данных, минимальная длительность трека это 3

#название альбомов, содержащих наименьшее количество треков.

sel9 = connection.execute("""SELECT Album.name FROM Album
JOIN Track ON Album.id = Track.album_id
ORDER BY Track.id DESC
LIMIT 1;""").fetchall()
print(sel9)
