from django.test import TestCase
from core.models import Agenda

class AgendaModelTest(TestCase):
    def setUp(self):
        self.agenda = Agenda.objects.create(
            nome_completo="Renan Marques",
            telefone="(19) 99999-9999",  # número fictício
            email="renan.marques3@fatec.sp.gov.br",
            observacao="Cliente importante, prefere contato por e-mail."
        )

    def test_agenda_criada_com_sucesso(self):
        self.assertEqual(self.agenda.nome_completo, "Renan Marques")
        self.assertEqual(self.agenda.telefone, "(19) 99999-9999")
        self.assertEqual(self.agenda.email, "renan.marques3@fatec.sp.gov.br")
        self.assertEqual(self.agenda.observacao, "Cliente importante, prefere contato por e-mail.")

    def test_str_retorna_nome_e_email(self):
        self.assertEqual(str(self.agenda), "Renan Marques - renan.marques3@fatec.sp.gov.br")
