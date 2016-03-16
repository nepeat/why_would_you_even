<?php
// "Safe" Brainfuck wrapper.
// Safe according to the average PHP standards.

require __DIR__ . "/vendor/autoload.php";
set_time_limit(15);

$script = implode(array_slice($argv, 1));

igorw\brainfuck\execute($script);
?>