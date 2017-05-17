import os
import tempfile

from django.apps import apps as django_apps
from django.test import TestCase, tag

from ..models import ExportedTransactionFileHistory
from ..transaction import TransactionFileSender
from edc_sync_files.transaction.transaction_file_sender import TransactionFileSenderError


class TestTransactionFileSender(TestCase):

    @tag('send')
    def test_init(self):
        _, src = tempfile.mkstemp(text=True)
        src_path = os.path.dirname(src)
        dst_tmp_path = f'{tempfile.gettempdir()}/tmp'
        if not os.path.exists(dst_tmp_path):
            os.mkdir(dst_tmp_path)
        dst_path = f'{tempfile.gettempdir()}/dst'
        if not os.path.exists(dst_path):
            os.mkdir(dst_path)
        TransactionFileSender(
            history_model=ExportedTransactionFileHistory,
            update_history_model=False,
            src_path=src_path, dst_path=dst_path, dst_tmp_path=dst_tmp_path)

    @tag('send')
    def test_send_custom_paths(self):
        _, src = tempfile.mkstemp(text=True)
        with open(src, 'w') as fd:
            fd.write('erik' * 10000)
        src_filename = os.path.basename(src)
        src_path = os.path.dirname(src)
        dst_tmp_path = f'{tempfile.gettempdir()}/tmp'
        if not os.path.exists(dst_tmp_path):
            os.mkdir(dst_tmp_path)
        dst_path = f'{tempfile.gettempdir()}/dst'
        if not os.path.exists(dst_path):
            os.mkdir(dst_path)
        archive_path = f'{tempfile.gettempdir()}/archive'
        if not os.path.exists(archive_path):
            os.mkdir(archive_path)
        tx_file_sender = TransactionFileSender(
            history_model=ExportedTransactionFileHistory,
            update_history_model=False,
            src_path=src_path, dst_path=dst_path,
            dst_tmp_path=dst_tmp_path, archive_path=archive_path)
        tx_file_sender.send(filenames=[src_filename])
        self.assertTrue(os.path.exists(os.path.join(dst_path, src_filename)))
        self.assertTrue(os.path.exists(
            os.path.join(archive_path, src_filename)))

    @tag('send')
    def test_send_default_paths(self):
        app_config = django_apps.get_app_config('edc_sync_files')
        _, src = tempfile.mkstemp(text=True, dir=app_config.source_folder)
        src_filename = os.path.basename(src)
        tx_file_sender = TransactionFileSender(
            history_model=ExportedTransactionFileHistory,
            update_history_model=False)
        tx_file_sender.send(filenames=[src_filename])
        self.assertTrue(os.path.exists(os.path.join(
            app_config.destination_folder, src_filename)))
        self.assertTrue(os.path.exists(
            os.path.join(app_config.archive_folder, src_filename)))

    @tag('send')
    def test_send_update_history(self):
        app_config = django_apps.get_app_config('edc_sync_files')
        _, src = tempfile.mkstemp(text=True, dir=app_config.source_folder)
        src_filename = os.path.basename(src)
        ExportedTransactionFileHistory.objects.create(
            filename=src_filename, sent=False)
        tx_file_sender = TransactionFileSender(
            history_model=ExportedTransactionFileHistory)
        tx_file_sender.send(filenames=[src_filename])
        try:
            ExportedTransactionFileHistory.objects.get(
                filename=src_filename,
                sent=True, sent_datetime__isnull=False)
        except ExportedTransactionFileHistory.DoesNotExist:
            self.fail(
                'ExportedTransactionFileHistory.DoesNotExist unexpectedly raised')

    @tag('user')
    def test_transaction_file_sender_username(self):
        app_config = django_apps.get_app_config('edc_sync_files')
        tx_file_sender = TransactionFileSender(
            history_model=ExportedTransactionFileHistory,
            update_history_model=False, username=app_config.user)
        _, src = tempfile.mkstemp(text=True, dir=app_config.source_folder)
        src_filename = os.path.basename(src)
        self.assertRaises(TransactionFileSenderError, tx_file_sender.send, filenames=[src_filename])
