WITH turnstile_diff
AS (SELECT turnstile,
        time,
        entries - (lag(entries) OVER (PARTITION BY turnstile ORDER BY time)) AS entries,
        exits - (lag(exits) OVER (PARTITION BY turnstile ORDER BY time)) AS exits
FROM public.mta
)
SELECT turnstile,
	   date_trunc('day', time) AS time,
	   SUM(entries) AS day_entries,
	   SUM(exits) AS day_exists
FROM turnstile_diff
GROUP BY 1, 2;

