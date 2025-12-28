from selenium.webdriver.common.by import By

AD_BANNER_CLASSNAME = ('ad-banner-container', '__ad')

def __parse_employee__(self, employee_raw):

        try:
            # print()
            employee_object = {}
            employee_object['name'] = (employee_raw.text.split("\n") or [""])[0].strip()
            employee_object['designation'] = (employee_raw.text.split("\n") or [""])[3].strip()
            employee_object['linkedin_url'] = employee_raw.find_element(By.TAG_NAME, "a").get_attribute("href")
            # print(employee_raw.text, employee_object)
            # _person = Person(
            #     # linkedin_url = employee_raw.find_element_by_tag_name("a").get_attribute("href"),
            #     linkedin_url = employee_raw.find_element_by_tag_name("a").get_attribute("href"),
            #     name = (employee_raw.text.split("\n") or [""])[0].strip(),
            #     driver = self.driver,
            #     get = True,
            #     scrape = False,
            #     designation = (employee_raw.text.split("\n") or [""])[3].strip()
            #     )
            # print(_person, employee_object)
            # return _person
            return employee_object
        except Exception as e:
            # print(e)
            return None
