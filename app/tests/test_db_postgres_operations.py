import unittest
from app import app, db
from models.users import User


class TestDatabaseOperations(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        app.config.from_object('config.DevelopmentConfig')
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down test environment."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        """Test creating a user."""
        user = User(email='test@example.com', first_name='John',
                    last_name='Doe', password='password', is_admin=True)
        with app.app_context():
            db.session.add(user)
            db.session.commit()

            # Retrieve the user from the database to ensure it's
            # properly committed
            saved_user = User.query.filter_by(email='test@example.com').first()

            # Assert that user was created successfully
            self.assertIsNotNone(saved_user)
            self.assertEqual(saved_user.email, 'test@example.com')

    def test_get_user(self):
        """Test retrieving a user."""
        # Create a user first
        user = User(email='test@example.com', first_name='John',
                    last_name='Doe', password='password', is_admin=True)
        with app.app_context():
            db.session.add(user)
            db.session.commit()

            # Retrieve the user using its ID
            saved_user = User.query.filter_by(email='test@example.com').first()

            # Make a GET request to retrieve the user
            response = self.app.get(f'/users/{saved_user.id}')

            # Assert that the request was successful and user data matches
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['email'], 'test@example.com')

    def test_update_user(self):
        """Test updating a user."""
        # Create a user first
        user = User(email='test@example.com', first_name='John',
                    last_name='Doe', password='password', is_admin=True)
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        # Retrieve the user using its ID
            saved_user = User.query.filter_by(email='test@example.com').first()

        # Make a PUT request to update the user's data
            updated_data = {
                'email': 'updated@example.com',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'password': 'new_password'
            }
            response = self.app.put(f'/users/{saved_user.id}', json=
                                    updated_data)

        # Assert that the request was successful
            self.assertEqual(response.status_code, 200)

        # Retrieve the updated user from the database
            updated_user = User.query.filter_by(email='updated@example.com').first()
            self.assertIsNotNone(updated_user)
            self.assertEqual(updated_user.first_name, 'Jane')

    def test_delete_user(self):
        """Test deleting a user."""
    # Create a user first
        user = User(email='test@example.com', first_name='John',
                    last_name='Doe', password='password', is_admin=True)
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        # Retrieve the user using its ID
            saved_user = User.query.filter_by(email=
                                              'test@example.com').first()

        # Make a DELETE request to delete the user
            response = self.app.delete(f'/users/{saved_user.id}')

        # Assert that the request was successful and returned 204
            self.assertEqual(response.status_code, 200)

        # Try to retrieve the user again to ensure it's deleted
            deleted_user = User.query.get(saved_user.id)
            self.assertIsNone(deleted_user, 
            "User was not deleted from the database.")

if __name__ == '__main__':
    unittest.main()
