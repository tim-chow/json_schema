import re

def validate(json_schema, json_object):
    typ = json_schema.get("@type")
    if not isinstance(json_object, typ):
        raise RuntimeError("validate failure 1")

    if typ in [int, long, float]:
        if json_schema.get("@max_value") and \
            json_schema.get("@max_value") < json_object:
            raise RuntimeError("validate failure 2")
        if json_schema.get("@min_value") and \
            json_schema.get("@min_value") > json_object:
            raise RuntimeError("validate failure 3")
        return

    if typ in [str]:
        if json_schema.get("@regexp") and \
            not re.match(json_schema.get("regexp"), json_object):
            raise RuntimeError("validate failure 4")
        return

    if typ in [bool]:
        return

    if typ in [list]:
        for item in json_object:
            validate(json_schema["@value"], item)

    if typ in [dict]:
        required_keys = dict.fromkeys(
            json_schema.get("@required", []), True)

        for k, v in json_object.iteritems():
            required_keys.pop(k, None)
            schema = json_schema.get("@special_{%s}" % k)
            if schema:
                validate(schema, v)
                continue
            regexp = json_schema.get("@regexp")
            if not regexp:
                continue
            if not re.match(regexp, k):
                raise RuntimeError("validate failure 5")
            validate(json_schema["@value"], v)
        if required_keys:
            raise RuntimeError("validate failure 6")

if __name__ == "__main__":
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

