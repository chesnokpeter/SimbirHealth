.PHONY: account hospital

account: 
	uvicorn account.app:app --reload --port 8011

hospital:
	uvicorn hospital.app:app --reload --port 8021
