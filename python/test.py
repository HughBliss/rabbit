from NokiMQ import Service

BROKER = 'amqp://user:password@broker'


tasks = Service(BROKER, 'tasks')

tasks.emit('add', {
    'message': 'hello'
})
