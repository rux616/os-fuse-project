<?php

$buffer = [];
$fpointer = 0;
$numStamps = $_GET['numStamps'];

$handle = popen("", "r");
	if ($handle)
	{
		for ($i = $numStamps; $i > 0; --$i)
		{
			$buffer = fgets($handle, 32);
			echo "moving ftell " . ftell($handle);
		}
		
		$fpointer  = ftell($handle);
		
		echo ftell($handle);
		echo "Final destination " . $fpointer;
		echo $buffer;
		
		pclose($handle);
	}
	else
	{
		echo "Error: could not open file!\n";
	}			
?>