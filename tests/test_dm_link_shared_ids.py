import os
import importlib
import unittest

import datman
import datman.config

link_shared = importlib.import_module('bin.dm_link_shared_ids')

class TestRecord(unittest.TestCase):
    mock_redcap_record = {'par_id': 'STUDY_SITE_0001_01_01',
            'record_id': 0,
            'shared_parid_1': 'STUDY_SITE_0002_01_01',
            'shared_parid_2': 'STUDY2_CMH_9999_01_01',
            'shared_parid_8': 'OTHER_CMH_1234_01_01',
            'cmts': 'No comment.'}

    def test_doesnt_crash_with_bad_id(self):
        bad_redcap_record = {'par_id': 'STUDY_0001_01',
                'record_id': 0,
                'shared_parid': [],
                'cmts': ''}
        record = link_shared.Record(bad_redcap_record)
        assert record.id is None
        assert record.study is None
        assert not record.matches_study('STUDY')

    def test_finds_all_shared_ids_in_record(self):
        record = link_shared.Record(self.mock_redcap_record)

        expected = [self.mock_redcap_record['shared_parid_1'],
                    self.mock_redcap_record['shared_parid_2'],
                    self.mock_redcap_record['shared_parid_8']]

        assert sorted(record.shared_ids) == sorted(expected)
