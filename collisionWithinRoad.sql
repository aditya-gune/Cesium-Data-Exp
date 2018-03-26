select c.uniquekey, c.on_street, c.cross_street, co.name from public.collisions c
join citydb.cityobject co 
on ST_Within(ST_Transform(c.geompoint, 4326), ST_Transform(co.envelope, 4326))
limit 100;