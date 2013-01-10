__version__ = '0.2.0'

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 10000

from .hive_service import ThriftHive
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol

def connect(host=DEFAULT_HOST, port=DEFAULT_PORT):
    transport = TSocket.TSocket(host, port)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    client = ThriftHive.Client(protocol)
    transport.open()

    return client
