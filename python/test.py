from NokiMQ import Service

BROKER = 'amqp://user:password@broker'

tasks = Service(connection_string=BROKER, queue='tasks', loglevel="DEBUG")


tasks.emit('test', {
    'foo': 'bar',
    'bar': 'baz'
})
