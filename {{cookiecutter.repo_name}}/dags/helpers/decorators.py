from threading import Thread


def postpone(function):
    def decorator(*args, **kwargs):
        """
          Multi threading --decorator to run specific bit of code in different thread.
          To use it in a function, simply use the @postpone decorator. The function will then be passed onto a different thread.

        :param args:
        :param kwargs:
        :return: decorator
        """

        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return decorator
