from getgauge.python import step, after_scenario, data_store

from automation.win_calculator import WindowsCalculator, Operator


# --------------------------
# Gauge step implementations
# --------------------------

@step("Open Windows Calculator")
def open_windows_calculator():
    data_store.scenario["calculator"] = WindowsCalculator()


@step("Enter the number <number>")
def enter_the_number(operand):
    calculator = data_store.scenario["calculator"]
    digits = [int(d) for d in operand]
    for digit in digits:
        calculator.click_number(digit)


@step("Click on the <operator> button")
def click_on_the_button(operator):
    calculator = data_store.scenario["calculator"]
    calculator.click_operator(Operator(operator))


@step("Click on the '=' button")
def click_on_the_equals_button():
    calculator = data_store.scenario["calculator"]
    calculator.click_equal_button()


@step("The result should be <Expected result>")
def verify_that_the_result_is(expected_result):
    calculator = data_store.scenario["calculator"]
    result = calculator.get_result()
    assert result == expected_result, f"Expected result: {expected_result}, but got: {result}"


@step("Clear results")
def clear_results():
    calculator = data_store.scenario["calculator"]
    calculator.clear_calculator()


@step("Click on the history button")
def click_on_the_history_button():
    calculator = data_store.scenario["calculator"]
    calculator.click_by_image("history_button")


@step("Click on the clear history button")
def click_on_the_clear_history_button():
    calculator = data_store.scenario["calculator"]
    calculator.click_by_image("clear_history_button")


@step("The history should be empty")
def the_history_should_be_empty():
    calculator = data_store.scenario["calculator"]
    assert calculator.history_is_empty()

@step("The history should contain <calculation>")
def the_history_should_contain(result):
    calculator:WindowsCalculator = data_store.scenario["calculator"]
    assert calculator.history_contains(result)

@step("Close the calculator")
def close_the_calculator():
    calculator = data_store.scenario["calculator"]
    calculator.close_calculator()
    data_store.scenario.pop("calculator")
