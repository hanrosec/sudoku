curl.exe `
    -b "Cookie: Phpstorm-222038db=573bc6d4-ca4d-4ea0-bf2a-a1baf4ad366a; SID=efuerlsfcA/eTtYXQMS0z92kC5qfvzbT; user_ip=31.61.163.60; session=eyJ1c2VyX2lkIjoxfQ.ZdCkHA.zv2FtJiBKIBbCAdp_YkM5yxvFY0" `
    -H "Content-Type: application/json" `
    -X POST `
    -d '{
        \"time\":\"100\", 
        \"user_hash\": \"0c12459cb45f3a2732aca65e1c9183a421a194f1597d2431319f95ece6b0753d6c8eebfaecb3393c349d646312c5103349df47b71d523850493262a242bf6b01\",
        \"system_hash\": \"0c12459cb45f3a2732aca65e1c9183a421a194f1597d2431319f95ece6b0753d6c8eebfaecb3393c349d646312c5103349df47b71d523850493262a242bf6b01\",
        \"control_hash\": \"8242003d3651eaed45f1f595b3970322c17200d5e4f1ea17822decdb5deaceb0eb9ee0d27703afa7fccb46151e4878519d3a6fc90bb62f8a0412fb75ff523fcc\"
    }' `
    http://localhost:5000/game/add_to_leaderboard