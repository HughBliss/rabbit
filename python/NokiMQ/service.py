prefix = '[NokiMQ]:'

try:
    from ast import literal_eval
    from inspect import signature
    from re import fullmatch
    from pika import PlainCredentials, BlockingConnection, URLParameters
    from json import dumps, loads

except ModuleNotFoundError:
    print(f'{prefix} Attention! NokiMQ requires modules: "re", "pika", "json", "inspect", "ast". '
          f'Please install and try again')
    quit(-1)


class Service:
    def __init__(self, connection_string: str, queue: str, tasks = None):
        self._queue = queue
        self._tasks = tasks or {}

        print(f'{prefix} Connecting to "{connection_string}"')

        connection = None
        try:
            connection = BlockingConnection(
                URLParameters(connection_string)
            )
        except:
            print(f'{prefix} Connection failed')
            quit(-1)

        print(f'{prefix} Connected!')

        self._channel = connection.channel()
        self._channel.queue_declare(queue)


    def emit(self, pattern: str, body: dict):
        self._channel.basic_publish('', self._queue, dumps({
            'pattern': pattern,
            'data': body
        }).encode('utf-8'))

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

        else:
            task = self._tasks[pattern]

        return task

        # if len(signature(fn).parameters) != 1:
        #     raise Exception('Count of receiver function args must be 1')
        # if pattern in list(self.listeners.keys()):
        #     self.listeners[pattern].append(fn)
        # else:
        #     self.listeners[pattern] = [fn]


    def task(self, *args, **opts):
        def connect_task_to_cls(**opts):
            def _task_to_cls(func):
                res = self._task_from_func(func, **opts)
                return res
            return _task_to_cls

        if len(args) == 1:
            if callable(args[0]):
                return connect_task_to_cls(**opts)(*args)

    def listen(self):
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
        self._channel.start_consuming()
