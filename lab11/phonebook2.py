import psycopg2
import csv

def connect():
    return psycopg2.connect(
        host="localhost",
        database="suppliers",
        user="danelabyddin",
        password="2006"
    )

def create_table():
    sql = """
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            phone VARCHAR(20)
        );
    """
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
        print("Table created!")
    except Exception as e:
        print("Error creating table:", e)

def create_search_pattern():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE OR REPLACE FUNCTION search_pattern(pattern TEXT)
    RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
    BEGIN
        RETURN QUERY
        SELECT phonebook.id, phonebook.first_name, phonebook.phone
        FROM phonebook
        WHERE phonebook.first_name ILIKE '%' || pattern || '%'
           OR phonebook.phone LIKE '%' || pattern || '%';
    END;
    $$ LANGUAGE plpgsql;
    """)
    conn.commit()
    cur.close()
    conn.close()

def create_insert_update():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    DROP PROCEDURE IF EXISTS insert_update(VARCHAR, VARCHAR);
    CREATE OR REPLACE PROCEDURE insert_update(name_param VARCHAR, phone_param VARCHAR)
    AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = name_param) THEN
            UPDATE phonebook SET phone = phone_param WHERE first_name = name_param;
        ELSE
            INSERT INTO phonebook (first_name, phone) VALUES (name_param, phone_param);
        END IF;
    END;
    $$ LANGUAGE plpgsql;
    """)
    conn.commit()
    cur.close()
    conn.close()

def create_insert_many():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    DROP PROCEDURE IF EXISTS insert_many(TEXT[][]);
    CREATE OR REPLACE PROCEDURE insert_many(users TEXT[][])
    AS $$
    DECLARE
        user_record TEXT[];
    BEGIN
        FOREACH user_record SLICE 1 IN ARRAY users
        LOOP
            IF user_record[2] ~ '^\+?\d+$' THEN
                CALL insert_update(user_record[1], user_record[2]);
            ELSE
                RAISE NOTICE 'Invalid phone: %', user_record[2];
            END IF;
        END LOOP;
    END;
    $$ LANGUAGE plpgsql;
    """)
    conn.commit()
    cur.close()
    conn.close()

def create_get_paginated():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE OR REPLACE FUNCTION get_paginated(lim INT, offs INT)
    RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
    BEGIN
        RETURN QUERY
        SELECT phonebook.id, phonebook.first_name, phonebook.phone
        FROM phonebook
        ORDER BY phonebook.id
        LIMIT lim
        OFFSET offs;
    END;
    $$ LANGUAGE plpgsql;
    """)
    conn.commit()
    cur.close()
    conn.close()

def create_delete_user():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    DROP PROCEDURE IF EXISTS delete_user(VARCHAR, VARCHAR);
    CREATE OR REPLACE PROCEDURE delete_user(
        name_param VARCHAR DEFAULT NULL,
        phone_param VARCHAR DEFAULT NULL
    )
    AS $$
    BEGIN
        IF name_param IS NOT NULL THEN
            DELETE FROM phonebook WHERE first_name = name_param;
        END IF;
        IF phone_param IS NOT NULL THEN
            DELETE FROM phonebook WHERE phone = phone_param;
        END IF;
    END;
    $$ LANGUAGE plpgsql;
    """)
    conn.commit()
    cur.close()
    conn.close()

def load_data_from_csv():
    conn = connect()
    cur = conn.cursor()
    with open('/Users/danelabyddin/Documents/GitHub/PP2/lab11/data2.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute("CALL insert_update(%s, %s)", (row[0], row[1]))
    conn.commit()
    cur.close()
    conn.close()
    print("CSV data inserted!")

def test_calls():
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL insert_update('Тимур', '+77010009988');")

    users_list = [['1','Арман','+77017776655'], ['2','Санжар','+77018887766'], ['3','Ошибочный','123ABC']]
    cur.execute("CALL insert_many(%s);", (users_list,))

    cur.execute("SELECT * FROM search_pattern('Али');")

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.execute("SELECT * FROM get_paginated(5,0);")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.execute("CALL delete_user('Ошибочный', NULL);")
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_table()
    create_search_pattern()
    create_insert_update()
    create_insert_many()
    create_get_paginated()
    create_delete_user()
    load_data_from_csv()
    test_calls()
