from django.shortcuts import render
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
from selenium import webdriver
import lxml.html
import time
from .models import Student
driver = webdriver.Firefox(executable_path=r'/home/rahul/Desktop/project/nitdresults/geckodriver', firefox_options=options)

# Create your views here.

url = "https://erp.nitdelhi.ac.in/CampusLynxNITD/studentonindex.jsp"

def get_data(roll_no):
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
    time.sleep(2)
    try:
        driver.find_element_by_class_name("tdcolor").click()
        time.sleep(2)
        #print("Reached final page")
        root = lxml.html.fromstring(driver.page_source)
        values = root.xpath('.//tbody[@id="examgradeid"]//td')
        #print(values)

        #print(table_count)

        semesters = len(values) // 5;
        result = []
        for i in range(semesters):
            sgpa = values[5 * i + 2].text_content()
            cgpa = values[5 * i + 3].text_content()
            result.append(tuple([sgpa, cgpa]))

        stud_detail = root.xpath('.//span[@id="snamedetail"]')
        start_name = 15
        end_name = stud_detail[0].text_content().find('\xa0')
        student_name = stud_detail[0].text_content()[start_name:end_name]
        start_rollno = 21 + end_name
        end_rollno = start_rollno + 9
        student_rollno = stud_detail[0].text_content()[start_rollno:end_rollno]
        start_branch = end_rollno + 54
        end_branch = start_branch + 10
        branch = stud_detail[0].text_content()[start_branch:end_branch]
        print(branch[6])
        if branch[6] == 'e':
            student_branch = "CSE"
        elif branch[6] == 'i':
            student_branch = "EEE"
        else:
            student_branch = "ECE"

        data = tuple(list([student_rollno, student_name, student_branch, result]))
    except:
        data = -1

    return data



def home(request):
    return render(request, 'home.html')


def search(request):
    s_branch = request.POST['branch']
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

    """
    if branch == "cse":
        rollno += "121"
    elif branch == "ece":
        rollno += "122"
    elif branch == "eee":
        rollno += "123"
    """

    #rollno += "0001"
    rollno = int(rollno)
    table_data = []
    """
    

    except_count = 0
    for i in range(100):
        temp = str(rollno+i)
        data = get_data(temp)
        print(rollno+i, data)
        if data == -1:
            except_count += 1
            if except_count>5:
                break
            continue
        else:
            except_count = 0
            table_data.append(data)
            Student.objects.create(name=data[1], roll_no=data[0], branch=data[2], result=data[3])
    """
    sem -= 1
    data = Student.objects.filter(roll_no__startswith=rollno, branch=s_branch.upper())
    print(len(data))
    for i in data:
        try:
            table_data.append([i.roll_no, i.name, i.result[sem][0], i.result[sem][1]])
        except:
            pass


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
    rollno = int(rollno)
    sem = request.POST['sem']
    sem = int(sem)
    table_data = []
    sem -= 1
    try:
        data = Student.objects.get(roll_no=rollno)
        final_data = tuple([data.roll_no, data.name, data.result[sem][0], data.result[sem][1]])
        #print(final_data)
    except:
        return render(request, 'my_app/search_by_rollno.html')
    #print(data)
    table_data.append(final_data)
    return render(request, 'my_app/my_app.html', {
        'table_data': table_data,
    })
