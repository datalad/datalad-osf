# mock test to see if travis correctly decrypts
def test_travis_decrypt():
    import os
    assert 'OSF_USER' in os.environ
    assert 'OSF_PASSWORD' in os.environ
    assert 'OSF_TOKEN' in os.environ
