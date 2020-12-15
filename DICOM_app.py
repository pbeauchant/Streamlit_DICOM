import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pydicom as dicom
from tciaclient import TCIAClient
import urllib.request, urllib.error, urllib.parse, urllib.request, urllib.parse, urllib.error,sys
import urllib

def query_to_list(resp,properties):
    collection_json =json.loads(resp.read().decode("utf-8"))
    collection_list=[]
    for i in range(len(collection_json)):
        collection_list.append(collection_json[i][properties])
    return(collection_list)

import json
tcia_client = TCIAClient(baseUrl="https://services.cancerimagingarchive.net/services/v4",resource = "TCIA")

collection_list = query_to_list(tcia_client.get_collection_values(outputFormat = "json" ),'Collection')
collection_selected = st.selectbox(    "Which collection to browse ?",     collection_list)
if collection_selected is not None :
    patientId_list = query_to_list(tcia_client.get_patient(collection = collection_selected , outputFormat = "json" ),'PatientID')
    patient_selected = st.selectbox(    "Which patient to select ?",     patientId_list)
    if patient_selected is not None : 
        my_patient = json.loads(tcia_client.get_patient_study(patientId = patient_selected , outputFormat = "json" ).read())
        my_patient_studies = json.loads(tcia_client.get_series(studyInstanceUid =my_patient[0]['StudyInstanceUID']).read())
        #st.markdown(json.loads(tcia_client.get_getSOPInstanceUIDs(SeriesInstanceUID =my_patient_studies[0]['SeriesInstanceUID']).read()))
        SOPInstanceUID = query_to_list(tcia_client.get_getSOPInstanceUIDs(SeriesInstanceUID =my_patient_studies[0]['SeriesInstanceUID']),'SOPInstanceUID')
        st.markdown('----')
        url_dicom = "https://services.cancerimagingarchive.net/services/v4/TCIA/query/getSingleImage?SeriesInstanceUID={}&SOPInstanceUID={}".format(my_patient_studies[0]['SeriesInstanceUID'],SOPInstanceUID[len(SOPInstanceUID)//2])

        f = urllib.request.urlopen(url_dicom)
        myfile = f.read()
        from pydicom import dcmread
        from pydicom.filebase import DicomBytesIO
        raw = DicomBytesIO(myfile)
        ds = dcmread(raw)


        st.image(ds.pixel_array, clamp=True)
