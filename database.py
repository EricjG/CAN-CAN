import sqlite3

class DatabaseManager:
    def __init__(self, db_name='can_data.db'):
        """Initialize the database connection and create the table if it doesn't exist."""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        """Create a table for storing CAN messages."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS can_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                message_type TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()

    def insert_message(self, project_name, message_type, message):
        """Insert a new CAN message into the database."""
        self.cursor.execute('''
            INSERT INTO can_messages (project_name, message_type, message)
            VALUES (?, ?, ?)
        ''', (project_name, message_type, message))
        self.connection.commit()

    def query_messages(self, project_name):
        """Query messages based on the project name."""
        self.cursor.execute('''
            SELECT * FROM can_messages WHERE project_name = ?
        ''', (project_name,))
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.connection.close()
