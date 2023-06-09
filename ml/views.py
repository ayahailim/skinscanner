from django.shortcuts import render
from django.db import models
import cv2
import numpy as np
import keras
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import tensorflow
from keras.utils import img_to_array
import keras.utils
from keras.utils import load_img
from .models import preuser
from .serializers import preuserSerializer
from knox.auth import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
import tempfile
from rest_framework.permissions import IsAuthenticated
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image
from keras.applications.densenet import preprocess_input
#===========================================================================================================================   
class classAPIViewtf(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, id=None, format=None):
        user = request.user
        if id is not None:
            try:
                preuser_object = preuser.objects.get(id=id, user=user)
            except preuser.DoesNotExist:
                return Response({'error': 'Object not found.'}, status=404)
            serializer = preuserSerializer(preuser_object)
            return Response(serializer.data)
        else:
            preuser_objects = preuser.objects.filter(user=user)
            serializer = preuserSerializer(preuser_objects, many=True)
            return Response(serializer.data)
       
    def post(self,request,format=None):
        classes =['Basal Cell Carcinoma (BCC)', 'Chickenpox', 'Melanocytic Nevi (NV)', 'Melanoma',
                   'Normal', 'Ringworm', 'Warts Molluscum,Viral Infections']
        image_file = request.FILES.get('image')
        user = request.user
        if image_file:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(image_file.read())
                temp_file.flush()
                # Load the TFLite model
                interpreter = tf.lite.Interpreter(model_path='./ml/final_model.tflite')
                interpreter.allocate_tensors()
                # Load the image and preprocess
                test_image = load_img(temp_file.name,target_size=(224, 224))
                test_image = img_to_array(test_image) 
                test_image = np.expand_dims(test_image, axis=0)
                test_image = preprocess_input(test_image)
                # Set the input tensor to the interpreter
                input_details = interpreter.get_input_details()
                interpreter.set_tensor(input_details[0]['index'], test_image)
                # Invoke the interpreter to obtain the predictions
                interpreter.invoke()
                # Get the output tensor from the interpreter
                output_details = interpreter.get_output_details()
                output_data = interpreter.get_tensor(output_details[0]['index'])
                # Post-process the output data
                prediction_label = classes[np.argmax(output_data)]
                # Additional prediction logic
                max_pred = np.max(output_data)
                t = 0.90
                if max_pred < t:
                    prediction_label = "unknown"
                preuser.objects.create(user=user,image=image_file, prediction=prediction_label)
                return Response({'Disease': prediction_label}, status=200)
        else:
            return Response({'error': 'No image file provided.'}, status=400)
    
    def delete(self, request, id, format=None):
        user = request.user
        try:
            preuser_object = preuser.objects.get(id=id, user=user)
        except preuser.DoesNotExist:
            return Response({'error': 'Object not found.'}, status=404)
        preuser_object.delete()
        return Response({'success': 'Object deleted.'}, status=200)
        
'''class classAPIViewtf(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        preuser_objects = preuser.objects.filter(user=user)
        serializer = preuserSerializer(preuser_objects, many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        classes = ['Basal Cell Carcinoma (BCC)','Melanocytic Nevi (NV)','Melanoma','chicken Pox','Ringworm','Warts Molluscum,Viral Infections','normal']
        image_file = request.FILES.get('image')
        user = request.user
        if image_file:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(image_file.read())
                temp_file.flush()
                # Load the TFLite model
                interpreter = tf.lite.Interpreter(model_path='./ml/tflite_model.tflite')
                interpreter.allocate_tensors()
                # Load the image and preprocess it
                test_image = load_img(temp_file.name, target_size=(224, 224))
                test_image = img_to_array(test_image) / 255
                test_image = np.expand_dims(test_image, axis=0)
                # Set the input tensor to the interpreter
                input_details = interpreter.get_input_details()
                interpreter.set_tensor(input_details[0]['index'], test_image)
                # Invoke the interpreter to obtain the predictions
                interpreter.invoke()
                # Get the output tensor from the interpreter
                output_details = interpreter.get_output_details()
                output_data = interpreter.get_tensor(output_details[0]['index'])
                # Post-process the output data
                prediction_label = classes[np.argmax(output_data)]
                preuser.objects.create(user=user,image=image_file, prediction=prediction_label)
                return Response({'Disease': prediction_label}, status=200)
        else:
            return Response({'error': 'No image file provided.'}, status=400)'''


'''test_image = load_img('D:/aya1/photos/22.jpg', target_size=(224, 224))
test_image = image.img_to_array(test_image) / 255  # < - division by 255
test_image = np.expand_dims(test_image, axis=0)
test_model = keras.models.load_model('C:/Users/Ninja/Downloads/model (1).tflite',compile=False)
prediction = test_model.predict(test_image)

classes = ['not_skin','skin']
classes2 = ['Basal Cell Carcinoma (BCC)','Chickenpox','Melanocytic Nevi (NV)','Melanoma','Normal','Ringworm', 'Warts Molluscum,Viral Infections']
pred = classes[(np.argmax(prediction))]
if pred == 'not_skin' :
    print(pred)
else:
    test_model2 = keras.models.load_model('C:/Users/Ninja/Downloads/model(2).tflite',compile=False)
    prediction2 = test_model2.predict(test_image)
    test1= np.max(prediction2)
    if test1 < 0.90:
      print('other diseases')
    else:
      print(classes2[(np.argmax(prediction2))])'''

'''class twomodels(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        preuser_objects = preuser.objects.filter(user=user)
        serializer = preuserSerializer(preuser_objects, many=True)
        return Response(serializer.data)
    
    def post(self,request,format=None):
        classes = ['not_skin','skin']
        classes2 = ['Basal Cell Carcinoma (BCC)','Chickenpox','Melanocytic Nevi (NV)','Melanoma','Normal','Ringworm', 'Warts Molluscum,Viral Infections']
        image_file = request.FILES.get('image')
        user = request.user
        if image_file:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(image_file.read())
                temp_file.flush()
                # Load the first pre-trained model
                model1 = tf.keras.models.load_model('./ml/model2.tflite')
                # Load the second pre-trained model
                model2 = tf.keras.models.load_model('./ml/tflite_model.tflite')
                # Load the image and preprocess it
                test_image = load_img(temp_file.name, target_size=(224, 224))
                test_image = img_to_array(test_image) / 255
                test_image = np.expand_dims(test_image, axis=0)
                # Use the first model to predict the class of the input image
                prediction = model1.predict(test_image)
                # Find the index of the maximum predicted probability
                pred = classes[np.argmax(prediction)]
                if pred == 'not_skin':
                    prediction_label = pred
                else:
                    # Use the second model to predict the class of the input image
                    prediction2 = model2.predict(test_image)
                    # Find the index of the maximum predicted probability from the second model
                    pred2 = classes2[np.argmax(prediction2)]
                    # Check if the maximum predicted probability is less than 0.90
                    if np.max(prediction2) < 0.90:
                        prediction_label = 'other diseases'
                    else:
                        prediction_label = pred2
                preuser.objects.create(user=user,image=image_file, prediction=prediction_label)
                return Response({'Disease': prediction_label}, status=200)
        else:
            return Response({'error': 'No image file provided.'}, status=400)'''

'''def get(self, request, format=None):
        user = request.user
        preuser_objects = preuser.objects.filter(user=user)
        serializer = preuserSerializer(preuser_objects, many=True)
        return Response(serializer.data)'''

'''class classifierAPIView(APIView):
    def post(self,request):
        classes = ['Basal Cell Carcinoma (BCC)','Melanocytic Nevi (NV)','Melanoma','Monkey Pox','Ringworm','Warts Molluscum,Viral Infections','normal']
        image_file = request.FILES.get('image')
        if image_file:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(image_file.read())
                temp_file.flush()
                temp_model = load_model('./ml/7skin_model.h5')
                test_image = load_img(temp_file.name, target_size=(224, 224))
                test_image = img_to_array(test_image) / 255
                test_image = np.expand_dims(test_image, axis=0)
                prediction = temp_model.predict(test_image)
                max_pred = np.max(prediction)
                t = 0.95
                if max_pred < t:
                    prediction_label = "other diseases"
                else:
                    prediction_label = classes[np.argmax(prediction)]
                
                classifier.objects.create(image=image_file, prediction=prediction_label)
                return Response({'Disease': prediction_label}, status=200)
        else:
            return Response({'error': 'No image file provided.'}, status=400) '''

'''class classAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get(self, request, id=None, format=None):
        user = request.user
        if id is not None:
            try:
                preuser_object = preuser.objects.get(id=id, user=user)
            except preuser.DoesNotExist:
                return Response({'error': 'Object not found.'}, status=404)
            serializer = preuserSerializer(preuser_object)
            return Response(serializer.data)
        else:
            preuser_objects = preuser.objects.filter(user=user)
            serializer = preuserSerializer(preuser_objects, many=True)
            return Response(serializer.data)
        
    def post(self,request,format=None):
        classes = ['Basal Cell Carcinoma (BCC)','Melanocytic Nevi (NV)','Melanoma','chicken Pox','Ringworm','Warts Molluscum,Viral Infections','normal']
        image_file = request.FILES.get('image')
        user = request.user
        if image_file:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(image_file.read())
                temp_file.flush()
                temp_model = load_model('./ml/7skin_model.h5')
                test_image = load_img(temp_file.name, target_size=(224, 224))
                test_image = img_to_array(test_image) / 255
                test_image = np.expand_dims(test_image, axis=0)
                prediction = temp_model.predict(test_image)
                max_pred = np.max(prediction)
                t = 0.90
                if max_pred < t:
                    prediction_label = "unkown"
                else:
                    prediction_label = classes[np.argmax(prediction)]
                
                preuser.objects.create(user=user,image=image_file, prediction=prediction_label)
                return Response({'Disease': prediction_label}, status=200)
        else:
            return Response({'error': 'No image file provided.'}, status=400) 
    
    def delete(self, request, id, format=None):
        user = request.user
        try:
            preuser_object = preuser.objects.get(id=id, user=user)
        except preuser.DoesNotExist:
            return Response({'error': 'Object not found.'}, status=404)
        preuser_object.delete()
        return Response({'success': 'Object deleted.'}, status=200)'''