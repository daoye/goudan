import random
import os
from pony.orm import *
from datetime import datetime
from core import FILE

db = Database()

class ProxyItem(db.Entity):
    id = PrimaryKey(int, auto=True)
    host = Required(str)
    port = Required(int)
    protocol = Required(str) # This proxy's protocol, example: http,https,socks4,socks5
    supportProtocol = Required(str) # This proxy support's protocol, example: http,https,socks4,socks5,http/https,socks4/socks5
    expired = Required(int) # This proxy's expired time.
    usr = Optional(str) # This proxy's username.
    pwd = Optional(str) # This proxy's password.
    location = Optional(str) # This proxy's location.
    isok = Required(bool) # Is this proxy checked success.
    validCount = Required(int) # checked failed's count
    failedCount = Required(int) # connected failed' count

class Pool():
    def get(self, protocol):
        with db_session:
            qer = select(x for x in ProxyItem if x.expired >= datetime.now().timestamp() and x.protocol == protocol and x.isok == True)
            total = qer.count()
            idx = random.randint(0, total-1)
            return qer[idx:idx + 1][0]

def db_bind():
    db_path = FILE('data')
    if not os.path.exists(db_path):
        os.mkdir(db_path)
    db_file = FILE(os.path.join(db_path, 'database.sqlite'))
    db.bind(provider='sqlite', filename=db_file, create_db=True)
    db.generate_mapping(create_tables=True)