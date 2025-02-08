<?php

// What is a variable

// Variable types
/*
    String
    Integer
    Float
    Boolean
    Null
    Array
    Object
    Resource
*/

// 1. Declare variables
$name = "Zura";
$age = 28;
$isMale = true; // 3. Change into false
$height = 1.85;
$salary = null;

// 2. Print the variables. Explain what is concatenation
echo $name . '<br>';
echo $age . '<br>';
echo $isMale . '<br>';
echo $height . '<br>';
echo $salary . '<br>';

// 4. Print types of the variables
echo gettype($name) . '<br>';
echo gettype($age) . '<br>';
echo gettype($isMale) . '<br>';
echo gettype($height) . '<br>';
echo gettype($salary) . '<br>';

// 5. Print the whole variable
var_dump($name, $age, $isMale, $height, $salary);

// 6. Change the value of the variable
$name = false;

// 7. Print type of the variable
echo gettype($name) . '<br>';

// 8. Variable checking functions
is_string($name); // false
is_int($age); // true
is_bool($isMale); // true
is_double($height); // true

// 9. Check if variable is defined
var_dump(isset($name));
var_dump(isset($name2));
echo '<br>';

// 10. Constants
define('PI', 3.14);
echo PI.'<br>';
var_dump(defined('PI')); // defined(PI2)
echo '<br>';

// 12. Using PHP built-in constants
echo SORT_ASC.'<br>';
echo PHP_INT_MAX.'<br>';
