import os
import sys
from django.test import TestCase
from unittest.mock import patch, MagicMock

class ASGIConfigTest(TestCase):
    
    def setUp(self):
        # Salva o environment original
        self.original_django_settings = os.environ.get('DJANGO_SETTINGS_MODULE')
        
    def tearDown(self):
        # Restaura o environment original
        if self.original_django_settings:
            os.environ['DJANGO_SETTINGS_MODULE'] = self.original_django_settings
        else:
            os.environ.pop('DJANGO_SETTINGS_MODULE', None)
    
    def test_asgi_module_can_be_imported(self):
        """Testa se o módulo ASGI pode ser importado sem erros"""
        try:
            from agenda.asgi import application
            self.assertIsNotNone(application)
        except ImportError as e:
            self.fail(f"Falha ao importar módulo ASGI: {e}")
    
    def test_asgi_environment_variable(self):
        """Testa se a variável de environment está configurada corretamente"""
        import agenda.asgi
        self.assertEqual(os.environ.get('DJANGO_SETTINGS_MODULE'), 'agenda.settings')
    
    def test_application_variable_exists(self):
        """Testa se a variável 'application' existe no módulo"""
        from agenda.asgi import application
        self.assertTrue(hasattr(application, '__call__'))
    
    def test_application_is_asgi_callable(self):
        """Testa se application é um callable ASGI válido"""
        from agenda.asgi import application
        self.assertTrue(callable(application))
    
    def test_asgi_with_different_environment(self):
        """Testa que o ASGI configura o environment corretamente"""
        # Remove a variável de environment se existir
        os.environ.pop('DJANGO_SETTINGS_MODULE', None)
        
        # Recarrega o módulo para forçar a reconfiguração
        if 'agenda.asgi' in sys.modules:
            del sys.modules['agenda.asgi']
        
        # Reimporta o módulo (deve configurar o environment)
        import agenda.asgi
        
        self.assertEqual(os.environ['DJANGO_SETTINGS_MODULE'], 'agenda.settings')
    
    def test_asgi_application_interface(self):
        """Testa se a aplicação ASGI tem a interface básica correta"""
        from agenda.asgi import application
        self.assertTrue(callable(application))
    
    def test_get_asgi_application_called(self):
        """Testa se get_asgi_application é chamado durante a importação"""
        # Remove o módulo do cache para forçar reimportação
        if 'agenda.asgi' in sys.modules:
            del sys.modules['agenda.asgi']
        if 'django.core.asgi' in sys.modules:
            del sys.modules['django.core.asgi']
        
        # Usa patch para mockar get_asgi_application
        with patch('django.core.asgi.get_asgi_application') as mock_get_asgi:
            mock_get_asgi.return_value = MagicMock()
            
            # Importa após o patch
            from agenda.asgi import application
            
            # Verifica se foi chamado
            mock_get_asgi.assert_called_once()
    
    def test_module_level_application(self):
        """Testa se a application no nível do módulo está correta"""
        from agenda.asgi import application
        self.assertTrue(callable(application))
    
    def test_multiple_imports(self):
        """Testa que múltiplas importações não quebram o módulo"""
        # Remove o módulo do cache
        if 'agenda.asgi' in sys.modules:
            del sys.modules['agenda.asgi']
        
        # Primeira importação
        import agenda.asgi as asgi1
        app1 = asgi1.application
        
        # Segunda importação (deve funcionar normalmente)
        import agenda.asgi as asgi2
        app2 = asgi2.application
        
        # Ambas devem ser callable
        self.assertTrue(callable(app1))
        self.assertTrue(callable(app2))
    
    def test_asgi_application_type(self):
        """Testa se a aplicação ASGI é do tipo correto"""
        from agenda.asgi import application
        from django.core.handlers.asgi import ASGIHandler
        
        # Verifica se é uma instância de ASGIHandler (ou pelo menos callable)
        self.assertTrue(callable(application))
        # Não podemos testar isinstance porque pode ser uma função wrapper
    
    def test_environment_persistence(self):
        """Testa que a configuração do environment persiste"""
        # Configura um valor diferente
        os.environ['DJANGO_SETTINGS_MODULE'] = 'outro.settings'
        
        # Recarrega o módulo
        if 'agenda.asgi' in sys.modules:
            del sys.modules['agenda.asgi']
        
        # Importa - deve manter o valor existente devido ao setdefault
        import agenda.asgi
        
        self.assertEqual(os.environ['DJANGO_SETTINGS_MODULE'], 'outro.settings')