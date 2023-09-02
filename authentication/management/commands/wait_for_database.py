from django.core.management.base import BaseCommand
from django.db import connection
import time

DEFAULT_TIMEOUT = 20


class Command(BaseCommand):
    help = 'Wait until database is ready'
    requires_model_validation = False

    def add_arguments(self, parser):
        parser.add_argument('-t', '--timeout',type=int, action='store', dest='timeout',
            default=DEFAULT_TIMEOUT, help='Timeout for database connection')

    def wait_for_database(self, timeout=DEFAULT_TIMEOUT):
        ready = False
        for i in range(timeout):
            try:
                connection.connect()
                ready = True
                break
            except Exception as e:
                # Check error type
                error = str(e).splitlines()[0]
                if error.startswith('fe_sendauth: no password supplied'):
                    ready = True
                    break
                if error.startswith('FATAL:  no pg_hba.conf entry'):
                    ready = True
                    break
                if error.startswith('could not connect to server: Connection refused'):
                    pass
                elif error.startswith('FATAL:  the database system is starting up'):
                    pass
                else:
                    self.stdout.write(self.style.ERROR(error))
            time.sleep(1)
        connection.close()
        return ready

    def handle(self, *args, **options):
        ready = self.wait_for_database(options['timeout'])
        if ready:
            self.stdout.write(self.style.SUCCESS('Database ready'))
        else:
            self.stdout.write(self.style.ERROR('Timeout reached'))
