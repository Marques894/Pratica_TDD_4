from django.test import TestCase, Client
from django.urls import reverse, resolve
from core.views import login, logout, home, delete_contact, register_contact, edit_contact, show_contact
from http import HTTPStatus

class URLTests(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def test_login_url(self):
        """Testa se a URL de login está configurada corretamente"""
        url = reverse('login')
        self.assertEqual(url, '/login/')
        resolver = resolve('/login/')
        self.assertEqual(resolver.func, login)
    
    def test_logout_url(self):
        """Testa se a URL de logout está configurada corretamente"""
        url = reverse('logout')
        self.assertEqual(url, '/logout/')
        resolver = resolve('/logout/')
        self.assertEqual(resolver.func, logout)
    
    def test_home_url(self):
        """Testa se a URL home está configurada corretamente"""
        url = reverse('home')
        self.assertEqual(url, '/')
        resolver = resolve('/')
        self.assertEqual(resolver.func, home)
    
    def test_index_url(self):
        """Testa se a URL index está configurada corretamente"""
        url = reverse('index')
        self.assertEqual(url, '/index/')
        resolver = resolve('/index/')
        self.assertEqual(resolver.func, home)
    
    def test_register_contact_url(self):
        """Testa se a URL de registro de contato está configurada corretamente"""
        url = reverse('register_contact')
        self.assertEqual(url, '/register_contact/')
        resolver = resolve('/register_contact/')
        self.assertEqual(resolver.func, register_contact)
    
    def test_show_contact_url(self):
        """Testa se a URL de exibição de contatos está configurada corretamente"""
        url = reverse('show_contact')
        self.assertEqual(url, '/show_contact/')
        resolver = resolve('/show_contact/')
        self.assertEqual(resolver.func, show_contact)
    
    def test_edit_contact_url(self):
        """Testa se a URL de edição de contato está configurada corretamente"""
        url = reverse('edit_contact')
        self.assertEqual(url, '/edit_contact/')
        resolver = resolve('/edit_contact/')
        self.assertEqual(resolver.func, edit_contact)
    
    def test_delete_contact_url(self):
        """Testa se a URL de exclusão de contato está configurada corretamente"""
        url = reverse('delete_contact')
        self.assertEqual(url, '/delete_contact/')
        resolver = resolve('/delete_contact/')
        self.assertEqual(resolver.func, delete_contact)
    
    def test_reverse_urls(self):
        """Testa se reverse funciona para todas as URLs"""
        url_mappings = [
            ('login', '/login/'),
            ('logout', '/logout/'),
            ('home', '/'),
            ('index', '/index/'),
            ('register_contact', '/register_contact/'),
            ('show_contact', '/show_contact/'),
            ('edit_contact', '/edit_contact/'),
            ('delete_contact', '/delete_contact/'),
        ]
        
        for name, expected_path in url_mappings:
            with self.subTest(url_name=name):
                path = reverse(name)
                self.assertEqual(path, expected_path)
    
    def test_url_responses(self):
        """Testa se as URLs básicas respondem corretamente"""
        # URL de login deve ser pública e retornar 200
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
        # URL home deve redirecionar para login se não autenticado (302)
        response = self.client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 302 Redirect
        self.assertIn('/login/', response.url)  # Verifica se redireciona para login