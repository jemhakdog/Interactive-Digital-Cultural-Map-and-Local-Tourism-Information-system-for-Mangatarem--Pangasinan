import unittest
from app import create_app
from extensions import db
from models import Announcement, User, BarangayInfo

class AnnouncementTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        # db.create_all() and seed_database(self.app) are run inside create_app

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_test_user(self, username, role, barangay_id=None):
        existing = User.query.filter_by(username=username).first()
        if existing:
            return existing
        user = User(username=username, email=f"{username}@example.com", role=role, barangay_id=barangay_id)
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        return user

    def create_test_barangay(self, name):
        existing = BarangayInfo.query.filter_by(name=name).first()
        if existing:
            return existing
        barangay = BarangayInfo(name=name)
        db.session.add(barangay)
        db.session.commit()
        return barangay

    def test_announcement_model(self):
        """Test basic model fields and dictionary serialization."""
        brgy = self.create_test_barangay("Poblacion")
        user = self.create_test_user("contrib_user", "contributor", barangay_id=brgy.id)
        
        ann = Announcement(
            title="Road Closure Alert",
            content="Main highway closed due to maintenance.",
            user_id=user.id,
            barangay_id=brgy.id,
            status="pending"
        )
        db.session.add(ann)
        db.session.commit()
        
        # Verify columns
        self.assertIsNotNone(ann.id)
        self.assertEqual(ann.title, "Road Closure Alert")
        self.assertEqual(ann.content, "Main highway closed due to maintenance.")
        self.assertEqual(ann.status, "pending")
        
        # Verify to_dict serialization
        data = ann.to_dict()
        self.assertEqual(data["title"], "Road Closure Alert")
        self.assertEqual(data["barangay_name"], "Poblacion")
        self.assertEqual(data["author_name"], "contrib_user")

    def test_public_announcements_feed(self):
        """Test that only approved announcements display on public routes."""
        brgy = self.create_test_barangay("Poblacion")
        user = self.create_test_user("admin_user", "admin")
        
        # Create approved notice
        approved_ann = Announcement(
            title="Approved Notice",
            content="This notice should be visible.",
            user_id=user.id,
            status="approved"
        )
        # Create pending notice
        pending_ann = Announcement(
            title="Pending Notice",
            content="This should be hidden from public.",
            user_id=user.id,
            status="pending"
        )
        db.session.add_all([approved_ann, pending_ann])
        db.session.commit()

        # Query public feed
        resp = self.client.get("/announcements")
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode("utf-8")
        self.assertIn("Approved Notice", html)
        self.assertNotIn("Pending Notice", html)

        # Query home page index route
        resp_index = self.client.get("/")
        self.assertEqual(resp_index.status_code, 200)
        html_index = resp_index.data.decode("utf-8")
        self.assertIn("Approved Notice", html_index)
        self.assertNotIn("Pending Notice", html_index)

if __name__ == '__main__':
    unittest.main()
