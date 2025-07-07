"""
# Change Log v0.3.2

1. Richer Sound Effects
2. High Score Recording
3. 800x600 Resolution
4. Dynamic Explosion Animation
"""

import sys
try:
	import pygame
	from pydub.generators import Square,WhiteNoise,Sawtooth,Sine,Triangle
	# from pydub.playback import play
	import pydub
except ImportError:
	print(f'Some modules are not installed, please install them:\n\033[7m{sys.executable} -m pip install pydub pyaudio audioop-lts -i https://pypi.tuna.tsinghua.edu.cn/simple\033[0m')
	input('Press enter to exit')
	sys.exit(1)
# from multiprocessing import Process
import hashlib
import os
import base64
import random
import threading
import time

class TmpFile:
	def __init__(self,data:bytes,end='.png'):
		self.path = os.path.join(os.path.expandvars('%temp%'),hashlib.sha256(data).hexdigest()+end)
		with open(self.path,'wb') as f:
			f.write(data)
		self.rmwdel = False
	def open(self,mode='rb',encoding=None):
		return open(self.path,mode,encoding=encoding)
	def __del__(self):
		if not self.rmwdel:
			return
		try:
			os.remove(self.path)
		except:
			pass
class Position:
	def __init__(self,x=0,y=0):
		self.x=x
		self.y=y
	def __add__(self,other):
		return Position(self.x+other.x,self.y+other.y)
	def __sub__(self,other):
		return Position(self.x-other.x,self.y-other.y)
	def __getitem__(self,key):
		if key==0:
			return self.x
		elif key==1:
			return self.y
		else:
			raise IndexError('Position has only 2 dimensions')
	def __setitem__(self,key,value):
		if key==0:
			self.x=value
		elif key==1:
			self.y=value
		else:
			raise IndexError('Position has only 2 dimensions')
	def __str__(self):
		return f'({self.x},{self.y})'
	def __repr__(self):
		return f'Position({self.x},{self.y})'
class Enemy:
	def __init__(self,pos:Position,speed=1):
		self.pos=pos
		self.speed=speed
		self.destory=False
	def update(self):
		if self.destory:
			self.destory+=1
			return
		self.pos.y+=self.speed
		self.pos.y=self.pos.y%140
	def draw(self,scr):
		if self.destory:
			p=image.subsurface(0,15+5*(self.destory//21),7,5)
			p=pygame.transform.flip(p,self.pos.x%2==1,self.pos.y%2==1)
			scr.blit(p, (self.pos.x-3, self.pos.y-4))
		else:
			scr.blit(image.subsurface(10,6,7,5), (self.pos.x-3, self.pos.y-4))
	def get_rect(self):
		if self.destory:
			return pygame.Rect(-100,-100,0,0)
		return pygame.Rect(self.pos.x-3, self.pos.y-6, 7, 4)
def fade(cid,fm:pygame.Color,to:pygame.Color,t=60):
	for i in range(t):
		r=fm[0]+(to[0]-fm[0])*i/t
		g=fm[1]+(to[1]-fm[1])*i/t
		b=fm[2]+(to[2]-fm[2])*i/t
		palette[cid]=(r,g,b)
		time.sleep(1/t)

def debug():
	global com
	while True:
		try:com=(input('> '))
		except:pass
def play_audio(audio_segment:pydub.AudioSegment):
	p=os.path.join(os.path.expandvars('%temp%'),hashlib.sha256(audio_segment.raw_data).hexdigest()+'.wav')
	if not os.path.exists(p):
		audio_segment.export(p,format='wav')
	# _thread.start_new_thread(play, (audio_segment))
	# t=threading.Thread(target=play,args=(audio_segment,))
	# t.daemon=True
	# t.start()
	pygame.mixer.Sound(p).play()
dbmode=0
if dbmode:import _thread
if dbmode:
	_thread.start_new_thread(debug,())
pygame.init()

shoot=Square(200,bit_depth=8).to_audio_segment(100,-35).overlay(Triangle(200,bit_depth=8).to_audio_segment(100,-40)).overlay(WhiteNoise(1000,bit_depth=8).to_audio_segment(100,-32))
shoot_e=Triangle(200,bit_depth=8).to_audio_segment(100,-40)
explode=WhiteNoise(1000,bit_depth=8).to_audio_segment(400,-20).overlay(Square(300,bit_depth=8).to_audio_segment(400,-30))
explode_e=Square(280,bit_depth=8).to_audio_segment(200,-40).overlay(WhiteNoise(800,bit_depth=8).to_audio_segment(100,-25))
# gmo=Square(170,bit_depth=8).to_audio_segment(400,-30)+Square(150,bit_depth=8).to_audio_segment(400,-30)+Square(140,bit_depth=8).to_audio_segment(400,-30)
# play_audio(gmo)
f=TmpFile(base64.b85decode(b'iBL{Q4GJ0x0000DNk~Le0000`0000W1Oos70CyeYUjP6A0drDELIAGL9O(c600d`2O+f$vv5yP<VFdsH01r@1R7C&)0RR90{{R60*Z_ZO09M-V2><{932;bRa{vGizyJUazyWI3i3tDz02p*dSaefwW^{L9a%BKeVQFr3E>1;MAT=&AE;t)$>Zkw!0JddVNoGk&DgX!o000F58UY0W0RR91N&o-=8vz9X0RR91QUCw|C;<Zi0RR910ssI2F#!Sq5C8xGS^xk5X@>*=0RR91Y5)KL00000zjgrt=mP)%zjgrt=mP)%P+@6qbS_RsR3J4jF)la&0{{S!2LJ>B001yDGcW<50{{U400031000G`1ONd5005K#00000000620RRF31ONa4QaLyP0ssd91ONa4FflMN00000OlYF{9nK2n0004;Nkl<ZILnPwZI*&C3`~FnB)A8#bq`>l9zc-$pJ^u_MfVR{9wp*1$xKor79}QTrq@NXZ>n}<2SAk-Ky2zyM1nwULo~Dm24h?qli(8(!ml?*ai(B(641Oe#-h%p{~3dpgUx~Z<#Hw92bI%E3dNfg&En|;NT?vBnq(JZbsDI@BZW5HgnGo>v~m*|qC3zQ+nZFGjHWsnGd1HwH^Ei1_GaL3x9%lIj)m7U>+C=Z53}KJK)9JeEm%8H%%Z5k^+?oet8`#r2}E5E<(;voZY{$Poq4XMsd1}YkK(JPsvh97A{{tiwmms}NmjnW04V-d0DtaPeVkaw02<04C4@vaD$AmBKC4_Mfu6cV;^GN%dQK|!tU8WQJ`&SfD>?u&-R{;tGnF*v!J8;PemGf|#XM9QZyVk7l*LR~8%T08=(M_rGCsGpK76W#cPcbDGBC~B!kcNUYm8r>tv+PQ_-f%g{Mvv@w0f^mgC8wi0ysXVdLSD$o+6rfpzF~oOq@K-lf&b>H=1KCJ^(+C*|)$y+2u;iukc8|00000NkvXXu0mjf'))

screen = pygame.display.set_mode((800, 600))
scr=pygame.Surface((160, 120),depth=8)

image=pygame.image.load(f.path).convert(8)
image.set_colorkey((255, 255, 255))
palette=[(b,b,b) for b in range(256)]
palette[0]=pygame.Color(32,32,32)
palette[2]=pygame.Color(255,32,32)
palette[3]=pygame.Color(255,255,32)
palette[4]=pygame.Color(255,160,32)

score=0
pos=Position(80,80)
enemies:list[Enemy]=[]
bullets:list[Position]=[]
enemies_bullets=[]
t=0
gameover=False
ct=0
gamespeed=60
com=''
max_bullets=3
lives=3
_dying=False
def die():
	global gameover,lives,_dying
	_dying=True
	if lives>0:
		lives-=1
	else:
		gameover=True
while not gameover:
	scr.set_palette(palette)
	scr.fill(255)
	image.set_palette(scr.get_palette())
	_launched=False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			if dbmode:_thread.exit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key in [pygame.K_SPACE,pygame.K_RETURN] and len(bullets)<max_bullets and not _launched:
				bullets.append(Position(pos.x,pos.y))
				scr.blit(image.subsurface(9,15,5,2),(pos.x-2,pos.y-3))
				play_audio(shoot)
				_launched=True
	scr.blit(image.subsurface(40,0,26,6), (1, 1))
	keys=pygame.key.get_pressed()
	speed=Position(1.5,1)
	if keys[pygame.K_LEFT] or keys[pygame.K_a]:
		pos.x-=speed.x
	if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
		pos.x+=speed.x
	if keys[pygame.K_UP] or keys[pygame.K_w]:
		pos.y-=speed.y
	if keys[pygame.K_DOWN] or keys[pygame.K_s]:
		pos.y+=speed.y
	pos.x=pos.x%160
	pos.y=max(0,min(116,pos.y))
	pr=pygame.Rect(pos.x-4, pos.y, 9, 5)

	for i in range(len(str(score))): # draw score
		c=int(str(score)[i])
		scr.blit(image.subsurface(c*4,0,4,6), (30+i*4, 1))
	for i in range(lives): # draw lives
		scr.blit(image.subsurface(9,18,5,5), (1+i*6, 7))
	for i in bullets:
		i.y-=1.5
		if i.y<0:
			bullets.remove(i)
			continue
		scr.blit(image.subsurface(10,12,1,2),tuple(i))
		for j in enemies:
			if j.get_rect().collidepoint(i.x,i.y):
				j.destory=1
				play_audio(explode_e)
				sp=100
				if j.speed==2:
					sp=500
					score+=400
				score+=100
				bullets.remove(i)
				if score%6000==3000 or (3500>score%6000>=3000 and sp==500):
					threading.Thread(target=fade,args=(0,palette[0],(255,255,255))).start()
					threading.Thread(target=fade,args=(255,palette[255],(32,32,32))).start()
				elif score%6000==4500 or (5000>score%6000>=4500 and sp==500):
					threading.Thread(target=fade,args=(255,palette[255],(255,255,255))).start()
					threading.Thread(target=fade,args=(0,palette[0],(32,32,32))).start()
				break
	for i in enemies_bullets:
		i.y+=1.2
		if i.y>120:
			enemies_bullets.remove(i)
			continue
		scr.blit(image.subsurface(12,12,3,2),(i.x-1,i.y))
		if pr.collidepoint(i.x,i.y):
			die()
			break
	for i in enemies:
		if i.destory>60:
			enemies.remove(i)
			continue
		i.update()
		if random.random()<.0025 and not i.destory:
			enemies_bullets.append(Position(i.pos.x,i.pos.y))
			play_audio(shoot_e)
		i.draw(scr)
		if i.get_rect().colliderect(pr):
			die()
	scr.blit(image.subsurface(0,6,9,8), (pos.x-4, pos.y-1))

	# scr.blit(image, (0, 0))
	screen.blit(pygame.transform.scale(scr,screen.get_size()), (0, 0))
	pygame.display.update()
	pygame.time.Clock().tick(gamespeed)
	# score+=1
	pygame.display.set_caption(f'Air War - Score: {score}')
	t+=1
	if t%60==0:
		if random.random()<.05:
			enemies.append(Enemy(Position(random.randint(3,157),0),2))
		else:
			enemies.append(Enemy(Position(random.randint(3,157),0),random.random()+.1))
	if com !='':
		try:
			exec(com)
		except:
			print('Invalid command')
		com=''
	if _dying:
		play_audio(explode)
		scr.blit(image.subsurface(15,16,15,15), (pos.x-7, pos.y-4))
		for _ in range(30):
			scr.set_palette(palette)
			screen.blit(pygame.transform.scale(scr,screen.get_size()), (0, 0))
			pygame.display.update()
			pygame.event.get()
			pygame.time.Clock().tick(30)
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					pygame.quit()
					if dbmode:_thread.exit()
					sys.exit()
		_dying=False
		enemies=[]
		enemies_bullets=[]
		bullets=[]
		pos=Position(80,80)
		t=0
pygame.display.set_caption(f'Air War - Game Over - Score: {score}')
scr.fill(255,(57,49,46,7))
scr.blit(image.subsurface(18,6,44,5),(58,50))
if os.path.exists(os.path.expandvars('%APPDATA%/AirWar-HighScore.dat')):
	with open(os.path.expandvars('%APPDATA%/AirWar-HighScore.dat'),'rb') as f:
		highscore=int.from_bytes(f.read(),'big')
else:
	highscore=-1
if score>highscore:
	highscore=score
	scr.fill(255,(59,55,42,6))
	scr.blit(image.subsurface(32,16,40,4),(60,56))
	with open(os.path.expandvars('%APPDATA%/AirWar-HighScore.dat'),'wb') as f:
		f.write(score.to_bytes(8,'big'))
while 1:
	for event in pygame.event.get():
		if event.type in [pygame.QUIT,pygame.KEYDOWN]:
			pygame.quit()
			if dbmode:_thread.exit()
			sys.exit()
	screen.blit(pygame.transform.scale(scr,screen.get_size()), (0, 0))
	pygame.display.update()
	pygame.time.Clock().tick(60)
