from robocorp import windows
from robocorp.windows import WindowElement, ElementNotFound
from enum import Enum
from RPA.Desktop import Desktop


class Operator(Enum):
    PLUS = "Plus"
    MINUS = "Minus"
    MULTIPLY = "Multiply by"
    DIVIDE = "Divide by"


class WindowsCalculator:
    """A class for automating the Windows Calculator application."""
    # Locators
    CALCULATOR_WINDOW = 'regex:.*Calculator'
    BUTTON_TEMPLATE = 'automationid:"num{}Button"'
    PLUS_BUTTON = 'automationid:"plusButton"'
    EQUAL_BUTTON = 'automationid:"equalButton"'
    RESULT_OUTPUT = 'automationid:"NormalOutput"'
    CLEAR_BUTTON = 'automationid:"clearButton"'

    def __init__(self):
        self.calculator = self.open_calculator()

    def open_calculator(self) -> WindowElement:
        """Opens the Windows Calculator application and returns the window element."""
        windows.desktop().windows_run("calc.exe")
        self.window = windows.find_window(self.CALCULATOR_WINDOW)
        if not self.window:
            raise Exception("Calculator window not found.")
        return self.window

    def add_two_integers(self, a: int, b: int):
        """Adds two integers using the calculator."""
        self.click_number(a)
        self.click_plus_button()
        self.click_number(b)
        self.click_equal_button()

    def click_number(self, number: int):
        """Clicks the number button on the calculator."""
        self.calculator.click(self.BUTTON_TEMPLATE.format(number))

    def click_plus_button(self):
        """Clicks the plus (+) button on the calculator."""
        self.calculator.click(self.PLUS_BUTTON)

    def click_equal_button(self):
        """Clicks the equal (=) button on the calculator."""
        self.calculator.click(self.EQUAL_BUTTON)

    def check_result_is(self, expected_result: int):
        """Verifies the result displayed on the calculator."""
        expected_result = str(expected_result)
        result = self.calculator.find(self.RESULT_OUTPUT).name
        if result != expected_result:
            self.window.log_screenshot(level="ERROR")
            raise AssertionError(
                f"Expected result: {expected_result}, but got: {result}")

    def result_is(self):
        """Returns the result displayed on the calculator."""
        return int(self.calculator.find(self.RESULT_OUTPUT).name)
    
    def get_result(self):
        """Returns the result displayed on the calculator."""
        return self.calculator.find(self.RESULT_OUTPUT).name

    def clear_calculator(self):
        """Clears the calculator."""
        self.calculator.click(self.CLEAR_BUTTON)

    def close_calculator(self):
        """Closes the calculator application."""
        self.calculator.close_window(
            use_close_button=True, close_button_locator='automationid:"Close"')

    def click_operator(self, operator: Operator):
        """Clicks the operator button on the calculator."""
        name = operator.value
        self.calculator.click(f'name:"{name}"')

    def click_by_image(self, image_alias: str):
        """Clicks the button by image. The image details are stored in locators.json file."""
        desktop = Desktop()
        desktop.click(f'alias:{image_alias}')

    def history_is_empty(self):
        """Verifies that the history is empty."""
        try:
            self.calculator.find(
                'control:"TextControl" and name:"There’s no history yet."')
            return True
        except ElementNotFound:
            self.window.log_screenshot(level="ERROR")
            return False
        
    def history_contains(self, result: str):
        """Verifies that the history contains the calculation.

        Args:
            calculation: The calculation or number to search for in the history, e.g.,
            if you calculate '9 × 6= 54', you expect that '54' appears in the history.
            """
        try:
            self.calculator.find(
                f'control:"TextControl" and name:"{result}"',
            )
            return True
        except ElementNotFound:
            return False
        