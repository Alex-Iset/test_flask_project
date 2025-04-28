from psycopg.rows import dict_row


class UserRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM users")
            return [dict(row) for row in cur]

    def find(self, id):
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM users WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_by_term(self, search_term=""):
        with self.conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                    SELECT * FROM users
                    WHERE username ILIKE %s
                """,
                (f"%{search_term}%",),
            )
            return cur.fetchall()

    def save(self, user):
        if "id" in user and user["id"]:
            self._update(user)
        else:
            self._create(user)

    def _update(self, user):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET username = %s, email = %s WHERE id = %s",
                (user["username"], user["email"], user["id"]),
            )
        self.conn.commit()

    def _create(self, user):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id",
                (user["username"], user["email"]),
            )
            id = cur.fetchone()[0]
            user["id"] = id
        self.conn.commit()

    def destroy(self, user):
        with self.conn.cursor() as cur:
            cur.execute(
                "DELETE FROM users WHERE id = %s AND username = %s AND email = %s",
                (user["id"], user['username'], user['email']),
            )
        self.conn.commit()