import MySQLdb
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Create MySQL database if it does not exist'

    def handle(self, *args, **kwargs):
        db_name = 'db.mysql'  # database name
        user = 'skye'         # MySQL username
        password = 'admin'    # MySQL password
        host = 'localhost'    # SetMySQL host
        port = 3306           # Default MySQL port

        # Connect to MySQL server
        conn = MySQLdb.connect(
            user=user, passwd=password, host=host, port=port)
        cursor = conn.cursor()

        # Check if the database exists
        cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
        result = cursor.fetchone()

        if not result:
            # Create the database if it does not exist
            cursor.execute(f"CREATE DATABASE {db_name};")
            self.stdout.write(self.style.SUCCESS(
                f'Database "{db_name}" created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(
                f'Database "{db_name}" already exists.'))

        # Close the connection
        cursor.close()
        conn.close()


init = Command()
init.handle()
