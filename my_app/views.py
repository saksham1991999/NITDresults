from django.shortcuts import render
from selenium.webdriver.firefox.options import Options
options = Options()
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')
from selenium import webdriver
import lxml.html
import time
driver = webdriver.Firefox(executable_path=r'/home/rahul/Desktop/project/nitdresults/geckodriver', firefox_options=options)

# Create your views here.

url = "https://erp.nitdelhi.ac.in/CampusLynxNITD/studentonindex.jsp"

def get_data(roll_no, sem):
    driver.get(url)
    iframe = driver.find_elements_by_tag_name('iframe')[0]
    driver.switch_to.frame(iframe)
    rollno = driver.find_element_by_id("studentrollno")
    rollno.send_keys(roll_no)
    captchatext = driver.find_element_by_id("ebcaptchatext")
    captchafiller = captchatext.text
    captcha = driver.find_element_by_id("ebcaptchainput")
    captcha.send_keys(captchafiller)
    submit_button = driver.find_elements_by_id('cbutton')[0]
    submit_button.click()
    #print("Reached initial")
    time.sleep(1)
    try:
        driver.find_element_by_class_name("tdcolor").click()
        time.sleep(1)
        #print("Reached final page")
        root = lxml.html.fromstring(driver.page_source)
        values = root.xpath('.//tbody[@id="examgradeid"]//td')
        #print(values)
        sem -= 1
        table_count = sem*5+2
        #print(table_count)
        sgpa = values[table_count].text_content()
        cgpa = values[table_count+1].text_content()
        stud_detail = root.xpath('.//span[@id="snamedetail"]')
        start_name = 15
        end_name = stud_detail[0].text_content().find('\xa0')
        student_name = stud_detail[0].text_content()[start_name:end_name]
        start_rollno = 21 + end_name
        end_rollno = start_rollno + 9
        student_rollno = stud_detail[0].text_content()[start_rollno:end_rollno]
        data = tuple(list([student_rollno, student_name, sgpa, cgpa]))
    except:
        data = -1
        #print("Oops!", sys.exc_info()[0], "occured.")

    return data



def home(request):
    return render(request, 'home.html')


def search(request):
    branch = request.POST['branch']
    year = request.POST['year']
    sem = request.POST['sem']
    sem = int(sem)
    #print(branch, sem, year)
    rollno = ""

    if year == "1":
        rollno = "19"
    elif year == "2":
        rollno = "18"
    elif year == "3":
        rollno = "17"
    elif year == "4":
        rollno = "16"

    if branch == "cse":
        rollno += "121"
    elif branch == "ece":
        rollno += "122"
    elif branch == "eee":
        rollno += "123"

    rollno += "0001"
    rollno = int(rollno)

    table_data = []

    except_count = 0
    for i in range(100):
        temp = str(rollno+i)
        data = get_data(temp, sem)
        print(rollno+i, data)
        if data == -1:
            except_count += 1
            if except_count>5:
                break
            continue
        else:
            except_count = 0
            table_data.append(data)

    if len(table_data)==0:
        return render(request, 'home.html')

    return render(request, 'my_app/my_app.html', {
        'table_data': table_data,
    })

def search_by_rollno(request):
    return render(request, 'my_app/search_by_rollno.html')

def parse_search_rollno(request):
    rollno = request.POST['rollno']
    #print(rollno)
    sem = request.POST['sem']
    sem = int(sem)
    table_data = []
    data = get_data(rollno, sem)
    if data == -1:
        return render(request, 'my_app/search_by_rollno.html')
    #print(data)
    table_data.append(data)
    return render(request, 'my_app/my_app.html', {
        'table_data': table_data,
    })
