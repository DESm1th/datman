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
        export_settings = {
            'T1': {
                'formats': ['nii', 'dcm', 'mnc'],
                'qc_type': 'anat'
            },
        }

        def get_key(name):
            if name == 'ExportSettings':
                return datman.config.TagInfo(export_settings)
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
