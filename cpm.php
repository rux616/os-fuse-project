<?php
    $handle = fopen("timestamps.txt", "r") or die ("Could not open timestamps file");
    $buffer = "";
    const NUM_STAMPS = 60;
    const BYTES_PER_STAMP = 15;
     
    $fpointer;
     
    if ($handle)
    {
        #Set file pointer to read last 60 timestamps in file
        $fpointer = fseek($handle, -(NUM_STAMPS * BYTES_PER_STAMP), $whence = SEEK_END);
        fgets($handle); #toss out first timestamp
     
        for($i = 0; $i < NUM_STAMPS; ++$i)
        {
            $buffer .= fgets($handle, 32);
        }
     
        fclose($handle);

        #Debugging
        #print_r($buffer);

        return $buffer; #return the string of timestamps
    }
?>