SELECT turnstile,
        time,
        entries - (lag(entries) OVER (PARTITION BY turnstile ORDER BY time)) AS entries,
        exits - (lag(exits) OVER (PARTITION BY turnstile ORDER BY time)) AS exits
FROM public.mta