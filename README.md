Analyzing School Assessment Data Using K-Means Clustering
=========================================================

A project to examine the feasibility of using clustering to help analyze
Washington school assessment data.

### Authors
* Michael Delaney
* Lawrence Fritts
* Perry Hook

# Summary
Schools are currently being graded on the Washington State Assessment in reading, writing, math, and science at both the state and federal level.  Each year, the state provides the data to districts and schools from the previous year.  This data compares the last year's data with previous years and determines an adequate yearly progress goal for the current year.

A problem that faces a school is understanding why progress is not being made at a rate that matches or exceeds the adequate yearly progress.  Each year some schools continue to far exceed their adequate yearly progress goals while others founder.  Some years a school may go from not making adequate yearly progress to far exceeding it or vice-versa.

Schools that are struggling are often provided excuses such as:

* Our students socioeconomic status is low and the students have bigger problems to worry about.
* Our school is too large to be able to individualize instruction.
* We have a big non-English speaking population and they can't succeed.
* The objectives on the state assessment are too hard for students like ours.

A comparison of like schools (based on demographics) may help a school recognize that the learning required can be done if similar schools are performing better.


The data comes in two large files.  One file contains the demographic information for each school, the other the assessment information.  It is difficult to combine these two files for most people and even more difficult to then pull out information on schools that are similar to the one they are interested in.

Out project attempts to take these files and make this process simpler.  We envision a process such as this:

    1. A user visits our web app.
    2. They select their school:
        a. We limit the schools the type of school; elementary, middle, high.
        b. We then use k-means clustering to determine the 20% of schools that are closest to the school based on enrollment size.
        c. This cluster becomes the new dataset for further analysis.
    3. Now the user will select the next demographic item they would like to sort on:
        a. We then use k-means clustering to determine the 20% of those schools that are closest to the school based on that demographic data.
        b. That cluster becomes the new data set.
        c. Repeat the process until the user is ready to cluster on assessment data.
    4. When the user is ready to cluster on assessment data:
        a. The number of clusters is determined by the number of schools in data set / 5.
        b. The k-means cluster is ran and the clusters are presented to the user with the average of the assessment reported for each cluster.
