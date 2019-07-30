# Searching-UniProt

As a biologist I am always having to look up the function of genes one at a time by copy pasting the gene names into UniProt. Here I created a python script which can be run in the terminal that automates the proces. You can provide either a .csv file with a list of interesting genes or enter a genes into the terminal separated by space. The output is a doc file that contains information about protein function (molecular, bological) and aliases.

If you provide a .csv file, it should have a column named 'genes'. In this case the file name will be to get the 'tissue site' information which is used to name the output .doc file.

I hope this saves you some time as it has done for me.
Feel free to edit and share!

Disclaimer: Please use the code responsibly and do not inundate the server with multiple scraping requests which may lead to slowing or crashing of the server.

