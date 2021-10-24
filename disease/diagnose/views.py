#load cnn train model
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np


from django.shortcuts import render, redirect
from .forms import DiseaseForm
from django.contrib import messages
from django.conf import settings

classs = ['Actinic Keratosis (AKIEC)', 'Basal Cell Carcinoma (Bcc)','Benign Keratosis (BKL)', 'Dermatofibroma (DF)', 'Melanoma (Mel)', 'Melanocytic Nevus (NV)', 'Vascular Lesion (VASC)']
model = load_model("media/models/CNN_B64_E30.h5")

model_inception = load_model("media/models/InceptionV3_B64_E30.h5")
model_vgg = load_model("media/models/VGG16_B64_E30.h5")

def get_img_array(img_path):
    path = img_path
    img = image.load_img(path, target_size=(224, 224, 3))
    img = image.img_to_array(img) / 255
    img = np.expand_dims(img, axis=0)
    return img

def Diagnose(request):
    if request.method == 'POST':
        form = DiseaseForm(request.POST, request.FILES)
        if form.is_valid():
            frm = form.save(commit=False)
            frm.user = request.user
            #frm.summary = settings.MEDIA_ROOT + frm.image

            frm.save()
            path = "media/images/"+request.FILES['image'].name
            img = get_img_array(path)
            #custom model predict and percentage and insert
            res = classs[np.argmax(model.predict(img))]
            akiec = model.predict(img)[0][0] * 100
            bcc = model.predict(img)[0][1] * 100
            bkl = model.predict(img)[0][2] * 100
            df = model.predict(img)[0][3] * 100
            mel = model.predict(img)[0][4] * 100
            nv = model.predict(img)[0][5] * 100
            vasc = model.predict(img)[0][6] * 100
            max_value = max(akiec, bcc, bkl, df, mel, nv, vasc)
            parcentage = ((round (max_value, 2)))
            parcentage = str(parcentage)
            frm.summary = res
            frm.summary_val = parcentage
            customText = "Actinic Keratosis (AKIEC) <strong>"+str(round(akiec, 2))+"%</strong>, Basal Cell Carcinoma (Bcc) <strong>"+str(round(bcc, 2))+"%</strong>, Benign Keratosis (BKL) <strong>"+str(round(bkl, 2))+"%</strong>, Dermatofibroma (DF) <strong>"+str(round(df, 2))+"%</strong>, Melanoma (Mel) <strong>"+str(round(mel, 2))+"%</strong>, Melanocytic Nevus (NV) <strong>"+str(round(nv, 2))+"%</strong>, Vascular Lesion (VASC) <strong>"+str(round(vasc, 2))+"%</strong>. According this analysis we get max value is <strong>"+res+" "+parcentage+"%</strong>"
            frm.summary_desc = customText
            # custom model predict and percentage and insert end
            # inception model
            inception_res = classs[np.argmax(model_inception.predict(img))]
            akieci = model_inception.predict(img)[0][0] * 100
            bcci = model_inception.predict(img)[0][1] * 100
            bkli = model_inception.predict(img)[0][2] * 100
            dfi = model_inception.predict(img)[0][3] * 100
            meli = model_inception.predict(img)[0][4] * 100
            nvi = model_inception.predict(img)[0][5] * 100
            vasci = model_inception.predict(img)[0][6] * 100
            max_valuei = max(akieci, bcci, bkli, dfi, meli, nvi, vasci)
            parcentagei = ((round (max_valuei, 2)))
            parcentagei = str(parcentagei)
            frm.summary_inception = inception_res
            frm.summary_inception_val = parcentagei
            inceptionText = "Actinic Keratosis (AKIEC) <strong>"+str(round(akieci, 2))+"%</strong>, Basal Cell Carcinoma (Bcc) <strong>"+str(round(bcci, 2))+"%</strong>, Benign Keratosis (BKL) <strong>"+str(round(bkli, 2))+"%</strong>, Dermatofibroma (DF) <strong>"+str(round(dfi, 2))+"%</strong>, Melanoma (Mel) <strong>"+str(round(meli, 2))+"%</strong>, Melanocytic Nevus (NV) <strong>"+str(round(nvi, 2))+"%</strong>, Vascular Lesion (VASC) <strong>"+str(round(vasci, 2))+"%</strong>. According this analysis we get max value is <strong>"+inception_res+" "+parcentagei+"%</strong>"
            frm.summary_inception_desc = inceptionText
            #inception model end
            # vgg model
            vgg_res = classs[np.argmax(model_vgg.predict(img))]
            akiecv = model_vgg.predict(img)[0][0] * 100
            bccv = model_vgg.predict(img)[0][1] * 100
            bklv = model_vgg.predict(img)[0][2] * 100
            dfv = model_vgg.predict(img)[0][3] * 100
            melv = model_vgg.predict(img)[0][4] * 100
            nvv = model_vgg.predict(img)[0][5] * 100
            vascv = model_vgg.predict(img)[0][6] * 100
            max_valuev = max(akiecv, bccv, bklv, dfv, melv, nvv, vascv)
            parcentagev = ((round (max_valuev, 2)))
            parcentagev = str(parcentagev)
            frm.summary_vgg = vgg_res
            frm.summary_vgg_val = parcentagev

            vggText = "Actinic Keratosis (AKIEC) <strong>"+str(round(akiecv, 2))+"%</strong>, Basal Cell Carcinoma (Bcc) <strong>"+str(round(bccv, 2))+"%</strong>, Benign Keratosis (BKL) <strong>"+str(round(bklv, 2))+"%</strong>, Dermatofibroma (DF) <strong>"+str(round(dfv, 2))+"%</strong>, Melanoma (Mel) <strong>"+str(round(melv, 2))+"</strong>%, Melanocytic Nevus (NV) <strong>"+str(round(nvv, 2))+"%</strong>, Vascular Lesion (VASC) <strong>"+str(round(vascv, 2))+"%</strong>. According this analysis we get max value is <strong>"+vgg_res+" "+parcentagev+"%</strong>"
            frm.summary_vgg_desc = vggText

            #vgg model end
            frm.save()
            p = str(frm.id)
            #messages.success(request, "Imaged added successfully.")
            return redirect('/'+p)
        else :
            messages.error(request, "Error occured.")
            return redirect('/disease')
    else:
        if request.user.is_authenticated:
            form = DiseaseForm()
        else:
            messages.error(request, "You must login first!")
            return redirect('/account/login')
    return render(request, 'disease.html', {'form' : form})
