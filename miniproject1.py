import sqlite3
import random
from getpass import getpass
from datetime import datetime
connection = None
cursor = None
session_no = 0

def connect (path):
    global connection, cursor, art_use_both, id, session_no
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    cursor.execute("SELECT * FROM users")
    connection.commit()
    return

def user_ID(ID,Password):
    global connection, cursor, art_use_both, id
    cursor.execute("SELECT u.uid FROM users u WHERE u.uid =:num AND u.pwd =:pw;", {'num':ID, 'pw':Password})
    connection.commit()
    return

def artist_ID(ID,Password):
    global connection, cursor, art_use_both, id
    cursor.execute("SELECT a.aid FROM artists a WHERE a.aid =:num AND a.pwd =:pw;", {'num':ID, 'pw':Password})
    connection.commit()
    return

def check_user_ID(ID):
    global connection, cursor, art_use_both, id
    cursor.execute("SELECT u.uid FROM users u WHERE u.uid =:num;", {'num':ID})
    connection.commit()
    return

def new_artist():
    global connection, cursor, art_use_both, id
    
    id = input("Enter id: ")
    nam = input("Name: ")
    nat = input("Nationality: ")
    pw = getpass("Password: ")
    cursor.execute("""INSERT INTO artists (aid, name, nationality, pwd) VALUES (?,?,?,?)""", (id,nam,nat,pw))
    connection.commit
    return

def new_user():
    global connection, cursor, art_use_both, id
    
    id = input("Enter id: ")
    nam = input("Name: ")
    pw = getpass("Password: ")
    check_user_ID(id)
    rows = cursor.fetchone()
    while(rows != None):
        print("User ID you entered is already taken please enter different user ID.")
        id = input("Enter id: ")
        check_user_ID(id)
        rows = cursor.fetchone()
    cursor.execute("""INSERT INTO users (uid, name, pwd) VALUES (?,?,?)""", (id,nam,pw))
    connection.commit
    return

def both_artuser(ID,Password):
    global connection, cursor, art_use_both, id
    cursor.execute("SELECT a.aid FROM artists a, users u WHERE a.aid =:num AND u.uid =:num AND a.pwd =:pw AND u.pwd =:pw;", {'num':ID, 'pw' :Password})
    connection.commit()
    return

def artist_user_ID():
    global connection, cursor, art_use_both, id
    
    artist_user_id = input("Please enter your user ID: ")
    artist_user_pwd = getpass("Please enter your password: ")
 
    both_artuser(artist_user_id,artist_user_pwd)
    rows = cursor.fetchone()
    if (rows != None):
        id = rows[0]
        art_use_both = "both"
        connection.commit
        return
    user_ID(artist_user_id,artist_user_pwd)
    rows = cursor.fetchone()
    if (rows != None):
        id = rows[0]
        art_use_both = "user"
        connection.commit
        return
    
    artist_ID(artist_user_id,artist_user_pwd)
    row = cursor.fetchone()
    if (row != None):
        id = row[0]
        art_use_both = "artist"
        connection.commit()
        return

    print("Entered user ID or/and password is incorrect.")
    create_account = input("If you are a new customer, Would you like to create a new account? Yes or No: ")
    if ((create_account.upper() == "NO")):
        connection.commit()
        return "NO"
    elif (create_account.upper() == "YES"):
        new_user()
        art_use_both = "user"
        connection.commit()
        return
    connection.commit()
    return
 
def top_three_user():
    global connection, cursor, art_use_both, id   
    cursor.execute("WITH user_duration (uid, aid, duration) AS (SELECT l.uid, a.aid, SUM(l.cnt*s.duration) FROM listen l, artists a, perform p, songs s WHERE l.sid = p.sid AND p.aid = a.aid AND a.aid =:num AND p.sid = s.sid GROUP BY l.uid, a.aid) SELECT ud.uid FROM user_duration ud WHERE (SELECT COUNT(udd.duration) FROM user_duration udd WHERE (udd.duration >= ud.duration))<=3;", {'num':id})
    connection.commit()
    return

def check_song(title, duration):
    global connection, cursor, art_use_both, id
    cursor.execute("SELECT s.sid FROM songs s WHERE s.title =:ti AND s.duration =:du", {'ti':title, 'du':duration})
    connection.commit()
    return

def add_song():
    global connection, cursor, art_use_both, id
    song_id = random.randint(0,1000)
    title = input("Please enter title of your song: ") 
    duration = input("Please enter duration of your song: ")
    check_song(title,duration) 
    row = cursor.fetchone()
    if (row != None):
        print("The song that you are trying to add already exist in the database.")
        connection.commit()
        return
    cursor.execute("""INSERT INTO songs (sid, title, duration) VALUES (?,?,?)""", (song_id,title,duration))
    cursor.execute("""INSERT INTO perform (aid, sid) VALUES (?,?)""", (id,song_id))
    while True:
        try:
            other_artist = int(input("Please enter how many artist contributed in creating this song other than your self: "))
            break
        except:
            print("Please enter integer value only.")
    if (other_artist == 0):
        connection.commit()
        return
    for x in range(other_artist):
        artist_id = input("Please enter artist id: ")
        cursor.execute("""INSERT INTO perform (aid, sid) VALUES (?,?)""", (artist_id,song_id))
    
    connection.commit()
    return


def artist_login():
    global connection, cursor, art_use_both, id
    while True:
        try:
            in_int = int(input("How many of the following option you want to access 1) ADD NEW SONG, 2) GET TOP THREE USERS, 0) go to main screen? "))
            break
        except:
            print("Please enter integer value only.")
    if (in_int == 0):
        connection.commit()
        return
    for x in range(in_int):
        while True:
           try:
               in_put = input("Please select one of the follwing option 1) ADD NEW SONG, 2) GET TOP THREE USERS: ")
               break
           except:
               print("Please enter integer value only.")
        if (in_put == "1"):
            add_song()
        elif(in_put == "2"):
            top_three_user()
            print("[uid]")
            rows = cursor.fetchall()
            for each in rows:
                print(each["uid"])
    connection.commit()
    return

def start_session():
    global connection, cursor, art_use_both, id, session_no
    cur_date = datetime.now()
    session_no = random.randint(1,1000)
    end_date = "Null"
    cursor.execute("""INSERT or REPLACE INTO sessions (uid,sno,start,end) VALUES (?,?,?,?)""", (id,session_no,cur_date,end_date))
    connection.commit()
    return

def end_session():
    global connection, cursor, art_use_both, id, session_no
    cur_date = datetime.now()
    cursor.execute("UPDATE sessions SET end =:da  WHERE sno=:num;", {'da':cur_date, 'num':session_no})
    session_no = 0
    connection.commit()
    return
   
def check_keyword_table(ne_id):
    global connection, cursor, art_use_both, id, session_no
    cursor.execute("SELECT kt.id FROM keyword_table kt WHERE kt.id=:num;", {'num':ne_id})
    rows = cursor.fetchone()
    if (rows != None): 
        cursor.execute("UPDATE keyword_table SET cnt= (cnt+1) WHERE id=:nu;", {'nu':ne_id})
        connection.commit()
        return "true"
    connection.commit()
    return "false"

def check_keywords(keyword,a):
    global connection, cursor, art_use_both, id, session_no
    key = "%" + keyword + "%"
    song = "Song"
    playlist = "Playlist"
    cursor.execute("SELECT :son AS typ, s.sid AS id, s.title, s.duration FROM songs s WHERE s.title LIKE :num UNION SELECT :play AS typ, p.pid AS id, p.title, SUM(s.duration) FROM playlists p, plinclude pd, songs s WHERE p.title LIKE :num AND p.pid = pd.pid AND pd.sid = s.sid GROUP BY p.pid, p.title;", {'son':song, 'play':playlist, 'num':key})
    
    rows = cursor.fetchall()
    torf = "false"
    for each in rows:
        if (a != 0):
            torf = check_keyword_table(each["id"])
        x = 1
        if (torf == "false"):
            cursor.execute("""INSERT or IGNORE INTO keyword_table (typ,id,title,duration,cnt) VALUES (?,?,?,?,?)""", (each["typ"], each["id"], each["title"], each["duration"], x))
    connection.commit()
    return
    
def check_listen(song_id):
    global connection, cursor, art_use_both, id, session_no
    cursor.execute("SELECT l.uid FROM listen l WHERE l.uid =:n AND l.sno =:nu AND l.sid =:num;", {'n':id, 'nu':session_no, 'num':song_id})
    rows = cursor.fetchone()
    if (rows != None):
        cursor.execute("UPDATE listen SET cnt=(cnt+1) WHERE uid=:n AND sno=:nu AND sid=:num;", {'n':id, 'nu':session_no, 'num':song_id})
    else:
        cursor.execute("""INSERT or REPLACE INTO listen (uid,sno,sid,cnt) VALUES (?,?,?,?)""", (id,session_no,song_id,1))
    connection.commit()
    return

def song_info(song_id):
    global connection, cursor, art_use_both, id, session_no
    cursor.execute("SELECT a.name, s.sid, s.title, s.duration FROM artists a, perform p, songs s WHERE s.sid=:num AND s.sid = p.sid AND p.aid = a.aid;", {'num':song_id})
    rows = cursor.fetchall()
    for each in rows:
        print(each["name"], each["sid"], each["title"], each["duration"])
    cursor.execute("SELECT p.title FROM playlists p, plinclude pd WHERE pd.sid=:num AND pd.pid = p.pid;", {'num':song_id})
    rows = cursor.fetchall()
    for each in rows:
        print(each["title"])
    connection.commit()
    return

def add_playlist(song_id):
    global connection, cursor, art_use_both, id, session_no
    cursor.execute("SELECT p.pid FROM playlists p WHERE p.uid=:num;", {'num':id})
    rows = cursor.fetchall()
    if (rows != None):
        for each in rows:
            cursor.execute("""INSERT or REPLACE INTO plinclude (pid,sid,sorder) VALUES (?,?,?)""", (each["pid"], song_id, 1))
    else:
        play_id = random.randint(0,1000)
        name = input("Please enter title of your new playlist: ")
        cursor.execute("""INSERT or REPLACE INTO playlists (pid,title,uid) VALUES (?,?,?)""", (play_id, name, id))
        cursor.execute("""INSERT or REPLACE INTO plinclude (pid,sid,sorder) VALUES (?,?,?)""", (play_id, song_id, 1))   
    connection.commit()
    return

def song_option(song_id):
    global connection, cursor, art_use_both, id, session_no
    while True:
        try:
            so_op = int(input("How many of the following options you want to perform. 1) listen to it, 2) see more information about it, 3) add it to a playlist or 0) go to main page: "))
            break
        except:
            print("Please enter integer value only.")
    if (so_op == 0):
        connection.commit()
        return
    for i in range(so_op):
        while True:
           try:
               son_opt = int(input("Please select one of the following options 1) listen to it, 2) see more information about it, 3) add it to a playlist " ))
               break
           except:
               print("Please enter integer value only.")
        if (son_opt == 1):
            if (session_no == 0):
                start_session()  
            check_listen(song_id)
        elif(son_opt == 2):
            song_info(song_id) 
        elif(son_opt == 3):
            add_playlist(song_id)
    connection.commit()
    return

def check_playlist(playlist_id):
    global connection, cursor, art_use_both, id, session_no
    cursor.execute("SELECT p.pid FROM playlists p WHERE p.pid =:num;", {'num':playlist_id})
    connection.commit()
    return

def user_keyword():
    global connection, cursor, art_use_both, id, session_no
    key_word = input("Please enter keyword that you want to search for: ")
    key_wor = key_word.split()
    num_key = len(key_wor)
    for x in range(num_key):
        check_keywords(key_wor[x], x)
    cursor.execute("SELECT kt.typ, kt.id, kt.title, kt.duration FROM keyword_table kt ORDER BY kt.cnt DESC")
    rows = cursor.fetchall()
    t_or_f = True
    legth = len(rows)
    x = 0
    xx = 0
    while t_or_f:
        for i in range(5):
            if (legth > xx):
                each = rows[xx]
            else:
                break
            print(each["typ"], each["id"], each["title"], each["duration"])
            xx = xx + 1
        x = x+5
        if (legth <= x):
            t_or_f = False
        us_in = input("Would you like to see more artits? Yes or No? ")
        if (us_in.upper() == "NO"):
            t_or_f = False
    
    acces = input("Please enter do you want to access playlist or song: ")
    if(acces.upper() == "SONG"):
        while True:
            try:
                song_playlist = int(input("Please enter id of a song that you want to select: "))
                break
            except: 
                print("Please enter integer value only.")
        song_option(song_playlist)
        connection.commit()
        return
    while True:
       try:
           song_playlist = int(input("Please input playlist id that you want to access: "))
           break
       except:
           print("Please enter integer value only.")
    check_playlist(song_playlist)
    rows = cursor.fetchone()
    if (rows != None):
        cursor.execute("SELECT s.sid, s.title, s.duration FROM playlists p, plinclude pd, songs s WHERE p.pid =:num AND p.pid = pd.pid AND pd.sid = s.sid;", {'num':rows[0]})
        rows = cursor.fetchall()
        for each in rows:
            print(each["sid"], each["title"], each["duration"])
    while True:
        try:
            song_playlist = int(input("Please enter id of a song that you want to select: "))
            break
        except:
            print("Please enter integer value only.")
    song_option(song_playlist)
        
    connection.commit()
    return

def create_table():
    global connection, cursor, art_use_both, id, session_no
    cursor.execute("DROP TABLE IF EXISTS keyword_table;")
    cursor.execute('''
		CREATE TABLE keyword_table(
			typ TEXT,
			id TEXT,
			title TEXT,
			duration INT,
                        cnt INT,
			PRIMARY KEY (id)
		);
	''')
    cursor.execute("DROP TABLE IF EXISTS artist_table;")
    cursor.execute('''
                CREATE TABLE artist_table(
                        aid TEXT,
                        name TEXT,
                        nationality TEXT,
                        cnt INT,
                        PRIMARY KEY (aid)
                );
        ''')
    connection.commit()
    return

def check_artist_table(ar_id):
    global connection, cursor, art_use_both, id, session_no
    cursor.execute("SELECT at.aid FROM artist_table at WHERE at.aid=:num;", {'num':ar_id})
    ro = cursor.fetchone()
    if (ro != None):
        cursor.execute("UPDATE artist_table SET cnt=(cnt+1) WHERE aid=:num;", {'num':ar_id})
    connection.commit()
    return "false"

def check_key(keyword,a):
    global connection, cursor, art_use_both, id, session_no
    key = "%" + keyword + "%"
    cursor.execute("SELECT a.aid FROM artists a WHERE a.name LIKE :num UNION SELECT a.aid FROM artists a, songs s, perform p WHERE s.title LIKE :num AND s.sid = p.sid AND p.aid = a.aid;", {'num':key})
    row = cursor.fetchall()
    for each in row:
        cursor.execute("SELECT a.aid, a.name, a.nationality, COUNT(p.sid) FROM artists a, perform p WHERE a.aid =:num AND a.aid = p.aid;", {'num':each["aid"]})
        rows = cursor.fetchone()
        torf = "false"
        if (a != 0): 
            torf = check_artist_table(rows[0])
        if (torf == "false"):
            cursor.execute("""INSERT or REPLACE INTO artist_table (aid, name, nationality, cnt) VALUES (?,?,?,?)""", (rows[0], rows[1], rows[2], rows[3])) 
    connection.commit()
    return

def artist_key():
    global connection, cursor, art_use_both, id, session_no
    key_word = input("Please enter keyword that you want to search for: ")
    key_wor = key_word.split()
    num_key = len(key_wor)
    for x in range(num_key):
        check_key(key_wor[x], x)
   
    cursor.execute("SELECT at.name, at.nationality, at.cnt FROM artist_table at ORDER BY at.cnt DESC")
    rows = cursor.fetchall()
    t_or_f = True
    legth = len(rows)
    x = 0
    xx = 0
    while t_or_f: 
        for i in range(5):
            if (legth > xx):
                each = rows[xx]
            else:    
                break
            print(each["name"], each["nationality"], each["cnt"])
            xx = xx + 1
        x = x+5
        if (legth <= x):
            t_or_f = False
        us_in = input("Would you like to see more artits? Yes or No? ")
        if (us_in.upper() == "NO"):
            t_or_f = False
    
    son = input("PLease input artist id whose information that you want to access: ")
    cursor.execute("SELECT s.sid, s.title, s.duration FROM artists a, perform p, songs s WHERE a.name =:num AND a.aid = p.aid AND p.sid = s.sid;", {'num':son})
    rows = cursor.fetchall()
    for each in rows:
        print(each["sid"], each["title"], each["duration"])
    son_id = int(input("Please enter the id of a song that you want to select: "))
    song_option(son_id)
    connection.commit()
    return

def user_login():
    global connection, cursor, art_use_both, id, session_no
    while True:
        try: 
            user_inp = int(input("Please select how many of task you want to perform from following list: 1) Start session, 2) Seach for songs and playlists, 3) Seach for artists, 4) End session or 0) go to main page: "))
            break
        except:
            print("Please enter integer value only.")
    if (user_inp == 0):
       connection.commit()
       return
    user_i = 0
    create_table()
    torf = True
    for i in range(user_inp):
        while True:
            try:
                user_i = int(input("Please select one of the following task: 1) Start session, 2) Seach for songs and playlists, 3) Seach for artists, 4) End session: "))
                break
            except:
                print("Please enter integer value only.")
        if (user_i == 1):
            start_session()
        elif (user_i == 2):
            user_keyword()
        elif (user_i == 3):
            artist_key()
        elif (user_i == 4):
            end_session()
    if (session_no != 0):
        end_session()
    connection.commit()
    return

def main_call():
    global connection, cursor, art_use_both, id, session_no
    a = artist_user_ID()
    if (a == "NO"):
        connection.commit()
        return "NO"
    if (art_use_both == "both"):
        in_put = input("Would you like to login as user or artist? ")
        if (in_put.upper() == "ARTIST"):
            artist_login()
        elif (in_put.upper() == "USER"):
            user_login()
    elif (art_use_both == "artist"):
        artist_login()
    elif (art_use_both == "user"):
        user_login()
    connection.commit()
    return

def main():
    global connection, cursor, art_use_both, id, session_no
    
    database = input("Please the name of Data Base that you want work on: ")
    path = "./" + database +".db"
    connect(path)
    
    a = main_call()
    if (a == "NO"):
        connection.commit()
        connection.close()
        return
    t_o_f = True
    while t_o_f:
        in_put = input("Would you like to LogOut or exit from the program? ")
        if (in_put.upper() == "LOGOUT"):
            main_call()
        else:
            t_o_f = False


    connection.commit()
    connection.close()
    return

if __name__ == "__main__":
    main()
