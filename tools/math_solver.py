import sympy
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

class MathSolver:
    def __init__(self):
        self.transformations = (standard_transformations + (implicit_multiplication_application,))

    def validate_answer(self, student_answer: str, correct_answer: str) -> bool:
        """
        Compares student answer with correct answer using SymPy to handle algebraic equivalence.
        """
        try:
            # Clean up inputs
            s_ans = student_answer.strip().replace('^', '**')
            c_ans = correct_answer.strip().replace('^', '**')
            
            # Parse expressions
            expr1 = parse_expr(s_ans, transformations=self.transformations)
            expr2 = parse_expr(c_ans, transformations=self.transformations)
            
            # Check for equality
            # simplify(expr1 - expr2) == 0 checks if they are algebraically equivalent
            diff = sympy.simplify(expr1 - expr2)
            return diff == 0
        except Exception as e:
            print(f"Error validating math answer: {e}")
            # Fallback to string comparison if parsing fails
            return student_answer.strip() == correct_answer.strip()

    def solve(self, problem: str) -> str:
        """
        Solves a math problem (simplified version).
        Expects format like "Solve x + 2 = 5" or just an expression "2 + 2"
        """
        # This is a placeholder for a more complex solver if needed.
        # For now, we mainly use it for validation.
        return "Solver not fully implemented for generation, use Gemini."
