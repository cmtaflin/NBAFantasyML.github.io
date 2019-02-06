I created flask routes for everything and placed the HTML files where they will go so they work.  for now, use the "pointsposition_test.html" file to start with your code.

high-level notes:
I only changed the following HTML files:
    pointsposition_test - was "index.html" in your version.
    GraphStyles.css - I placed all of the css items you had individually into this central spot.
    /NBA-graph/center.html - this is the template to use for your other 4 position pages.

Big-ticket items I changed (that you will need to do on the other 4 pages):
    1) repoint the css file for each page to be "../static/css/GraphStyles.css" in addition to the standard styles.css.
    2) change the path to the individual pages from the index to match the correct syntax.
    3) point to the new javascript file for each page. Please rename the app.js file you have for each to be "app_powerforward.js" (or whatever the position name is), and copy it to the central js folder.


Once you have those updates on all 5 sub-pages, verify it works.  We would like to have the same formatting as the rest of the pages, but at least it loads.

Note that out of the existing pages, only the heatmap.html page points to the test html file.  Once we know this is working, we can update the rest.