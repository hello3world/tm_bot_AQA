questions = {
    'Selenium Basics': [
        {
            'question': 'What is Selenium?',
            'options': [
                'A library for working with APIs',
                'A tool for automating web browsers',
                'A programming language',
                'A framework for web application development'
            ],
            'correct': 'A tool for automating web browsers'
        },
        {
            'question': 'Which method is used to open a new browser window in Selenium WebDriver?',
            'options': [
                'driver.get()',
                'driver.open()',
                'driver.start()',
                'driver.launch()'
            ],
            'correct': 'driver.get()'
        }
    ],
    'Working with Elements': [
        {
            'question': 'How to find an element on the page by its id?',
            'options': [
                "find_element(By.XPATH, '//input[@name=\"username\"]')",
                "find_element(By.XPATH, '//*[@id=\"element_id\"]')",
                "find_element(By.XPATH, '//button[text()=\"Submit\"]')",
                "find_elements(By.XPATH, '//tagname[@attribute=\"value\"]')"
            ],
            'correct': "find_element(By.XPATH, '//*[@id=\"element_id\"]')"
        },
        {
            'question': 'Which method is used to enter text into a text field?',
            'options': [
                'element.enter_text()',
                'element.set_text()',
                'element.send_keys()',
                'element.type_text()'
            ],
            'correct': 'element.send_keys()'
        }
    ],
    'Waits': [
        {
            'question': 'What is WebDriverWait in Selenium?',
            'options': [
                'A method to set the test execution time',
                'A class to implement explicit waits',
                'An interface for configuring the browser',
                'A function to find elements'
            ],
            'correct': 'A class to implement explicit waits'
        },
        {
            'question': 'Which method is used to wait for an element to appear on the page?',
            'options': [
                'WebDriverWait.until()',
                'WebDriverWait.wait_for_element()',
                'WebDriverWait.element_appear()',
                'WebDriverWait.wait()'
            ],
            'correct': 'WebDriverWait.until()'
        }
    ],
    'Navigation': [
        {
            'question': 'Which method is used to navigate back in the browser history?',
            'options': [
                'driver.back()',
                'driver.previous()',
                'driver.navigate_back()',
                'driver.history_back()'
            ],
            'correct': 'driver.back()'
        },
        {
            'question': 'Which method is used to refresh the current page?',
            'options': [
                'driver.refresh()',
                'driver.reload()',
                'driver.update()',
                'driver.renew()'
            ],
            'correct': 'driver.refresh()'
        }
    ],
    'Frames and Windows': [
        {
            'question': 'How to switch to a frame by its name?',
            'options': [
                'driver.switch_to.frame()',
                'driver.switch_to_frame_by_name()',
                'driver.change_frame()',
                'driver.set_frame()'
            ],
            'correct': 'driver.switch_to.frame()'
        },
        {
            'question': 'How to close the current browser window?',
            'options': [
                'driver.close()',
                'driver.quit()',
                'driver.exit()',
                'driver.terminate()'
            ],
            'correct': 'driver.close()'
        }
    ]
}