"""
Ejecutor rápido de la suite completa de pruebas unitarias.
"""
import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
