from flask import Flask, request, jsonify, send_file
import psycopg2
import os

app = Flask(__name__)

# link to PostgreSQL database
conn = psycopg2.connect(
    dbname="dccmj812eekhos",
    user="ucr5qdnoskkrji",
    password="p2c13e25424fdbed5e757c215849f436242d5ba41ab52438c42f457fc66e0b883",
    host="cdgn4ufq38ipd0.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com",
    port="5432"
)

# create connection instance
cur = conn.cursor()

# initiate the data base
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone_number VARCHAR(20) NOT NULL UNIQUE,
        status VARCHAR(20) CHECK (status IN ('failed', 'success', 'in_progress')),
        certificate VARCHAR(15) NOT NULL UNIQUE
    )
""")
conn.commit()

@app.route('/users', methods=['GET'])
def get_users():
    # 查询所有用户
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # 根据用户ID查询用户
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/')
def hello_world():
    return send_file('static/index.html')


@app.route('/users', methods=['POST'])
def create_user():
    # 创建新用户
    data = request.json
    name = data['name']
    phone_number = data['phone_number']
    status = data['status']
    certificate = data['certificate']
    cur.execute("INSERT INTO users (name, phone_number, status, certificate) VALUES (%s, %s, %s, %s) RETURNING id", (name, phone_number, status, certificate))
    new_user_id = cur.fetchone()[0]
    conn.commit()
    return jsonify({'message': 'User created', 'user_id': new_user_id}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # 更新用户信息
    data = request.json
    name = data['name']
    phone_number = data['phone_number']
    status = data['status']
    certificate = data['certificate']
    cur.execute("UPDATE users SET name = %s, phone_number = %s, status = %s, certificate = %s WHERE id = %s", (name, phone_number, status, certificate, user_id))
    conn.commit()
    return jsonify({'message': 'User updated'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # 删除用户
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    return jsonify({'message': 'User deleted'})

@app.route('/users/status/<phone_number>', methods=['GET'])
def get_user_status_by_phone_number(phone_number):
    cur.execute("SELECT status, certificate FROM users WHERE phone_number = %s", (phone_number,))
    user_status = cur.fetchone()
    if user_status:
        return jsonify({'status': user_status[0], 'certificate': user_status[1]}) # 返回 status 和 certificate
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/users/certificate/<certificate>', methods=['GET'])
def get_user_status_by_certificate(certificate):
    cur.execute("SELECT name, phone_number, status FROM users WHERE certificate = %s", (certificate,))
    user_info = cur.fetchone()
    if user_info:
        return jsonify({'name': user_info[0], 'phone_number': user_info[1], 'status': user_info[2]})
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)