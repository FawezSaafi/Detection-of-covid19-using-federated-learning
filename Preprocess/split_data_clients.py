import argparse
import os
import shutil
parser = argparse.ArgumentParser(description='Test.')
parser.add_argument('--input', action='store', type=str, help='input path')
parser.add_argument('--output', action='store', type=str, help='output path')
parser.add_argument('--cl1Id', action='store', type=str, help='client id ')
parser.add_argument('--cl2Id', action='store', type=str, help='client id ')
parser.add_argument('--cl3Id', action='store', type=str, help='client id ')
parser.add_argument('--cl4Id', action='store', type=str, help='client id ')
parser.add_argument('--fraction1', action='store', type=float, help='fraction of the client id ')
parser.add_argument('--fraction2', action='store', type=float, help='fraction of the client id ')
parser.add_argument('--fraction3', action='store', type=float, help='fraction of the client id ')
parser.add_argument('--fraction4', action='store', type=float, help='fraction of the client id ')
args = parser.parse_args()
input_path, output_path,cl_id1,cl_id2,cl_id3,cl_id4, fraction1, fraction2, fraction3, fraction4 =vars(args)['input'],vars(args)['output'],vars(args)['cl1Id'],vars(args)['cl2Id'],vars(args)['cl3Id'],vars(args)['cl4Id'],vars(args)['fraction1'],vars(args)['fraction2'],vars(args)['fraction3'],vars(args)['fraction4']


parser.add_argument('--port', action='store', type=int, help='client port')

def distribute(input_path, output_path,cl_id1,cl_id2,cl_id3,cl_id4,client1, client2, client3, client4):
    covid = []
    normal = []
    for filename in os.listdir(input_path + "//covid"):
        covid.append(filename)
    for filename in os.listdir(input_path + "//normal"):
        normal.append(filename)
    covid_img = dict()
    covid_img["client1"] = round(len(covid) * client1)
    covid_img["client2"] = round(len(covid) * client2)
    covid_img["client3"] = round(len(covid) * client3)
    covid_img["client4"] = round(len(covid) * client4)
    print(covid_img)
    normal_img = dict()
    normal_img["client1"] = round(len(normal) * client1)
    normal_img["client2"] = round(len(normal) * client2)
    normal_img["client3"] = round(len(normal) * client3)
    normal_img["client4"] = round(len(normal) * client4)
    print(normal_img)

    s = 0
    i=0

    for filename in normal:
        i=i+1
        print(i)
        if i <= normal_img["client1"] :
            shutil.copy(input_path + "//normal//" + filename, output_path + "//"+cl_id1+"//normal//" + filename)
            s=s+1
            #print("client 1 in process")
        elif i> s and i<= normal_img["client1"]+normal_img["client2"]:
            shutil.copy(input_path + "//normal//" + filename, output_path + "//"+cl_id2+"//normal//" + filename)
            s = s + 1
            #print("client 2 in process")

        elif i> s and i<= normal_img["client1"]+normal_img["client2"]+normal_img["client3"]:
            shutil.copy(input_path + "//normal//" + filename, output_path + "//"+cl_id3+"//normal//" + filename)
            s = s + 1
            #print("client 3 in process")
            #print("i",i,"s",s)
        elif i>= normal_img["client1"]+normal_img["client2"]+normal_img["client3"] -1 :
            shutil.copy(input_path + "//normal//" + filename, output_path + "//"+cl_id4+"//normal//" + filename)
            #print("client 4 in process")

    s = 0
    i = 0
    for filename in covid:
        i = i + 1
        if i <= covid_img["client1"]:
            shutil.copy(input_path + "//covid//" + filename, output_path + "//"+cl_id1+"//covid//" + filename)
            s = s + 1
            print()
        elif i > s and i <= covid_img["client1"] + covid_img["client2"]:
            shutil.copy(input_path + "//covid//" + filename, output_path + "//"+cl_id2+"//covid//" + filename)
            s = s + 1

        elif i > s and i <= covid_img["client1"] + covid_img["client2"] + covid_img["client3"]:
            shutil.copy(input_path + "//covid//" + filename, output_path + "//"+cl_id3+"//covid//" + filename)
            s = s + 1
        elif i >= covid_img["client1"] + covid_img["client2"] + covid_img["client3"] -1 :
            shutil.copy(input_path + "//covid//" + filename, output_path + "//"+cl_id4+"//covid//" + filename)
    print("process finished")


distribute(input_path, output_path,cl_id1,cl_id2,cl_id3,cl_id4, fraction1, fraction2, fraction3, fraction4)
#python split_data_clients.py --input "/run/media/fawaz/DATA/datasets/chest_xray/Training" --output "/home/fawaz/Desktop/FL_dataset/" --cl1Id 1 --cl2Id 2 --cl3Id 3 --cl4Id 4 --fraction1 0.5 --fraction2 0.5 --fraction3 0 --fraction4 0