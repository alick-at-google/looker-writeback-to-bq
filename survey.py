from google.cloud import bigquery
from datetime import date
import json


def patient_survey(request):
    client = bigquery.Client.from_service_account_json(
        'sandbox-trials-demo-cmanage.json')
    request_json = request.get_json(silent=True)

    ease_of_scheduling_appointment = request_json["form_params"]["Ease Of Scheduling Appointment"]
    wait_time_for_appointment = request_json["form_params"]["Wait Time For Appointment"]
    cleanliness_and_appearance_of_facility = request_json[
        "form_params"]["Cleanliness And Appearance Of Facility"]
    overall_care_rating = request_json["form_params"]["Overall Care Rating"]
    likelihood_of_recommendation = request_json["form_params"]["Likelihood Of Recommendation"]
    # insert record into sql table
    sql_string = f"""
        INSERT INTO
        looker-private-demo.healthcare_demo_live.patient_survey(
            ease_of_scheduling_appointment,
            wait_time_for_appointment,
            cleanliness_and_appearance_of_facility,
            overall_care_rating,
            likelihood_of_recommendation
        )
        VALUES (
            '{ease_of_scheduling_appointment}',
            '{wait_time_for_appointment}',
            '{cleanliness_and_appearance_of_facility}',
            '{overall_care_rating}',
            '{likelihood_of_recommendation}'
        )
        """
    query_job = client.query(sql_string)
    results = query_job.result()

    return (json.dumps({
        "looker": {
            "success": True,
            "refresh_query": True
        }
    }), 200)
