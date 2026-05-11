# Problem 3 Support Code

This repository contains the runnable Python support code for Problem 3.

## Run the Python Tests

```bash
cd problem3/python
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest
```

The tests cover Python integer parsing and the translated paragraph-detecting token reader.
