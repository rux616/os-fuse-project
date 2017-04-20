<?php
//saves the fpointer to a file, need a seperate file to timestamps for this.
//0 needs to be the value stored in this file at first.

$buffer = "";
$numStamps = $_GET['numStamps'];
#$j = 0;

$handle = fopen("timestamps.txt", "r") 
	or die ("Error: could not open timestamps!\n");
$write = fopen("fpointer.txt", "r+") 
	or die ("could not open fpointer");

$fpointer = fgets($write);

	
	if ($handle and $write)
	{
		fseek($handle, $fpointer, SEEK_SET);  //set file pointer
		
		for ($i = $numStamps; $i > 0; --$i)
		{
			$buffer .= fgets($handle, 32);
			#trim($buffer, $character_mask = " \n");
			#echo "moving ftell: " . ftell($handle);
			#echo "<br> <br>";
			#$j = $j + 1;
		}
		
		$write = fopen("fpointer.txt", "w") or die ("failed to open fpointer");	
		
		$fpointer = ftell($handle);
		fwrite($write, $fpointer);
		
		#echo ftell($handle);
		#echo " <br> Final destination <br> " . $fpointer;
		#echo "<br>";
		
		echo $buffer;

		fclose($handle);
		fclose($write);
		
		return $buffer;
	}	
?>