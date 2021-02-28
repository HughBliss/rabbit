import logging
from ast import literal_eval
from inspect import signature
from re import fullmatch
from pika import PlainCredentials, BlockingConnection, URLParameters
from json import dumps, loads



class Service:
    def __init__(self, connection_string: str, queue: str, tasks = None, loglevel="WARNING"):
        self._queue = queue
        self._tasks = tasks or {}
        self._logger = logging.getLogger(queue)

        stream_handler = logging.StreamHandler()
        # TODO: сделать кастомнй форматер чтобы добавлять пробелы (https://stackoverflow.com/questions/6692248/python-logging-string-formatting/22707429)
        stream_format = logging.Formatter('[NokiMQ]   - %(asctime)s  [%(name)s] %(levelname)s     %(message)s')
        stream_handler.setFormatter(stream_format)
        self._logger.addHandler(stream_handler)
        self._logger.setLevel(logging.getLevelName(loglevel))

        self._logger.info(f'Connecting to "{connection_string}"')
        connection = None
        try:
            connection = BlockingConnection(
                URLParameters(connection_string)
            )
        except:
            self._logger.critical('Connection failed')
            quit(-1)

        self._logger.info('Connected!')

        self._channel = connection.channel()
        self._channel.queue_declare(queue)


    def emit(self, pattern: str, body: dict):
        try:
            self._channel.basic_publish('', self._queue, dumps({
                'pattern': pattern,
                'data': body
            }).encode('utf-8'))
            self._logger.info(f'Emited {pattern}')
        except:
            self._logger.error(f'Emit {pattern} failed')

    def _task_from_func(self, func, pattern=None, bind = False, **opts):
        # TODO: проверить нет ли функций с таким именем, если есть, то придумать нвое

        pattern = pattern or func.__name__

        if pattern not in self._tasks:
            run = func if bind else staticmethod(func)

            task = type(func.__name__, (),dict({
                'service': self,
                'pattern': pattern,
                'run': run,
                '_decorated': True,
                '__doc__': func.__doc__,
                '__module__': func.__module__,
                '__annotations__': func.__annotations__,
                '__wrapped__': run}, **opts))()

            try:
                task.__qualname__ = func.__qualname__
            except AttributeError:
                pass
            self._tasks[task.pattern] = task
            self._logger.info(f'Task {pattern} was binded')

        else:
            task = self._tasks[pattern]
            self._logger.warning(f'Task {pattern} was rebinded')

        return task


    def task(self, *args, **opts):
        def connect_task_to_cls(**opts):
            def _task_to_cls(func):
                res = self._task_from_func(func, **opts)
                return res
            return _task_to_cls

        if len(args) == 1:
            if callable(args[0]):
                return connect_task_to_cls(**opts)(*args)
            else:
                self._logger.warning(f'The first argument need to be a function')
        else:
            self._logger.warning(f'Task deсorator needs a function')

    def listen(self):
        try:
            def callback(_, __, ___, body):

                body = loads(body.decode('utf-8'))
                # print(self._tasks[body['pattern']].run(body['data']))
                try:
                    self._tasks[body['pattern']].run(body['data'])
                except: pass

            self._channel.basic_consume(
                queue=self._queue,
                on_message_callback=callback,
                auto_ack=True
            )
            self._logger.info('Consumming...')
            self._channel.start_consuming()
        except:
            self._logger.critical('Consuming error')
            quit(-1)
