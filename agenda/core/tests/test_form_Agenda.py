from django.test import TestCase
from core.forms import AgendaForm

class AgendaFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'nome_completo': 'Renan Marques',
            'telefone': '19999999999',  # número fictício
            'email': 'renan.marques3@fatec.sp.gov.br',
            'observacao': 'Teste'
        }

    def test_form_has_fields(self):
        form = AgendaForm()
        expected_fields = ['nome_completo', 'telefone', 'email', 'observacao']
        self.assertSequenceEqual(list(form.fields), expected_fields)

    def test_valid_form(self):
        form = AgendaForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_nome_completo_no_empty_fields(self):
        data = self.valid_data.copy()
        data['nome_completo'] = ''
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome_completo', form.errors)

    def test_nome_completo_no_digits(self):
        data = self.valid_data.copy()
        data['nome_completo'] = 'Renan123'
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'O nome completo deve conter apenas letras e espaços.',
            form.errors['nome_completo']
        )

    def test_phone_with_letters(self):
        data = self.valid_data.copy()
        data['telefone'] = '19999abc90'
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'O telefone deve conter apenas números.',
            form.errors['telefone']
        )

    def test_phone_lower_necessary_digits(self):
        data = self.valid_data.copy()
        data['telefone'] = '123456789'
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'O telefone deve ter entre 10 e 11 dígitos.',
            form.errors['telefone']
        )

    def test_phone_more_digits_than_necessary(self):
        data = self.valid_data.copy()
        data['telefone'] = '1999999999999'
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'O telefone deve ter entre 10 e 11 dígitos.',
            form.errors['telefone']
        )

    def test_email_must_be_institucional(self):
        data = self.valid_data.copy()
        data['email'] = 'usuario@gmail.com'
        form = AgendaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Informe seu e-mail institucional.',
            form.errors['email']
        )
