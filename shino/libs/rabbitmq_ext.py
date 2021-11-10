# coding: utf-8
# @Time : 9/8/21 10:29 AM

from kombu import Connection


class RabbitmqExt:

    def __init__(self, host, port, user, password, vhost):
        self.conn = Connection(f'amqp://{user}:{password}@{host}:{port}/{vhost}')

    def send(self, msg, to_queue):
        if not isinstance(msg, dict):
            return False
        with self.conn as conn:
            # conn.heartbeat_check()
            with conn.SimpleQueue(to_queue) as queue:
                queue.put(msg, serializer="json", compression="zlib")
                return True

    def send_many(self, messages, to_queue):
        if not isinstance(messages, list):
            return False
        with self.conn as conn:
            for msg in messages:
                if not isinstance(msg, dict):
                    continue
                with conn.SimpleQueue(to_queue) as queue:
                    queue.put(msg, serializer="json", compression="zlib")

    def receive(self, from_queue):
        with self.conn as conn:
            with conn.SimpleQueue(from_queue) as queue:
                msg = queue.get(block=True, timeout=2)
                msg.ack()
                return msg.payload