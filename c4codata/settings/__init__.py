import os
from settings.config import Demo

env = os.environ['C4C_ODATA_ENV']

if env == 'DEMO':
    auto_config = Demo
else:
    raise ValueError(f"Environment variable {env} should be specified. Available value: DEMO")
