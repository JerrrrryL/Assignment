-- Gold Query for example_task_1.json
-- Show all attorneys who represent H-1B dependent employers
-- Calculate Attorney Case Load (ACL) and Attorney Success Rate (ASR)

SELECT
    e.corphandle AS employer_name,
    a.lawmail AS attorney_email,
    COUNT(DISTINCT ca.docketkey) AS attorney_case_load,
    COUNT(DISTINCT CASE
        WHEN LOWER(c.statustag) = 'certified' THEN ca.docketkey
        ELSE NULL
    END) AS certified_cases,
    ROUND(
        (COUNT(DISTINCT CASE
            WHEN LOWER(c.statustag) = 'certified' THEN ca.docketkey
            ELSE NULL
        END)::NUMERIC / COUNT(DISTINCT ca.docketkey)) * 100,
        2
    ) AS attorney_success_rate
FROM cases c
JOIN employer e ON c.homefirm = e.corphandle AND c.homezip = e.zipref
JOIN case_attorney ca ON c.filekey = ca.docketkey
JOIN attorney a ON ca.counselmail = a.lawmail
WHERE c.h1bdep = 'Yes'
GROUP BY e.corphandle, a.lawmail
HAVING COUNT(DISTINCT ca.docketkey) >= 2
ORDER BY attorney_success_rate DESC, attorney_case_load DESC;
