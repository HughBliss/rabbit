from NokiMQ import Service

BROKER = 'amqp://user:password@broker'

tasks = Service(BROKER, 'tasks')

@tasks.task
def add(x):
    print('from add')
    print(x)


@tasks.task
def test(x):
    print('from test')
    print(x)

tasks.listen()
