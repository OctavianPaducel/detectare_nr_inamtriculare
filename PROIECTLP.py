import time
import tkinter as tk
import sys
import cv2
import imutils
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'
image = cv2.imread('test.jpg')
image = imutils.resize(image, width=450 )
cv2.imshow("poza originala", image)
cv2.waitKey(0)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("poza in alb-negru", gray_image)
cv2.waitKey(0)
gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
cv2.imshow("poza netezita", gray_image)
cv2.waitKey(0)
edged = cv2.Canny(gray_image, 30, 200)
cv2.imshow("poza taiata", edged)
cv2.waitKey(0)
cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
image1=image.copy()
cv2.drawContours(image1,cnts,-1,(0,255,0),3)
cv2.imshow("contururile",image1)
cv2.waitKey(0)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
screenCnt = None
image2 = image.copy()
cv2.drawContours(image2,cnts,-1,(0,255,0),3)
cv2.imshow("primele 30 de contururi",image2)
cv2.waitKey(0)
i=7
for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        if len(approx) == 4:
                screenCnt = approx
                x, y, w, h = cv2.boundingRect(c)
                new_img = image[y:y + h, x:x + w]
                cv2.imwrite('./' + str(i) + '.png', new_img)
                i += 1
                break
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
cv2.imshow("numarul de inmatriculare detectat", image)
cv2.waitKey(0)
Cropped_loc = './7.png'
cv2.imshow("poza taiata final", cv2.imread(Cropped_loc))
plate = pytesseract.image_to_string(Cropped_loc, lang='eng')
string_value = plate
s = ''.join(ch for ch in string_value if ch.isalnum())
plate = s
print("Numarul de inmatriculare detectat:", plate)
cv2.waitKey(0)
cv2.destroyAllWindows()
k = 0
with open('numere_inmatriculare.txt', 'r') as f:
        lines = []
        for line in f:
            lines.append(line)
            for part in line.split():
                if plate in part:
                    k = k + 1
                    words_in_line = line.split()
                    for x in words_in_line:
                        print("Bine ai venit, "+ words_in_line[1] + " "+ words_in_line[2]+"!")
                        break
                    print("Daca vreti sa intrati in parcare apasati butonul DA")
                    print("Daca vreti sa renuntati apasati butonul NU")
                    root = tk.Tk()
                    root.title("INTRARE PARCARE")
                    def onclick1():
                        for remaining in range(10, 0, -1): #in loc de 10(secunde) punem 3600 pentru a avea acces in parcare o ora
                            sys.stdout.write("\r")
                            sys.stdout.write("{:2d} secunde ramase.".format(remaining))
                            sys.stdout.flush()
                            time.sleep(1)

                        sys.stdout.write("\rTimpul a expirat!Va uram o zi buna!            \n")
                    def onclick2():
                        print("O zi frumoasa!")


                    btn1 = tk.Button(root, text="DA", command=onclick1)
                    btn2 = tk.Button(root, text="NU", command=onclick2)
                    btn1.pack()
                    btn2.pack()
                    root.mainloop()
if k == 0:
               print("Numarul dumneavoastra de inmatriculare nu este gasit.")