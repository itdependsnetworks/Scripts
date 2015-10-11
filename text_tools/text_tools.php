<!DOCTYPE HTML PUBLIC "-//W3C//DTD W3 HTML//EN">
<html>
<title>Text Tools</title>

<body bgcolor="white" text="#000000" link=darkblue vlink=darkblue>

<p><center>
  </center>
<p align="center"><b><font size="+4">Text Tools</font> </b><br>

<hr>
<body>

Enter Changes on Left, and Configlet on Right<br>

<form action="./text_tools.cgi" method="POST" name="text_tools" id="text_tools">
<textarea rows="25" cols="100" name="interfaces" form="text_tools">
Enter Interfaces here, "OldInterface,NewInterface"
</textarea>
<textarea rows="25" cols="100" name="configs" form="text_tools">
Enter Configurations here,
</textarea>
<br>


<!--<input text name="configs" form="text_tools">-->
<input type="radio" name="type" value="onetime">Each line is a find replace for the whole config<br>
<input type="radio" name="type" value="multiple">Config is repeated multiple times, Seperate variables to find by comma on first line, and respective changes on each additional line<br>
<input type="submit" value="Submit" >
</form> 


</body>
</html>

