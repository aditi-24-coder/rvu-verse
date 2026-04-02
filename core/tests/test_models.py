# tests/test_models.py
from django.test import TestCase
from core.models import Department

class DepartmentModelTest(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(
            code='5',
            name='School of Computer Science and Engineering (SOCSE)',
            description='Computer Science Department'
        )

    def test_department_str(self):
        self.assertEqual(str(self.dept), 'School of Computer Science and Engineering (SOCSE)')

    def test_department_code_choice(self):
        self.assertIn((self.dept.code, self.dept.name), Department.DEPT_CHOICES)
