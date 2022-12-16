import pytest
import json
import logging
import os
import joblib
from prediction_service.prediction import form_response, api_response
import prediction_service


input_data = {
    "incorrect_range":
    {"PM2.5": 1000,
     "PM10": 1500,
     "NO": 450,
     "NO2": 400,
     "NOx": 520,
     "NH3": 400,
     "CO": 200,
     "SO2": 200,
     "O3": 330,
     "Benzene": 500,
     "Toluene": 500,
     "Xylene": 315
     },

    "correct_range":
    {"PM2.5": 500,
     "PM10": 500,
     "NO": 250,
     "NO2": 200,
     "NOx": 320,
     "NH3": 100,
     "CO": 100,
     "SO2": 150,
     "O3": 230,
     "Benzene": 300,
     "Toluene": 300,
     "Xylene": 115
     },

    "incorrect_col":
    {"PM25": 800,
     "PM10": 500,
     "NO": 250,
     "NO2": 200,
     "NOx": 320,
     "NH3": 100,
     "CO": 100,
     "So2": 150,
     "O3": 230,
     "Benzene": 300,
     "Toluene": 300,
     "Xylene":115
     }
}

TARGET_range = {
    "min": 13.0,
    "max": 2049.0
}


def test_form_response_correct_range(data=input_data["correct_range"]):
    res = form_response(data)
    assert TARGET_range["min"] <= res <= TARGET_range["max"]


def test_api_response_correct_range(data=input_data["correct_range"]):
    res = api_response(data)
    assert TARGET_range["min"] <= res["response"] <= TARGET_range["max"]


def test_form_response_incorrect_range(data=input_data["incorrect_range"]):
    with pytest.raises(prediction_service.prediction.NotInRange):
        res = form_response(data)


def test_api_response_incorrect_range(data=input_data["incorrect_range"]):
    res = api_response(data)
    assert res["response"] == prediction_service.prediction.NotInRange().message


def test_api_response_incorrect_col(data=input_data["incorrect_col"]):
    res = api_response(data)
    assert res["response"] == prediction_service.prediction.NotInCols().message
