# eBayDashboard
oAuth automation to PowerBi Dashboard for eBay Sellers

This is a simple two-script process to automate the pulling of data for Power Bi.  
You could use this for other programs or add to it, where necessary to meet your needs.

1st part is a token generator, that generates an oAuth token as well as the refresh token for trough the eBay developer program.  It requires and eBay developer account, as well as a eBay sellers account.  A user pop-up is generated that you grant yourself permissions to access your eBay sellers account.  After doing so, both an Oauth Token (good for 2 hours) and a refresh token (good for 18 months to generate new oAuth Tokens), is produced.

2nd part is a script that takes the refresh token and generates a new Oauth token to utilize to pull the information for the dashboard.  Right now, it currently is setup to pull information for about 5 different requests.  The actual dataframes or tables, that are created, will be noted in all capital letters.
