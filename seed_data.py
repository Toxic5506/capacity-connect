import json
from datetime import datetime, timedelta, timezone
from app import create_app
from models import db, User, Profile, Course, Enrollment, Assessment, Question, Submission, Certificate, Resource, Announcement, Feedback, Competency

app = create_app()

def seed_database():
    with app.app_context():
        # Recreate tables cleanly
        db.drop_all()
        db.create_all()

        now = datetime.now(timezone.utc)

        # 1. Users
        # Mayank (Admin / Lead User)
        mayank = User(
            name="Mayank",
            email="mayank@capacityconnect.org",
            role="admin",
            status="approved",
            job_title="Lead Systems Architect & Capacity Director"
        )
        mayank.set_password("password123")
        db.session.add(mayank)
        db.session.flush()

        mayank_profile = Profile(
            user_id=mayank.id,
            bio="Lead Systems Architect with over 8 years of experience designing scalable digital learning ecosystems, cloud backends, and organizational competency frameworks.",
            organization="Capacity Connect Headquarters",
            department="Digital Transformation & Learning",
            phone="+91 98765 43210",
            location="New Delhi, India"
        )
        mayank_profile.qualifications = [
            {"degree": "Master of Technology (M.Tech)", "institution": "Indian Institute of Technology (IIT)", "year": "2021", "field": "Computer Science & Systems Engineering"},
            {"degree": "Bachelor of Technology (B.Tech)", "institution": "National Institute of Technology (NIT)", "year": "2019", "field": "Information Technology & Software Systems"}
        ]
        mayank_profile.experience = [
            {"role": "Lead Systems Architect & Capacity Director", "company": "Capacity Connect Network", "duration": "2023 - Present", "description": "Spearheading national digital competency infrastructure, learning management portals, and automated evaluation engines."},
            {"role": "Senior Cloud Solutions Architect", "company": "Enterprise Cloud Global", "duration": "2020 - 2023", "description": "Engineered distributed microservices, automated CI/CD deployments, and facilitated over 50 enterprise technical capacity cohorts."}
        ]
        mayank_profile.skills = ["Cloud Architecture", "AWS Solutions", "Python & Flask", "Organizational Learning", "Competency Mapping", "Cybersecurity Governance", "Agile Management"]
        mayank_profile.interests = ["AI-driven Learning", "Competency Frameworks", "High-Performance Systems", "Mentorship & Coaching"]
        db.session.add(mayank_profile)

        # Sarah Jenkins (Trainer)
        sarah = User(
            name="Dr. Sarah Jenkins",
            email="trainer.sarah@capacityconnect.org",
            role="trainer",
            status="approved",
            job_title="Senior Agile Coach & Management Consultant"
        )
        sarah.set_password("password123")
        db.session.add(sarah)
        db.session.flush()

        sarah_profile = Profile(
            user_id=sarah.id,
            bio="Doctorate in Organizational Behavior with 12+ years consulting for Fortune 500 enterprises on agile project leadership and team performance.",
            organization="Global Agile Institute",
            department="Executive Training",
            phone="+1 555 234 5678",
            location="Boston, MA"
        )
        sarah_profile.qualifications = [
            {"degree": "Ph.D. in Organizational Leadership", "institution": "Harvard University", "year": "2014", "field": "Management Science"},
            {"degree": "M.B.A.", "institution": "Columbia Business School", "year": "2010", "field": "Strategic Management"}
        ]
        sarah_profile.experience = [
            {"role": "Principal Management Fellow", "company": "Agile Leadership Partners", "duration": "2016 - Present", "description": "Trained over 4,000 project leaders across 18 countries on modern delivery models."},
        ]
        sarah_profile.skills = ["Project Management", "Agile Methodologies", "Scrum Master", "Leadership Coaching", "Stakeholder Communication"]
        sarah_profile.interests = ["Cross-Functional Collaboration", "Continuous Improvement", "Modern Pedagogy"]
        db.session.add(sarah_profile)

        # Rajesh Kumar (Trainer)
        rajesh = User(
            name="Prof. Rajesh Kumar",
            email="trainer.rajesh@capacityconnect.org",
            role="trainer",
            status="approved",
            job_title="Principal Data Scientist & Cloud Architect"
        )
        rajesh.set_password("password123")
        db.session.add(rajesh)
        db.session.flush()

        rajesh_profile = Profile(
            user_id=rajesh.id,
            bio="Cloud specialist and AI researcher with 10+ years hands-on experience in AWS infrastructure, distributed data analytics, and machine learning pipelines.",
            organization="TechNova Labs",
            department="Cloud & AI R&D",
            phone="+91 99887 76655",
            location="Bengaluru, India"
        )
        rajesh_profile.qualifications = [
            {"degree": "M.S. in Computer Science", "institution": "Georgia Institute of Technology", "year": "2015", "field": "Distributed Computing"}
        ]
        rajesh_profile.skills = ["Cloud Computing", "AWS", "Python", "Data Science", "Machine Learning", "System Design"]
        rajesh_profile.interests = ["Serverless Systems", "Big Data", "Edge Computing"]
        db.session.add(rajesh_profile)

        # Trainee Alex Rivera
        alex = User(
            name="Alex Rivera",
            email="trainee.alex@capacityconnect.org",
            role="trainee",
            status="approved",
            job_title="Data Analyst Associate"
        )
        alex.set_password("password123")
        db.session.add(alex)
        db.session.flush()

        alex_profile = Profile(
            user_id=alex.id,
            bio="Aspiring data engineer passionate about business intelligence and cloud data pipelines.",
            organization="Apex Logistics",
            department="Data Analytics"
        )
        alex_profile.skills = ["Python", "SQL", "Tableau", "Data Analysis"]
        db.session.add(alex_profile)

        # Trainee Priya Sharma
        priya = User(
            name="Priya Sharma",
            email="trainee.priya@capacityconnect.org",
            role="trainee",
            status="pending",  # Test pending approval workflow
            job_title="Operations Coordinator"
        )
        priya.set_password("password123")
        db.session.add(priya)

        db.session.commit()

        # 2. Courses (Exact 6 matching screenshot)
        c1 = Course(
            code="PRJ-101",
            title="Foundations of Project Management",
            description="Learn the core principles of project management including planning, scheduling, risk management, and stakeholder engagement to lead high-performing delivery teams.",
            category="Management",
            level="Beginner",
            duration="4 Weeks",
            is_featured=True,
            trainer_id=sarah.id,
            syllabus="Module 1: Project Lifecycle & Governance\nModule 2: Scoping & Work Breakdown Structures (WBS)\nModule 3: Agile vs Waterfall Frameworks\nModule 4: Risk Mitigation & Stakeholder Buy-in",
            thumbnail_url="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=600&q=80"
        )
        c2 = Course(
            code="DAT-201",
            title="Data Analytics with Python",
            description="Master data analysis techniques using Python, Pandas, and NumPy. Covers data cleaning, visualization, statistical inference, and real-world corporate case studies.",
            category="Technology",
            level="Intermediate",
            duration="6 Weeks",
            is_featured=True,
            trainer_id=rajesh.id,
            syllabus="Module 1: Python Fundamentals & Data Structures\nModule 2: Pandas DataFrame Wrangling\nModule 3: Data Visualization with Matplotlib & Seaborn\nModule 4: Exploratory Data Analysis & Case Studies",
            thumbnail_url="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=600&q=80"
        )
        c3 = Course(
            code="CLD-301",
            title="Cloud Computing & AWS Fundamentals",
            description="A new advanced-level course on AWS cloud services is now available. Enroll now to get hands-on experience with EC2, S3, RDS, IAM, VPC, and Lambda.",
            category="Technology",
            level="Intermediate",
            duration="5 Weeks",
            is_featured=True,
            trainer_id=rajesh.id,
            syllabus="Module 1: Cloud Architecture Fundamentals\nModule 2: Compute & Storage (EC2, S3, EBS)\nModule 3: Databases & Networking (RDS, DynamoDB, VPC)\nModule 4: Serverless Computing & Security (Lambda, IAM)",
            thumbnail_url="https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=600&q=80"
        )
        c4 = Course(
            code="LDR-102",
            title="Effective Leadership & Team Dynamics",
            description="Develop essential leadership skills, emotional intelligence, constructive feedback mechanisms, conflict resolution, and drive organizational transformation.",
            category="Management",
            level="Beginner",
            duration="3 Weeks",
            is_featured=True,
            trainer_id=sarah.id,
            syllabus="Module 1: Emotional Intelligence in the Workplace\nModule 2: Psychological Safety & Trust\nModule 3: Conflict De-escalation & Difficult Conversations\nModule 4: Empowering High-Autonomy Teams",
            thumbnail_url="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=600&q=80"
        )
        c5 = Course(
            code="SEC-202",
            title="Cybersecurity Essentials & Risk Governance",
            description="Understand modern cyber threat vectors, incident response protocols, zero-trust architectures, and organizational security policies.",
            category="Technology",
            level="Intermediate",
            duration="4 Weeks",
            is_featured=False,
            trainer_id=rajesh.id,
            syllabus="Module 1: Cyber Threat Landscape\nModule 2: Identity, Access & Encryption\nModule 3: Incident Response & Business Continuity\nModule 4: Security Compliance & Audit",
            thumbnail_url="https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=600&q=80"
        )
        c6 = Course(
            code="AI-401",
            title="AI & Generative Intelligence for Business",
            description="Learn how to harness generative AI, prompt engineering, and LLM automation to supercharge productivity and decision intelligence across departments.",
            category="Technology",
            level="Advanced",
            duration="4 Weeks",
            is_featured=False,
            trainer_id=rajesh.id,
            syllabus="Module 1: Generative AI Foundations\nModule 2: Prompt Engineering & Automation\nModule 3: Enterprise AI Integration & Ethics\nModule 4: Future Trends & Strategy",
            thumbnail_url="https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=600&q=80"
        )

        db.session.add_all([c1, c2, c3, c4, c5, c6])
        db.session.commit()

        # 3. Enrollments (Mayank enrolled in Course 1, so Screenshot stat "1 My Enrollments" matches!)
        e1 = Enrollment(
            user_id=mayank.id,
            course_id=c1.id,
            enrolled_at=now - timedelta(days=12),
            progress=65,
            status="in_progress"
        )
        e2 = Enrollment(
            user_id=alex.id,
            course_id=c2.id,
            enrolled_at=now - timedelta(days=5),
            progress=40,
            status="in_progress"
        )
        e3 = Enrollment(
            user_id=alex.id,
            course_id=c3.id,
            enrolled_at=now - timedelta(days=2),
            progress=15,
            status="in_progress"
        )
        db.session.add_all([e1, e2, e3])

        # 4. Announcements (Matching Screenshot 1 exactly)
        a1 = Announcement(
            title="Welcome to Capacity Connect!",
            content="We are excited to launch our new digital capacity building platform. Explore courses, build your professional profile, and start your learning journey today.",
            tag="Announcement",
            author_name="Admin Team",
            author_id=mayank.id,
            is_pinned=True,
            created_at=now - timedelta(days=6)
        )
        a2 = Announcement(
            title="New Course: Cloud Computing & AWS Fundamentals",
            content="A new advanced-level course on AWS cloud services is now available. Enroll now to get hands-on experience with EC2, S3, RDS, and Lambda.",
            tag="New Content",
            author_name="Admin Team",
            author_id=mayank.id,
            is_pinned=True,
            created_at=now - timedelta(days=4)
        )
        a3 = Announcement(
            title="Q3 Training Schedule Released",
            content="The training schedule for Q3 2026 has been published. Check the course catalog for upcoming sessions, live workshops, and expert office hours.",
            tag="Notification",
            author_name="Admin Team",
            author_id=mayank.id,
            created_at=now - timedelta(days=2)
        )
        a4 = Announcement(
            title="Annual Capacity Excellence Awards Announced",
            content="Congratulations to all department teams who completed over 90% of their learning modules this quarter! Digital badges and certificates have been awarded.",
            tag="Achievement",
            author_name="Admin Team",
            author_id=mayank.id,
            created_at=now - timedelta(hours=14)
        )
        db.session.add_all([a1, a2, a3, a4])

        # 5. Assessments & Subject-wise MCQs
        asm1 = Assessment(
            title="Project Management Foundations Assessment",
            subject="Project Management",
            description="Comprehensive MCQ assessment evaluating competency in scoping, scheduling, risk matrix analysis, and stakeholder engagement.",
            course_id=c1.id,
            trainer_id=sarah.id,
            time_limit_minutes=15,
            passing_score=70,
            deadline=now + timedelta(days=30),
            is_active=True
        )
        db.session.add(asm1)
        db.session.flush()

        questions_asm1 = [
            Question(
                assessment_id=asm1.id,
                question_text="Which document formally authorizes the existence of a project and gives the project manager authority to apply organizational resources?",
                option_a="Project Charter",
                option_b="Scope Statement",
                option_c="Work Breakdown Structure (WBS)",
                option_d="Stakeholder Register",
                correct_option="A",
                explanation="The Project Charter formally authorizes the project and confers organizational authority upon the project manager."
            ),
            Question(
                assessment_id=asm1.id,
                question_text="In Agile Scrum methodology, what is the recommended maximum duration for a daily stand-up meeting?",
                option_a="30 minutes",
                option_b="15 minutes",
                option_c="45 minutes",
                option_d="1 hour",
                correct_option="B",
                explanation="Daily Scrum meetings are time-boxed to a maximum of 15 minutes to keep teams aligned without unnecessary overhead."
            ),
            Question(
                assessment_id=asm1.id,
                question_text="What does the 'Critical Path' represent in a project schedule network diagram?",
                option_a="The path with the highest financial budget",
                option_b="The longest sequence of dependent activities representing the shortest possible project duration",
                option_c="The sequence containing all high-risk technical milestones",
                option_d="The path where all team members have maximum availability",
                correct_option="B",
                explanation="The Critical Path is the sequence of stages determining the minimum time needed for an operation to complete. Any delay on this path delays the whole project."
            ),
            Question(
                assessment_id=asm1.id,
                question_text="When performing Quantitative Risk Analysis, what does an 'Expected Monetary Value' (EMV) calculation do?",
                option_a="Estimates total company valuation",
                option_b="Calculates the probability of an event multiplied by its financial impact",
                option_c="Measures return on capital investment over 5 years",
                option_d="Determines the exact contract price for third-party vendors",
                correct_option="B",
                explanation="EMV calculates the statistical average of future uncertain outcomes by multiplying probability (P) by impact (I)."
            ),
            Question(
                assessment_id=asm1.id,
                question_text="Which of the following describes the 'Cone of Uncertainty' in project management?",
                option_a="Project estimates become more accurate as more information is gathered over time",
                option_b="Risk increases exponentially as the project approaches delivery",
                option_c="Stakeholder satisfaction decreases as deliverables expand",
                option_d="Team velocity decreases during complex technical sprints",
                correct_option="A",
                explanation="The Cone of Uncertainty illustrates that at the beginning of a project, variance in estimates is high, but narrows as knowledge increases."
            )
        ]
        db.session.add_all(questions_asm1)

        # Assessment 2: Cloud Computing Assessment
        asm2 = Assessment(
            title="Cloud Architecture & AWS Competency Test",
            subject="Cloud Computing",
            description="Assess your knowledge of core AWS architectural pillars, high availability, storage classes, and identity management.",
            course_id=c3.id,
            trainer_id=rajesh.id,
            time_limit_minutes=20,
            passing_score=75,
            deadline=now + timedelta(days=45),
            is_active=True
        )
        db.session.add(asm2)
        db.session.flush()

        questions_asm2 = [
            Question(
                assessment_id=asm2.id,
                question_text="Which AWS service provides resizable compute capacity in the cloud as virtual servers?",
                option_a="Amazon S3",
                option_b="Amazon EC2",
                option_c="AWS Lambda",
                option_d="Amazon RDS",
                correct_option="B",
                explanation="Amazon Elastic Compute Cloud (EC2) provides scalable computing capacity in the AWS Cloud."
            ),
            Question(
                assessment_id=asm2.id,
                question_text="What is the primary benefit of deploying resources across multiple Availability Zones (AZs)?",
                option_a="Decreased billing cost",
                option_b="High availability and fault tolerance against data center failures",
                option_c="Higher GPU core clock speed",
                option_d="Exemption from AWS IAM policies",
                correct_option="B",
                explanation="Multi-AZ deployments ensure continuous uptime and automatic failover in the event of an outage in a single facility."
            ),
            Question(
                assessment_id=asm2.id,
                question_text="Which Amazon S3 storage tier is most cost-effective for long-term archival data accessed once or twice a year?",
                option_a="S3 Standard",
                option_b="S3 Intelligent-Tiering",
                option_c="S3 Glacier Flexible Retrieval / Deep Archive",
                option_d="S3 One Zone-IA",
                correct_option="C",
                explanation="S3 Glacier Deep Archive is Amazon S3's lowest-cost storage tier for long-term retention."
            ),
            Question(
                assessment_id=asm2.id,
                question_text="In the AWS Shared Responsibility Model, which of the following is the customer's responsibility?",
                option_a="Physical security of data centers",
                option_b="Hypervisor patching and maintenance",
                option_c="Customer data encryption, IAM user credentials, and OS security updates on EC2",
                option_d="Disposal of decommissioned storage hardware drives",
                correct_option="C",
                explanation="Security 'IN' the cloud (data, OS, configurations, access management) is the customer's responsibility."
            )
        ]
        db.session.add_all(questions_asm2)

        # 6. Certificates
        cert1 = Certificate(
            user_id=mayank.id,
            course_id=c1.id,
            assessment_id=asm1.id,
            cert_code="CC-2026-PM8829",
            title="Certified Practitioner in Modern Project Management",
            recipient_name="Mayank",
            issuer="Capacity Connect Global Certification Board",
            score=95.0,
            issue_date=now - timedelta(days=8)
        )
        db.session.add(cert1)

        # 7. Trainer Library Resources
        res1 = Resource(
            title="AWS Cloud Architecture Masterclass: Multi-Tier Design",
            description="Complete recorded lecture covering VPC segmentation, auto-scaling groups, Elastic Load Balancers, and secure bastion hosts.",
            resource_type="video",
            file_or_url="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
            category="Technology",
            course_id=c3.id,
            trainer_id=rajesh.id,
            file_size="420 MB",
            duration="52 mins"
        )
        res2 = Resource(
            title="Agile Sprint Planning & Velocity Estimation Guide",
            description="Executive slide presentation detailing Story Points, Planning Poker, Scrum artifacts, and burn-down analytics.",
            resource_type="presentation",
            file_or_url="/static/uploads/agile_planning_slides.pdf",
            category="Management",
            course_id=c1.id,
            trainer_id=sarah.id,
            file_size="6.8 MB",
            duration="38 slides"
        )
        res3 = Resource(
            title="Python for Data Science Cheat Sheet & Reference Notebook",
            description="Comprehensive PDF cheat sheet covering Pandas indexing, NumPy vectorization, grouping, and clean code principles.",
            resource_type="document",
            file_or_url="/static/uploads/python_data_cheatsheet.pdf",
            category="Technology",
            course_id=c2.id,
            trainer_id=rajesh.id,
            file_size="3.2 MB",
            duration="16 pages"
        )
        res4 = Resource(
            title="Organizational Emotional Intelligence & Constructive Feedback",
            description="Recorded video seminar on handling high-stakes stakeholder discussions, de-escalation, and non-violent communication.",
            resource_type="video",
            file_or_url="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
            category="Management",
            course_id=c4.id,
            trainer_id=sarah.id,
            file_size="310 MB",
            duration="45 mins"
        )
        res5 = Resource(
            title="Cybersecurity Incident Response Playbook & Runbook Template",
            description="Standard Operating Procedure (SOP) document for triage, threat containment, root cause analysis, and audit documentation.",
            resource_type="document",
            file_or_url="/static/uploads/cybersecurity_sop_playbook.pdf",
            category="Technology",
            course_id=c5.id,
            trainer_id=rajesh.id,
            file_size="4.5 MB",
            duration="28 pages"
        )
        db.session.add_all([res1, res2, res3, res4, res5])

        # 8. Feedback
        fb1 = Feedback(
            course_id=c1.id,
            user_id=mayank.id,
            rating=5,
            comments="Outstanding course! The real-world frameworks and risk matrix exercises immediately helped streamline our quarterly delivery pipelines."
        )
        fb2 = Feedback(
            course_id=c2.id,
            user_id=alex.id,
            rating=5,
            comments="Prof. Rajesh explains complex Pandas workflows with such clarity. The hands-on labs were extremely practical."
        )
        db.session.add_all([fb1, fb2])

        # 9. Competencies for Competency Mapping
        comp1 = Competency(name="Agile Project Management", category="Management", trainer_id=sarah.id, proficiency_level="Expert", years_experience=12)
        comp2 = Competency(name="Executive Leadership Coaching", category="Management", trainer_id=sarah.id, proficiency_level="Expert", years_experience=10)
        comp3 = Competency(name="AWS Cloud Solutions Architecture", category="Technology", trainer_id=rajesh.id, proficiency_level="Expert", years_experience=9)
        comp4 = Competency(name="Python & Machine Learning", category="Technology", trainer_id=rajesh.id, proficiency_level="Expert", years_experience=8)
        comp5 = Competency(name="Cybersecurity & Zero Trust Architecture", category="Technology", trainer_id=rajesh.id, proficiency_level="Advanced", years_experience=6)
        comp6 = Competency(name="DevOps & Automated CI/CD Pipelines", category="Technology", trainer_id=mayank.id, proficiency_level="Expert", years_experience=7)
        comp7 = Competency(name="Data Governance & Ethics", category="Data Science", trainer_id=sarah.id, proficiency_level="Advanced", years_experience=5)

        db.session.add_all([comp1, comp2, comp3, comp4, comp5, comp6, comp7])

        db.session.commit()
        print(">>> Database seeded successfully with demo users, courses, assessments, announcements, and resources!")

if __name__ == "__main__":
    seed_database()
