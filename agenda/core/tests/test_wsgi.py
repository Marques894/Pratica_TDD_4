import os
import sys
from django.test import TestCase
from django.conf import settings
from importlib import import_module

class WSGIConfigTest(TestCase):
    
    def setUp(self):
        # Configura o environment para teste
        self.original_django_settings = os.environ.get('DJANGO_SETTINGS_MODULE')
        
    def tearDown(self):
        # Restaura o environment original
        if self.original_django_settings:
            os.environ['DJANGO_SETTINGS_MODULE'] = self.original_django_settings
        else:
            os.environ.pop('DJANGO_SETTINGS_MODULE', None)
    
    def test_wsgi_module_can_be_imported(self):
        """Testa se o módulo WSGI pode ser importado sem erros"""
        try:
            from agenda.wsgi import application
            self.assertIsNotNone(application)
        except ImportError as e:
            self.fail(f"Falha ao importar módulo WSGI: {e}")
    
    def test_wsgi_environment_variable(self):
        """Testa se a variável de environment está configurada corretamente"""
        # Importa o módulo wsgi para executar a configuração
        import agenda.wsgi
        
        self.assertEqual(os.environ.get('DJANGO_SETTINGS_MODULE'), 'agenda.settings')
    
    def test_application_variable_exists(self):
        """Testa se a variável 'application' existe no módulo"""
        from agenda.wsgi import application
        
        self.assertTrue(hasattr(application, '__call__'))
        self.assertIsNotNone(application)
    
    def test_application_is_wsgi_callable(self):
        """Testa se application é um callable WSGI válido"""
        from agenda.wsgi import application
        
        # Verifica se é callable (função/método/classe com __call__)
        self.assertTrue(callable(application))
    
    def test_wsgi_with_different_environment(self):
        """Testa que o WSGI configura o environment corretamente"""
        # Remove a variável de environment se existir
        os.environ.pop('DJANGO_SETTINGS_MODULE', None)
        
        # Recarrega o módulo para forçar a reconfiguração
        if 'agenda.wsgi' in sys.modules:
            del sys.modules['agenda.wsgi']
        
        # Reimporta o módulo (deve configurar o environment)
        import agenda.wsgi
        
        self.assertEqual(os.environ['DJANGO_SETTINGS_MODULE'], 'agenda.settings')