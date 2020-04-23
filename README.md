# Covid-Datafest-2020

Link: https://covid-air-quality.herokuapp.com/

Recently in the news there has been a notable incline in articles pertaining to the decrease in air pollutants among other positive environmental consequences, from India, to China, to experts warning us that this may not be true.
With so many opposing views, we wanted to quantitatively investigate these claims with data and ask “is COVID-19 actually helping the environment?”

**Dashboard Run-through:** The first page allows you to select a city, and select the pollutant, or pollutants that you want to observe. If a change point exists, it will be indicated by a gray line. The slider on the bottom allows you to adjust the time that you’re observing and to zoom in on sections you would like to see closer. You can overlay species if you’d like to see that as well. 

If you would like to view multiple cities, you can go to the second page, which allows you to view trends for several cities for a certain pollutant. 

The third page allows you to view change points in the US for the desired pollutant, if it did occur. Bigger bubbles correspond to earlier change points, so for example, Jacksonville had a change point on February 4, whereas Fresno had a change point on March 6. We decided to examine these change points and compare them to the lockdown dates of cities to see if change points occurred after lockdown, since lockdown implies less mass transportation and manufacturing. However, upon closer analysis, we discovered that in the US, no change points occurred after lockdown for the cities that were locked down. 

To further explore this, we decided to look at China. On page 4, we take a closer look at change points in China. This first graph shows that 71 change points occurred before lockdown, and 35 change points occur after lock down. We hypothesized that maybe it takes some time for change points to occur after lockdown, since lockdown shouldn’t imply immediate improvement in air quality. This second chart examines, for China, where lockdown was placed earlier, the difference in days between change point date and lockdown date for change point dates that occur after lockdown happened. From this, we see that on average, change points occur around 20 days after lockdown. Since the US went on lockdown later, we think this may be the reason why we haven’t seen drastic improvement in air quality yet. In addition, China’s lockdown policies were more strict, meaning sources of air pollution were restricted better. 

The last chart shows us a breakdown of the pollutants that underwent a change. We see that, like many news articles have claimed, no2 did indeed constitute a decent portion of the change points that occurred. 

In conclusion, it seems that the US has not yet reached a point where there are observable change points for multiple air pollutants. However, we hypothesize that this change may happen later on. 

