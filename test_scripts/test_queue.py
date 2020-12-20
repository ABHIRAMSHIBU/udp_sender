import sys
sys.path.append("..")
import unittest
from Queue import Queue



class QueueTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def test_queue(self):
        myQueue = Queue(10)
        self.assertIsNone(myQueue.dequeue())
        self.assertTrue(myQueue.isEmpty())
        self.assertFalse(myQueue.isFull())
        self.assertIsNone(myQueue.peek())
        myQueue.enqueue(1)
        myQueue.enqueue(2)
        myQueue.enqueue(3)
        self.assertEqual(myQueue.dequeue(), 1)
        self.assertEqual(myQueue.dequeue(), 2)
        self.assertEqual(myQueue.dequeue(), 3)


if __name__ == "__main__":
    unittest.main()
