import httpretty
import pytest
import requests
from argparse import ArgumentTypeError
from issuesapp import *

@pytest.mark.httpretty
def test_GitHubAPIRequest_returns_parsed_json():
    
    repos = GitHubAPIRequest('users/testuser/repos')

    assert repos[0]['name'] == 'betaflight'
    assert repos[1]['name'] == 'betaflight-configurator'
    assert repos[2]['name'] == 'betaflight-configurator-nightlies'



@pytest.mark.httpretty
def test_GitHubAPIRequest_raise_exception_on_unsuccesful_request():

    with pytest.raises(HTTPGeneralException):
        assert GitHubAPIRequest('omg/wtf')

@pytest.mark.httpretty
def test_GetReposByUser():

    repos = list(GetReposByUser('testuser'))
  
    assert repos[0] == 'betaflight'
    assert repos[1] == 'betaflight-configurator'
    assert repos[2] == 'betaflight-configurator-nightlies'
    assert repos[3] == 'betaflight-crsf-tx-scripts'

@pytest.mark.httpretty
def test_GetIssuesByUserRepo_values():
    issues = list(GetIssuesByUserRepo('testuser','blackbox-tools'))

    assert issues[5] == (2, 'Provide pre built binaries.')

@pytest.mark.httpretty
def test_GetIssuesByUserRepo_length():
    issues = list(GetIssuesByUserRepo('testuser','blackbox-tools'))
    
    assert len(issues) == 6

@pytest.mark.httpretty
def test_GetIssuesByUserRepo_empty():
    issues = list(GetIssuesByUserRepo('testuser','betaflight-configurator-nightlies'))
    
    assert len(issues) == 0

def test_GithubCredsType_exception_on_passwd():
   with pytest.raises(ArgumentTypeError):
       assert GithubCredsType('antonzolotukhin:AbraKadbra31337')

def test_GithubCredsType_exception_on_toolong_token():
   with pytest.raises(ArgumentTypeError):
       assert GithubCredsType('adolf:1bea06ef9c1b7b2a8babadcb87ba426d3feb7b6e1')

def test_GithubCredsType_exception_on_toolong_login():
   with pytest.raises(ArgumentTypeError):
       assert GithubCredsType('qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty:1bea06ef9c1b7b2a8babadcb87ba426d3feb7b6e')

def test_GithubCredsType_empty_is_ok():
       assert GithubCredsType('') == ''

def test_GithubCredsType_login_token_is_ok():
    creds='vasya:1bea06ef9c1b7b2a8babadcb87ba426d3feb7b6e'
    assert GithubCredsType(creds) == creds

