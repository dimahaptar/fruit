import requests

print(requests.get('http://127.0.0.1:9990/').content)

print(requests.post('http://127.0.0.1:9990/products',
                    data={"name": "bad", "category": "no",
                          "price": .1, "quantity": 20}).content)
