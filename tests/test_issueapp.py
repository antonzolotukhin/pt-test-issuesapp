import pytest
from argparse import ArgumentTypeError
from pttestissuesapp import issuesapp


@pytest.mark.httpretty
def test_GitHubAPIRequest_returns_parsed_json():

    repos = issuesapp.GitHubAPIRequest('users/testuser/repos')

    assert repos[0]['name'] == 'betaflight'
    assert repos[1]['name'] == 'betaflight-configurator'
    assert repos[2]['name'] == 'betaflight-configurator-nightlies'


@pytest.mark.httpretty
def test_GitHubAPIRequest_raise_exception_on_unsuccesful_request():
    with pytest.raises(issuesapp.HTTPGeneralException):
        assert issuesapp.GitHubAPIRequest('omg/wtf')


def test_GetReposByUser(GitHubAPIRequest_mock):

    repos = list(issuesapp.GetReposByUser('testuser'))

    assert repos[0] == 'betaflight'
    assert repos[1] == 'betaflight-configurator'
    assert repos[2] == 'betaflight-configurator-nightlies'
    assert repos[3] == 'betaflight-crsf-tx-scripts'


def test_GetIssuesByUserRepo_values(GitHubAPIRequest_mock):
    issues = list(issuesapp.GetIssuesByUserRepo('testuser', 'blackbox-tools'))

    assert issues[5] == (2, 'Provide pre built binaries.')


def test_GetIssuesByUserRepo_length(GitHubAPIRequest_mock):
    issues = list(issuesapp.GetIssuesByUserRepo('testuser', 'blackbox-tools'))

    assert len(issues) == 6


def test_GetIssuesByUserRepo_empty(GitHubAPIRequest_mock):
    issues = issuesapp.GetIssuesByUserRepo('testuser',
                                           'betaflight-configurator-nightlies')

    assert len(list(issues)) == 0


def test_GithubCredsType_exception_on_passwd():
    with pytest.raises(ArgumentTypeError):
        assert issuesapp.GithubCredsType('antonzolotukhin:AbraKadbra31337')


def test_GithubCredsType_exception_on_toolong_token():
    with pytest.raises(ArgumentTypeError):
        c = 'randlf:1bea06ef9c1b7b2a8babadcb87ba426d3feb7b6e1'
        assert issuesapp.GithubCredsType(c)


def test_GithubCredsType_exception_on_toolong_login():
    with pytest.raises(ArgumentTypeError):
        u = 'qwertyqwertyqwertyqwertyqwertyqwertyqwertyqwerty'
        p = '1bea06ef9c1b7b2a8babadcb87ba426d3feb7b6e'
        c = u + ':' + p
        assert issuesapp.GithubCredsType(c)


def test_GithubCredsType_empty_is_ok():
    assert issuesapp.GithubCredsType('') == ''


def test_GithubCredsType_login_token_is_ok():
    c = 'vasya:1bea06ef9c1b7b2a8babadcb87ba426d3feb7b6e'
    assert issuesapp.GithubCredsType(c) == c
