import sys
import cv2

encrypt={}
decrypt={}

def encode(b,im):
        i=0
        flag=1
        s=im.shape
        for x in range(s[0]):
                for y in range(s[1]):
                        if (i==len(b)):
                                z='/'
                                flag=0
                        elif b[i]==' ':
                                z='@'
                        elif b[i]=='\n':
                                z='\\n'
                        else:
                                z=b[i]
                        c1='{:b}'.format(im[x,y,0]).zfill(8)
                        c2='{:b}'.format(im[x,y,1]).zfill(8)
                        c3='{:b}'.format(im[x,y,2]).zfill(8)
                        cb='{:b}'.format(encrypt[z]).zfill(6)
                        c1=c1[0:6]+cb[0:2]
                        c2=c2[0:6]+cb[2:4]
                        c3=c3[0:6]+cb[4:6]
                        im[x,y,0]=int(c1,2)
                        im[x,y,1]=int(c2,2)
                        im[x,y,2]=int(c3,2)
                        if(flag==0):
                                return im
                        else:
                                i+=1		


def decode(im,key):
		img=cv2.imread(im,1)
		mssg=''
		s=img.shape
		for x in range(s[0]):
			for y in range(s[1]):
				c1='{:b}'.format(img[x,y,0]).zfill(8)
				c2='{:b}'.format(img[x,y,1]).zfill(8)
				c3='{:b}'.format(img[x,y,2]).zfill(8)
				
				cc=c1[8-2:8]+c2[8-2:8]+c3[8-2:8]
				cc=int(cc,2)
				if cc>=40:
					return mssg
				if cc == 37:
					mssg+=' '
				else:
					mssg+=decrypt[cc]
								
				

def main(a):
	sym=a[1]
	fname=a[2]
	imgname=a[3]
	fp=open(sym,'r')
	buf=fp.read().split('\n')
	for x in buf:
		x=x.split(' ')
		if len(x) == 2:
			encrypt.update({x[1]:int(x[0])})
			decrypt.update({int(x[0]):x[1]})	
	fp.close()
	fp=open(fname,'r')
	img=cv2.imread(imgname,1)
	s=img.shape
	s=s[0]*s[1]
	buf=fp.read()
	f=len(buf)
	if (f >= s):
		print("ERROR: Message size too large, choose a larger image")
	else:
		im=encode(buf,img)
		cv2.imwrite('encry.tiff',im)		
		cv2.imshow('IMAGE',im)
		cv2.waitKey(0)
		
	mssg=decode('encry.tiff',2)	
	print("decrypted msg: ",mssg)
	fp=open('dec_msg.txt','w')
	fp.write(mssg)
	fp.close()
	print("open file Decode.txt to view your decrypted message")
if __name__=='__main__':
	main(sys.argv)
	
