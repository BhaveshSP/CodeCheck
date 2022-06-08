# Imports  
import cv2 
import numpy as np 
from pyzbar.pyzbar import decode 


# Get the valid ids list from the file 
known_ids = []
with open("valid_member_ids.txt") as file:
	# split the ids in the file by new line
	# since each line has only one id 
	known_ids = file.read().splitlines()


# Use Image 
# img = cv2.imread("bar_code_dummy.jpg")

# Use Camera Image 
capture = cv2.VideoCapture(0)
capture.set(3,1280)
capture.set(4,720)

while True :
	# Camera Feed 
	_, img = capture.read()
	
	# img = cv2.flip(img,1)

	# Check each bar code in the frame
	for scanned_code in decode(img):
		text = ""
		color = (0,255,0)
		id_code = scanned_code.data.decode("utf-8")
		# If the code on the scanned code is in the valid or known ids 
		# the person is authorized 
		if id_code in known_ids:
			text = "Authorized"
			color = (0,255,0)
		# If the code on the scanned code is not in the valid or know ids 
		#  the person is un-authorized
		else:
			text = "Un-Authorized"
			color = (0,0,255)
		# Draw a polygon around the scanned code 
		poly_points = np.array([scanned_code.polygon],np.int32)
		# reshape the scanned code polygon to match the polylines of cv2
		poly_points = poly_points.reshape((-1,1,2))
		cv2.polylines(img,[poly_points],True,color,6)
		# Write text on the screen to show authorized or un-authorized 
		# Get the top-left coordinates of rectangle around the scanned code 
		text_points = scanned_code.rect 
		# Write Text or Put Text on the frame 
		cv2.putText(img,text,(text_points[0],text_points[1]-10),cv2.FONT_HERSHEY_PLAIN,1,color,2)

	# Show the frame on the window
	cv2.imshow("QR Auth",img)
	# Wait key with delay 1 millisecond 
	key = cv2.waitKey(1)
	# If the key pressed is s then stop the execution else continue 
	if key == ord("s"):
		break

# Release the resources allocated to the program  
capture.release()
cv2.destroyAllWindows()