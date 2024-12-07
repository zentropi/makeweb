import unittest
import os
from makeweb.dictdb import DictDB

class TestDictDB(unittest.TestCase):
    def setUp(self):
        self.db_file = "test_db.db"
        self.db = DictDB(self.db_file)
    
    def tearDown(self):
        self.db.close()
        try:
            os.remove(self.db_file)
        except OSError:
            pass
    
    def test_basic_operations(self):
        # Test string values
        self.db['test1'] = 'hello'
        self.assertEqual(self.db['test1'], 'hello')
        
        # Test numeric values
        self.db['test2'] = 42
        self.assertEqual(self.db['test2'], 42)
        
        # Test boolean
        self.db['test3'] = True
        self.assertEqual(self.db['test3'], True)
    
    def test_complex_types(self):
        # Test list
        test_list = [1, 2, "three", True]
        self.db['list'] = test_list
        self.assertEqual(self.db['list'], test_list)
        
        # Test dict
        test_dict = {"name": "test", "value": 42}
        self.db['dict'] = test_dict
        self.assertEqual(self.db['dict'], test_dict)
    
    def test_context_manager(self):
        with DictDB(self.db_file) as db:
            db['key'] = 'value'
            self.assertEqual(db['key'], 'value')
        
        # Test persistence after context manager
        with DictDB(self.db_file) as db:
            self.assertEqual(db['key'], 'value')
    
    def test_dict_methods(self):
        test_data = {
            'a': 1,
            'b': 2,
            'c': 3
        }
        
        # Add test data
        for k, v in test_data.items():
            self.db[k] = v
        
        # Test keys
        self.assertEqual(set(self.db.keys()), set(test_data.keys()))
        
        # Test values
        self.assertEqual(set(self.db.values()), set(test_data.values()))
        
        # Test items
        self.assertEqual(set(self.db.items()), set(test_data.items()))
        
        # Test contains
        self.assertTrue('a' in self.db)
        self.assertFalse('x' in self.db)
    
    def test_deletion(self):
        self.db['delete_me'] = 'value'
        self.assertTrue('delete_me' in self.db)
        del self.db['delete_me']
        self.assertFalse('delete_me' in self.db)
    
    def test_persistence(self):
        # Write some data
        self.db['persist'] = 'test'
        self.db.close()
        
        # Reopen and verify
        db2 = DictDB(self.db_file)
        self.assertEqual(db2['persist'], 'test')
        db2.close()

    def test_range_queries(self):
        # Setup test data
        test_data = {
            'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5
        }
        for k, v in test_data.items():
            self.db[k] = v
            
        # Test exclusive range queries
        self.assertEqual(
            list(self.db.keys('b', 'd', incl=False)), 
            ['b', 'c']
        )
        
        # Test inclusive end (default behavior)
        self.assertEqual(
            list(self.db.keys('b', 'd')), 
            ['b', 'c', 'd']
        )
        
        # Test values range (exclusive)
        self.assertEqual(
            list(self.db.values('b', 'd', incl=False)),
            [2, 3]
        )
        
        # Test items range (default inclusive)
        self.assertEqual(
            list(self.db.items('b', 'd')),
            [('b', 2), ('c', 3), ('d', 4)]
        )

    def test_transaction_rollback(self):
        # Set initial value
        self.db['test_key'] = 'initial'
        
        # Attempt a transaction that will fail
        try:
            with DictDB(self.db_file) as db:
                db['test_key'] = 'modified'
                self.assertEqual(db['test_key'], 'modified')
                raise Exception("Forced rollback")
        except Exception:
            pass
            
        # Verify the value was not changed
        self.assertEqual(self.db['test_key'], 'initial')
        

if __name__ == '__main__':
    unittest.main()