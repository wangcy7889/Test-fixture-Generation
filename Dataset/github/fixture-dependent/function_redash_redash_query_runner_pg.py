import select
import psycopg2

def _wait(conn, timeout=None):
    while 1:
        try:
            state = conn.poll()
            if state == psycopg2.extensions.POLL_OK:
                break
            elif state == psycopg2.extensions.POLL_WRITE:
                select.select([], [conn.fileno()], [], timeout)
            elif state == psycopg2.extensions.POLL_READ:
                select.select([conn.fileno()], [], [], timeout)
            else:
                raise psycopg2.OperationalError('poll() returned %s' % state)
        except select.error:
            raise psycopg2.OperationalError('select.error received')