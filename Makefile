.PHONY: account hospital timetable

account: 
	uvicorn account.app:app --reload --port 8011

hospital:
	uvicorn hospital.app:app --reload --port 8021

timetable:
	uvicorn timetable.app:app --reload --port 8031
