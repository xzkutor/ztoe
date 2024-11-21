import pytest
from bs4 import BeautifulSoup
from ztoe.schedule import Schedule, isElectricityPlanned

@pytest.fixture
def sample_html():
    return """
    <html>
    <body>
        <table style="border-collapse: collapse;table-layout:fixed;width:810pt">
            <tr><td>01.01.2023</td></tr>
            <tr><th>Time</th><th>Sector</th><th>Queue</th></tr>
            <tr><td>08:00</td><td>1</td><td>I</td></tr>
            <tr><td>09:00</td><td>2</td><td>II</td></tr>
        </table>
    </body>
    </html>
    """

@pytest.mark.asyncio
async def schedule_initialization(sample_html):
    schedule = Schedule(sample_html)
    assert schedule._html is not None
    assert isinstance(schedule._html, BeautifulSoup)

@pytest.mark.asyncio
async def get_all_schedules(sample_html):
    schedule = Schedule(sample_html)
    all_data = await schedule.get_all()
    assert len(all_data) == 2
    assert all_data[0]["sector"] == 1
    assert all_data[1]["queue"] == 2

@pytest.mark.asyncio
async def get_queue_data(sample_html):
    schedule = Schedule(sample_html)
    await schedule.get_all()
    queue_data = await schedule.get_queue(1)
    assert len(queue_data) == 1
    assert queue_data[0]["queue"] == 1

@pytest.mark.asyncio
async def get_sector_data(sample_html):
    schedule = Schedule(sample_html)
    await schedule.get_all()
    sector_data = await schedule.get_sector(2)
    assert len(sector_data) == 1
    assert sector_data[0]["sector"] == 2

def electricity_planned():
    assert isElectricityPlanned("#ffffff") is True
    assert isElectricityPlanned("#000000") is False