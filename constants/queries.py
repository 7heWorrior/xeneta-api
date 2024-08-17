GET_FILTERED_PRICES = """
WITH 
filtered_prices AS (
    SELECT p.day, p.price
    FROM prices p
    JOIN ports o ON p.orig_code = o.code
    JOIN ports d ON p.dest_code = d.code
    WHERE p.day BETWEEN %(date_from)s AND %(date_to)s
    AND (o.code = %(origin)s OR o.parent_slug = %(origin)s)
    AND (d.code = %(destination)s OR d.parent_slug = %(destination)s)
)
SELECT fp.day, AVG(fp.price) as average_price, COUNT(fp.price) as price_count
FROM filtered_prices fp
GROUP BY fp.day
"""