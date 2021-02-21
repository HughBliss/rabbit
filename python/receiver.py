import pika, sys, os

def main():
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='broker', credentials=credentials))

    channel = connection.channel()
    channel.queue_declare(queue='tasks')
    channel.queue_declare(queue='results')


    def callback(ch, method, properties, body):
        print(' [python] [receiver] Execution started')
        try:
            exec(body.decode('utf-8'))
            channel.basic_publish(exchange='',
                        routing_key='results',
                        body='{"pattern":"result","data":"Execution complited ok"}')
            print(' [python] [receiver] Execution complited ok ' + body.decode('utf-8'))
        except:
            channel.basic_publish(exchange='',
                        routing_key='results',
                        body='{"pattern":"result","data":"Execution failed"}')
            print(' [python] [receiver] Execution failed')


    channel.basic_consume(queue='tasks', on_message_callback=callback, auto_ack=True)

    print(' [python] [receiver] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
