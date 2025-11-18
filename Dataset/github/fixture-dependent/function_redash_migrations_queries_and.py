from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import ProgrammingError
revision = '65fc9ede4746'

def upgrade():
    try:
        op.add_column('queries', sa.Column('is_draft', sa.Boolean, default=True, index=True))
        op.add_column('dashboards', sa.Column('is_draft', sa.Boolean, default=True, index=True))
        op.execute("UPDATE queries SET is_draft = (name = 'New Query')")
        op.execute('UPDATE dashboards SET is_draft = false')
    except ProgrammingError as e:
        if 'column "is_draft" of relation "queries" already exists' in str(e):
            print("Can't run this migration as you already have is_draft columns, please run:")
            print('./manage.py db stamp {} # you might need to alter the command to match your environment.'.format(revision))
            exit()