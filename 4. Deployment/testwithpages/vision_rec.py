import cv2
import time
import streamlit as st
import numpy as np
import torch
import pandas as pd
from PIL import Image, ImageEnhance
import os

def app():

    st.markdown("""
    # Clothes Detection Engine 
    # 
    """)
    
    image_folder = "Data/"
    path = 'customer_img'

    #fitting local model using yolov5 github files
    @st.cache
    def weights():
        model = torch.hub.load('ultralytics/yolov5', 'custom', 'model_weight/best.pt', force_reload=True)
        return model
    model = weights()

    @st.cache
    def get_products():
        products = pd.read_csv('csv/product_db.csv')
        products = products.loc[:, ~products.columns.str.contains('^Unnamed')]
        return products
    products = get_products()

        #defining model confidence threshold
    model.conf = 0.2
    #defining different clothes categories for later
    top = ['Blouses', 'Jackets_Coats','Jumpers', 'Polos', 'Shirts', 'T-Shirts']
    bottom = ['Jeans', 'Shorts', 'Skirts', 'Trousers']
    one_piece = ['Dresses', 'Suits']
    #clothes categories for later
    FRAME_WINDOW = st.image([])
    #Set Video Resolution
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # img = cv2.imread('outline.png')
    # img_height, img_width, _ = img.shape
    #Set Timer
    TIMER = int(10)
    path = 'customer_img'



    st.header("Vision Recommendation")

    st.subheader('Upload your image')

    select = st.selectbox('Select how to load image:', ['','Load Image', 'Webcam'])

    if select == 'Load Image':
        user_image = st.file_uploader("Please upload an image of your face",type=['jpg','png','jpeg'])
        if user_image is not None:
            img = Image.open(user_image)
            st.image(img, width = 300)
            if st.button('Save Picture'):
                
                with open(os.path.join(path, 'customer.jpg'),"wb") as f:
                    f.write(user_image.getbuffer())
                    st.text('Image saved!')

                    my_bar = st.progress(0)

                    my_bar.progress(2)

                    
                    clothes = []



                    #preprocessing images somewhat - might not be necessary for future images
                    #replace image with captured image in future
                    image = Image.open(path + '/customer.jpg')
                    # image = image.rotate(270, expand=True)
                    #sharpness / color / brightness can be manipulated
                    enhancer = ImageEnhance.Brightness(image)
                    enhancer.enhance(1.2).save(path + '/customer_new.jpg')

                    my_bar.progress(15)

                    #calculating predictions
                    
                    results = model(path + '/customer_new.jpg', augment=True, size=900)
                    #not sure how to change path for save - other than changing os and changing back
                    results.save()

                    

                    #putting predictions in dataframe
                    df = results.pandas().xyxy[0]

                    #just cleaning to make dataframe look better (dropping bounding box values)
                    df = df.drop(columns = ["xmin", "ymin", "xmax", "ymax"])
                    #creating separate dataframes for each clothes category (CAN be cleaner)
                    top_df = df[df['name'].isin(top)]
                    top_df = top_df.loc[top_df.groupby('name')['confidence'].idxmax()]
                    top_df = top_df.sort_values(by='confidence', ascending=False).head(1).reset_index()

                    my_bar.progress(30)

                    bottom_df = df[df['name'].isin(bottom)]
                    bottom_df = bottom_df.loc[bottom_df.groupby('name')['confidence'].idxmax()]
                    bottom_df = bottom_df.sort_values(by='confidence', ascending=False).head(1).reset_index()

                    one_piece_df = df[df['name'].isin(one_piece)]
                    one_piece_df = one_piece_df.loc[one_piece_df.groupby('name')['confidence'].idxmax()]
                    one_piece_df = one_piece_df.sort_values(by='confidence', ascending=False).head(1).reset_index()

                    #append necessary clothes categories into list
                    my_bar.progress(45)

                    try:
                        if one_piece_df.loc[0, 'confidence'] > top_df.loc[0, 'confidence']:
                            clothes.append(one_piece_df.loc[0, 'name'])    
                    except:
                        pass

                    try:
                        if clothes not in one_piece:
                            clothes.append(top_df.loc[0, 'name']) 
                    except:
                        pass
                    try:
                        if clothes not in one_piece:
                            clothes.append(bottom_df.loc[0,'name'])
                    except:
                        pass
                    try:
                        if clothes not in top or bottom:
                            clothes.append(one_piece_df.loc[0, 'name'])
                    except:
                        pass

                    profile_expander_1 = st.beta_expander('For Men')
                    my_bar.progress(70)
                    with profile_expander_1:

                        products = get_products()

                        products = products[products['Gender'] == 'Mens']

                        products = products[products['Category'].isin(clothes)]

                        if products.empty is True:

                            profile_expander_1.empty()

                        else:
                            
                            products = products.groupby(['Category','Brand']).apply(lambda x:x.sample(1)).reset_index(drop = True)

                            n_columns = 2
                            
                            for item in products['Brand'].unique():
                                count = 0
                                st.subheader(item)
                                item_df = products[products['Brand']==item]
                                cols = st.beta_columns(n_columns)
                                for i in range(n_columns):
                                    try:
                                        df_row = item_df.iloc[count]
                                        im = Image.open(image_folder + df_row['Image Location'])
                                        im = im.resize((150, 180))
                                        cols[i].write(str(df_row['Name']))
                                        cols[i].image(im)
                                        count+=1

                                    except:
                                        pass


                    my_bar.progress(85)
                    profile_expander_2 = st.beta_expander('For Women')

                    with profile_expander_2:
                        products = get_products()
                         
                        products = products[products['Gender'] == 'Womens']
                    

                        products = products[products['Category'].isin(clothes)]

                        if products.empty is True:
                            profile_expander_2.empty()
                        else:
                            products = products.groupby(['Category','Brand']).apply(lambda x:x.sample(1)).reset_index(drop = True)

                            n_columns = 2
                            
                            for item in products['Brand'].unique():
                                count = 0
                                st.subheader(item)
                                item_df = products[products['Brand']==item]
                                cols = st.beta_columns(n_columns)
                                for i in range(n_columns):
                                    try:
                                        df_row = item_df.iloc[count]
                                        im = Image.open(image_folder + df_row['Image Location'])
                                        im = im.resize((150, 180))
                                        cols[i].write(str(df_row['Name']))
                                        cols[i].image(im)
                                        count+=1

                                    except:
                                        pass

                    my_bar.progress(100)
                    time.sleep(2)
                    my_bar.empty()
    # button = st.button("Recommend Me Shops")
    # # x=100
    # # y=50

    if select == 'Webcam':
        
        clothes = []

        prev = time.time()

        while TIMER >= 0:
            _,frame = cap.read()
            # Display countdown on each frame
            # specify the font and draw the
            # countdown using puttext

            # frame[y: y+img_height, x: x+img_width] = img
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, str(TIMER), 
                        (200, 250), font,
                        7, (0, 255, 255),
                        4, cv2.LINE_AA)


            FRAME_WINDOW.image(frame, channels='BGR')

            # current time
            cur = time.time()

            # Update and keep track of Countdown
            # if time elapsed is one second 
            # than decrese the counter
            if cur-prev >= 1:
                prev = cur
                TIMER = TIMER-1

        else:
            _,frame = cap.read()
            FRAME_WINDOW.image(frame, channels='BGR')
            # Display the clicked frame for 2 seconds

            # time for which image displayed
            cv2.waitKey(2000)

            # Save the frame
            cv2.imwrite(os.path.join(path, 'customer.jpg'), frame)

            st.write("Done")
            
            time.sleep(2)

            cap.release()
            cv2.destroyAllWindows()


    #Keep image on?

        # button_x = st.button("Do it")

        my_bar = st.progress(0)
        #preprocessing images somewhat - might not be necessary for future images
        #replace image with captured image in future
        image = Image.open(path + '/customer.jpg')
        # image = image.rotate(270, expand=True)
        #sharpness / color / brightness can be manipulated
        enhancer = ImageEnhance.Brightness(image)
        enhancer.enhance(1.2).save(path + '/customer_new.jpg')

        #calculating predictions
        results = model(path + '/customer_new.jpg', augment=True, size=900)
        #not sure how to change path for save - other than changing os and changing back
        results.save()

        #putting predictions in dataframe
        df = results.pandas().xyxy[0]
        my_bar.progress(15)
        #just cleaning to make dataframe look better (dropping bounding box values)
        df = df.drop(columns = ["xmin", "ymin", "xmax", "ymax"])
        #creating separate dataframes for each clothes category (CAN be cleaner)
        top_df = df[df['name'].isin(top)]
        top_df = top_df.loc[top_df.groupby('name')['confidence'].idxmax()]
        top_df = top_df.sort_values(by='confidence', ascending=False).head(1).reset_index()

        bottom_df = df[df['name'].isin(bottom)]
        bottom_df = bottom_df.loc[bottom_df.groupby('name')['confidence'].idxmax()]
        bottom_df = bottom_df.sort_values(by='confidence', ascending=False).head(1).reset_index()

        one_piece_df = df[df['name'].isin(one_piece)]
        one_piece_df = one_piece_df.loc[one_piece_df.groupby('name')['confidence'].idxmax()]
        one_piece_df = one_piece_df.sort_values(by='confidence', ascending=False).head(1).reset_index()
        my_bar.progress(30)
        #append necessary clothes categories into list
        #looking at confidence value top/one-piece and adding it into list if one-piece confidence is higher
        #otherwise pass
        try:
            if one_piece_df.loc[0, 'confidence'] > top_df.loc[0, 'confidence']:
                clothes.append(one_piece_df.loc[0, 'name'])    
        except:
            pass

        try:
            if clothes not in one_piece:
                clothes.append(top_df.loc[0, 'name']) 
        except:
            pass
        try:
            if clothes not in one_piece:
                clothes.append(bottom_df.loc[0,'name'])
        except:
            pass
        try:
            if clothes not in top or bottom:
                clothes.append(one_piece_df.loc[0, 'name'])
        except:
            pass

        my_bar.progress(50)

        profile_expander_1 = st.beta_expander('For Men')

        with profile_expander_1:
            
            products = get_products()

            products = products[products['Gender'] == 'Mens']

            products = products[products['Category'].isin(clothes)]

            if products.empty is True:

                profile_expander_1.empty()

            else:
                
                products = products.groupby(['Category','Brand']).apply(lambda x:x.sample(1)).reset_index(drop = True)

                n_columns = 2
                
                for item in products['Brand'].unique():
                    count = 0
                    st.subheader(item)
                    item_df = products[products['Brand']==item]
                    cols = st.beta_columns(n_columns)
                    for i in range(n_columns):
                        try:
                            df_row = item_df.iloc[count]
                            im = Image.open(image_folder + df_row['Image Location'])
                            im = im.resize((150, 180))
                            cols[i].write(str(df_row['Name']))
                            cols[i].image(im)
                            count+=1

                        except:
                            pass
        my_bar.progress(75)
        profile_expander_2 = st.beta_expander('For Women')

        with profile_expander_2:

            products = get_products()
             
            products = products[products['Gender'] == 'Womens']
        

            products = products[products['Category'].isin(clothes)]

            if products.empty is True:
                profile_expander_2.empty()
            else:
                products = products.groupby(['Category','Brand']).apply(lambda x:x.sample(1)).reset_index(drop = True)

                n_columns = 2
                
                for item in products['Brand'].unique():
                    count = 0
                    st.subheader(item)
                    item_df = products[products['Brand']==item]
                    cols = st.beta_columns(n_columns)
                    for i in range(n_columns):
                        try:
                            df_row = item_df.iloc[count]
                            im = Image.open(image_folder + df_row['Image Location'])
                            im = im.resize((150, 180))
                            cols[i].write(str(df_row['Name']))
                            cols[i].image(im)
                            count+=1

                        except:
                            pass
        my_bar.progress(100)
        time.sleep(2)
        my_bar.empty()