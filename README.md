# Bibliometric-Article-Analysis
# Table of contents
1. [Introduction](#introduction)
2. [How to use](#paragraph1)


## Introduction <a name="introduction"></a>
This is a tool created by AUC interns in order to analyze and visualize the bibliometric data for a given DOI. The tool recieves one DOI as input and displays bibliometric data scarped from the web. This bibliometric data includes: the name of the article, the name of the journal that it was published in, the citescore and quartile of that journal, the number of articles that cited this article, and whether or not the journal that it was published in is open access or not.

In addition, the tool also scraped the web to find all the articles that were cited in the given article. It displays a table containing all the articles that were found along with all the bibliometric data mentioned in the above paragraph. It then sorts this table based on the citescore of the journals that the cited articles were published in and recommends (if found) two journals with the highest citescore and two open access journals that have the highest citescore. Lastly the tool visualizes the findings by a scatter plot based on the cited articles' journal citescore, comparing them to the original article's journal citescore, it also visualizes a bar chart based on the counts of each quartile of the cited articles' journals, marking the quartile of the original article's journal.

## How to use <a name="paragraph1"></a>
1. Install python from: https://www.python.org/downloads/
2. Download the code as a zip and then unzip it or use git clone command to download the code
3. Go to the directory to where the code was saved
4. Right click and click on "Run in Terminal" option.
![image](https://user-images.githubusercontent.com/78408934/187026405-b51781b7-e9ea-4fd3-b5cf-6f99db5ab736.png)
5. Run "pip install -r Requirements.txt" in the terminal
6. Copy and paste the contents of "Run.txt" into the terminal
7. Control + click on the outputed link which will take you to the website
![image](https://user-images.githubusercontent.com/78408934/187026498-236c9638-511d-4b8e-9f22-eb15c60b5c07.png)




