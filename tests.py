#!/usr/bin/env python

try:
    import gevent
except ImportError:
    gevent = None

import functools
import sys
import threading
import unittest

from pedis import Client
from pedis import QueueServer

TEST_HOST = '127.0.0.1'
TEST_PORT = 31339


def run_queue_server():
    server = QueueServer(host=TEST_HOST, port=TEST_PORT,
                         use_gevent=gevent is not None)
    if gevent is not None:
        t = gevent.spawn(server.run)
    else:
        t = threading.Thread(target=server.run)
        t.daemon = True
        t.start()
    return t, server


class KeyPartial(object):
    def __init__(self, client, key):
        self.client = client
        self.key = key

    def __getattr__(self, attr):
        return functools.partial(getattr(self.client, attr), self.key)


class TestMiniRedisDatabase(unittest.TestCase):
    def setUp(self):
        self.c = Client(host=TEST_HOST, port=TEST_PORT)
        self.c.flush()

    def test_list(self):
        lq = KeyPartial(self.c, 'queue')

        lq.lpush('i1')
        lq.lpush('i2')
        lq.rpush('i3')
        lq.rpush('i4')
        result = lq.lrange(0)
        self.assertEqual(result, ['i2', 'i1', 'i3', 'i4'])

        self.assertEqual(lq.lpop(), 'i2')
        self.assertEqual(lq.rpop(), 'i4')
        self.assertEqual(lq.llen(), 2)

        self.assertEqual(lq.lrem('i3'), 1)
        self.assertEqual(lq.lrem('i3'), 0)

        lq.lpush('a1', 'a2', 'a3', 'a4')
        self.assertEqual(lq.lindex(2), 'a2')

        lq.lset(2, 'x')
        self.assertEqual(lq.lrange(1, 3), ['a3', 'x'])

        lq.ltrim(1, 4)
        self.assertEqual(lq.lrange(0), ['a3', 'x', 'a1'])
        self.assertEqual(lq.lflush(), 3)

    def test_kv(self):
        kp = KeyPartial(self.c, 'k1')
        kp.set(['alpha', 'beta', 'gamma'])
        self.assertEqual(kp.get(), ['alpha', 'beta', 'gamma'])

        res = kp.append(['pi', b'omega'])
        self.assertEqual(res, ['alpha', 'beta', 'gamma', 'pi', b'omega'])

        kp.set([b'foo', b'bar', b'baz'])
        self.assertEqual(kp.get(), [b'foo', b'bar', b'baz'])

    def test_incr_decr(self):
        self.assertEqual(self.c.incr('i'), 1)
        self.assertEqual(self.c.decr('i'), 0)
        self.assertEqual(self.c.incrby('i2', 3), 3)
        self.assertEqual(self.c.incrby('i2', 2), 5)

    def test_persistence(self):
        self.c.set('k1', 'v1')
        self.c.hset('h1', 'k1', 'v1')
        self.c.sadd('s1', 'v1', 'v2')
        self.assertTrue(self.c.save('/tmp/pedis.state'))
        self.c.flushall()

        self.assertTrue(self.c.get('k1') is None)
        self.assertTrue(self.c.hget('h1', 'k1') is None)
        self.assertTrue(self.c.scard('s1') == 0)

        self.c.set('k1', 'x1')
        self.c.set('k2', 'x2')
        self.assertTrue(self.c.restore('/tmp/pedis.state'))
        self.assertEqual(self.c.get('k1'), 'v1')
        self.assertTrue(self.c.get('k2') is None)
        self.assertEqual(self.c.hget('h1', 'k1'), 'v1')
        self.assertEqual(self.c.scard('s1'), 2)

        self.c.flushall()
        self.c.set('k1', 'x1')
        self.c.set('k2', 'x2')
        self.assertTrue(self.c.merge('/tmp/pedis.state'))
        self.assertEqual(self.c.get('k1'), 'x1')
        self.assertEqual(self.c.get('k2'), 'x2')
        self.assertEqual(self.c.hget('h1', 'k1'), 'v1')
        self.assertEqual(self.c.scard('s1'), 2)

    def test_expiry(self):
        self.c.mset({'k1': 'v1', 'k2': 'v2', 'k3': 'v3'})

        # Make it appear to expire in the past.
        self.c.expire('k2', -1)
        self.c.expire('k3', 3)
        self.assertEqual(self.c.mget('k1', 'k2', 'k3'), ['v1', None, 'v3'])


if __name__ == '__main__':
    server_t, server = run_queue_server()
    unittest.main(argv=sys.argv)
