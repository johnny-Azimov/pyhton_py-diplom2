import psycopg2 as pg

def create_db():
    with pg.connect(
        dbname='d2',
        user='d2', 
        password='d2') as conn:
        print("Database opened successfully")
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS users (
                id serial PRIMARY KEY,
                vk_id integer
                )
                """)
            cur.execute("""CREATE TABLE IF NOT EXISTS users_matches (
                id serial PRIMARY KEY,
                user_id integer REFERENCES users(id),
                vk_url varchar(100)
                )
                """)
            cur.execute("""CREATE TABLE IF NOT EXISTS matches_photos (
                id serial PRIMARY KEY,
                user_id integer REFERENCES users_matches(id),
                photo_url text
                )
                """)
            print("Table created successfully")


def check_tables():
    with pg.connect(
        dbname='d2',
        user='d2', 
        password='d2') as conn:
        with conn.cursor() as cur:
            cur.execute("select * from pg_tables where tablename = 'users'")
            users_table = cur.fetchone()
            cur.execute("select * from pg_tables where tablename = 'users_matches'")
            users_matches_table = cur.fetchone()
            cur.execute("select * from pg_tables where tablename = 'matches_photos'")
            matches_photos_table = cur.fetchone()

            if users_table and users_matches_table and matches_photos_table:
                    return True


def add_user(user_vk_id):
    with pg.connect(
        dbname='d2',
        user='d2', 
        password='d2') as conn:
        with conn.cursor() as cur:
            cur.execute("""insert into users (vk_id) values (%s) RETURNING id""", (user_vk_id,))
            res = cur.fetchone()
            last_id = res[0]
            conn.commit()
            print("User added successfully")
            return last_id


def add_match(user_id, match_vk_url):
    with pg.connect(
        dbname='d2',
        user='d2', 
        password='d2') as conn:
        with conn.cursor() as cur:
            cur.execute("""insert into users_matches (user_id, vk_url) values (%s, %s) RETURNING id""", (user_id, match_vk_url))
            res = cur.fetchone()
            last_id = res[0]
            conn.commit()
            print("Matching user added successfully")
            return last_id


def add_match_photos(match_id, photo_url):
    with pg.connect(
        dbname='d2',
        user='d2', 
        password='d2') as conn:
        with conn.cursor() as cur:
            cur.execute("""insert into matches_photos (match_id, photo_url) values (%s, %s) RETURNING id""", (match_id, photo_url))
            res = cur.fetchone()
            conn.commit()
            print("Photo added successfully")


def get_user_matches(user_id):
    with pg.connect(
        dbname='d2',
        user='d2', 
        password='d2') as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT users_matches.vk_url, matches_photos.photo_url FROM matches_photos join users_matches on users_matches.id = matches_photos.match_id join users on users.id = users_matches.user_id WHERE users.id = %s""" % (
                    user_id))
            print(cur.fetchall())


def write_db_output(account, output):
    with pg.connect(
        dbname='d2',
        user='d2', 
        password='d2') as conn:
        with conn.cursor() as cur:
            last_id = add_user(account)
            for match in output:
                match_id = add_match(last_id, match['vk_link'])
                for photo in match['photos']:
                    add_match_photos(match_id, photo)

