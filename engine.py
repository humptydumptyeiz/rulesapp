from rules.operators import StringOperator, NumericOperator, DateTimeOperator


value_type_operator_mapping = {
    'String': StringOperator,
    'Integer': NumericOperator,
    'Datetime': DateTimeOperator
}


def run_all(rule_list,
            data):

    for rule in rule_list:
        result = run(rule, data)
        if result:
            print data


def run(rule, data):
    rule_fails = check_condition(rule['condition'], data)
    if rule_fails:
        return True
    return False


def check_condition(condition, data):
    operations = condition['operations']
    if data['signal'] == condition['signal_id']:
        results = []
        for operation in operations:
            operator = _get_operator(operation['name'], data['value_type'], data['value'])
            if operator:
                results.append(not _do_operator_comparison(operator, operation['name'], operation.get('comparison_value', '')))
            else:
                results.append(False)
        results = any(results)
        return not results if condition['logical_operation'] is 'all' else results
    else:
        return False


def _get_operator(operation, value_type, value):
    operator = value_type_operator_mapping.get(value_type)
    return operator(value) if (operator and hasattr(operator, operation)) else False


def _do_operator_comparison(operator, operation, comparison_value):
    try:
        result = getattr(operator, operation)(comparison_value)
    except Exception as e:
        print 'Exception ', e.message
        return True
    else:
        return result


if __name__ == '__main__':
    import argparse
    import json
    import sys

    def start_engine(rules, data, **kwargs):
        rules_file = rules[0]
        data_file = data[0]
        with open(rules_file, 'r') as f:
            try:
              rule_list = json.loads(f.read())
            except:
                sys.exit(-1)
        with open(data_file, 'r') as f:
            try:
                data = json.loads(f.read())
            except:
                sys.exit(-1)
        for datum in data:
            run_all(rule_list, datum)

    options = argparse.ArgumentParser()
    options.set_defaults(method = start_engine)
    options.add_argument('--rules', nargs=1, help='json file of rules')
    options.add_argument('--data', nargs=1, help='data file')
    arguments = options.parse_args()
    arguments.method(**vars(arguments))
