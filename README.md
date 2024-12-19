# ZTOE

A package for handling ZTOE schedules.

## Installation

To install the package, run the following command in your terminal:

```sh
pip install .
```
## Usage
### Basic Example
Here is a basic example of how to use the ztoe package to fetch and process schedule data:

```python
import asyncio
import aiohttp
from ztoe.client import Client
import logging

logger = logging.getLogger(__name__)

async def main():
    async with aiohttp.ClientSession() as session:
        client = Client(session)
        schedule = await (await client.get_schedule()).get_all()

        for item in schedule:
            print(f"queue={item['queue']} sub_queue={item['sub_queue']} schedule_data={item['data']}")

logging.basicConfig(level=logging.DEBUG)
asyncio.run(main())
```
### Running Tests
To run the tests, run the following command in your terminal:

```sh
python -m unittest
``` 
## Development
### Setting up the Development Environment
To set up the development environment, run the following command in your terminal:

```sh
pip install -r requirements.txt
pip install -e .
``` 
### Adding Dependencies
To add a new dependency, update the install_requires section in setup.py and run:

```sh
pip install .
```
## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Authors
- **[Andrii Mozharovsky](am@swordfish.name)**