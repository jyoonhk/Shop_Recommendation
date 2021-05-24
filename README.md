![Banner](/Deployment/images/Banner_4.png)

### Project Goals:

ShopRec is a **Computer Vision recommendation system**, used for in store personalised clothing recommendations.

ShopRec aims to **personalise** customer retail shopping experience, and revitalise in store shopping.


### Business Case:
ShopRec aims to provide benefits to businesses:
- Undiscovered Opportunity:
  * Lack of multi brand / shop recommendation systems.
  * Gap in the market for computer vision.
- Multiple Benefits: 
  * Customers, Shops and Shopping Centres will all benefit from innovation.


### Model Overview:
3 facial recognition models were tested and implemented using external data and our user data. The models are: User Detection, Emotion Detection, and Gender/Age Detection.

These are a mixture of pretrained models e.g. OpenCV and face_recognition libraries, and a Deep Learning CNN model we have trained.

Each model follows a similar process: 
- Detect a face from an image
- Process this face through a feature model (e.g. user name, emotions, gender/age)
- Overlay the model outputs on the original image

More details are given below.
![Process](/Images/process1.jpg)

#### 1. User Detector:
```
Purpose: Security & Law Enforcement, Mobile device security, Tracking attendance.
```
A pretrained facial recognition model from the OpenCV face_recognition library was used to detect users from the images uploaded to our internal database. 

This model will identify unauthorised faces that differ significantly from users in our database. Users that are recognised by the model will be labelled in green and their movements logged for attendance tracking.


#### 2. Emotion Detector:
```
Purpose: Security & Law Enforcement.
```
A Convolutional Neural Network was trained to detect facial emotions by using a Kaggle dataset with over 35,000 images of various facial emotions. 

The CNN model was trained to detect: Anger, Disgust, Fear, Happiness, Sadness, Surprise, and Neutral expressions.

![Distribution of emotions in training dataset](/Images/emotions1.jpg)
![Accuracy/Loss - Train v Test against Epoch](/Images/emotions3.jpg)


#### 3. Gender and Age Detector:
```
Purpose: Smart Advertisement, Tracking attendance.
```
The model for age and gender was pre-trained from Adience data set with 26,580 photos, while the face detection model is from OpenCV's DNN module.
- The Gender has 2 classes: Male and Female
- Age is divided between 8 classes: 0 – 2, 4 – 6, 8 – 12, 15 – 20, 25 – 32, 38 – 43, 48 – 53, 60 – 100

![Distribution of Age/Gender](/Images/agegender2.jpg)


#### *Conclusions*
This project has demonstrated some uses of facial recognition technology, within Security & Law Enforcement, attendance tracking and advertising. 

Further enhancements could include:

- Enriching the original datasets to better differentiate between similar users.
- Aggregating our 3 models into 1 model to simultaneously detect authorised users, emotions, and gender/age.
- Enhance model to differentiate between real people and pictures/images of people.

Concerns on Facial Recognition include:

- Privacy / Misuse of Facial Data: The technology could enable mass surveillance of all people; there is no widespread legislation of facial recognition technology.
- Security Breaches: Improper storage of user images could expose users to privacy breaches / security threats / stolen identity.
- Bias and Inaccuracies: Algorithms trained on racially biased datasets could lead to misidentifying and/or discrimination of people from minority ethnic backgrounds.
