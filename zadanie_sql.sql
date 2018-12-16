--select * from picie;
--select * from gdzie_kupic;
--select * from czym_zagryzc;

SELECT p.co,
       p.kiedy,
       coalesce(CASE
                    WHEN p.co = 'Whiskey'
                         AND cz.rodzaj <> 'malosolny' THEN NULL
                    WHEN p.co = 'Gin'
                         AND gk.sklep <> 'Zabka' THEN NULL
                    ELSE p.zapitka
                END, '') zapitka,
       coalesce(CASE
                    WHEN cz.rodzaj <> 'malosolny'
                         AND p.co = 'Whiskey' THEN NULL
                    ELSE gk.sklep
                END, '') sklep,
       coalesce(CASE
                    WHEN cz.rodzaj <> 'malosolny'
                         AND p.co = 'Whiskey' THEN NULL
                    ELSE gk.cena||'zł'
                END, '') cena,
       coalesce(cz.potrawa, ''),
       coalesce(cz.rodzaj, '')
FROM picie p
LEFT OUTER JOIN gdzie_kupic gk ON p.co=gk.co
AND p.kiedy=gk.kiedy
AND CASE
        WHEN p.co = 'Vodka' THEN gk.id = p.id
        ELSE 1=1
    END
LEFT OUTER JOIN czym_zagryzc cz ON p.co=cz.co
AND CASE
        WHEN gk.sklep = 'Biedronka' THEN cz.potrawa = 'herbata'
        WHEN gk.sklep = 'Centrum' THEN cz.potrawa = 'czipsy'
        WHEN gk.sklep = 'Kiosk' THEN cz.potrawa = NULL
        ELSE 1=1
    END
ORDER BY p.kiedy ASC,
         gk.cena DESC,
         cz.potrawa DESC;