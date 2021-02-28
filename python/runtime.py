from NokiMQ import Service

BROKER = 'amqp://user:password@broker'

tasks = Service(connection_string=BROKER, queue='tasks', loglevel="DEBUG")

answers = Service(connection_string=BROKER, queue='answers', loglevel="DEBUG")

@tasks.task
def add(x):
    print('from add')
    print(x)


@tasks.task
def test(x):
    print('from test')
    print(x)

@tasks.task
def test(x):
    print('from test')
    print(x)

answers.emit('someFunc', {
    'foo': 'bar'
})

tasks.task()

tasks.listen()
