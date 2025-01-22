## Troubleshooting population weights:

**what if only 10% (or some small proportion) of the PG_id field has population?**
This will not occur because the proportion is calculated as a function of the total population in that cell. So even if the total PG cell is 100 (which is very small) those 100 citizens will be distributed between the smaller units within the pg. 

1. we could develop a function that applies the value associated with the greatest population proportion (irrespective of the total population contained)
- but if zero, fallback to area proportionality


**or a dynamic approach that selects between the area proportion if total (or normalized) population proportion is below some threshold**

2. Assign weights based on population density of PG values. 

This would require a distribution curve for population in that country for that year.
- **What proportion of PG cells in Country X have no population data?**

- If population values (of pg id) are in the highest 85 percentile of population values in the country then population proportion is considered exclusively (obviously there would be population coverage in these areas)

- If population values are in the top 50th percentile apply some unique weight to area vs population proportionality

- If population values are in the bottom 50th percentile (or zero) just consider area proportionality

Example:
The total population for pg_id determines the percentile threshold:
If the PG_Cell_total_population (e.g., 15,000) is above the 85th percentile, use proportional population exclusively.
If the PG_Cell_total_population is between the 50th and 85th percentiles, apply a 75% weight to population and 25% to area.
If the PG_Cell_total_population is below the 50th percentile, use proportional area exclusively.