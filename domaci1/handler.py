from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

db_connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="admin"
)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/osobe', methods=['GET'])
def get_osobe():
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT id, ime, prezime, godine FROM osoba")
        rows = cursor.fetchall()

        osobe = []
        for row in rows:
            osoba = {
                'id': row[0],
                'ime': row[1],
                'prezime': row[2],
                'godine': row[3]
            }
            osobe.append(osoba)

        return jsonify(osobe)

    except psycopg2.Error as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500

    finally:
        cursor.close()


@app.route('/osoba', methods=['POST'])
def add_osoba():
    try:
        data = request.json
        ime = data['ime']
        prezime = data['prezime']
        godine = data['godine']

        cursor = db_connection.cursor()
        cursor.execute(
            "INSERT INTO osoba (ime, prezime, godine) VALUES (%s, %s, %s)", (ime, prezime, godine))
        db_connection.commit()

        return jsonify({'message': 'Osoba uspješno dodana'})

    except psycopg2.Error as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500

    finally:
        cursor.close()


@app.route('/osoba/<int:id>', methods=['DELETE'])
def delete_osoba(id):
    try:
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM osoba WHERE id = %s", (id,))
        db_connection.commit()

        return jsonify({'message': f'Osoba s ID-om {id} uspješno obrisana'})

    except psycopg2.Error as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500

    finally:
        cursor.close()


if __name__ == '__main__':
    app.run(debug=True)
