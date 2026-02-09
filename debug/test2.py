import requests

config = {
    "url": "https://my.irancell.ir/api/gift/v1/refer_a_friend",
    "headers": {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "fa",
        "authorization": "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJmaXJzdF9uYW1lIjoiXHUwNjQ1XHUwNjJkXHUwNjQ1XHUwNjJmXHUwNjJjXHUwNjQ4XHUwNjI3XHUwNjJmIiwibGFzdF9uYW1lIjoiXHUwNjQ2XHUwNjJjXHUwNjQxXHUwNjRhIiwiZW1haWwiOm51bGwsInNlcnZpY2VfY29kZSI6IkdTTSIsInNpbV90eXBlIjoiZmQiLCJvcGVyYXRpb25fc3RhdHVzIjoiYWN0aXZlIiwicHJvZmlsZV90eXBlIjoiaW5kaXZpZHVhbCIsInByZWZlcnJlZF9sYW5ndWFnZSI6ImZhIiwiY3VzdG9tZXJfdHlwZSI6InByZXBhaWQiLCJjb3dfZGF0ZSI6bnVsbCwicGhvbmVfbnVtYmVyIjoiOTg5MDQ2Njk5MDk1Iiwic3ViIjoiOTg5MDQ2Njk5MDk1IiwiaW5zdGFsbGF0aW9uX2lkIjoiMTIxNmVkMjktNTAxYy00MGM4LTkzNjItZWViY2E3ZjA3NjcyIiwiY2xpZW50X2lkIjoiNDcyNWE5OTdlOTRiMzcyYjFjMjZlNDI1MDg2ZjRhMTciLCJjbGllbnRfbmFtZSI6IndlYiIsInNqdGkiOiJhNzVlY2E5Ny03MDE1LTQ2ZGQtYTU2Mi02NTEyZjc3NWJkOWQiLCJtdG5pIjp7ImZpcnN0X25hbWUiOiJcdTA2NDVcdTA2MmRcdTA2NDVcdTA2MmZcdTA2MmNcdTA2NDhcdTA2MjdcdTA2MmYiLCJsYXN0X25hbWUiOiJcdTA2NDZcdTA2MmNcdTA2NDFcdTA2NGEiLCJzZXJ2aWNlX2NvZGUiOiJHU00iLCJzaW1fdHlwZSI6ImZkIiwicmVnaXN0cmF0aW9uX2RhdGUiOiIyMDIwLTEwLTA1IDExOjUzOjE2Iiwib3BlcmF0aW9uX3N0YXR1cyI6ImFjdGl2ZSIsInByb2ZpbGVfdHlwZSI6ImluZGl2aWR1YWwiLCJjdXN0b21lcl90eXBlIjoicHJlcGFpZCIsImNvd19kYXRlIjpudWxsfSwiaWF0IjoxNzY3NDI2NjA3LCJleHAiOjE3Njc0OTg2MDd9.iN0BnlpwjxeaLblLDoX3v_0fd0ZfKi7EtaBnHmHNmYNidxnyEQhFgxgrEUahbvpVuthNF5VTHvPETCa2VHM3sOwPFoC0m4IBwXNT7IOVkEJFhs_90pY8s9mCsGv-CQmgdyRzck-cjLmUNcF2VEhVghTycUipg3sm0Pk5Ripc6wYpWy5RXqn7AMvgIaOP0cdURiJXaN3XVrzCk_wlODXJxPE2vpTbxAzXNDyUmoWqBgyM-OTWMblkV4SO7Dj5Qdvu-gbbtiFZJ73qLz963zqnEejBJ1X6UMZ-DRML3ccPuWjdH6gEmDNAEoENThd0EgiG_PlyYeLmgB9T6wk6ZwOai-Jg7bN2x0gOVsai6PTa7hejkxqJ_fYe9Pc9l1hGC9mgJzxLLMnvjs8472zaFf6VrpWEVYlvOYPuKbF9ZL03BtxeXXJX4JiOn2HfJm11B_aPHMHbyAC1VDl2N5R24QNNL6LE3RpCj33ktTYgvOmi0G3AFs59fvfMvGHhUhvNHng7NLs1dzPIFcP5E-p2oeNx_pCBwxsOlV88GrsKXFiZKU3LRMLbPVCN6cVF-64-NBJvVgQhUHeLvizW4nWroZ-0MbqAzBJBEr11gLMHTio9GKvwwUqKoPDD0cx8Hjb3KMzZtgC6730M-11lu2JH-mkdcogjNQVJd4IbzwACD43U7rs",
        "cookie": "CVRaaaaaaaaaaaaaaaa_session_=CJGKAPGLCOJACDALEOBODEJNLNPEKGKDLHEAKPOKDGFLLFKKCMCPGCBKDOGIPPALGKLDAFJDBBIOJPNAIOGAHEGGIKGFNEPINFIDFMPFIHNDPHEPEGNIKJDLGKIKNGDD; CVRaaaaaaaaaaaaaaaa_session_=NJAAAPKBFHHMHCIHJAEKPNJPDFEJHDELMFJFCNLMIGKOHGCEGHKDPJCJKDFENGPJBAKDAHDJANJDDADIKPHADKHHPKEHKMCKHFNAOHABBMJMLGHJJAOFJDAFAKAHEEAA; _pk_id.1.8dd7=b79c86e54db22cff.1764668523.; _pk_ref.1.8dd7=%5B%22%22%2C%22%22%2C1764887634%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; zbl_utm=ZBLU2FsdGVkX19HL2x6MA1ulA2albCBJ4CtCty8/WB5jv2SnEiO++RojZWZEawYewC4fHZEy7LLjtPJ8j43+kctbyeFUtCozHQTzIzNBX5rDMUV0LVQKSLxYt+8ISz56EoGRDwZgmv37X0/GLEAZ/IrBQ==; zbl_anonymous_id=ZBLU2FsdGVkX1++D6/xoV4YEr5kkM7V3/lJYC+liFWqZF/7DjVj9b2BTCr0Zo39ZOfu; zbl_user=ZBLU2FsdGVkX1/eSa7zEFlm1EMLgDymjYbY04DwXxnwRivOglcFPEFVMAqBrTJvcKjzW7qKQrTcwsz1oNEO8b24jA==; CVRaaaaaaaaaaaaaaaa_session_=LJPKKOJMFPGMGKNIPEMFINBPCPBAGLLHNIBFBNOJHGNJPGMAPBNHCKHAONNGPDCOGDKDMHHDHJFJLEFMGBAAMMFKOMNANIDIHCHIGCHAMHCAFOCAFLDGGNHLKOAAFMNJ; CWP01ce7e2e=0174e85e00fd28a78377ce5b5a2491a4c8bdfbfdfb83bffac6d0828e6993e1093deb06d72ceba44aad7fb29735d16f94ed2170f2526c264a023e5d465cd80210e46c859912; CWP45fbcf99027=08b7167e39ab20007aec9abd75e1170405114e3f3770ee81feb7d5c5665a57a97a6f8d5b340e86b708c135cd5c1130009ff0f4563d3b9fa77059a80335e6bbec57e94b3a3a0bd819b6a4e34cef64ccb2dbace5398e69d44ca974a8a9a7117cc2",
        "connection": "keep-alive",
        "content-type": "application/json",
        "origin": "https://my.irancell.ir",
        "referer": "https://my.irancell.ir/invite/confirm",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "x-app-version": "9.67.1"
    }
}

a = requests.post(config["url"], headers=config["headers"], json={
    "friend_number": "989024188951",
    "application_name": "NGMI",
})
print(a.status_code)
b = a.json()
print(b)