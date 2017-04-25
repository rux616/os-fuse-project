<?php
    $buffer = "";
    $numStamps = $_GET['numStamps'];

    $handle = fopen("timestamps.txt", "r")
        or die ("Error: could not open timestamps!\n");
    $write = fopen("fpointer.txt", "r")
        or die ("could not open fpointer");

    $fpointer = fgets($write);  #retrieve file pointer

    if ($handle and $write)
    {
        fseek($handle, $fpointer, SEEK_SET);    #set file pointer to start read

        for ($i = $numStamps; $i > 0; --$i)
        {
            $buffer .= fgets($handle, 32);

            #Debugging;
            #echo "moving ftell: " . ftell($handle);
            #echo "<br> <br>";                          
        }

        #Truncate and open file for storing fpointer
        $write = fopen("fpointer.txt", "w")
            or die ("failed to open fpointer");

        $fpointer = ftell($handle); #get file pointer for current position
        fwrite($write, $fpointer);  #save file pointer for next read

        #Debugging
        #echo ftell($handle);
        #echo " <br> Final destination <br> " . $fpointer;
        #echo "<br>";
        #echo $buffer;

        fclose($handle);    #close both files
        fclose($write);

        return $buffer;     #return the timestamp string
    }
?>