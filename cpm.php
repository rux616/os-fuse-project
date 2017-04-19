<?php
$handle = fopen("timestamps.txt", "r") or die ("Could not open timestamps file");
$buffer = "";
const NUM_STAMPS = 60;
$fpointer;

if ($handle)
{
    $fpointer = fseek($handle, -900, $whence = SEEK_END);

    for($i = 0; $i < NUM_STAMPS; ++$i)
    {
        $buffer .= fgets($handle, 32);
    }

    fclose($handle);

    print_r($buffer);
    
    return $buffer;
}

?>