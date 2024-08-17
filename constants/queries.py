GET_FILTERED_PRICES = """
WITH filtered_prices AS (
    SELECT p.day, p.price
    FROM prices p
    JOIN ports o ON p.orig_code = o.code
    JOIN ports d ON p.dest_code = d.code
    WHERE p.day BETWEEN %s AND %s
    AND (o.code = %s OR o.parent_slug = %s)
    AND (d.code = %s OR d.parent_slug = %s)
)
SELECT fp.day, AVG(fp.price) as average_price, COUNT(fp.price) as price_count
FROM filtered_prices fp
GROUP BY fp.day
ORDER BY fp.day
"""
