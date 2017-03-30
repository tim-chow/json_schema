# json_schema

Python版的json schema工具，用来校验json

---

# 例子：

```
schema = {
    "@type": list,
    "@value": {
            "@type": dict,
            "@required": ["2.2.2.2", "key_name"],

            "@special_{key_name}": {
                "@type": list,
                "@value": {
                    "@type": int,
                    "@max_value": 10000,
                    "@min_value": 30,
                }
            },

            "@regexp": "(\d+\.){3}\d+",
            "@value": {
                "@type": int
            }
    }
}

validate(schema, [{"key_name": [31, 1000], "1.1.1.1": 3, "2.2.2.2": 4}])
```
