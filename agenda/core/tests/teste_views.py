from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Agenda
from core.forms import LoginForm, AgendaForm
from http import HTTPStatus

class ViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='renan.marques3@fatec.sp.gov.br',
            password='testpass123'
        )
        self.contact = Agenda.objects.create(
            nome_completo='Renan Marques Test',
            telefone='19987654321',
            email='renan.marques3@fatec.sp.gov.br',
            observacao='Test observation'
        )
    
    # Testes para Login View
    def test_login_view_get(self):
        """Testa acesso GET à view de login"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIsInstance(response.context['form'], LoginForm)
    
    def test_login_view_post_valid(self):
        """Testa login com credenciais válidas"""
        data = {
            'email': 'renan.marques3@fatec.sp.gov.br',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('login'), data)
        self.assertIn(response.status_code, [HTTPStatus.OK, HTTPStatus.FOUND])
    
    def test_login_view_post_invalid(self):
        """Testa login com credenciais inválidas"""
        data = {
            'email': 'invalid@email.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_login_redirect_when_authenticated(self):
        """Testa redirecionamento quando usuário já está autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('home'))
    
    # Testes para Logout View
    def test_logout_view_post(self):
        """Testa logout via POST"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'logout.html')
    
    def test_logout_view_get_redirect(self):
        """Testa que logout via GET redireciona para home"""
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('home'))
    
    # Testes para Home View
    def test_home_view_authenticated(self):
        """Testa acesso à home quando autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_home_view_unauthenticated(self):
        """Testa que home redireciona quando não autenticado"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('/login/', response.url)
    
    # Testes para Register Contact View
    def test_register_contact_view_get_authenticated(self):
        """Testa acesso GET ao registro de contato quando autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('register_contact'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'register_contact.html')
    
    def test_register_contact_view_post_valid(self):
        """Testa registro de contato com dados válidos"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'nome_completo': 'Novo Contato Test',
            'telefone': '19912345678',
            'email': 'novo.contato@fatec.sp.gov.br',
            'observacao': 'Nova observação'
        }
        response = self.client.post(reverse('register_contact'), data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(Agenda.objects.filter(nome_completo='Novo Contato Test').exists())
    
    def test_register_contact_view_post_invalid(self):
        """Testa registro de contato com dados inválidos"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'nome_completo': '',  # Nome vazio - inválido
            'telefone': 'invalid',
            'email': 'email-invalido',
            'observacao': 'Test'
        }
        response = self.client.post(reverse('register_contact'), data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'register_contact.html')
        self.assertTrue(response.context['error'])
    
    # Testes para Show Contact View
    def test_show_contact_view_authenticated(self):
        """Testa exibição de contatos quando autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('show_contact'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'show_contact.html')
        self.assertIn('contacts', response.context)
        self.assertEqual(len(response.context['contacts']), 1)
    
    def test_show_contact_view_unauthenticated(self):
        """Testa que show_contact redireciona quando não autenticado"""
        response = self.client.get(reverse('show_contact'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertIn('/login/', response.url)
    
    # Testes para Edit Contact View
    def test_edit_contact_view_get_authenticated(self):
        """Testa acesso GET à edição de contato quando autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('edit_contact'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'edit_contact.html')
        self.assertIn('contacts', response.context)
    
    def test_edit_contact_view_post_valid(self):
        """Testa edição de contato com dados válidos"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'id': self.contact.id,
            'nome_completo': 'Nome Editado',
            'telefone': '19999999999',
            'email': 'editado@fatec.sp.gov.br',
            'observacao': 'Observação editada'
        }
        response = self.client.post(reverse('edit_contact'), data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('home'))
        
        # Verifica se o contato foi atualizado
        updated_contact = Agenda.objects.get(id=self.contact.id)
        self.assertEqual(updated_contact.nome_completo, 'Nome Editado')
    
    def test_edit_contact_view_post_invalid_id(self):
        """Testa edição de contato com ID inválido"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'id': 9999,  # ID que não existe
            'nome_completo': 'Nome',
            'telefone': '19999999999',
            'email': 'test@fatec.sp.gov.br',
            'observacao': 'Test'
        }
        response = self.client.post(reverse('edit_contact'), data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'edit_contact.html')
        self.assertTrue(response.context['error'])
    
    def test_edit_contact_view_post_missing_id(self):
        """Testa edição de contato sem ID"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'nome_completo': 'Nome',
            'telefone': '19999999999',
            'email': 'test@fatec.sp.gov.br',
            'observacao': 'Test'
        }
        response = self.client.post(reverse('edit_contact'), data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'edit_contact.html')
        self.assertTrue(response.context['error'])
    
    # Testes para Delete Contact View
    def test_delete_contact_view_get_authenticated(self):
        """Testa acesso GET à exclusão de contato quando autenticado"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('delete_contact'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'delete_contact.html')
        self.assertIn('contacts', response.context)
    
    def test_delete_contact_view_post_valid(self):
        """Testa exclusão de contato válida"""
        self.client.login(username='testuser', password='testpass123')
        contact_id = self.contact.id
        data = {'id': contact_id}
        response = self.client.post(reverse('delete_contact'), data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Agenda.objects.filter(id=contact_id).exists())
    
    def test_delete_contact_view_post_invalid_id(self):
        """Testa exclusão de contato com ID inválido"""
        self.client.login(username='testuser', password='testpass123')
        data = {'id': 9999}  # ID que não existe
        response = self.client.post(reverse('delete_contact'), data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'delete_contact.html')
        self.assertTrue(response.context['error'])
    
    def test_delete_contact_view_post_missing_id(self):
        """Testa exclusão de contato sem ID"""
        self.client.login(username='testuser', password='testpass123')
        data = {}  # Sem ID
        response = self.client.post(reverse('delete_contact'), data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'delete_contact.html')
        self.assertTrue(response.context['error'])