"""Test all utilities implemented."""
from flaskapi.v1.user.util import hash_password, verify_password


def test_hashing_password():
    password = 'password123'
    hashed_password, salt = hash_password(password=password)

    assert password != hashed_password
    assert isinstance(salt, str)
    assert isinstance(hashed_password, str)


def test_verifying_password():
    password = 'fhsfis8we'
    fake_password = 'passeiw12&'
    fake_password1 = 'passeiwfdafa12&'
    fake_password2 = 'fhsfis8we '
    hashed_pass, salt = hash_password(password=password)
    # Verify password
    assert not verify_password(password=fake_password, pass_hash=hashed_pass,
                               salt=salt)
    assert not verify_password(password=fake_password1, pass_hash=hashed_pass,
                               salt=salt)
    assert not verify_password(password=fake_password2, pass_hash=hashed_pass,
                               salt=salt)
    assert verify_password(password=password, pass_hash=hashed_pass,
                           salt=salt)
    assert not verify_password(password=password, pass_hash=hashed_pass+'27W',
                               salt=salt)
    assert not verify_password(password=password, pass_hash=hashed_pass,
                               salt=salt+'r7U')
