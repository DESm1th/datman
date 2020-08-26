import importlib

import pytest
from mock import patch, Mock, call

import datman.config

uc = importlib.import_module('bin.update_config')


class TestPromptUser:

    @patch('builtins.input')
    def test_true_only_when_y_given(self, mock_input):
        user_input = [
            '         ',
            '',
            'y',
            'n',
        ]

        mock_input.side_effect = lambda x: user_input.pop()

        assert uc.prompt_user('Test message') is False
        assert uc.prompt_user('Test message') is True
        assert uc.prompt_user('Test message') is False
        assert uc.prompt_user('Test message') is False

    @patch('builtins.input')
    def test_raises_runtime_error_for_unexpected_response(self, mock_input):
        mock_input.return_value = 'dfgsxcvqa'
        with pytest.raises(RuntimeError):
            uc.prompt_user('Test message')


class TestUpdateTags:

    @patch('datman.dashboard.get_tags')
    def test_tag_created_in_database_if_doesnt_exist(self, mock_db_tags):
        config = self.get_config()
        uc.update_tags(config)
        assert call('T1', create=True) in mock_db_tags.call_args_list

    @patch('datman.dashboard.get_tags')
    def test_existing_tag_updated_when_settings_changed(self, mock_db_tags):
        config = self.get_config()

        db_tag = Mock()
        db_tag.tag = 'T1'
        db_tag.qc_type = 'func'
        db_tag.pha_type = 'func'
        existing_tags = [db_tag]

        mock_db_tags.side_effect = self.get_tag_func(existing_tags)

        uc.update_tags(config)

        assert len(existing_tags) == 1
        db_tag = existing_tags[0]
        assert db_tag.tag == 'T1'
        assert db_tag.qc_type == 'anat'
        assert db_tag.pha_type is None

    @patch('bin.update_config.delete_records')
    @patch('datman.dashboard.get_tags')
    def test_calls_delete_records_if_undefined_tags_exist(
            self, mock_db_tags, mock_delete):
        config = self.get_config()

        bad_tag = Mock()
        bad_tag.tag = 'T2'
        expected_tag = Mock()
        expected_tag.tag = 'T1'
        existing_tags = [bad_tag, expected_tag]

        mock_db_tags.side_effect = self.get_tag_func(existing_tags)

        uc.update_tags(config)

        assert mock_delete.call_count == 1
        assert mock_delete.call_args[0] == ([bad_tag],)

    def get_config(self):
        def get_key(name):
            if name == 'ExportSettings':
                return {
                            'T1': {
                                'formats': ['nii', 'dcm', 'mnc'],
                                'qc_type': 'anat'
                            },
                        }
            raise datman.config.UndefinedSetting

        config = Mock(spec=datman.config.config)
        config.get_key.side_effect = get_key

        return config

    def get_tag_func(self, existing_tags):
        # Provide a mock datman.dashboard.get_tag interface
        # with 'existing_tags' as the fake records.
        def get_tag(tag=None, create=False):
            if not tag:
                return existing_tags

            found = [item for item in existing_tags if item.tag == tag]
            if not found and create:
                new_tag = Mock()
                new_tag.tag = tag
                existing_tags.append(new_tag)
                return [new_tag]

            return found
        return get_tag


class TestDeleteRecords:

    def test_nothing_deleted_when_skip_delete_flag_set(self):
        records = self.get_mock_records()
        uc.delete_records(records, skip_delete=True)
        for item in records:
            assert item.delete.call_count == 0

    def test_all_given_records_deleted_when_delete_all_set(self):
        records = self.get_mock_records()
        uc.delete_records(records, delete_all=True)
        for item in records:
            assert item.delete.call_count == 1

    @patch('builtins.input')
    def test_delete_func_used_to_delete_when_provided(self, mock_input):
        mock_input.return_value = 'y'
        def delete_func(x):
            x.alt_delete()
        records = self.get_mock_records()
        uc.delete_records(records, delete_func=delete_func)

        for item in records:
            assert item.delete.call_count == 0

        for item in records:
            assert item.alt_delete.call_count == 1

    @patch('builtins.input')
    @patch('bin.update_config.prompt_user')
    def test_prompt_changed_when_flag_set(self, mock_prompt, mock_input):
        mock_input.return_value = 'y'
        records = self.get_mock_records()

        message = 'Testing prompt flag'
        uc.delete_records(records, prompt=message)
        for call in mock_prompt.call_args_list:
            assert message in call.args[0]

    @patch('builtins.input')
    def test_records_only_deleted_when_user_consents(self, mock_input):
        responses = ['n', 'n', 'y', 'n']
        mock_input.side_effect = lambda x: responses.pop()
        records = self.get_mock_records()

        uc.delete_records(records)

        assert records[0].delete.call_count == 0
        assert records[1].delete.call_count == 1
        assert records[2].delete.call_count == 0
        assert records[3].delete.call_count == 0

    def get_mock_records(self):
        records = []
        for _ in range(4):
            records.append(Mock())
        return records


class TestUpdateExpectedScans:

    def test_no_crash_if_site_undefined_in_config(self):
        config = self.get_config()
        uc.update_expected_scans(Mock(), 'BADSITE', config)

    def test_no_crash_if_no_scans_defined_for_site(self):
        mock_study = Mock()
        mock_study.scantypes = {}
        config = self.get_config()
        uc.update_expected_scans(mock_study, 'NOSCANS', config)

    def test_no_scantypes_added_if_none_defined_in_config(self):
        mock_study = Mock()
        mock_study.scantypes = {}
        config = self.get_config()
        uc.update_expected_scans(mock_study, 'NOSCANS', config)
        assert mock_study.update_scantype.call_count == 0

    @patch('bin.update_config.delete_records')
    def test_attempts_to_delete_database_scantypes_if_not_in_config(self,
            mock_delete):
        mock_study = Mock()
        mock_t1 = Mock()
        mock_t1.scantype_id = 'T1'
        mock_t2 = Mock()
        mock_t2.scantype_id = 'T2'
        mock_study.scantypes = {
            'SITE': [mock_t1, mock_t2]
        }
        config = self.get_config()

        uc.update_expected_scans(mock_study, 'SITE', config)
        assert mock_delete.call_count == 1
        assert mock_delete.call_args_list[0].args[0][0] == mock_t2

    def test_expected_tags_updated_in_database(self):
        mock_t1 = Mock()
        mock_t1.scantype_id = 'T1'
        mock_study = Mock()
        mock_study.scantypes = {
            'SITE': [mock_t1]
        }
        config = self.get_config()

        uc.update_expected_scans(mock_study, 'SITE', config)
        assert mock_study.update_scantype.call_count == 1
        assert mock_study.update_scantype.call_args_list[0][0][1] == 'T1'

    def get_config(self):
        tag_settings = {
            'T1': {
                'formats': ['nii', 'dcm', 'mnc'],
                'qc_type': 'anat',
                'bids': {'class': 'anat', 'modality_label': 'T1w'},
                'Pattern': {'SeriesDescription': ['T1', 'BRAVO']},
                'Count': 1
            }
        }

        def get_tags(name):
            if name == 'SITE':
                return datman.config.TagInfo(tag_settings)
            if name == 'NOSCANS':
                return datman.config.TagInfo({})
            raise datman.config.UndefinedSetting

        config = Mock(spec=datman.config.config)
        config.get_tags.side_effect = get_tags

        return config
