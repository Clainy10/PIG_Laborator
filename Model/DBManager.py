import psycopg2
from typing import List, Dict, Any

class DatabaseManager:
    def __init__(self, dbname: str = "SuperDBPietrePro2026_db", user: str = "postgres", password: str = "Clainy", host: str = "localhost", port: int = 5432) -> None:
        self.conn_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }
        self.initializeaza_tabela()

    def _conectare(self):
        return psycopg2.connect(**self.conn_params)

    def initializeaza_tabela(self) -> None:
        with self._conectare() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS pietre (
                        id SERIAL PRIMARY KEY,
                        tip VARCHAR(50) NOT NULL,
                        nume VARCHAR(100) NOT NULL,
                        duritate NUMERIC,
                        densitate NUMERIC,
                        extra NUMERIC
                    );
                """)
                conn.commit()

    def obtine_toate(self) -> List[Dict[str, Any]]:
        with self._conectare() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, tip, nume, duritate, densitate, extra FROM pietre ORDER BY id ASC;")
                rows = cur.fetchall()
                return [
                    {
                        "id": str(row[0]),
                        "tip": row[1],
                        "nume": row[2],
                        "duritate": float(row[3]),
                        "densitate": float(row[4]),
                        "extra": float(row[5])
                    }
                    for row in rows
                ]

    def insereaza(self, tip: str, nume: str, duritate: float, densitate: float, extra: float) -> None:
        with self._conectare() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO pietre (tip, nume, duritate, densitate, extra) VALUES (%s, %s, %s, %s, %s);",
                    (tip, nume, duritate, densitate, extra)
                )
                conn.commit()

    def sterge(self, id_piatra: str) -> None:
        with self._conectare() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM pietre WHERE id = %s;", (int(id_piatra),))
                conn.commit()

    def actualizeaza(self, id_piatra: str, tip: str, nume: str, duritate: float, densitate: float, extra: float) -> None:
        with self._conectare() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE pietre SET tip = %s, nume = %s, duritate = %s, densitate = %s, extra = %s WHERE id = %s;",
                    (tip, nume, duritate, densitate, extra, int(id_piatra))
                )
                conn.commit()