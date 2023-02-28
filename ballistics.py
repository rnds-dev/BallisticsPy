from tkinter import *
from math import cos, sin, tan, atan
from time import sleep, time
sc = 10 #10 px = 1 m
x = 1080
scrn = x / 1080

bg ='#101010'
bg_sec = '#202020'
abg = '#404349'
ctext = '#c1cacf'
aaaa = '#8fbaa6'
drkGr = '#8f9295'
Cbtn = ['#89b4a4', "#a8b9d0", '#93beae', '#b2c3da']
fnt = 'Arial'
h1 = 935*scrn

start = False
window = Tk()
window.title('Bulletistic movement')
window.state('zoomed')
window.geometry(str(int(1920*scrn)) + 'x' + str(int(1080*scrn)))
window.wm_attributes('-alpha', 0.99)

cnvs = Canvas(window, width = 1920*scrn, height = 1080*scrn, highlightthickness = 0, bg = bg)
cnvs.place(x = 0, y = 0)
cnvsB = Canvas(window, width = 1620*scrn, height = 935*scrn, highlightthickness = 0, bg = bg_sec)
cnvsB.place(x = 40*scrn, y = 40*scrn)

Label(window, text="ПАРАМЕТРЫ", font = ('Arial Black', int(17*scrn)), bg = bg, fg = aaaa, justify=CENTER).place(x = 1670*scrn, y = 40*scrn)
Label(window, text="Y", font = ('Arial', int(13*scrn)), bg = bg, justify=CENTER, fg = drkGr).place(x = 40*scrn, y = 15*scrn)
Label(window, text="X", font = ('Arial', int(13*scrn)), bg = bg, justify=CENTER, fg = drkGr).place(x = 1640*scrn, y = 975*scrn)

def stop(info, c):
	global start, T, sc, g, pos, h1
	start = False
	st_end = ['T = ' + str(round(T, 2))+' s'+' '*5, 'L = ' + str(round((pos[0]/sc)/scrn, 2))+' m'+' '*5, 'H = ' + str(round((((935*scrn)-h1)/sc)/scrn, 2))+' m'+' '*5, info]
	cnvsB.itemconfig(trgt, fill = Cbtn[c])
	for i in range(4):
		Label(window, text= st_end[i], font = (fnt, int(15*scrn)), bg = bg_sec, fg = ctext, width = 0, justify = LEFT).place(x = 50*scrn, y = (50+30*i)*scrn)
		cnvsB.create_rectangle(50*scrn, (50+30*i)*scrn, 100*scrn, (50+25+30*i)*scrn, fill = bg_sec, width = 0)
	h1 = 935*scrn

def motion():
	global start, vx, k1, k2, vy, m,g,T, L, R, sc, H, V, x,y, pos, h1
	while start:
		bullet(x,y)
		pos = cnvsB.coords(blt)
		if pos[3]<h1:
			h1 = pos[3]

		if V < 0.001:
			stop('V = 0' + ' '*3, 1)

		if H != 0 or L != 0 or R != 0:
			if (((L*sc)-2)*scrn<=pos[0]<=((L*sc)+2)*scrn and (935-(H)*sc)*scrn>=pos[1]>=(935-(H+2*R)*sc)*scrn) or (L*sc*scrn<=pos[0]<=(L+2*R)*sc*scrn and (935 - H*sc - 1)*scrn<=pos[1]<=(935 - H*sc + 1)*scrn):
				stop('Got it'+ ' '*3, 0)
	
			elif (935 - (H+2*R)*sc -2)*scrn <=pos[1]<=(935 - (H+2*R)*sc + 2)*scrn and L*sc*scrn<=pos[0]<=(L+2*R)*sc*scrn:
				stop('Got it'+ ' '*3, 0)
	
		if not(0<=pos[0]) or not(pos[3]<=935*scrn +1):
			stop('Miss', 1)

		t = 0.01
		vx -= (k1 + k2*((vx**2+vy**2)**0.5))*vx*t/m
		vy -= ((k1 + k2*((vx**2+vy**2)**0.5))*vx+m*g)*t/m
		x += vx * t
		y -= vy * t
		T += t
		sleep(0.001)
		window.update()

def bullet(x,y):
	global blt, sc, scrn
	blt = cnvsB.create_oval((int(x*sc*scrn), int((935+y*sc)*scrn)-1, 1+int(x*sc*scrn),int((935+(y*sc))*scrn)), fill = ctext, width = 0)
def act(action):
	global start, vx, vy, sc, T, v, y, k1, k2, m, L, R, H, V, x,y, trgt, l, scrn
	def dlt(v):
		v.delete(0, END)
	def value(v):
		return float('0' + v.get())

	if action == 'CLEAR':
		for i in range(5):
			dlt(l[i])
	if action == 'START': 
		start = True
		cnvsB.delete(ALL)

		L, H, R = value(trgtL), value(trgtH), value(trgtR)
		V, A, Pb = value(bulletV), value(bulletA), value(bulletP)
		p_env, nu_env = value(envP), value(envNu)
		
		T, r = 0, 1
		k1 = 6*3.14*nu_env
		k2 = 0.2*3.14*r*r*p_env
		m = 4*3.14*(r**3)*Pb/3

		trgt = cnvsB.create_oval(int(L*sc*scrn), int(935-(H+2*R)*sc)*scrn, int((L+2*R)*sc*scrn), int((935-H*sc)*scrn), fill = Cbtn[1], width = 0)
		alf = A*3.14/180
		x, y = 0, 0
		vx = V*cos(alf)
		vy = V*sin(alf)
		motion()

g = 9.81		
text = ['Target', 'Projectile', 'Environment', "Target Radius R", 'Target Distance L', 'Target Height H',
'Beginning projectile speed V₀', 'Angle to the horizon α ⁰', 'Material density', 'Media density',
'Media viscosity', 'START', 'CLEAR']

def entr():
	return Entry(window,  font=(fnt,int(14*scrn)), fg = ctext, bg = bg_sec,  borderwidth = 0, justify = CENTER)
def plc(v, y1, y2):
	v.place(x = 1670*scrn, y = (y1 + y2)*scrn, width = 240*scrn, height = 28*scrn)
def ins(v, i):
	l = ['7800', '1.29','0.0182']
	v.insert(0, l[i])
def btn(bg_sectn, txt, i, afg):
	btn = Button(window, text=txt, bg = bg_sec, fg = bg_sectn, activebackground = '#404349', activeforeground = afg, font=('Arial Black', int(13*scrn)), borderwidth = 0, command=lambda: act(txt))
	btn.place(x = 1670*scrn, y = (863+(55+2)*i)*scrn, width = 240*scrn, height = 55*scrn)
def lines(x1L, y1L, x2L, y2L, xT, yT, i):
	cnvs.create_line(x1L*scrn, y1L*scrn, x2L*scrn, y2L*scrn, fill = drkGr, width = 1)
	cnvs.create_text(xT*scrn, yT*scrn, text=str(int(i*5))+'m', justify=CENTER, font=(fnt, int(7*scrn)), fill = drkGr)

trgtR = entr()
trgtL = entr()
trgtH = entr()
bulletV = entr()
bulletA = entr()
bulletP = entr()
envP = entr()
envNu = entr()
l = [trgtR, trgtL, trgtH, bulletV, bulletA, bulletP, envP, envNu]

for i in range(31):
	lines(40+(i+1)*50, 975-3, 40+(i+1)*50, 975+3, 40+(i+1)*50, 975+15, i+1)		#lines on OX
	if i<3:
		plc(l[i], 145, 75*i)
		plc(l[i+3], 418, 75*i)
		ins(l[i+5], i)
		Label(window, text=text[i], font = (fnt, int(15*scrn)), bg = bg, fg = aaaa).place(x = 1670*scrn, y = (80+270*i)*scrn)						#Titles
	if 3<=i<5:
		plc(l[i+3], 691, 75*(i-3))
	if i < 18:
		lines(40-3, 975-(i+1)*50, 40+3, 975-(i+1)*50, 20-3, 975-(i+1)*50, i+1)	#lines on OY
	if i < 8:
		Label(window, text=text[i+3], font = (fnt, int(13*scrn)), bg = bg, fg = ctext).place(x = 1670*scrn, y = (115 + (i%3)*75 + (270*(i//3)))*scrn)	#text in blocks
	if i < 2:
		btn(Cbtn[i], text[i+11], i, Cbtn[i+2])																					#buttons
while not start:
	window.update()
window.mainloop()