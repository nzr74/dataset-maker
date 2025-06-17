import pytest
from unittest.mock import patch, MagicMock
from websites.bama import Bama


# @patch("websites.bama.BeautifulSoup")
# def test_extract_car_data_success(mock_bs, mock_extract, mock_savedata):
#     # Setup mocks
#     mock_instance = mock_extract.return_value
#     mock_instance.get_urls.return_value = ["url1"]
#     mock_instance.get_data.return_value = "<html></html>"

#     # Mock BeautifulSoup and its find/find_all
#     mock_soup = MagicMock()
#     mock_bs.return_value = mock_soup
#     mock_soup.find.side_effect = [
#         MagicMock(text="1,000,000"),  # price
#         MagicMock(text="برند، مدل"),  # brand_and_type
#         None,  # for car_details div, will be handled below
#     ]
#     # For .find_all and .find().find_all
#     mock_soup.find_all.side_effect = [
#         [MagicMock(text="1400"), MagicMock(text="مدل")],  # type_and_year
#     ]
#     car_details_mock = MagicMock()
#     car_details_mock.find_all.return_value = [
#         MagicMock(text="10,000km"),
#         MagicMock(text="بنزین"),
#         MagicMock(text="اتوماتیک"),
#         MagicMock(text="سالم"),
#         MagicMock(text="سفید"),
#     ]

#     # Patch the third .find to return car_details_mock
#     def find_side_effect(*args, **kwargs):
#         if args[1] == "bama-vehicle-detail-with-icon":
#             return car_details_mock
#         return MagicMock(text="dummy")

#     mock_soup.find.side_effect = find_side_effect

#     bama = Bama("car", missing_value="N/A")
#     save_instance = mock_savedata.return_value

#     bama.extract_car_data()

#     save_instance.save_data.assert_called()
#     assert save_instance.save_data.call_args[1]["missing_value"] == "N/A"
#     assert save_instance.save_data.call_args[1]["site"] == "bama"


# @patch("websites.bama.BeautifulSoup")
# def test_extract_car_data_handles_exceptions(
#     mock_bs, mock_extract, mock_savedata, capsys
# ):
#     # Setup mocks to raise AttributeError
#     mock_instance = mock_extract.return_value
#     mock_instance.get_urls.return_value = ["url1"]
#     mock_instance.get_data.return_value = "<html></html>"
#     mock_bs.return_value.find.side_effect = AttributeError

#     bama = Bama("car", missing_value="N/A")
#     bama.extract_car_data()
#     captured = capsys.readouterr()
#     assert "error" in captured.out


#############################################


import pytest
from unittest.mock import patch, MagicMock
from websites.bama import Bama


@pytest.fixture
def divar_instance():
    return Bama("car", missing_value="N/A")


def test_init_valid_category():
    d = Bama("car", missing_value="N/A")
    assert d.category == "car"
    assert d.missing_value == "N/A"


def test_init_invalid_category():
    with pytest.raises(Exception):
        Bama("invalid", missing_value="N/A")


@patch("websites.bama.Extract")
def test_extract_page_urls(mock_extract, divar_instance):
    mock_instance = mock_extract.return_value
    mock_instance.get_urls.return_value = ["url1", "url2"]
    urls = divar_instance.extract_page_urls()
    assert urls == ["url1", "url2"]
    mock_extract.assert_called_once()
    mock_instance.get_urls.assert_called_once()


@patch("websites.bama.util.Savedata")
@patch("websites.bama.Extract")
@patch("websites.bama.BeautifulSoup")
def test_extract_car_data_handles_exceptions(
    mock_bs, mock_extract, mock_savedata, divar_instance
):
    divar_instance.extract_page_urls = MagicMock(return_value=["url1"])
    # Simulate get_data raising an exception
    mock_extract.return_value.get_data.side_effect = ValueError("fail")
    divar_instance.extract_car_data()  # Should not raise


def test_categories_dict():
    assert "car" in Bama.categories
    assert isinstance(Bama.categories["car"], str)


@pytest.fixture
def divar_instance():
    return Bama("car", missing_value="N/A")


@patch("websites.bama.util.Savedata")
@patch("websites.bama.Extract")
@patch("websites.bama.BeautifulSoup")
def test_extract_car_data_happy_path(
    mock_bs, mock_extract, mock_savedata, divar_instance, capsys
):
    # Mock URLs
    divar_instance.extract_page_urls = MagicMock(return_value=["url1"])
    # Mock Extract.get_data
    mock_extract.return_value.get_data.return_value = "<html></html>"
    # Mock BeautifulSoup and its find_all
    mock_soup = MagicMock()
    mock_bs.return_value = mock_soup

    # Mock car_brand, mileage_year_color, car_details, car_condition
    car_brand = [
        MagicMock(text="brand0"),
        MagicMock(text="brand1"),
        MagicMock(text="brand2"),
        MagicMock(text="BrandName"),
    ]
    mileage_year_color = [
        MagicMock(text="10000"),
        MagicMock(text="2020"),
        MagicMock(text="Red"),
    ]

    # car_details: one with "برند و تیپ", one with "نوع سوخت", one with "گیربکس", one with "مهلت بیمهٔ شخص ثالث", one with "قیمت پایه"
    def make_detail(title, value):
        detail = MagicMock()
        detail.find.side_effect = lambda tag, class_: MagicMock(
            text=title if tag == "p" else value
        )
        return detail

    car_details = [
        make_detail("برند و تیپ", "TypeNameBrandName"),
        make_detail("نوع سوخت", "Gasoline"),
        make_detail("گیربکس", "Automatic"),
        make_detail("مهلت بیمهٔ شخص ثالث", "6 months"),
        make_detail("قیمت پایه", "1٬000٬000تومان"),
    ]

    # car_condition: one with "موتور", one with "شاسی جلو", one with "شاسی عقب", one with "وضعیت شاسی‌ها", one with "بدنه"
    def make_condition(title, value):
        condition = MagicMock()
        condition.find.side_effect = lambda tag, class_: MagicMock(
            text=title if tag == "p" else value
        )
        return condition

    car_condition = [
        make_condition("موتور", "Good"),
        make_condition("شاسی جلو", "OK"),
        make_condition("شاسی عقب", "OK"),
        make_condition("بدنه", "Clean"),
    ]
    # Setup find_all side_effect
    mock_soup.find_all.side_effect = [
        car_details,  # car_details
        car_condition,  # car_condition
        mileage_year_color,  # mileage_year_color
        car_brand,  # car_brand
    ]

    mock_save = mock_savedata.return_value
    divar_instance.extract_car_data()
    mock_save.save_data.assert_called_once()
    captured = capsys.readouterr()
    assert "done!!!!!!!!!" in captured.out


@patch("websites.bama.util.Savedata")
@patch("websites.bama.Extract")
@patch("websites.bama.BeautifulSoup")
def test_extract_car_data_handles_value_error(
    mock_bs, mock_extract, mock_savedata, divar_instance, capsys
):
    divar_instance.extract_page_urls = MagicMock(return_value=["url1"])
    mock_extract.return_value.get_data.side_effect = ValueError("fail")
    divar_instance.extract_car_data()
    mock_savedata.return_value.save_data.assert_not_called()
    captured = capsys.readouterr()
    assert "error" in captured.out


@patch("websites.bama.util.Savedata")
@patch("websites.bama.Extract")
@patch("websites.bama.BeautifulSoup")
def test_extract_car_data_handles_attribute_error(
    mock_bs, mock_extract, mock_savedata, divar_instance, capsys
):
    divar_instance.extract_page_urls = MagicMock(return_value=["url1"])
    mock_extract.return_value.get_data.return_value = "<html></html>"
    mock_bs.return_value.find_all.side_effect = AttributeError("fail")
    divar_instance.extract_car_data()
    mock_savedata.return_value.save_data.assert_not_called()
    captured = capsys.readouterr()
    assert "error" in captured.out


@patch("websites.bama.util.Savedata")
@patch("websites.bama.Extract")
@patch("websites.bama.BeautifulSoup")
def test_extract_car_data_handles_index_error(
    mock_bs, mock_extract, mock_savedata, divar_instance, capsys
):
    divar_instance.extract_page_urls = MagicMock(return_value=["url1"])
    mock_extract.return_value.get_data.return_value = "<html></html>"
    # Simulate car_brand list too short
    mock_soup = MagicMock()
    mock_bs.return_value = mock_soup
    mock_soup.find_all.side_effect = [
        [],  # car_details
        [],  # car_condition
        [],  # mileage_year_color
        [MagicMock(text="brand0")],  # car_brand (too short)
    ]
    divar_instance.extract_car_data()
    mock_savedata.return_value.save_data.assert_not_called()
    captured = capsys.readouterr()
    assert "error" in captured.out


@patch("websites.bama.util.Savedata")
@patch("websites.bama.Extract")
@patch("websites.bama.BeautifulSoup")
def test_extract_car_data_multiple_urls(
    mock_bs, mock_extract, mock_savedata, divar_instance
):
    divar_instance.extract_page_urls = MagicMock(return_value=["url1", "url2"])
    mock_extract.return_value.get_data.return_value = "<html></html>"
    mock_soup = MagicMock()
    mock_bs.return_value = mock_soup
    # Setup for two URLs
    car_brand = [
        MagicMock(text="brand0"),
        MagicMock(text="brand1"),
        MagicMock(text="brand2"),
        MagicMock(text="BrandName"),
    ]
    mileage_year_color = [
        MagicMock(text="10000"),
        MagicMock(text="2020"),
        MagicMock(text="Red"),
    ]

    def make_detail(title, value):
        detail = MagicMock()
        detail.find.side_effect = lambda tag, class_: MagicMock(
            text=title if tag == "p" else value
        )
        return detail

    car_details = [
        make_detail("برند و تیپ", "TypeNameBrandName"),
        make_detail("نوع سوخت", "Gasoline"),
        make_detail("گیربکس", "Automatic"),
        make_detail("مهلت بیمهٔ شخص ثالث", "6 months"),
        make_detail("قیمت پایه", "1٬000٬000تومان"),
    ]

    def make_condition(title, value):
        condition = MagicMock()
        condition.find.side_effect = lambda tag, class_: MagicMock(
            text=title if tag == "p" else value
        )
        return condition

    car_condition = [
        make_condition("موتور", "Good"),
        make_condition("شاسی جلو", "OK"),
        make_condition("شاسی عقب", "OK"),
        make_condition("بدنه", "Clean"),
    ]
    # Each call to find_all returns the same mock data
    mock_soup.find_all.side_effect = [
        car_details,
        car_condition,
        mileage_year_color,
        car_brand,  # url1
        car_details,
        car_condition,
        mileage_year_color,
        car_brand,  # url2
    ]
    mock_save = mock_savedata.return_value
    divar_instance.extract_car_data()
    assert mock_save.save_data.call_count == 2
