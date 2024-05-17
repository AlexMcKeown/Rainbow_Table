# MD5 Rainbow_Table
How the Reduction Function works:
The reduction function takes a hash value and converts it into an integer. 
This integer is then added together with j a variability counter. Lastly we then mod the two variables (hash_int + j) by the total number of lines read in by the password.txt file. We then repeat this an addition four more times and then save the hash and original word.

Applied formula:
(hash_int + j) % Passwords-Read-in

hash_int: hash value converted into an integer

j: represents a counter integer which starts from 0 and increases by increments of 1 for every loop until j == 5 then it stops. The purpose of the counter is that it add's variability to the reduction function
 
Passwords-Read-in: number of lines read in by the password.txt
