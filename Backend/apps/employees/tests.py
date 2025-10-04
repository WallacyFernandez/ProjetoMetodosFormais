"""
Testes do app de funcionários.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date

from apps.employees.models import EmployeePosition, Employee, Payroll, PayrollHistory
from apps.finance.models import UserBalance

User = get_user_model()


class EmployeePositionModelTest(TestCase):
    """Testes para o modelo EmployeePosition."""

    def setUp(self):
        self.position = EmployeePosition.objects.create(
            name='Caixa',
            description='Responsável pelo caixa',
            base_salary=Decimal('1500.00'),
            min_salary=Decimal('1200.00'),
            max_salary=Decimal('2000.00'),
            department='CAIXA'
        )

    def test_position_creation(self):
        """Testa criação de cargo."""
        self.assertEqual(self.position.name, 'Caixa')
        self.assertEqual(self.position.department, 'CAIXA')
        self.assertTrue(self.position.is_active)

    def test_position_str(self):
        """Testa representação string do cargo."""
        expected = 'Caixa - Caixa'
        self.assertEqual(str(self.position), expected)

    def test_get_default_positions(self):
        """Testa método de cargos padrão."""
        positions = EmployeePosition.get_default_positions()
        self.assertIsInstance(positions, list)
        self.assertGreater(len(positions), 0)
        
        # Verificar se tem campos obrigatórios
        for position in positions:
            self.assertIn('name', position)
            self.assertIn('base_salary', position)
            self.assertIn('department', position)


class EmployeeModelTest(TestCase):
    """Testes para o modelo Employee."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='João',
            last_name='Silva'
        )
        
        self.position = EmployeePosition.objects.create(
            name='Vendedor',
            base_salary=Decimal('1400.00'),
            min_salary=Decimal('1100.00'),
            max_salary=Decimal('1800.00'),
            department='VENDAS'
        )
        
        self.employee = Employee.objects.create(
            user=self.user,
            name='Maria Santos',
            cpf='12345678901',
            email='maria@example.com',
            position=self.position,
            salary=Decimal('1500.00')
        )

    def test_employee_creation(self):
        """Testa criação de funcionário."""
        self.assertEqual(self.employee.name, 'Maria Santos')
        self.assertEqual(self.employee.cpf, '12345678901')
        self.assertEqual(self.employee.employment_status, 'ACTIVE')
        self.assertTrue(self.employee.is_active)

    def test_employee_str(self):
        """Testa representação string do funcionário."""
        expected = 'Maria Santos - Vendedor'
        self.assertEqual(str(self.employee), expected)

    def test_employee_terminate(self):
        """Testa demissão de funcionário."""
        self.employee.terminate()
        self.assertEqual(self.employee.employment_status, 'TERMINATED')
        self.assertIsNotNone(self.employee.termination_date)
        self.assertFalse(self.employee.is_active)

    def test_employee_reactivate(self):
        """Testa reativação de funcionário."""
        self.employee.terminate()
        self.employee.reactivate()
        self.assertEqual(self.employee.employment_status, 'ACTIVE')
        self.assertIsNone(self.employee.termination_date)
        self.assertTrue(self.employee.is_active)

    def test_salary_validation(self):
        """Testa validação de salário."""
        # Salário abaixo do mínimo
        with self.assertRaises(ValidationError):
            employee = Employee(
                user=self.user,
                name='Test',
                cpf='98765432100',
                position=self.position,
                salary=Decimal('1000.00')  # Abaixo do mínimo
            )
            employee.full_clean()

        # Salário acima do máximo
        with self.assertRaises(ValidationError):
            employee = Employee(
                user=self.user,
                name='Test',
                cpf='98765432100',
                position=self.position,
                salary=Decimal('2000.00')  # Acima do máximo
            )
            employee.full_clean()


class PayrollModelTest(TestCase):
    """Testes para o modelo Payroll."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='João',
            last_name='Silva'
        )
        
        self.position = EmployeePosition.objects.create(
            name='Caixa',
            base_salary=Decimal('1500.00'),
            min_salary=Decimal('1200.00'),
            max_salary=Decimal('2000.00'),
            department='CAIXA'
        )
        
        self.employee = Employee.objects.create(
            user=self.user,
            name='Maria Santos',
            cpf='12345678901',
            position=self.position,
            salary=Decimal('1500.00')
        )
        
        self.payroll = Payroll.objects.create(
            employee=self.employee,
            payment_month=date(2025, 1, 1),
            base_salary=Decimal('1500.00'),
            overtime_hours=Decimal('10.00'),
            overtime_value=Decimal('150.00'),
            bonus=Decimal('100.00'),
            deductions=Decimal('50.00')
        )

    def test_payroll_creation(self):
        """Testa criação de folha de pagamento."""
        self.assertEqual(self.payroll.employee, self.employee)
        self.assertEqual(self.payroll.payment_status, 'PENDING')
        self.assertEqual(self.payroll.total_amount, Decimal('1700.00'))  # 1500 + 150 + 100 - 50

    def test_payroll_calculate_total(self):
        """Testa cálculo do total da folha."""
        total = self.payroll.calculate_total()
        expected = Decimal('1700.00')  # 1500 + 150 + 100 - 50
        self.assertEqual(total, expected)

    def test_payroll_mark_as_paid(self):
        """Testa marcação como pago."""
        self.payroll.mark_as_paid()
        self.assertEqual(self.payroll.payment_status, 'PAID')
        self.assertEqual(self.payroll.payment_date, date.today())

    def test_payroll_str(self):
        """Testa representação string da folha."""
        expected = 'Maria Santos - 01/2025'
        self.assertEqual(str(self.payroll), expected)


class PayrollHistoryModelTest(TestCase):
    """Testes para o modelo PayrollHistory."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='João',
            last_name='Silva'
        )
        
        self.history = PayrollHistory.objects.create(
            user=self.user,
            payment_month=date(2025, 1, 1),
            total_employees=5,
            total_amount=Decimal('7500.00')
        )

    def test_history_creation(self):
        """Testa criação de histórico."""
        self.assertEqual(self.history.user, self.user)
        self.assertEqual(self.history.total_employees, 5)
        self.assertEqual(self.history.total_amount, Decimal('7500.00'))

    def test_history_str(self):
        """Testa representação string do histórico."""
        expected = 'Pagamentos 01/2025 - João Silva'
        self.assertEqual(str(self.history), expected)