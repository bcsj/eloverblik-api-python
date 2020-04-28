# eloverblik-api-python
A simple python setup for extracting your energy consumption data from www.eloverblik.dk using the provided API.

For information on the API go here (website in Danish):  
https://energinet.dk/El/Elmarkedet/MDA---Ny-loesning

For the technical document on the API go here (pdf in English):  
https://energinet.dk/-/media/E035C87801B74321A03C07FFC3085EFA.pdf

## Getting an ACCESS TOKEN
To get an **ACCESS TOKEN** go to www.eloverblik.dk, click **Privat** and log in using **NemID**. 
When logged in click the small "person" icon in the top right corner and select **Datadeling** (Data Sharing) in the drop down menu.
Click **Opret Token** (Create Token) and give the token a name. Copy the displayed **ACCESS TOKEN** and store it securely.
Place the token in a textfile "eloverblik.token".

**DO NOT SHARE YOUR ACCESS TOKEN!**

