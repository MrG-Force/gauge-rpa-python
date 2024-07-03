# Calculator basic operations

The Windows Calculator must be able to perform basic operations such as addition, subtraction, multiplication, and division.

   |Operand 1|Operator   |Operand 2|Expected result|
   |---------|-----------|---------|---------------|
   |1        |Plus       |2        |3              |
   |20       |Multiply by|3        |60             |
   |612      |Divide by  |6        |102            |
   |32       |Minus      |12       |20             |

* Open Windows Calculator

Here are two versions of the same test:

## Basic operations with integers
* Enter the number <Operand 1>
* Click on the <Operator> button
* Enter the number <Operand 2>
* Click on the '=' button
* The result should be <Expected result>

## Basic operations with integers using concept
* Calculate <Operand 1> <Operator> <Operand 2>
* The result should be <Expected result>

## Division by zero
* Calculate "3" "Divide by" "0"
* The result should be "Cannot divide by zero"

## Show and clear the history (using image locators)
* Calculate "690" "Divide by" "5"
* The result should be "138"
* Clear results
* Click on the history button
* The history should contain "138"
* Click on the clear history button
* The history should be empty

_____________________________
Teardown steps:

* Close the calculator
