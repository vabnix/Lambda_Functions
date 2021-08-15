import pika

parameters = pika.URLParameters('amqp://guest:brEdugeqaq2!@xmb.lwolf.com:5672')
# credentials = pika.PlainCredentials('guest', 'brEdugeqaq2!')
# parameters = pika.ConnectionParameters('xmb.lwolf.com', 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

connection.close()
