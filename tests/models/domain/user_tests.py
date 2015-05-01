import unittest, mock, datetime, bcrypt
from nose2.tools import such
from santa.models.domain.user import User
from tests import AppLifeCycle, fix_case
from mongoengine import ValidationError, NotUniqueError

with such.A('User model') as it:
    it.uses(AppLifeCycle)

    @it.has_setup
    def setup():
        return

    @it.has_teardown
    def teardown():
        return

    @it.has_test_setup
    def setup_each_test_case():
        return

    @it.has_test_teardown
    def teardown_each_test_case():
        return

    with it.having('fields'):
        with it.having('name'):
            @it.should('require name')
            def test_require_name():
                user = User(email='takoman@takoman.co')
                it.assertRaisesRegexp(ValidationError, "Field is required: \['name'\]", user.save)

        with it.having('email'):
            @it.should('require email')
            def test_require_email():
                user = User(name='Takoman')
                it.assertRaisesRegexp(ValidationError, "Field is required: \['email'\]", user.save)

            @it.should('have unique email')
            def test_unique_email():
                User(name='Takoman', email='takoman@takoman.co').save()
                user = User(name='Takoman 2', email='takoman@takoman.co')
                it.assertRaisesRegexp(NotUniqueError, "Tried to save duplicate unique keys", user.save)

        with it.having('role'):
            @it.should('have default user role')
            def test_default_role():
                user = User(name='Takoman', email='takoman@takoman.co').save()
                assert user.role == ['user']

            @it.should('only allow certain fields')
            def test_allowed_roles():
                user = User(name='Takoman', email='takoman@takoman.co', role=[u'user']).save()
                assert User.objects(email='takoman@takoman.co').first().role == [u'user']
                user.role.append(u'takoman')
                user.save()
                assert User.objects(email='takoman@takoman.co').first().role == [u'user', u'takoman']
                user.role.append(u'admin')
                user.save()
                assert User.objects(email='takoman@takoman.co').first().role == [u'user', u'takoman', u'admin']
                user.role.append(u'agent')
                it.assertRaisesRegexp(ValidationError, "Value must be one of", user.save)

        with it.having('created_at and updated_at'):
            @it.should('have default created_at and updated_at timestamps')
            def test_default_created_at_and_updated_at():
                User(name='Takoman', email='takoman@takoman.co').save()
                now = datetime.datetime.utcnow()
                created_at = User.objects(email='takoman@takoman.co').first().created_at
                updated_at = User.objects(email='takoman@takoman.co').first().updated_at
                # TODO: We should freeze the time, like TimeCop in Ruby
                assert (now - created_at).seconds < 5
                assert (now - updated_at).seconds < 5

    with it.having('hooks'):
        with it.having('#normalize_user'):
            @it.should('normalize user data')
            @unittest.skip('Modify document in pre_save_post_validation hook is not working')
            def test_normalize_user():
                User(name='Takoman', email='TaKOmAN@taKoMAn.cO', password='password').save()
                user = User.objects(name='Takoman').first()
                assert user.email == 'takoman@takoman.co'
                hashed = user.password
                assert bcrypt.hashpw('password', hashed) == hashed

    with it.having('instance methods'):
        with it.having('#send_welcome_email'):
            @it.should('send welcome email with correct info')
            @fix_case
            @mock.patch('santa.models.domain.user.MandrillAPI')
            @mock.patch('santa.models.domain.user.WelcomeEmailComposer')
            @mock.patch('santa.models.domain.user.Emailer')
            def test_send_welcom_email(Emailer, WelcomeEmailComposer, MandrillAPI, case=None):
                postman = MandrillAPI.return_value
                composer = WelcomeEmailComposer.return_value
                emailer = Emailer.return_value
                emailer.send_email = mock.Mock()
                user = User(name='Takoman', email='takoman@takoman.co')
                user.send_welcome_email()

                MandrillAPI.assert_called_with()
                WelcomeEmailComposer.assert_called_with('welcome.html')
                Emailer.assert_called_once_with(to_name='Takoman',
                                                to_email='takoman@takoman.co',
                                                postman=postman,
                                                composer=composer)
                emailer.send_email.assert_called_once_with()

        with it.having('#link_social_auth'):
            @it.should('link the user to the social data passed in')
            @fix_case
            @mock.patch('santa.models.domain.user.SocialAuth')
            def test_link_social_auth(SocialAuth, case=None):
                # TODO Consider using some sort of fabricator instead of hard code here.
                data = {
                    'uid': '10152476049619728',
                    'info': {
                        'name': 'Takoman',
                        'email': 'takoman+1@takoman.co',
                        'nickname': 'Takomanman',
                        'first_name': 'Tako',
                        'last_name': 'Man',
                        'location': '401 Broadway, New York',
                        'description': 'Social Auth',
                        'image': 'http://lala.com/lala.jpg',
                        'phone': '123-456-7890',
                        'urls': {}
                    },
                    'credentials': {},
                    'extra': {}
                }
                social_auth = SocialAuth.return_value
                social_auth.save = mock.Mock()
                user = User(name='Takoman', email='takoman@takoman.co')
                user.link_social_auth(data)
                SocialAuth.assert_called_once_with(user=user,
                                                   uid='10152476049619728',
                                                   name='Takoman',
                                                   email='takoman+1@takoman.co',
                                                   nickname='Takomanman',
                                                   first_name='Tako',
                                                   last_name='Man',
                                                   location='401 Broadway, New York',
                                                   description='Social Auth',
                                                   image='http://lala.com/lala.jpg',
                                                   phone='123-456-7890')
                social_auth.save.assert_called_once_with()

it.createTests(globals())
