import unittest
from app import create_app
from models import db, User, Course, Assessment, Certificate, Announcement, Submission, Enrollment

class CapacityConnectTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_01_homepage_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Capacity Connect', response.data)
        self.assertIn(b'Mayank', response.data)
        self.assertIn(b'Announcements', response.data)
        self.assertIn(b'Featured Courses', response.data)

    def test_02_auth_quick_logins(self):
        # Admin login
        res_admin = self.client.get('/auth/quick-login/admin', follow_redirects=True)
        self.assertEqual(res_admin.status_code, 200)
        self.assertIn(b'Mayank', res_admin.data)

        # Trainer login
        res_trainer = self.client.get('/auth/quick-login/trainer', follow_redirects=True)
        self.assertEqual(res_trainer.status_code, 200)
        self.assertIn(b'Dr. Sarah Jenkins', res_trainer.data)

        # Trainee login
        res_trainee = self.client.get('/auth/quick-login/trainee', follow_redirects=True)
        self.assertEqual(res_trainee.status_code, 200)
        self.assertIn(b'Alex Rivera', res_trainee.data)

    def test_03_courses_catalog_and_detail(self):
        res = self.client.get('/courses')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Foundations of Project Management', res.data)
        self.assertIn(b'Data Analytics with Python', res.data)

        c = Course.query.first()
        res_detail = self.client.get(f'/courses/{c.id}')
        self.assertEqual(res_detail.status_code, 200)
        self.assertIn(c.title.encode(), res_detail.data)

    def test_04_enrollment_and_feedback(self):
        # Log in as trainee Alex
        self.client.get('/auth/quick-login/trainee', follow_redirects=True)
        c = Course.query.filter_by(code='LDR-102').first()

        # Enroll
        res_enroll = self.client.post(f'/courses/{c.id}/enroll', follow_redirects=True)
        self.assertEqual(res_enroll.status_code, 200)
        self.assertIn(b'Enrolled Active', res_enroll.data)

        # Submit Feedback
        res_fb = self.client.post(f'/courses/{c.id}/feedback', data={
            'rating': '5',
            'comments': 'Super practical leadership frameworks!'
        }, follow_redirects=True)
        self.assertEqual(res_fb.status_code, 200)
        self.assertIn(b'Super practical leadership frameworks!', res_fb.data)

    def test_05_assessment_quiz_and_certification(self):
        # Log in as Mayank
        self.client.get('/auth/quick-login/admin', follow_redirects=True)
        asm = Assessment.query.first()
        self.assertIsNotNone(asm)

        # Open take page
        res_take = self.client.get(f'/assessments/{asm.id}/take')
        self.assertEqual(res_take.status_code, 200)
        self.assertIn(asm.title.encode(), res_take.data)

        # Submit answers (all correct)
        form_data = {}
        for q in asm.questions:
            form_data[f'question_{q.id}'] = q.correct_option

        res_sub = self.client.post(f'/assessments/{asm.id}/submit', data=form_data, follow_redirects=True)
        self.assertEqual(res_sub.status_code, 200)
        self.assertIn(b'Congratulations! You Passed!', res_sub.data)
        self.assertIn(b'100.0%', res_sub.data)

    def test_06_trainer_library_and_upload(self):
        # Log in as trainer Sarah
        self.client.get('/auth/quick-login/trainer', follow_redirects=True)
        res_lib = self.client.get('/library')
        self.assertEqual(res_lib.status_code, 200)
        self.assertIn(b'Trainer Knowledge Library', res_lib.data)

        # Upload web resource
        res_up = self.client.post('/library/upload', data={
            'title': 'Test Agile Video Stream',
            'description': 'Test resource description',
            'resource_type': 'video',
            'category': 'Management',
            'external_url': 'https://example.com/test.mp4',
            'duration': '15 mins'
        }, follow_redirects=True)
        self.assertEqual(res_up.status_code, 200)
        self.assertIn(b'Test Agile Video Stream', res_up.data)

    def test_07_admin_dashboard_and_users(self):
        # Log in as admin
        self.client.get('/auth/quick-login/admin', follow_redirects=True)

        res_dash = self.client.get('/admin/dashboard')
        self.assertEqual(res_dash.status_code, 200)
        self.assertIn(b'Analytics & Institutional Oversight', res_dash.data)

        # User approval check
        res_users = self.client.get('/admin/users')
        self.assertEqual(res_users.status_code, 200)
        self.assertIn(b'Priya Sharma', res_users.data)

        # Approve Priya
        priya = User.query.filter_by(email='trainee.priya@capacityconnect.org').first()
        res_appr = self.client.post(f'/admin/users/{priya.id}/approve', data={'action': 'approve'}, follow_redirects=True)
        self.assertEqual(res_appr.status_code, 200)
        self.assertIn(b'approved', res_appr.data.lower())

    def test_08_competency_matrix(self):
        self.client.get('/auth/quick-login/admin', follow_redirects=True)
        res_comp = self.client.get('/admin/competency-matrix')
        self.assertEqual(res_comp.status_code, 200)
        self.assertIn(b'Competency Mapping Matrix', res_comp.data)
        self.assertIn(b'AWS Cloud Solutions Architecture', res_comp.data)

    def test_09_certificate_view(self):
        cert = Certificate.query.first()
        self.assertIsNotNone(cert)
        res_cert = self.client.get(f'/certificate/{cert.cert_code}')
        self.assertEqual(res_cert.status_code, 200)
        self.assertIn(cert.recipient_name.encode(), res_cert.data)
        self.assertIn(cert.cert_code.encode(), res_cert.data)

    def test_10_landing_and_dashboard_routes(self):
        # Test landing route
        res_landing = self.client.get('/landing')
        self.assertEqual(res_landing.status_code, 200)
        self.assertIn(b'Capacity Connect', res_landing.data)
        self.assertIn(b'Transform Your Potential', res_landing.data)
        self.assertIn(b'The Capacity Connect Advantage', res_landing.data)

        # Test dashboard route
        res_dash = self.client.get('/dashboard')
        self.assertEqual(res_dash.status_code, 200)
        self.assertIn(b'Mayank', res_dash.data)
        self.assertIn(b'Available Courses', res_dash.data)

    def test_11_user_registration_pending_workflow(self):
        # 0. Clean up any existing candidate from previous test runs
        existing = User.query.filter_by(email='candidate@test.org').first()
        if existing:
            db.session.delete(existing)
            db.session.commit()

        # 1. Register new trainee
        res_reg = self.client.post('/auth/register', data={
            'name': 'New Candidate',
            'email': 'candidate@test.org',
            'password': 'password123',
            'role': 'trainee',
            'job_title': 'Junior Analyst',
            'organization': 'FinTech Corp'
        }, follow_redirects=True)
        self.assertEqual(res_reg.status_code, 200)
        self.assertIn(b'pending Administrator approval', res_reg.data)

        # 2. Verify account is pending in DB
        candidate = User.query.filter_by(email='candidate@test.org').first()
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate.status, 'pending')

        # 3. Attempt login before approval (should be blocked)
        res_login_fail = self.client.post('/auth/login', data={
            'email': 'candidate@test.org',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'pending Administrator approval', res_login_fail.data)

        # 4. Admin approves candidate
        self.client.get('/auth/quick-login/admin', follow_redirects=True)
        res_appr = self.client.post(f'/admin/users/{candidate.id}/approve', data={'action': 'approve'}, follow_redirects=True)
        self.assertEqual(res_appr.status_code, 200)

        # 5. Candidate can now log in
        self.client.get('/auth/logout', follow_redirects=True)
        res_login_success = self.client.post('/auth/login', data={
            'email': 'candidate@test.org',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(res_login_success.status_code, 200)
        self.assertIn(b'Welcome back, New Candidate!', res_login_success.data)

    def test_12_trainer_create_questionnaire_and_assessment(self):
        # Trainer logs in
        self.client.get('/auth/quick-login/trainer', follow_redirects=True)

        res_get = self.client.get('/trainer/assessments/new')
        self.assertEqual(res_get.status_code, 200)
        self.assertIn(b'Create MCQ Assessment Questionnaire', res_get.data)

        # Post new questionnaire
        res_create = self.client.post('/trainer/assessments/new', data={
            'title': 'Automated CI/CD Pipelines Evaluation',
            'subject': 'DevOps & Automation',
            'description': 'Test practical knowledge of CI/CD tooling.',
            'time_limit_minutes': '20',
            'passing_score': '75',
            'deadline': '2026-12-31',
            'question_counter': '2',
            'q_text_1': 'What is the primary benefit of Continuous Integration?',
            'q_a_1': 'Early defect detection',
            'q_b_1': 'Manual testing delay',
            'q_c_1': 'No version control',
            'q_d_1': 'Slower releases',
            'q_correct_1': 'A',
            'q_expl_1': 'CI detects defects early by testing code changes continuously.',
            'q_text_2': 'Which tool is commonly used for containerization in CI?',
            'q_a_2': 'Docker',
            'q_b_2': 'Notepad',
            'q_c_2': 'Paint',
            'q_d_2': 'Calculator',
            'q_correct_2': 'A',
            'q_expl_2': 'Docker provides portable containers for reproducible build environments.'
        }, follow_redirects=True)
        self.assertEqual(res_create.status_code, 200)

        # Verify assessment exists in DB
        asm = Assessment.query.filter_by(title='Automated CI/CD Pipelines Evaluation').first()
        self.assertIsNotNone(asm)
        self.assertEqual(asm.questions.count(), 2)

    def test_13_trainer_dedicated_upload_hub_and_delete(self):
        self.client.get('/auth/quick-login/trainer', follow_redirects=True)

        # View upload hub
        res_hub = self.client.get('/trainer/upload')
        self.assertEqual(res_hub.status_code, 200)
        self.assertIn(b'Trainer Video & Lecture Upload Hub', res_hub.data)

        # Upload video lecture resource
        res_upload = self.client.post('/trainer/upload', data={
            'title': 'Mastering Kubernetes Cluster Networking',
            'description': 'Full deep dive into CNI, Services, and Ingress controllers.',
            'resource_type': 'video',
            'category': 'Technology',
            'external_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'duration': '45 mins'
        }, follow_redirects=True)
        self.assertEqual(res_upload.status_code, 200)
        self.assertIn(b'Successfully uploaded "Mastering Kubernetes Cluster Networking"', res_upload.data)

        # Verify resource in DB
        res_obj = Resource.query.filter_by(title='Mastering Kubernetes Cluster Networking').first()
        self.assertIsNotNone(res_obj)

        # Delete the resource
        res_del = self.client.post(f'/trainer/delete-resource/{res_obj.id}', follow_redirects=True)
        self.assertEqual(res_del.status_code, 200)
        self.assertIn(b'was removed', res_del.data)

        # Verify deletion in DB
        deleted_res = db.session.get(Resource, res_obj.id)
        self.assertIsNone(deleted_res)

    def test_14_profile_management(self):
        self.client.get('/auth/quick-login/trainee', follow_redirects=True)

        # View profile
        res_view = self.client.get('/profile')
        self.assertEqual(res_view.status_code, 200)
        self.assertIn(b'Alex Rivera', res_view.data)

        # Update basic profile info
        res_basic = self.client.post('/profile', data={
            'action': 'update_basic',
            'name': 'Alex Rivera',
            'job_title': 'Senior Solutions Architect',
            'organization': 'Apex Technologies',
            'bio': 'Passionate about distributed cloud systems.',
            'department': 'Cloud Engineering',
            'location': 'New York, USA'
        }, follow_redirects=True)
        self.assertEqual(res_basic.status_code, 200)
        self.assertIn(b'Profile information updated successfully', res_basic.data)

        # Update skills
        res_skills = self.client.post('/profile', data={
            'action': 'update_skills',
            'skills': 'Kubernetes, Terraform, Python, AWS, Docker',
            'interests': 'Quantum Computing, AI Engineering'
        }, follow_redirects=True)
        self.assertEqual(res_skills.status_code, 200)
        self.assertIn(b'Skills &amp; professional interests updated', res_skills.data)

        # Verify profile updated
        alex = User.query.filter_by(email='trainee.alex@capacityconnect.org').first()
        self.assertEqual(alex.job_title, 'Senior Solutions Architect')
        self.assertIn('Kubernetes', alex.profile.skills)

    def test_15_admin_announcements_creation(self):
        self.client.get('/auth/quick-login/admin', follow_redirects=True)

        res_view = self.client.get('/admin/announcements')
        self.assertEqual(res_view.status_code, 200)

        # Create new announcement
        res_create = self.client.post('/admin/announcements', data={
            'action': 'create',
            'title': 'Q4 Enterprise Hackathon & Learning Summit',
            'tag': 'Announcement',
            'content': 'All registered trainees are invited to participate in the upcoming digital hackathon.',
            'is_pinned': '1'
        }, follow_redirects=True)
        self.assertEqual(res_create.status_code, 200)
        self.assertIn(b'Announcement published to homepage feed!', res_create.data)

        # Check it appears on dashboard
        res_dash = self.client.get('/dashboard')
        self.assertIn(b'Q4 Enterprise Hackathon &amp; Learning Summit', res_dash.data)

    def test_16_competency_mapping_search_and_matching(self):
        self.client.get('/auth/quick-login/admin', follow_redirects=True)

        # View competency matrix
        res_matrix = self.client.get('/competency-mapping')
        self.assertEqual(res_matrix.status_code, 200)
        self.assertIn(b'Competency Mapping & Trainer Identification', res_matrix.data)

        # Search subject "Cloud"
        res_search = self.client.get('/competency-mapping?subject=Cloud')
        self.assertEqual(res_search.status_code, 200)
        self.assertIn(b'Dr. Sarah Jenkins', res_search.data)
        self.assertIn(b'AWS Cloud Solutions Architecture', res_search.data)

if __name__ == '__main__':
    unittest.main()
