import pika

credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='broker', credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='tasks')

channel.basic_publish(exchange='',
                      routing_key='tasks',
                      body='print("Hello World!")')

print(""" [python] [sender] Sent 'print("Hello World")' """)

connection.close()
