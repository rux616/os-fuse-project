<?php
$handle = fopen("timestamps.txt", "r") or die ("Could not open timestamps file");
$buffer = [];
$fpointer;

if ($handle)
{
    $fpointer = fseek($handle, -900, $whence = SEEK_END);

    for($i = 0; i < 60; ++i)
    {
        $buffer[$i] = fgets($handle, 32);
    }

    fclose($handle);
    
    return $buffer;
}

?>