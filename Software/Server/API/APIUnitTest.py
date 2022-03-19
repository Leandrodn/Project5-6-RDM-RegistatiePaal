import requests
import unittest
import json

API_URL = 'http://81.169.254.222'

REGISTER_URL = "{}/register".format(API_URL)
RETRIEVE_URL = "{}/retrieve".format(REGISTER_URL)
ADMIN_URL = "{}/admin".format(API_URL)
ADD_STUDENT_URL = "{}/addstudent".format(ADMIN_URL)
ADD_COURSE_URL = "{}/addcourse".format(ADMIN_URL)
ADD_INSTITUTE_URL = "{}/addinstitute".format(ADMIN_URL)

# testen van het registreren
class RegistrationTest(unittest.TestCase):
    def test_normal_registration(self):
        response = requests.post(REGISTER_URL, json={'stnum':'1003152','method':'QR-code','workshop':'Metaalwerkplaats'})
        response_data = response.status_code
        self.assertEqual(response_data, 201)
    def test_wrong_studentnumber_registration(self):
        response = requests.post(REGISTER_URL, json={'stnum':'1000000','method':'QR-code','workshop':'Metaalwerkplaats'})
        response_data = response.status_code
        self.assertEqual(response_data, 400)
    def test_wrong_method_registration(self):
        response = requests.post(REGISTER_URL, json={'stnum':'1003152','method':'RFID','workshop':'Metaalwerkplaats'})
        response_data = response.status_code
        self.assertEqual(response_data, 400)
    def test_wrong_workshop_registration(self):
        response = requests.post(REGISTER_URL, json={'stnum':'1003152','method':'QR-code','workshop': 'Kartonwerkplaats'})
        response_data = response.status_code
        self.assertEqual(response_data, 400)

# testen van data ophalen
class RetrieveTest(unittest.TestCase):
    def test_normal_retrieval(self):
        response = requests.get(RETRIEVE_URL)
        response_data = response.status_code
        self.assertEqual(response_data, 200)
    def test_abnormal_retrieval(self): # de api hoort alle json data te negeren
        response = requests.get(RETRIEVE_URL, json={'retrieve':'True'})
        response_data = response.status_code
        self.assertEqual(response_data, 200)

# testen toevoegen Student
class AddstudentTest(unittest.TestCase):
    def test_normal_addstudent(self):
        response = requests.post(ADD_STUDENT_URL, json={"stnum":"1078521","name":"Sjoerd", "shorti":"CMI", "sname": "TI"})
        response_data = response.status_code
        self.assertEqual(response_data, 201)
    def test_duplicate_studentnumber_addstudent(self):
        response = requests.post(ADD_STUDENT_URL, json={"stnum":"1078521","name":"Sjoerd","shorti":"CMI","sname":"TI"})
        response_data = response.status_code
        self.assertEqual(response_data, 400)
    def test_wrong_institute_addstudent(self):
        response = requests.post(ADD_STUDENT_URL, json={"stnum":"1078521","name":"Sjoerd","shorti":"ARRR","sname":"TI"})
        response_data = response.status_code
        self.assertEqual(response_data, 400)
    def test_wrong_course_addstudent(self):
        response = requests.post(ADD_STUDENT_URL, json={"stnum":"1078521","name":"Sjoerd","shorti":"CMI","sname":"BOE"})
        response_data = response.status_code
        self.assertEqual(response_data, 400)

# testen toevoegen Instituut
class AddinstituteTest(unittest.TestCase):
    def test_normal_addinstitute(self):
        response = requests.post(ADD_INSTITUTE_URL, json={"shorti":"WdK", "longi":"Willem de Kooning Academy"})
        response_data = response.status_code
        self.assertEqual(response_data, 201)
    def test_wrong_shortname_addinstitute(self):
        response = requests.post(ADD_INSTITUTE_URL, json={"shorti":"WdKaaaa", "longi":"Willem de Kooning Academy"})
        response_data = response.status_code
        self.assertEqual(response_data, 400)

# testen toevoegen Course
class AddcourseTest(unittest.TestCase):
    def test_normal_addcourse(self):
        response = requests.post(ADD_COURSE_URL, json={"sname":"SW", "lname":"Social Work"})
        response_data = response.status_code
        self.assertEqual(response_data, 201)
    def test_wrong_shortname_addcourse(self):
        response = requests.post(ADD_COURSE_URL, json={"sname":"SocialW", "lname":"Social Work"})
        response_data = response.status_code
        self.assertEqual(response_data, 400)

if __name__ =='__main__':
    unittest.main()
