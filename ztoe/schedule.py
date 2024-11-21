from bs4 import BeautifulSoup
import roman
import logging
import functools
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

UPDATE_TIME_PLACEHOLDER = "Дата оновлення інформації"

def isElectricityPlanned(value: str) -> bool:
    """
    Check if electricity is planned based on the color value.

    Args:
        value (str): The color value in hex format.

    Returns:
        bool: True if electricity is planned, False otherwise.
    """
    return value == "#ffffff"

def load_data(func):
    """
    Decorator to load data if the schedule is empty.

    Args:
        func (function): The function to wrap.

    Returns:
        function: The wrapped function.
    """
    @functools.wraps(func)
    async def wrapper_checkcache(self, *args, **kwargs):
        if len(self._schedule) == 0:
            if len(await self.get_all()) == 0:
                return []
        value = await func(self, *args, **kwargs)
        return value

    return wrapper_checkcache

class Schedule:
    """
    Class to represent and process the schedule from HTML.

    Attributes:
        _html (Optional[BeautifulSoup]): Parsed HTML content.
        _schedule (List[Dict[str, Any]]): List of schedule data.
    """
    _html: Optional[BeautifulSoup] = None
    _schedule: List[Dict[str, Any]] = []

    def __init__(self, html: str):
        """
        Initialize the Schedule with HTML content.

        Args:
            html (str): The HTML content as a string.
        """
        self._html = BeautifulSoup(html, 'html.parser')

    async def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all schedule data from the HTML.

        Returns:
            List[Dict[str, Any]]: List of schedule data.
        """
        if self._html is None:
            return []

        tables = self._html.find_all('table', attrs={'style': "border-collapse: collapse;table-layout:fixed;width:810pt"})
        if not tables:
            logger.error("No tables found in the HTML")
            return []

        all_data = []
        for table in tables:
            table_data = self._process_table(table)
            all_data.extend(table_data)

        self._schedule = all_data
        return self._schedule

    @staticmethod
    def _process_table(self, table) -> List[Dict[str, Any]]:
        """
        Process a single table to extract schedule data.

        Args:
            table: The table element to process.

        Returns:
            List[Dict[str, Any]]: List of schedule data from the table.
        """
        first_row_values = []

        rows = table.find_all('tr')[1:]
        if not rows:
            logger.error("No rows found in the table")
            return []

        cells = rows[0].find_all(['td', 'th'])
        for cell in cells:
            text = cell.get_text(strip=True)
            if text:
                first_row_values.append(text)

        logger.debug(first_row_values)

        sector = 1
        queue = 1
        time_cell = 0
        table_data = []

        for row in rows[1:]:
            row_data = {}
            cells = row.find_all(['td', 'th'])

            for cell in cells:
                text = cell.get_text(strip=True)
                style = cell.get('style', '')
                color = None

                if 'background' in style:
                    color = style.split('background:')[-1].split(';')[0].strip()

                if text or color is None:
                    if text.strip().isdecimal():
                        sector = int(text)
                    elif text.strip().isalpha():
                        try:
                            queue = roman.fromRoman(text.strip())
                            time_cell = 0
                        except roman.InvalidRomanNumeralError as e:
                            logger.error('Error converting Roman numeral', exc_info=e)
                            return []
                else:
                    row_data[time_cell] = {'time': first_row_values[time_cell], 'electricity': isElectricityPlanned(color)}
                    logger.debug(f"Adding value for sector={sector} queue={queue} time={first_row_values[time_cell]} electricity={isElectricityPlanned(color)}")
                    time_cell += 1

            logger.debug(f"Adding data for sector={sector} and queue={queue}, data={row_data}")
            table_data.append({"sector": sector, "queue": queue, "data": row_data})

        return table_data

    @load_data
    async def get_queue(self, queue: int) -> List[Dict[str, Any]]:
        """
        Get schedule data for a specific queue.

        Args:
            queue (int): The queue number.

        Returns:
            List[Dict[str, Any]]: List of schedule data for the queue.
        """
        return [i for i in self._schedule if i["queue"] == queue]

    @load_data
    async def get_sector(self, sector: int) -> List[Dict[str, Any]]:
        """
        Get schedule data for a specific sector.

        Args:
            sector (int): The sector number.

        Returns:
            List[Dict[str, Any]]: List of schedule data for the sector.
        """
        return [i for i in self._schedule if i["sector"] == sector]