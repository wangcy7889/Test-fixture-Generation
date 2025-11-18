import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def init_driver(headless=True, proxy=None, show_images=False, option=None):
    chromedriver_path = chromedriver_autoinstaller.install()
    options = Options()
    if headless is True:
        print('Scraping on headless mode.')
        options.add_argument('--disable-gpu')
        options.headless = True
    else:
        options.headless = False
    options.add_argument('log-level=3')
    if proxy is not None:
        options.add_argument('--proxy-server=%s' % proxy)
        print('using proxy : ', proxy)
    if show_images == False:
        prefs = {'profile.managed_default_content_settings.images': 2}
        options.add_experimental_option('prefs', prefs)
    if option is not None:
        options.add_argument(option)
    driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
    driver.set_page_load_timeout(100)
    return driver