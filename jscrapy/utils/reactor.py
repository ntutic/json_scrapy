import asyncio
import sys
from contextlib import suppress

from twisted.internet import asyncioreactor, error

from jscrapy.utils.misc import load_object


def listen_tcp(portrange, host, factory):
    """Like reactor.listenTCP but tries different ports in a range."""
    from twisted.internet import reactor
    if len(portrange) > 2:
        raise ValueError(f"invalid portrange: {portrange}")
    if not portrange:
        return reactor.listenTCP(0, factory, interface=host)
    if not hasattr(portrange, '__iter__'):
        return reactor.listenTCP(portrange, factory, interface=host)
    if len(portrange) == 1:
        return reactor.listenTCP(portrange[0], factory, interface=host)
    for x in range(portrange[0], portrange[1] + 1):
        try:
            return reactor.listenTCP(x, factory, interface=host)
        except error.CannotListenError:
            if x == portrange[1]:
                raise


class CallLaterOnce:
    """Schedule a function to be called in the next reactor loop, but only if
    it hasn't been already scheduled since the last time it ran.
    """

    def __init__(self, func, *a, **kw):
        self._func = func
        self._a = a
        self._kw = kw
        self._call = None

    def schedule(self, delay=0):
        from twisted.internet import reactor
        if self._call is None:
            self._call = reactor.callLater(delay, self)

    def cancel(self):
        if self._call:
            self._call.cancel()

    def __call__(self):
        self._call = None
        return self._func(*self._a, **self._kw)


def install_reactor(reactor_path, event_loop_path=None):
    """Installs the :mod:`~twisted.internet.reactor` with the specified
    import path. Also installs the asyncio event loop with the specified import
    path if the asyncio reactor is enabled"""
    reactor_class = load_object(reactor_path)
    if reactor_class is asyncioreactor.AsyncioSelectorReactor:
        with suppress(error.ReactorAlreadyInstalledError):
            if sys.version_info >= (3, 8) and sys.platform == "win32":
                policy = asyncio.get_event_loop_policy()
                if not isinstance(policy, asyncio.WindowsSelectorEventLoopPolicy):
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            if event_loop_path is not None:
                event_loop_class = load_object(event_loop_path)
                event_loop = event_loop_class()
                asyncio.set_event_loop(event_loop)
            else:
                event_loop = asyncio.get_event_loop()
            asyncioreactor.install(eventloop=event_loop)
    else:
        *module, _ = reactor_path.split(".")
        installer_path = module + ["install"]
        installer = load_object(".".join(installer_path))
        with suppress(error.ReactorAlreadyInstalledError):
            installer()


def verify_installed_reactor(reactor_path):
    """Raises :exc:`Exception` if the installed
    :mod:`~twisted.internet.reactor` does not match the specified import
    path."""
    from twisted.internet import reactor
    reactor_class = load_object(reactor_path)
    if not reactor.__class__ == reactor_class:
        msg = ("The installed reactor "
               f"({reactor.__module__}.{reactor.__class__.__name__}) does not "
               f"match the requested one ({reactor_path})")
        raise Exception(msg)


def is_asyncio_reactor_installed():
    from twisted.internet import reactor
    return isinstance(reactor, asyncioreactor.AsyncioSelectorReactor)
