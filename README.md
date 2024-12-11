## To-Do List

### Environment Setup
- [ ] Install Python 3.8 or higher.
- [ ] Set up a virtual environment using `venv` or `conda`.
- [ ] Install Playwright with `pip install playwright` and run `playwright install` to install browser binaries.


### Code Development
- [ ] Implement `init_browser()` in `utils/browser.py` for initializing Playwright browser instances.
- [ ] Create `load_applicant_data()` in `utils/yaml_loader.py` for reading applicant data from YAML.
- [ ] Develop handlers for each job platform (lever.py, workable.py, etc.) in the handlers directory.
- [ ] Write main application logic in `main.py` to orchestrate reading URLs, loading data, and calling handlers.

### Data Management
- [ ] Prepare a YAML file for storing applicant data securely.
- [ ] Set up an Excel file or other data source for job URLs.
- [ ] Implement data parsing and error handling for input data sources.

### Selector Strategy
- [ ] Identify and test CSS selectors, XPath, or text selectors for each target job application platform.
- [ ] Implement robust and dynamic selector handling to manage variations and updates in web forms.

### Testing and Validation
- [ ] Write unit tests for each functional component (handlers, data loaders, browser management).
- [ ] Conduct dry runs with test data to ensure scripts perform actions correctly without actual form submissions.

### Error Handling and Logging
- [ ] Develop comprehensive error handling strategies to manage timeouts, incorrect data, and navigation errors.
- [ ] Implement logging for tracking script execution, successes, and points of failure.
