import pytest
from project import get_city, get_url, format_day, format_temp, format_weather


def test_get_city():
    assert get_city("107.164.65.255") == "Madrid"
    assert get_city("91.117.127.34") == "Porrino"
    assert get_city("195.235.204.40") == "Aljaraque"

    with pytest.raises(SystemExit):
        get_city("cat") == "Aljaraque"
    with pytest.raises(SystemExit):
        get_city("91.117") == "Aljaraque"
    with pytest.raises(SystemExit):
        get_city("elephant") == "Aljaraque"


def test_get_url():
    assert get_url("marbella") == "https://www.tiempo.com/marbella.htm"
    assert get_url("Marbella") == "https://www.tiempo.com/marbella.htm"
    assert get_url("madrid") == "https://www.tiempo.com/madrid.htm"
    assert get_url("Madrid") == "https://www.tiempo.com/madrid.htm"


def test_format_day():
    assert format_day("8 Ago") == "08/08"
    assert format_day("10 Ene") == "01/10"
    assert format_day("25 Dic") == "12/25"


def test_format_weather():
    assert format_weather("Niebla") == "🌫️"
    assert format_weather("Cielos nubosos") == "🌤️"
    assert format_weather("Cielos despejados") == "☀️"

    assert format_weather("Abracadabra") == None
    assert format_weather("9") == None
    assert format_weather("Cat") == None
