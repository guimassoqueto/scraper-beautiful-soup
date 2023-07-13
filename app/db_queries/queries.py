select_geral = """
SELECT id
FROM products
WHERE price > 100 
AND reviews > 2000 
AND category not ilike '%cd%'
AND category not ilike '%filmes%'
AND category not ilike '%brinquedos%'
AND category not ilike '%moda%'
AND discount > 20
AND is_prime 
ORDER BY discount;
"""
