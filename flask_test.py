from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# 连接到 PostgreSQL 数据库
conn = psycopg2.connect(
    dbname="dccmj812eekhos",
    user="ucr5qdnoskkrji",
    password="p2c13e25424fdbed5e757c215849f436242d5ba41ab52438c42f457fc66e0b883",
    host="cdgn4ufq38ipd0.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com",
    port="5432"
)

# 创建游标对象
cur = conn.cursor()

# 初始化数据库表格
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone_number VARCHAR(20) NOT NULL UNIQUE,
        status VARCHAR(20) CHECK (status IN ('failed', 'success', 'in_progress'))
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

@app.route('/users', methods=['POST'])
def create_user():
    # 创建新用户
    data = request.json
    name = data['name']
    phone_number = data['phone_number']
    status = data['status']
    cur.execute("INSERT INTO users (name, phone_number, status) VALUES (%s, %s, %s) RETURNING id", (name, phone_number, status))
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
    cur.execute("UPDATE users SET name = %s, phone_number = %s, status = %s WHERE id = %s", (name, phone_number, status, user_id))
    conn.commit()
    return jsonify({'message': 'User updated'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # 删除用户
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    return jsonify({'message': 'User deleted'})

@app.route('/users/status/<phone_number>', methods=['GET'])
def get_user_status(phone_number):
    # 根据电话号码查询用户状态
    cur.execute("SELECT status FROM users WHERE phone_number = %s", (phone_number,))
    user_status = cur.fetchone()
    if user_status:
        return jsonify({'status': user_status[0]})
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)