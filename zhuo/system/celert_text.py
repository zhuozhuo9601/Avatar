import time

from tasks import add

result = add.delay(1,2)
while not result.ready():
    time.sleep(1)
print('task done: {0}'.format(result.get()))

