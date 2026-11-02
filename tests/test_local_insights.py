import socket
import unittest
import urllib.request

from local_insights import NetworkBlocked, load, no_network, outliers


class LocalInsightsTest(unittest.TestCase):
    def test_network_blocked_inside_guard(self):
        with no_network():
            with self.assertRaises(NetworkBlocked):
                urllib.request.urlopen("https://example.com", timeout=2)
            with self.assertRaises(NetworkBlocked):
                socket.getaddrinfo("example.com", 443)

    def test_guard_restores_socket(self):
        before = socket.getaddrinfo
        with no_network():
            pass
        self.assertIs(socket.getaddrinfo, before)

    def test_greece_unsubscribe_outlier(self):
        rows = load("examples/black_friday_results.csv")
        flagged = [(m, metric) for m, metric, *_ in outliers(rows, "unsub_rate")]
        self.assertEqual(flagged, [("GR", "unsub_rate")])


if __name__ == "__main__":
    unittest.main()
