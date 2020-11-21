# python-query-filter

This tool adds several features to Python's built-in `filter` function.
- Use a range of _query_ predicates to compose complex filters over nested data.
- Pass keword arguments for matching non-nested keys and attributes exactly.
- Pass any number of custom predicate functions.


## Basic keyword filter

If you're lucky enough to be working with collections of flat dictionaries
and only need exactly, matches, you can simply use keyword arguments.

```python
>>> from query_filter import query_filter
>>> data = [
        {
            "id": 1,
            "first_name": "Allsun",
            "last_name": "Shergill",
            "email": "ashergill0@icq.com",
            "gender": "Female"
        },
        {
            "id": 2,
            "first_name": "Mattie",
            "last_name": "Mazzilli",
            "email": "mmazzilli1@elpais.com",
            "gender": "Male"
        }
    ]
>>> list(query_filter(data, gender="Male")) 
[{'id': 2,
  'first_name': 'Mattie',
  'last_name': 'Mazzilli',
  'email': 'mmazzilli1@elpais.com',
  'gender': 'Male'}]
```

## Filter predicates

### Using Any, All and Not

### List of inbuild predicates

### Writing custom predicates
