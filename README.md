# SEO Scraper by Holger Kurtz
Tools for analysing a web pages structure

## Input: UR
Takes domain like "kulturdata" as an input

## Process:
1. Download page
    1.1 find title
    1.2 find description
    1.3 find h1, h2, h3, h4
    1.4 find p
    1.4 find a 
    1.5 find a linktext 
- optional = 1.6 calculate link juice (how many clicks away from homepage?)
 
2. Safe to database 
- columns : url, title, description, h1, h2, h3, h4, p, a, linktextt, (linkjuice) 

3. Open new page
    3. if href 
    3.1 for every a open a 

4. Repeat

## Output: 
- mind map that shows linked sitemap?
- databse (csv?)
- PDF with comments?
 
