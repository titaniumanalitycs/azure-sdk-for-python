# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
USAGE:
    python test_samples.py

    Set the environment variables with your own values before running the samples.
    See independent sample files to check what env variables must be set.
"""


import subprocess
import functools
import sys
import os
import pytest
import pprint
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormTrainingClient
from testcase import FormRecognizerTest, GlobalFormRecognizerAccountPreparer


def run(cmd, my_env):
    os.environ['PYTHONUNBUFFERED'] = "1"
    proc = subprocess.Popen(cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.STDOUT,
        env = my_env
    )
    stdout, stderr = proc.communicate()

    return proc.returncode, stdout, stderr

def _test_file(file_name, account, key):
    os.environ['AZURE_FORM_RECOGNIZER_ENDPOINT'] = account
    os.environ['AZURE_FORM_RECOGNIZER_KEY'] = key
    path_to_sample = os.path.abspath(
        os.path.join(os.path.abspath(__file__), "..", "..", "./samples/" + file_name))
    my_env = dict(os.environ)
    if sys.version_info < (3, 5):
        my_env = {key: str(val) for key, val in my_env.items()}
    code, out, err = run([sys.executable, path_to_sample], my_env=my_env)
    try:
        assert code == 0
        assert err is None
    except AssertionError as e:
        e.args += (out, )
        raise AssertionError(e)

class TestSamples(FormRecognizerTest):
    @pytest.mark.live_test_only
    @GlobalFormRecognizerAccountPreparer()
    def test_sample_authentication(self, resource_group, location, form_recognizer_account, form_recognizer_account_key):
        os.environ['AZURE_FORM_RECOGNIZER_AAD_ENDPOINT'] = self.get_settings_value("FORM_RECOGNIZER_AAD_ENDPOINT")
        os.environ['AZURE_CLIENT_ID'] = self.get_settings_value("CLIENT_ID")
        os.environ['AZURE_CLIENT_SECRET'] = self.get_settings_value("CLIENT_SECRET")
        os.environ['AZURE_TENANT_ID'] = self.get_settings_value("TENANT_ID")
        _test_file('sample_authentication.py', form_recognizer_account, form_recognizer_account_key)

    @pytest.mark.live_test_only
    @GlobalFormRecognizerAccountPreparer()
    def test_sample_get_bounding_boxes(self, resource_group, location, form_recognizer_account, form_recognizer_account_key):
        os.environ['CONTAINER_SAS_URL'] = self.get_settings_value("FORM_RECOGNIZER_STORAGE_CONTAINER_SAS_URL")
        ftc = FormTrainingClient(form_recognizer_account,  AzureKeyCredential(form_recognizer_account_key))
        container_sas_url = os.environ['CONTAINER_SAS_URL']
        poller = ftc.begin_training(container_sas_url, use_training_labels=False)
        model = poller.result()
        os.environ['CUSTOM_TRAINED_MODEL_ID'] = model.model_id
        _test_file('sample_get_bounding_boxes.py', form_recognizer_account, form_recognizer_account_key)

    @pytest.mark.live_test_only
    @GlobalFormRecognizerAccountPreparer()
    def test_sample_manage_custom_models(self, resource_group, location, form_recognizer_account, form_recognizer_account_key):
        _test_file('sample_manage_custom_models.py', form_recognizer_account, form_recognizer_account_key)

    @pytest.mark.live_test_only
    @GlobalFormRecognizerAccountPreparer()
    def test_sample_recognize_content(self, resource_group, location, form_recognizer_account, form_recognizer_account_key):
        _test_file('sample_recognize_content.py', form_recognizer_account, form_recognizer_account_key)

    @pytest.mark.live_test_only
    @GlobalFormRecognizerAccountPreparer()
    def test_sample_recognize_custom_forms(self, resource_group, location, form_recognizer_account, form_recognizer_account_key):
        os.environ['CONTAINER_SAS_URL'] = self.get_settings_value("FORM_RECOGNIZER_STORAGE_CONTAINER_SAS_URL")
        ftc = FormTrainingClient(form_recognizer_account,  AzureKeyCredential(form_recognizer_account_key))
        container_sas_url = os.environ['CONTAINER_SAS_URL']
        poller = ftc.begin_training(container_sas_url, use_training_labels=False)
        model = poller.result()
        os.environ['CUSTOM_TRAINED_MODEL_ID'] = model.model_id
        _test_file('sample_recognize_custom_forms.py', form_recognizer_account, form_recognizer_account_key)

    @pytest.mark.live_test_only
    @GlobalFormRecognizerAccountPreparer()
    def test_sample_recognize_receipts_from_url(self, resource_group, location, form_recognizer_account, form_recognizer_account_key):
        _test_file('sample_recognize_receipts_from_url.py', form_recognizer_account, form_recognizer_account_key)

    @pytest.mark.live_test_only
    @GlobalFormRecognizerAccountPreparer()
    def test_sample_recognize_receipts(self, resource_group, location, form_recognizer_account, form_recognizer_account_key):
        _test_file('sample_recognize_receipts.py', form_recognizer_account, form_recognizer_account_key)

    @pytest.mark.live_test_only
    @GlobalFormRecognizerAccountPreparer()
    def test_sample_train_model_with_labels(self, resource_group, location, form_recognizer_account, form_recognizer_account_key):
        os.environ['CONTAINER_SAS_URL'] = self.get_settings_value("FORM_RECOGNIZER_STORAGE_CONTAINER_SAS_URL")
        _test_file('sample_train_model_with_labels.py', form_recognizer_account, form_recognizer_account_key)

    @pytest.mark.live_test_only
    @GlobalFormRecognizerAccountPreparer()
    def test_sample_train_model_without_labels(self, resource_group, location, form_recognizer_account, form_recognizer_account_key):
        os.environ['CONTAINER_SAS_URL'] = self.get_settings_value("FORM_RECOGNIZER_STORAGE_CONTAINER_SAS_URL")
        _test_file('sample_train_model_without_labels.py', form_recognizer_account, form_recognizer_account_key)

    @pytest.mark.live_test_only
    @GlobalFormRecognizerAccountPreparer()
    def test_sample_strongly_typing_recognized_form(self, resource_group, location, form_recognizer_account, form_recognizer_account_key):
        _test_file('sample_strongly_typing_recognized_form.py', form_recognizer_account, form_recognizer_account_key)

    @pytest.mark.live_test_only
    @GlobalFormRecognizerAccountPreparer()
    def test_sample_copy_model(self, resource_group, location, form_recognizer_account, form_recognizer_account_key):
        os.environ['CONTAINER_SAS_URL'] = self.get_settings_value("FORM_RECOGNIZER_STORAGE_CONTAINER_SAS_URL")
        ftc = FormTrainingClient(form_recognizer_account,  AzureKeyCredential(form_recognizer_account_key))
        container_sas_url = os.environ['CONTAINER_SAS_URL']
        poller = ftc.begin_training(container_sas_url, use_training_labels=False)
        model = poller.result()
        os.environ['AZURE_SOURCE_MODEL_ID'] = model.model_id
        os.environ["AZURE_FORM_RECOGNIZER_TARGET_ENDPOINT"] = form_recognizer_account
        os.environ["AZURE_FORM_RECOGNIZER_TARGET_KEY"] = form_recognizer_account_key
        os.environ["AZURE_FORM_RECOGNIZER_TARGET_REGION"] = location
        os.environ["AZURE_FORM_RECOGNIZER_TARGET_RESOURCE_ID"] = \
            "/subscriptions/" + self.get_settings_value("SUBSCRIPTION_ID") + "/resourceGroups/" + \
            resource_group.name + "/providers/Microsoft.CognitiveServices/accounts/" + \
            FormRecognizerTest._FORM_RECOGNIZER_NAME
        _test_file('sample_copy_model.py', form_recognizer_account, form_recognizer_account_key)

    @pytest.mark.live_test_only
    @GlobalFormRecognizerAccountPreparer()
    def test_sample_differentiate_output_models_trained_with_and_without_labels(
            self, resource_group, location, form_recognizer_account, form_recognizer_account_key
    ):
        os.environ['CONTAINER_SAS_URL'] = self.get_settings_value("FORM_RECOGNIZER_STORAGE_CONTAINER_SAS_URL")
        ftc = FormTrainingClient(form_recognizer_account,  AzureKeyCredential(form_recognizer_account_key))
        container_sas_url = os.environ['CONTAINER_SAS_URL']
        poller = ftc.begin_training(container_sas_url, use_training_labels=False)
        unlabeled_model = poller.result()
        poller = ftc.begin_training(container_sas_url, use_training_labels=True)
        labeled_model = poller.result()
        os.environ["ID_OF_MODEL_TRAINED_WITH_LABELS"] = labeled_model.model_id
        os.environ["ID_OF_MODEL_TRAINED_WITHOUT_LABELS"] = unlabeled_model.model_id
        _test_file('sample_differentiate_output_models_trained_with_and_without_labels.py',
                   form_recognizer_account,
                   form_recognizer_account_key
                   )
