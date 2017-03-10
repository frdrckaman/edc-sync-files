import os

from django.test.testcases import TestCase
from django.test.utils import tag
from django.conf import settings
from faker import Faker
from edc_example.models import TestModel
from edc_sync.models import OutgoingTransaction

from edc_sync_files.classes import TransactionDumps
from edc_sync_files.models import History


@tag('TestTransactionDumps')
class TestTransactionDumps(TestCase):

    def setUp(self):
        self.fake = Faker()

    def test_export_to_json_file(self):
        # Create transactions
        TestModel.objects.using('client').create(f1=self.fake.name())
        TestModel.objects.using('client').create(f1=self.fake.name())

        # Dump transaction
        path = os.path.join(settings.MEDIA_ROOT, "transactions", "outgoing")
        tx_dumps = TransactionDumps(path, using='client', hostname="010")

        outgoing_transactions = OutgoingTransaction.objects.using('client').filter(
            is_consumed_server=True)
        self.assertGreater(outgoing_transactions.count(), 0)

        self.assertTrue(tx_dumps.is_exported_to_json)

        outgoing_transactions = OutgoingTransaction.objects.using('client').filter(
            is_consumed_server=True)
        self.assertGreater(outgoing_transactions.count(), 0)

        self.assertEqual(History.objects.all().count(), 1)