=== How to do EVERYTHING Associated With Running this Model ===

**It is recommended to install Notepad++ because it is very effective for opening
the .grd, .dep files and .bat files. It's also just better than the default notepad. 

===Part 1-Set-Up: 

Step 1: 
Create a folder to hold everything or open the folder called ModelFiles. This folder
contains all the files for a model run. 

Step 2: 
Either create a new file that has the following format or use the current
Inputs2D.txt file and change the inputs. This inputs file will be read in by 
yGrid.py, make sure to update the name of the file in the code specified by the 
comments. 
It is worth noting that width is perpendicular to the motu and length is parrallel
to the motu. 
- Format of the Inputs File (Replace discriptions with values): 
- Please note that all slopes must be floats (decimals). If you want a slope of 1 it must be 1.0. Everything else must be a whole number.  
	offSl = Lenght of off shore deep water area.
	offSd = Off shore depth.
	offSlope = Off shore slope leading up to the reef flat.
	dto = The distance the reef pit is from the ocean. 
	reefdep = The depth of the reef flat. 
	rpW = The width of the reef pit. 
	rpdep = The depth of the reef pit. 
	rpsl = The slope on either side of the reef pit. 
	dtm = The distance the reef pit is from the motu. 
	motuW = The width of the motu.
	land = The elevation of the land. 
	mtSlope = The slope from the reef flat leading up to the motu. 
	lgW = The width of the lagoon. 
	lgDep = The depth of the lagoon.
	bckSlope = The slope of the motu going down to the bottom of the lagoon.
	maxXres = The maximum resolution in X.
	minXres = The minimum resolution in X.
	rflatLen = The length of the reef flat. 
	rpLen = The length of the reef pit. 
	motuL = The lenght of the motu. 
	Ymin = Minimum resolution in Y. 
	Ymax = Maximum resolution in Y.
	rpRes = The resolution at the reef pit. 
	motuRes = Resolution at the motu
	rfRes = The resolution of the entire reef flat. 
	offshoreRes = The resolution of the off shore area. 
	lgRes = Resolution of the lagoon.
	reefslopeRes = Resolution of the reef slope. 
	motuSlpRes = Resolution of the slope of the motu coming from the reef flat. 
	backslopeRes = Resolution of the slope behind the motu. 
	
Step 3: 
Copy and paste the inputs file from step 2, gridCreation1D.py, yGrid.py,
ntcdfReader.py, createCY.py, params.txt, jonswap.txt, and the .bat file to run XBeach into 
the folder you created to hold everything in step 1, or check if they are all in the ModelFiles
folder. 

Step 4: 

For detailed instructions as to how to run this file open the yGrid.py file and 
read the comments near the bottom of the file. 

Run the yGrid.py file. Have yGrid.py print the shape of X, Y and Z.It will 
create 3 new files. You do not have to worry about them.They are being used 
by the gridCreation1D.py file to creat the X and Z files. This will also create 
a file with the indicies of the first corner of each geologic formation (ex: 1540, 0
could be the start of the reef flat). It will also contain the length and width for
each feature. 

 - Step 4a: 
	- To run this file open the terminal and type G: or the letter of the drive you are using. G: Will take 
		you to the G drive.
	Press enter. 
	- Next type cd and then the file path to the folder where the yGrid.py is located. 
		Example Filepath: cd \Shared drives\Ortiz Atolls Database\Excavation Pits\JConnors_2DReefPit\Model data\Real Grid Creation\ModelFiles>
		- This will take you to the ModelFiles folder. The last argument in this line should be the name of the folder you want to go to. 
	- Next type py (if Windows) or python3 (if Mac) and then yGrid.py and press enter. This will run the file. 

Step 5: 
Now take the shape of X and Y that was printed out and open params.txt and fill in the 
nx and ny spot with 1- number of rows and 1- number of cols. The shape will read rows columns. 
ROWS is Y, COLUMNS is X. Y is first and X is second. It's wierd. 

Step 6: 
Open, but do not run the .bat file. You will see "call ..\..\..\XBeach_Files\xbeach.exe".
The ..\..\..\ means that the file is going up 3 directories. The XBeach_Files\xbeach.exe means 
that .bat file is then going into the XBeach_Files folder and running xbeach.exe. If you put
the .bat file in another folder inside the one from step one you will need to add another 
..\ to go up one more directory. 

Step 7: 
Open the jonswap.txt file and put in the desired inputs: 
	- Each of these numbers requires 4 decimal places. 
	Hm0		 = Wave Height
	Tp 		 = Wave Period in seconds
	mainang  = Wave Angle
	gammajsp = Enhanment factor (use defualt = 3.3000) 
	fnyq	 = Highest frequency used

Step 8:
Open the params.txt file and enter all the variable names you want to 
at the bottom of the file. Variable names can be found in the XBeach 
mannual. Be sure to update the number of variables, nglobalvar, to the
exact number of variables you have. 

Step 9: 
With in the params.txt file there are parameters called the xfile, yfile
depfile, nx, ny, xori and yori. The xfile, yfile and depfile need to be set to the names
of the .grd files and .dep file, file extensions included. Nx, and ny need to be set to the 
number of rows and columns minus 1. When you printed out the shape of X and Y the first 
number is ny and the second one is nx. Be sure to subract one from each number you're 
going to enter. xori and yori are usually 0. They are where the grid originates from.
	
***Check In: The files you should have in the folder now:
	- The inputs file. 
	- gridCreation1D.py
	- yGrid.py
	- createCT.py
	- ntcdfReader.py
	- params.txt
	- jonswap.txt
	- the .bat file
	- 4 .txt files 
		- 3 of these .txts are used in the gridCreation1D.py, do not worry about them. 
		- The fourth one contains the bounds for the land forms in the model.
	- 2 .grd files 
	- 1 .dep file
	
Step 10: 
Create another folder within the original one you made in step one. This is the 
control case foler. Move the createCT.py file into this folder. Copy the .dep file, 
both .grd files, the bounds .txt, the Inputs file, the params.txt, jonswap.txt 
and the .bat file into the new control folder. 

Step 11: 
Create another inputs.txt file for the control case. Set the rpdep to the reefdep number 
and the rpsl number to 0 to create a grid without a reef pit or set the land parameter 
to the reefdep parameter and the rpdep to the reefdep and the rpsl to 0 to create a grid 
without a motu and reef pit. 

Step 12: 
Run the createCT.py file the same way you ran the yGrid.py file, but this time cd into the control folder. 
This file will generate atleast one grid without a reef pit. For more detailed instructions on this file 
see the comments within the file. 

***Check In: The Files in this folder should be: 
	- The inputs file for the first case.
	- The inputs file for the Control case.
	- createCT.py
	- params.txt
	- jonswap.txt
	- the .bat file (You will need to open this an add another ..\ to go up one more directory) 
	- 4 .txt files 
		- 3 of these .txts are used in the gridCreation1D.py, do not worry about them. 
		- The fourth one contains the bounds for the land forms in the model.
	- 2 .grd files from the original folder. 
	- 1 .dep file from the original folder. 
	- 1 or 2 .dep files from generated from the createCT.py run. 
	
Step 13: 
Be sure to change the name of the depfile to the name of the .dep file generated from the createCT.py file. 

===Optional Steps (1D runs):

Step 1: 
If you would like to create a 1D profile of the model, create another folder to contain these runs. Within this folder create three 
more folders, one for the 1D reef pit run, one for the 1D run with just the reef flat and one for the 1D run with just the motu. 

Step 2: 
Go back to the original x.grd file from the first folder and copy one line of code from the .grd file for x. In each of the
1D profile runs create a new x.grd file and paste in the one line from the original file. 

Step 3: 
For each of the 1D folders create a new .dep file. Now go to the original .dep file and find a line or numbers that corresponds to the reef pit, 
just the motu, and just the reef flat. Copy these lines into the corresponding .dep files in each folder. To tell each line appart 
the reef pit line's numbers will drop down to the rpdep within the reef flat. The reef flat line will have no positive values and have a 
constant depth without going down to the reef pit depth. The line with just the motu will have positive values but no values at the 
reef pit depth. 

Step 4: 
Copy in the jonswap.txt and the params.txt. Within the params.txt get rid of the yfile filename and the yori number. Set the ny equal to 0. Change the name of 
the xfile and depfile to the appropriate names of the .dep and .grd files in the folder. The nx should be the same. Also copy in the .bat file to each folder
and add another ..\ to the call line for each .bat file. 

Now that all the grids and dep files have been made you can run the model. 

===Part 2-Running the Model: 

Step 1: 
Open Command Prompt, type cd and the file path to the folder used in part 1. 
If the folder is on a different drive, for example the G: drive, first just type 
the name of that drive to switch into that drive. For example typing G: and then enter 
will change to the G drive. 

Example filepath: G:\Shared drives\Ortiz Atolls Database\Excavation Pits\JConnors_2DReefPit\Model data\Real Grid Creation\ModelFiles 
The last entry into this line is the name of the folder you want to access. 

- Accessing the ModelFiles folder in the example: 
	1. Type into the command line G: 
	2. Then type in cd Shared drives\Ortiz Atolls Database\Excavation Pits\JConnors_2DReefPit\Model data\Real Grid Creation\ModelFiles

Step 2: 
Call the .bat file by typing the name of the file into command prompt. Press enter, 
if set up correctly it should run. If there is an error that says cannot find specified
directory check the .bat file and see if the correct amount of ..\ have been entered. 

Step 3: 
Watch the model run for a bit, once it gets out of the start up sequence it will most 
likely be fine. Once its done it will generate a file called xboutput.nc. If there was an error 
in the model there will be some text in the XBerror.txt. 

Step 4: 
To run the control case, cd into the control case folder. Change the name to whatever you named the control case folder to. 
Then run the .bat file in the command line just like the run from above. If you have 1D cases you must cd into each of those folders 
and run the .bat files in there from the command line as well.  
cd Shared drives\Ortiz Atolls Database\Excavation Pits\JConnors_2DReefPit\Model data\Real Grid Creation\ModelFiles\"ControlCaseFolderName"

===Part 3- Analyzing the Data: 

Step 1: 
Open the ntcdfReader.py file. Read the comments as to how to enter in the correct file paths. 
Within these descpritive comments there are directions as how to run each function to generate 
each plot. 

Step2: 
Scroll down to the bottom of the file. There are comments that start with a #n.(functionName). These will run 
the figures, but they are commented out. To uncomment something delete the # in front of it. These comments are 
plots for the variables in the xboutputs file. Within each comment there should be the name of the variable being 
called. Uncomment the ones you want and run the file. 
**WARNING: Do not uncomment more than 20 figures. Python has a limit of 20 figures and the code will run for a long
time and then present you with an error. Also, if there are more than 20 figures being called at the same time you will
be able to fry an egg on your computer.  

Step 3: 
After running these functions click on the Save icon at the bottom of the figure and save it whatever folder you 
want. 

Step 4: 
If there is not a function for the variable that you want read the comments within the file about how to use the function 
and enter in the correct variable name. The variables available are at the bottom of the params.txt file. 
