# GeoSpacial data visualization project

In this project we are looking to find the new office location for our start-up - a company in a gaming industry. We are a young and innovative company and we want our employees to be happy.

Our employees have the following requirements:

- Our designers like to go to design talks and share knowledge. There must be some nearby companies that also do design.
- 30% of the company staff have at least 1 child.
- Our developers like to be near successful tech startups that have raised at least 1 Million dollars.
- Our Executives like Starbucks A LOT. Ensure there's a starbucks not too far.
- Account managers need to travel a lot.
- Everyone in our company is between 25 and 40, give them some place to go party.
- Our CEO is vegan.
- We want to make our maintenance guy happy, a basketball stadium must be around 10 Km.
- Our office dog—"Dobby" needs a hairdresser every month. Ensure there's one not too far away.

# MongoDB query the Crunchbase dataset

From the crunchbase dataset we select companies which might be interesting to our designers and developers:
- Companies where category is 'design'
- Companies that have 'design' in the name
- Advertising agencies
- Companies that have 'design' in one of their tag-lists
- Companies in the Web space
- Start-up companies (founded after 2009)
- Companies with more than 10 employees

In order to satisfy the requirement of total fundraising 1m dollars, we exclude the companies where 'total_money_raised' is below $1m.

I have cleaned the data to remove the compnaies where raised amount is not available, or where the coordinates are not available. From a database of 690 companies we end up with a database of 250 addresses.

The dataset looks like this:

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/table0.jpg">
</p>

# Find the quality countries to establish your business in

From Our World in Data get the following datasets:

- % of adults holding secondary and tertiary education
- Healthcare expenditures as % of GDP
- Corruption Perception Index
- Homicide rate (World Bank)

https://ourworldindata.org/charts?search

The data is visualized by sorting the countries by each criteria:

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/homicide.png">
</p>

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/corruption.png">
</p>

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/education.png">
</p>

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/healthcare.png">
</p>

Next I create a combined index which will define the quality of the country:

- Education - higher is better
- Healthcare - higher is better
- Homicide - lower is better
- Corruption - lower is better

We give every indicator an equal weight of 25% and calculated a weighted ranking.

But before doing that we need to standardize the values by their mean and standard deviation: standartized score = (x - mean)/std

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/rank.png">
</p>

## From top countries find the suitable cities

- Filter the company database to see which of the companies are in the top 15 countries. 
- From the filtered database pick 3 top cities with the largest amount of relevant companies to us (design, advertisement, web, and tech start-ups)
- Find the mid-point between the companies in those three cities

This results in London, Berlin and Collingwood (Melbourne) as the top cities and the respective coordinates (mid-point of all start-ups around) below:

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/table1.jpg">
</p>

### Plot the maps of the three cities

In the maps below you will see the mid-point between the suitable companies in the city.

The mid-point is calcualted as a geographical mid-point where latitude = sum (latitude) / count (latitude)

## London

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/london_map1.jpg">
</p>

## Berlin

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/berlin_map1.jpg">
</p>

## Melbourne

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/melbourne_map1.jpg">
</p>


### Find the most suitable locations in the city

Search the Forsquare database for the following amenities in the area, with the respective distances:

- School (includes primary and secondary school) - 5km
- Starbucks - 2km
- Bar - 2km
- Club - 2km
- Airport - 30km
- Vegan Restaurant - 1.5km
- Basketball - 4km
- Pet grooming - 3km

## London

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/london_map2.jpg">
</p>

## Berlin

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/berlin_map2.jpg">
</p>

## Melbourne

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/melbourne_map2.jpg">
</p>

## Compare the cost of living across these cities

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/london_melbourne.jpg">
</p>

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/berlin_melbourne.jpg">
</p>


As we are a young startup and we care a lot about our employees, we want a location where they can play and grow without spending a fortune. Berlin seems to be the perfect combination of that.

# Our start-up goes to???


# Berlin!!!

<p align="center">
<img src="https://github.com/berserkus/GeoViz_mongoDB_project/blob/main/output/Berlin.jpg">
</p>
