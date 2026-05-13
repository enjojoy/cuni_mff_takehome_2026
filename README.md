# Take-Home Support Code

This repository contains support files for the take-home assignment.

The copyable YAML automaton definition for Problem 1 is in `problem1/automaton_l1.yaml`.

## Run the Python Tests

```bash
cd problem3/python
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest
```

The tests cover Python integer parsing and the translated paragraph-detecting token reader.
