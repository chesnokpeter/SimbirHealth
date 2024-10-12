.PHONY: account hospital timetable, document

account: 
	uvicorn account.app:app --reload --port 8011

hospital:
	uvicorn hospital.app:app --reload --port 8021

timetable:
	uvicorn timetable.app:app --reload --port 8031

document:
	uvicorn document.app:app --reload --port 8041
