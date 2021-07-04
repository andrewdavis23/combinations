# combinations
Create combinations of lists

Input two lists of integers and click compile to get every combination of the two lists.  Duplicates are removed.

How it works:
1. Split the input lists into arrays on '\n'
2. Remove all empty strings.  This will allow users to include empty rows in the input.
3. Sort the arrays by integers.  If strings are in the list, the program will not work.
4. Format the combinations as a tab delimited list: combos += i + '\t' + j + '\n'


![image](https://user-images.githubusercontent.com/47924318/124390394-5e0e7b80-dcb9-11eb-8fd4-54649fbec401.png)
