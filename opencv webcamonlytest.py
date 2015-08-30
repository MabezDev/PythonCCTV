import  numpy as np
import  cv2
 
#cargamos template and initialize the webcam:
face_cascade =  cv2.CascadeClassifier ( 'haarcascade_frontalface_alt.xml' )
cap =  cv2.VideoCapture ( 0 )
 
while ( True ):
    #leemos one frame and save it
    ret, img =  cap.read ()
 
    #convertimos image to black and white
    gray =  cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
 
    #buscamos the coordinates of the faces (if any) and
    #guardamos its position
    #faces =  face_cascade.detectMultiScale (gray, 1.3 , 5 )
 
    #Dibujamos A rectangle in the coordinates of each face

    #Mostramos Image
    cv2.imshow ( 'img' , gray)
     
    # with the key 'q' we leave the program
    if  cv2.waitKey ( 1 ) & 0xFF  ==  ord ( 'q' ):
        break
cap.release ()
cv2.destroyAllWindows ()
