import unittest
import sys
sys.path.append("..")
from Stack import stack



class StackTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.s = stack()

    @classmethod
    def tearDownClass(self):
        del(self.s)

    def test_stack1(self):
        self.s.push(5)
        self.assertEqual(self.s.peek(), 5)  
        self.s.push(5)
        self.s.push(64)
        self.s.push(777)
        self.assertEqual(self.s.size(), 4,"THIS ERROR")
        self.assertEqual(self.s.pop(), 777)
        self.assertEqual(self.s.peek(), 64)
        self.assertEqual(self.s.pop(), 64)
        self.assertEqual(self.s.pop(), 5)
        self.assertEqual(self.s.pop(), 5)
        self.assertIsNone(self.s.pop(handle=True))


if __name__ == "__main__":
    unittest.main()