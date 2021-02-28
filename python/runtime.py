from NokiMQ import Service
import logging

log = logging.getLogger('Runtime')
log_handler = logging.StreamHandler()
log_format = logging.Formatter('[%(name)s]  - %(asctime)s   %(levelname)s     %(message)s')
log_handler.setFormatter(log_format)
log.addHandler(log_handler)
log.setLevel(logging.DEBUG)

BROKER = 'amqp://user:password@broker'

tasks = Service(connection_string=BROKER, queue='tasks', loglevel="DEBUG")

@tasks.task
def add(x, y):
    log.info('from add')
    log.info(x + y)


@tasks.task
def test(foo, bar):
    log.info('from test')
    tasks.emit('add', {
        'x': foo,
        'y': bar
    })

tasks.listen()
