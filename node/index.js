const { connect } = require('amqplib/callback_api')


connect('amqp://user:password@broker', (connectionError, connection) => {
    if (connectionError) {
        throw connectionError;
    }
    connection.createChannel((channelError, channel) => {
        if (channelError) {
            throw channelError
        }

        channel.assertQueue('tasks', { durable: false })
        channel.assertQueue('results', { durable: false })

        channel.sendToQueue('tasks', Buffer.from(`

for i in range(10):
    print('Nikita pidor')

        `))

        channel.consume('results',
            (msg) => {
                console.log(`[node] [receiver] Received from Python message: ${msg.content.toString()}`);
            },
            {
                noAck: true
            }
        )
    })
})
