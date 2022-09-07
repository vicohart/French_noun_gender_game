import sqlite3
from constants import DATABASE, PLAYER_ID

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn


def select_next_word_collection(conn, player_id, size):
    cur = conn.cursor()
    cur.execute(
        '''SELECT rank, word, gender FROM main m 
        LEFT JOIN finalized f ON m.rank = f.word_id
        WHERE F.word_id IS NULL OR f.player_id != ?
        LIMIT ?''', 
        (player_id, size,)
        )

    words = cur.fetchall()

    return words


def get_word_collection(PLAYER_ID, WORD_COLLECTION_SIZE):
    conn = create_connection(DATABASE)
    word_collection = select_next_word_collection(conn, PLAYER_ID, WORD_COLLECTION_SIZE)
    conn.close

    return word_collection


def insert_attempt_data(PLAYER_ID, word_id, answer_is_correct, today):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute(
        '''INSERT into attempts (player_id, word_id, correct, date)
        VALUES (?, ?, ?, ?)''',
        (PLAYER_ID, word_id, answer_is_correct, today)
    )
    conn.commit()
    conn.close()


def save_game(PLAYER_ID, WORDS_PER_GAME, score, day, duration):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute(
        '''SELECT id FROM attempts
        WHERE player_id = ?
        ORDER BY id DESC LIMIT ?''',
        (PLAYER_ID, 1)
    )
    
    last_attempt = cur.fetchall()[0][0]
    first_attempt = last_attempt - WORDS_PER_GAME + 1

    cur.execute(
        '''INSERT into games (player_id, attempts_id_start, attempts_id_end, score, date, duration)
        VALUES (?, ?, ?, ?, ?, ?)''',
        (PLAYER_ID, first_attempt, last_attempt, score, day, duration)
    )

    conn.commit()
    conn.close()


def update_finalized(PLAYER_ID, WORDS_PER_GAME, day):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute(
        '''SELECT word_id, correct FROM attempts
        WHERE player_id = ?
        ORDER BY id DESC LIMIT ?''',
        (PLAYER_ID, 1000)
    )

    latest_attempts = cur.fetchall()

    words_to_check_dict = {attempt[0]: {'checking': True, 'streak': 0} for attempt in latest_attempts[:WORDS_PER_GAME]}

    keep_checking = True
    for (word_id, correct) in latest_attempts:
        if word_id not in words_to_check_dict:
            continue

        if keep_checking:
            if correct:
                words_to_check_dict[word_id]['streak'] += 1
            else:
                words_to_check_dict[word_id]['checking'] = False

            keep_checking = False
            for word_entry in words_to_check_dict.values():
                if word_entry['checking']:
                    keep_checking = True
        else:
            break
    
    finalized = [word_id for word_id, entry in words_to_check_dict.items() if entry['streak'] >= 4]

    for word_id in finalized:
        cur.execute(
            '''INSERT into finalized (player_id, word_id, date)
            VALUES (?, ?, ?)''',
            (PLAYER_ID, word_id, day)
        )
    
    conn.commit()
    conn.close()


def get_level(PLAYER_ID):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute(
        '''SELECT word_id FROM finalized
        WHERE player_id = ?
        ORDER BY id DESC LIMIT ?''',
        (PLAYER_ID, 10)
    )
    
    latest_finalized = cur.fetchall()
    avg_recent_finalized = sum([value[0] for value in latest_finalized]) / 10
    
    current_level = int((avg_recent_finalized - 100) // 1000 + 1)

    return current_level