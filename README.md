**Command to run** - 
> python engine.py --rules /path/to/rules.json --data /path/to/data.json

**Approach**

Each operation of each condition is checked against single data hashmap.
A condition has key
> logical_operation

whose value choices are -
> any - return True if any operation fails, else return False
> all - return True only when all operations fail, else return False   

Operations are run only when the *value_type* of *data* allows the said *operation*

Operations allowed on data_type **String** -

>**same_as** - data value is equal to rule value
>
>**equal_to_case_insensitive** - data value is equal to rule value ignoring case
>
>**starts_with** - data value starts with rule value
>
>**ends_with** - data value ends with rule value
>
>**contains** - data value has rule value as substring
>
>**matches_regex** - data value matches regex of rule value
 

Operations allowed on data_type **Datetime** -

> **is_before** - data value is less then rule value
>
> **is_before_or_at** - data value is less than or equal to rule value
>
> **is_after** - data value is greater than rule value
>
> **is_after_or_at** - data value is greater than or equal to rule value
>
> **is_at** - data value is equal to rule value 
>
> **is_not_at** - data value is not equal to rule value
>
> **is_at_moments_before_now** - current datetime value is greater than data value than rule value 
>
> **is_not_in_future** - data value is not greater than current datetime value



Operations allowed on data_type **Integer** -

> **not_equal_to**
>
> **equal_to**
>
> **greater_than**
>
> **greater_than_or_equal_to**
>
> **less_than**
>
> **less_than_or_equal_to**


*rules.json*
```javascript

[
  {
    "condition": {
      "operations": [
        {
          "comparison_value": "HIGH",
          "name": "equal_to_case_insensitive"
        }
      ],
      "signal_id": "ATL1",
      "logical_operation": "any"
    }
  },
  {
    "condition": {
      "operations": [
        {
          "name": "is_not_in_future"
        },
        {
          "comparison_value": "2017-09-22 05:24:18",
          "name": "is_after"
        }
      ],
      "signal_id": "ATL10",
      "logical_operation": "all"
    }
  },
  {
    "condition": {
      "operations": [

        {
          "comparison_value": "81.386",
          "name": "greater_than_or_equal_to"
        }
      ],
      "signal_id": "ATL6",
      "logical_operation": "all"
    }
  },
  {
    "condition": {
      "operations": [

        {
          "comparison_value": {"days": 400, "seconds": 77366, "microseconds": 559674 },
          "name": "is_at_moments_before_now"
        }
      ],
      "signal_id": "ATL9",
      "logical_operation": "all"
    }
  }
]
```


**Improvements**

1. Testcase  - This has the highest priority. Testcases are missing becasue of shortage of time
2. Rules generator UI - This would help in generating rules on the fly. 


