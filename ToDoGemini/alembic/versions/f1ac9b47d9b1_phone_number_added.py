"""phone number added

Revision ID: f1ac9b47d9b1
Revises: 
Create Date: 2025-04-27 15:20:52.878305

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1ac9b47d9b1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users',sa.Column('phone_number', sa.String(), nullable=True))



def downgrade() -> None:
    """Downgrade schema."""
    #op.drop_column('users', 'phone_number')
    pass
# database bir sey eklemek istiyorsam once onu modelime ekliyorum
#sonra alembic ekliyorm ve olusturulan dosyalarda metadata yerine models eklyiorum
# ilk bunu degistiriyom database linki ile
#sqlalchemy.url = sqlite:///./todoai_app.db
# sonra meta datayi
#target_metadata =models.Base.metadata
# sonra terminala alembic revision -m "phone number added" bunu yaziyorum ve bu dosya olusuyor
# sonra bu dosyanin icindei upgrade yerine kodumu yazip
# terminalden
#  alembic upgrade f1ac9b47d9b1 bunu calistiriyorum
# revision stringinide bu dosya icinden aliyorum
