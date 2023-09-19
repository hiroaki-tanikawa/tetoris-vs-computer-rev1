from pygame.locals import *
import pygame
import sys
import numpy as np
import random
import time

pygame.init()
#画面表示-----------------
Scale=0.7##########################画面に合わせてサイズ調整
#ブロックN数
n_h=20  #高さ
n_w=10  #横
#テトリスプレイ領域大きさ
Sc_height=950*Scale #高さ
Sc_width=Sc_height/2#幅
#ブロック大きさ
b_h=Sc_height/n_h
b_w=Sc_width/n_w
#バックスクリーン大きさ
back_height=Sc_height+b_h*2 #高さ 上:ブロック1個分空け
back_width=Sc_width*2+b_w*6*2#幅  左:ブロック3個分空け
#回転領域正方形1辺長さ
b_n=4 
#-------------------------
#フォントサイズ---------------------
fontsize=50
font = pygame.font.Font(None,fontsize)

#スタート画面--------------
background_color=(10,10,100)#背景色
back_color=(10,10,50)#テトリスエリア背景色
block_color=(200,200,200)#ブロック色
                                     
screen    = pygame.display.set_mode(((back_width),(back_height)))
screen.fill(background_color)
fonts = pygame.font.Font(None,int(Scale*(250)))
texts = fonts.render('TETORIS',True,(200,55,55))
screen.blit(texts,[int(Scale*(350)),int(Scale*(300))])      

fontss = pygame.font.Font(None,int(Scale*(100)))
textss = fontss.render('vs COMPUTER',True,(255,255,255))
screen.blit(textss,[int(Scale*(500)),int(Scale*(500+100))])   
pygame.display.update()

# 初期設定----------------
i,j=int(n_w/3),1
block_choice=1
block_N=5 #ブロックの種類
# ①ブロック
BlockLoca=np.zeros([n_h+2,n_w+2])
BlockLoca_me=np.zeros([n_h+2,n_w+2])
BlockLoca_pc=np.zeros([n_h+2,n_w+2])
# ②ブロック(1ターン進行)
BlockLoca_pro=np.zeros([n_h+2,n_w+2])
# ③背景
BackDisp=np.zeros([n_h+2,n_w+2]) 
BackDisp[:,0]=1
BackDisp[:,n_w+1]=1
BackDisp[n_h+1,:]=1
BackDisp_me=np.zeros([n_h+2,n_w+2]) 
BackDisp_me[:,0]=1
BackDisp_me[:,n_w+1]=1
BackDisp_me[n_h+1,:]=1
BackDisp_pc=np.zeros([n_h+2,n_w+2]) 
BackDisp_pc[:,0]=1
BackDisp_pc[:,n_w+1]=1
BackDisp_pc[n_h+1,:]=1
# ④表示用(背景+ブロック)
ShowDisp=np.zeros([n_h+2,n_w+2])
ShowDisp_me=np.zeros([n_h+2,n_w+2])
ShowDisp_pc=np.zeros([n_h+2,n_w+2])
Block_small=np.zeros([b_n,b_n])
Block_small_rotate=np.zeros([b_n,b_n])
#-------------------------

def init():
 BackDisp[:,:]=np.zeros([n_h+2,n_w+2])
 BackDisp[:,0]=1
 BackDisp[:,n_w+1]=1
 BackDisp[n_h+1,:]=1
 BlockLoca_pro[:,:]=np.zeros([n_h+2,n_w+2])
 BlockLoca[:,:]=np.zeros([n_h+2,n_w+2])


def ini_block(block_choice):
    
    i,j=int(n_w/3),1
    BlockLoca=np.zeros([n_h+2,n_w+2])   
    # L字型
    if block_choice==1:
        BlockLoca[j][i+1]=1
        BlockLoca[j+1][i+1]=1
        BlockLoca[j+2][i+1]=1
        BlockLoca[j+2][i+2]=1
    # o字型
    elif block_choice==2:   
        BlockLoca[j+1][i+1]=1
        BlockLoca[j+2][i+1]=1
        BlockLoca[j+2][i+2]=1
        BlockLoca[j+1][i+2]=1
    # I字型
    elif block_choice==3:
        BlockLoca[j][i+1]=1
        BlockLoca[j+1][i+1]=1
        BlockLoca[j+2][i+1]=1
        BlockLoca[j+3][i+1]=1
    # Z字型
    elif block_choice==4:
        BlockLoca[j][i+1]=1
        BlockLoca[j+1][i+1]=1
        BlockLoca[j+1][i+2]=1
        BlockLoca[j+2][i+2]=1
    # 逆Z字型
    elif block_choice==5:
        BlockLoca[j][i+2]=1
        BlockLoca[j+1][i+2]=1
        BlockLoca[j+1][i+1]=1
        BlockLoca[j+2][i+1]=1
    return i,j,BlockLoca

def move_state():
 right,left,down,drop,p_rotate,m_rotate=False,False,False,False,False,False      
 if event.key==pygame.K_RIGHT: right=True #右進行
 if event.key==pygame.K_LEFT: left=True #左進行 
 if event.key==pygame.K_DOWN: down=True #下進行  
 if event.key==pygame.K_UP: drop=True #急落下
 if event.key==pygame.K_f: p_rotate=True#右回転
 if event.key==pygame.K_s: m_rotate=True#左回転  
 return right,left,down,drop,p_rotate,m_rotate

def block_90deg_rotate(i,j,b_n,BlockLoca):
 
 Block_small=np.zeros([b_n,b_n])
 Block_small_rotate=np.zeros([b_n,b_n])
 if i<n_w-(b_n-2) and i>0 and j<n_h-(b_n-2):   
  Block_small[0:b_n,0:b_n]=BlockLoca[j:j+b_n,i:i+b_n]
  for k in range (0,b_n,1):
    Block_small_rotate[k,:]=Block_small[::-1,k]
  BlockLoca_pro[:,:]=np.zeros([n_h+2,n_w+2])
  BlockLoca_pro[j:j+b_n,i:i+b_n]=Block_small_rotate[:,:]
  if np.all((BlockLoca_pro[:,:]+BackDisp[:,:])<2): 
   BlockLoca[:,:]=BlockLoca_pro[:,:]
 return i,j,BlockLoca
  
def block_m90deg_rotate(i,j,b_n,BlockLoca):
 
 Block_small=np.zeros([b_n,b_n])
 Block_small_rotate=np.zeros([b_n,b_n])
 if i<n_w-(b_n-2) and i>0 and j<n_h-(b_n-2):   
  Block_small[0:b_n,0:b_n]=BlockLoca[j:j+b_n,i:i+b_n]
  for k in range (0,b_n,1):
    Block_small_rotate[:,k]=Block_small[k,::-1]
  BlockLoca_pro[:,:]=np.zeros([n_h+2,n_w+2])
  BlockLoca_pro[j:j+b_n,i:i+b_n]=Block_small_rotate[:,:]
  if np.all((BlockLoca_pro[:,:]+BackDisp[:,:])<2): 
   BlockLoca[:,:]=BlockLoca_pro[:,:]
 return i,j,BlockLoca 

def block_move(i,j,BlockLoca,BackDisp,right,left,down,drop):
 i_new,j_new = i,j

 #ドロップ----------------------
 if drop==True:
  #ブロックを仮に移動
  BlockLoca_pro[:,:]= np.zeros([n_h+2,n_w+2])   
  for pro in range (1,n_h+2,1): 
   for m in range (1,n_w+1,1):
    for n in range (1,n_h+1,1): 
     if BlockLoca[n][m]==1:   
       BlockLoca_pro[n+pro][m]=1  
   for k in range (0,n_h+2,1):
    if max(BlockLoca_pro[k,0:n_w+2]+BackDisp[k,0:n_w+2])>1:
     i_new,j_new=i,j+pro-1
     drop=False
     break
   if drop==False:
    break
  
  BlockLoca_pro[:,:]= np.zeros([n_h+2,n_w+2])
  for m in range (1,n_w+1,1):
   for n in range (1,n_h+1,1): 
    if BlockLoca[n][m]==1:
     BlockLoca_pro[n+(j_new-j)][m]=1
     BackDisp_me[n+(j_new-j)][m]=1

 #1マス移動
 if right==True: 
   i_new=i+1
   BlockLoca_pro[:,:]= np.zeros([n_h+2,n_w+2])   
 elif left==True: 
   i_new=i-1
   BlockLoca_pro[:,:]= np.zeros([n_h+2,n_w+2])   
 elif down==True: 
   j_new=j+1
   BlockLoca_pro[:,:]= np.zeros([n_h+2,n_w+2])   
  #ブロックを仮に移動
 for m in range (1,n_w+1,1):
  for n in range (1,n_h+1,1): 
   if BlockLoca[n][m]==1:
    BlockLoca_pro[n+(j_new-j)][m+(i_new-i)]=1

 for k in range (0,n_h+2,1):
  if max(BlockLoca_pro[k,0:n_w+2]+BackDisp[k,0:n_w+2])>1:
   i_new,j_new = i,j
   BlockLoca_pro[:,:]=BlockLoca[:,:]
   break
 i,j=i_new,j_new
 BlockLoca[:,:]=BlockLoca_pro[:,:] 
 return i,j,BlockLoca,BackDisp

def block_drop_pc(BlockLoca_pc,BackDisp_pc):
 BlockLoca_pro_pc=np.zeros([n_h+2,n_w+2])
 for pro in range (1,n_h+1,1):
  BlockLoca_pro_pc[0+pro:n_h+2,:]=BlockLoca_pc[0:n_h+2-pro,:]
  if np.any((BlockLoca_pro_pc+BackDisp_pc)>=2):
     BlockLoca_pc=np.zeros([n_h+2,n_w+2]) 
     BlockLoca_pc[0:n_h+1,:]=BlockLoca_pro_pc[1:n_h+2,:]
     break 
 return BlockLoca_pc

def block_put(BlockLoca,BackDisp):
       #背景にブロック書く
       for m in range (1,n_w+2,1):
        for n in range (1,n_h+2,1): 
         if BlockLoca[n][m]==1:
          BackDisp[n][m]=1
       return BackDisp          
       
def show_display(i,j,put_me=False,put_pc=False):
 if GameLoop==True and put_me==True:
    pygame.draw.rect\
    (screen,back_color,pygame.Rect(b_w*3,b_h,Sc_width,Sc_height))
    pygame.draw.rect\
    (screen,(200,200,200),pygame.Rect(b_w*3,b_h,Sc_width,Sc_height),1)

    ShowDisp_me[:,:]=BackDisp_me[:,:]+BlockLoca_me[:,:]
    for k in range (1,n_h+1,1):
      for l in range (1,n_w+1,1):   
        if ShowDisp_me[k][l]>0:
            pygame.draw.rect\
            (screen,block_color,pygame.Rect(3*b_w+(l-1)*b_w,b_h+(k-1)*b_h, b_w-2, b_h-2))
    pygame.display.update() 

 elif GameLoop==True and put_pc==True:
    pygame.draw.rect\
    (screen,back_color,pygame.Rect(9*b_w+Sc_width,b_h,Sc_width,Sc_height))
    pygame.draw.rect\
    (screen,(200,200,200),pygame.Rect(9*b_w+Sc_width,b_h,Sc_width,Sc_height),1)

    ShowDisp_pc[:,:]=BackDisp_pc[:,:]+BlockLoca_pc[:,:]
    for k in range (1,n_h+1,1):
      for l in range (1,n_w+1,1):   
        if ShowDisp_pc[k][l]>0:
            pygame.draw.rect\
            (screen,block_color,pygame.Rect(9*b_w+Sc_width+(l-1)*b_w,b_h+(k-1)*b_h, b_w-2, b_h-2))
    pygame.display.update()

def show_points():
 pygame.draw.rect\
 (screen,background_color,pygame.Rect(0,0,b_w*3,b_h*6))
 font_s = pygame.font.Font(None,int(Scale*(80)))
 text_you = font_s.render('YOU',True,(200,200,200))
 point_you = font_s.render(str(delete_lines_me),True,(200,200,200))
 screen.blit(text_you,[int(0),int(3*n_w)])
 screen.blit(point_you,[int(0),int(6*n_w)]) 
 pygame.draw.rect\
 (screen,background_color,pygame.Rect(Sc_width+b_w*5,0,b_w*3,b_h*6))
 text_com = font_s.render('COM',True,(200,200,200))
 point_com = font_s.render(str(delete_lines_pc_r),True,(200,200,200))
 screen.blit(text_com,[int(Sc_width+18*n_w),int(3*n_w)])   
 screen.blit(point_com,[int(Sc_width+18*n_w),int(6*n_w)])          
 

def escape():
  pygame.quit()
  sys.exit()

# メインプログラム--------------------------------------------------------------------
GameLoop=False
delete_lines_me=0
delete_lines_pc_r=0 
while True:
 #ゲーム開始前
 for event in pygame.event.get():
    if event.type == KEYDOWN:
        #画面クローズ
        if event.type == QUIT or event.key == K_ESCAPE: escape()
        #ゲーム開始
        elif event.key == K_SPACE:
          GameLoop=True 
          init()
          for p in range(1,n_h+1):
            BackDisp_me[p,1:n_w+1]=0
            BackDisp_pc[p,1:n_w+1]=0
          block_choice=random.randint(1,block_N)  
          i_me,j_me,BlockLoca_me=ini_block(block_choice)
          i_pc,j_pc,BlockLoca_pc=ini_block(block_choice)
          screen.fill(background_color)
          show_display(i_me,j_me,put_me=True,put_pc=False)
          show_display(i_pc,j_pc,put_me=False,put_pc=True)
  
 while GameLoop==True:
  time=pygame.time.get_ticks()
  show_points()
  #ブロック置き(自動：プレイヤー)---------------
  put_me=False
  for k in range(1,n_h+1,1):
     for l in range(1,n_w+1,1):   
      if BlockLoca_me[k,l]==1 and BackDisp_me[k+1,l]== 1:
       BackDisp_me=block_put(BlockLoca_me,BackDisp_me)#ブロック置き
       block_choice=random.randint(1,block_N)
       i_me,j_me,BlockLoca_me=ini_block(block_choice)#ブロック初期配置
       put_me=True
       break
     if put_me==True:break
     
  #ブロック消し(自動：プレイヤー)---------------
  for k in range (1,n_h+1,1):        
     if np.all(BackDisp_me[k,1:n_w+1])==np.all(np.ones([1,n_w])):
      BackDisp_me[1:k+1,1:n_w+1]=BackDisp_me[0:k,1:n_w+1]
      delete_lines_me+=1

  #ゲームオーバー(プレイヤー)---------------
  if np.any(BackDisp_me[1,1:n_w+1])>0:
    GameLoop=False
    screen.fill(back_color)
    fontsize=100
    font = pygame.font.Font(None,fontsize)
    text_surface = font.render("GAME OVER", True, (200,100,100))
    screen.blit(text_surface,[back_width/4,back_height/2.4])
    pygame.display.update()
    break           
  #ゲームオーバー(COM)---------------
  elif np.any(BackDisp_pc[2,1:n_w+1])>0:
    GameLoop=False
    screen.fill(back_color)
    fontsize=100
    font = pygame.font.Font(None,fontsize)
    text_surface = font.render("YOU WIN!!!", True, (200,100,100))
    screen.blit(text_surface,[back_width/4,back_height/2.4])
    pygame.display.update()
    break  
  
  #時間おきのブロック自動落下(プレイヤー)-----------------------------------
  elif np.mod(time,1500)==0:
    right_me,left_me,down_me,drop_me=False,False,True,False   
    i_me,j_me,BlockLoca_me,BackDisp_me = block_move(i_me,j_me,BlockLoca_me,BackDisp_me,right_me,left_me,down_me,drop_me)
    show_display(i_me,j_me,put_me=True,put_pc=False)

  #COM操作--------------------------------------------------------
  elif np.mod(time,1000)==0:
       #ブロック落とし方評価------------------------------
      List      =[] 
      value=0
      deadspace=0
      takasa=np.zeros([n_w+1])

      block_choice_pc=random.randint(1,block_N)
      for move_N in range(-n_w+1,n_w+1,1):#ブロック位置
          for rotate_N in range(0,4):#ブロック回転
               i_pc,j_pc,BlockLoca_pro_pc=ini_block(block_choice_pc)

               value=0
               for k in range(0,rotate_N+1):
                 i,j,BlockLoca_pro_pc=block_90deg_rotate(i_pc,j_pc,b_n,BlockLoca_pro_pc)         
               move_pc=True
               for n in range(1,n_h+1):
                  for m in range(1,n_w+1):             
                      if (m+move_N)<1 and BlockLoca_pro_pc[n][m]==1 or (m+move_N>n_w) and BlockLoca_pro_pc[n][m]==1:  
                          i_pc=int(n_w/3)
                          move_pc=False
                          value=-100000000#ブロック一部が枠外の場合得点マイナス
                          break
                  if move_pc==False:break      

               if move_pc==True:
                  i_pc=int(n_w/3)+move_N
                  BlockLoca_pc=np.zeros([n_h+2,n_w+2]) 
                  for n in range(1,n_h+1):
                     for m in range(1,n_w+1):        
                        if BlockLoca_pro_pc[n][m]==1:            
                          BlockLoca_pc[n][m+move_N]=1
                  
                  if np.all(BlockLoca_pc==0):value=-100000000 #ブロックすべてが枠外の場合も得点マイナス
                      
               BlockLoca_pro_pc[:][:]=BlockLoca_pc[:][:]
               BlockLoca_pc=np.zeros([n_h+2,n_w+2])#BlockLoca_pcはzeroに戻しておきたい。ブロック落下してしまう。 
               #仮にドロップさせる--------------
               BlockLoca_pro_pc=block_drop_pc(BlockLoca_pro_pc,BackDisp_pc) 
               BackDisp_pro_pc=BlockLoca_pro_pc[:,:]+BackDisp_pc[:,:]#BackDisp_pcは本チャンなので書き換えない

               ###テトリスAI評価-------------------------------------------------------------
               sukima=0
               hikusa=0  
               for m in range (1,n_w+1,1):                
                for n in range (1,n_h+1,1): 
                 if BlockLoca_pro_pc[n][m]>=1:
                  if BackDisp_pro_pc[n+1][m]==0:sukima=sukima+1#F5: 閉じてはないがブロックが入らないスペースの数    
                  if BackDisp_pro_pc[n][m+1]==0:sukima=sukima+1
                  if BackDisp_pro_pc[n][m-1]==0:sukima=sukima+1
                  hikusa=hikusa+n#F1: 置いたブロックの低さ

               delete_lines_pc=0
               for k in range (1,n_h+1,1):        
                if np.all(BackDisp_pro_pc[k,:]>=1):
                 delete_lines_pc=delete_lines_pc+1
               value_delete=(delete_lines_pc**3)*1 #F6: 消したライン数

               tetoris_bonus=0 #F7: 4ライン消しボーナス  
               for n in range (4,n_h+1-4,1): 
                if np.all(BackDisp_pro_pc[n,1:n_w+1]>=1) and \
                  np.all(BackDisp_pro_pc[n+1,1:n_w+1]>=1) and \
                  np.all(BackDisp_pro_pc[n+2,1:n_w+1]>=1) and \
                  np.all(BackDisp_pro_pc[n+3,1:n_w+1]>=1):
                  tetoris_bonus=1
 
               deadspace=0
               for m in range (1,n_w+1,1):
                for n in range (n_h,1,-1):
                 if BackDisp_pro_pc[n][m]==0:
                   i=n  
                   d_deadspace=0 
                   while BackDisp_pro_pc[i][m]==0:  
                     d_deadspace=d_deadspace+1
                     if i<1:
                         d_deadspace=0
                         break
                     i=i-1
                   deadspace=deadspace+d_deadspace #F4: 閉じたスペースの数 
                       
               for m in range (1,n_w+1,1):
                for n in range (1,n_h+1,1):
                 if BackDisp_pro_pc[n][m]==1:
                   takasa[m]=n_h-n+1
                   break 
               takasa_sum=sum(takasa)
               
               takasa_ave=takasa_sum/n_w
               tosyutsu=0 
               for m in range (1,n_w+1,1): 
                    for n in range (1,n_h-int(takasa_ave+4)+1,1): 
                     if BackDisp_pro_pc[n][m]==1:
                         tosyutsu=tosyutsu+1#F3: 飛び出た列の数

               takasa_migi=np.zeros([n_w+1])
               takasa_migi[0:n_w]=takasa[1:n_w+1]
               koteisa=np.zeros([n_w])                     
               koteisa[:]=abs(takasa_migi[0:n_w]-takasa[0:n_w])#F2: 周りのブロックとの高低差
               koteisa_sum=sum(koteisa[1:n_w+1])

               four_mizo=0 #F8: 4ライン消しできる隙間が作れるか
               for n in range (4,(n_h+1)-3,1):
                #右端に溝/左端に溝              
                if np.all(BackDisp_pro_pc[n,1:n_w]==1) and BackDisp_pro_pc[n,n_w]==0 and \
                   np.all(BackDisp_pro_pc[n+1,1:n_w]==1) and BackDisp_pro_pc[n+1,n_w]==0 and \
                   np.all(BackDisp_pro_pc[n+2,1:n_w]==1) and BackDisp_pro_pc[n+2,n_w]==0 and  \
                   np.all(BackDisp_pro_pc[n+3,1:n_w]==1) and BackDisp_pro_pc[n+3,n_w]==0 or \
                   BackDisp_pro_pc[n,1]==0 and np.all(BackDisp_pro_pc[n,2:n_w+1]==1) and \
                   BackDisp_pro_pc[n+1,1]==0 and np.all(BackDisp_pro_pc[n+1,2:n_w+1]==1) and \
                   BackDisp_pro_pc[n+2,1]==0 and np.all(BackDisp_pro_pc[n+2,2:n_w+1]==1) and \
                   BackDisp_pro_pc[n+3,1]==0 and np.all(BackDisp_pro_pc[n+3,2:n_w+1]==1):
                   four_mizo=1
               
               #F=評価項目--------------------------------
               F1=hikusa       #F1: 置いたブロックの低さ
               F2=koteisa_sum  #F2: 周りのブロックとの高低差
               F3=tosyutsu     #F3: 飛び出た列の数
               F4=deadspace    #F4: 閉じたスペースの数
               F5=sukima       #F5: 閉じてはないがブロックが入らないスペースの数    
               F6=value_delete #F6: 消したライン数
               F7=tetoris_bonus#F7: 4ライン消しボーナス
               F8=four_mizo    #F8: 4ライン消しできる隙間が作れるか
               #-----------------------------------------
               #a=重み(重要度)----------------------------
               a1=50  #置いたブロックの低さ
               a2=-10 #周りのブロックとの高低差
               a3=-10 #飛び出た列の数
               a4=-80 #閉じたスペースの数
               a5=0   #閉じてはないがブロックが入らないスペースの数    
               a6=200 #消したライン数
               a7=0   #4ライン消しボーナス
               a8=5   #4ライン消しできる隙間が作れるか
               #------------------------------------------
               #評価関数-----------------------------------
               value=value+a1*F1+a2*F2+a3*F3+a4*F4+a5*F5+a6*F6+a7*F7+a8*F8 
               #-------------------------------------------
               if np.any((BlockLoca_pc[:,:]+BackDisp_pc[:,:])>=2):value=-10000000 #重複防止
               #評価値リスト
               List.append([i_pc,rotate_N,int(value)])               

      #点数の高いものを選ぶ------------
      value_list=[]
      for a in range(len(List)):
       value_list.append(List[a][2])#valueをappendしリスト作成
      index=np.argmax(value_list)#value最大のindex
      i_pc     =int(List[index][0])
      rotate_N =int(List[index][1])
      value    =int(List[index][2])

      #正式にドロップさせる-----------------
      BlockLoca_pc=np.zeros([n_h+2,n_w+2])
      i_pc,j_pc,BlockLoca_pro_pc=ini_block(block_choice_pc)
      BlockLoca_pc[:,:]=BlockLoca_pro_pc[:,:] 
      show_display(i_pc,j_pc,put_me=False,put_pc=True)
      
      for k in range(0,rotate_N+1):
        i,j,BlockLoca_pro_pc=block_90deg_rotate(int(n_w/3),j_pc,b_n,BlockLoca_pro_pc)
      show_display(i_pc,j_pc,put_me=False,put_pc=True)

      i_pc_ini=int(n_w/3)
      i_pc=int(List[index][0])
      d_i_pc=i_pc-i_pc_ini
      BlockLoca_pc=np.zeros([n_h+2,n_w+2])         
      for m in range (1,n_w+1,1):
        for n in range (1,n_h+1,1):
          if BlockLoca_pro_pc[n][m]>=1:
             BlockLoca_pc[n][m+d_i_pc]=1 #落下前：ここでやっとBlockLoca_pcを書き換える

      show_display(i_pc,j_pc,put_me=False,put_pc=True)     
      BlockLoca_pc[:,:] =block_drop_pc(BlockLoca_pc,BackDisp_pc)#落下後
      BackDisp_pc[:,:]=BlockLoca_pc[:,:]+BackDisp_pc[:,:]
      
      #ブロック消し---------------
      for k in range (1,n_h+1,1):        
       if np.all(BackDisp_pc[k,1:n_w+1]>=1):
        BackDisp_pc[1:k+1,1:n_w+1]=BackDisp_pc[0:k,1:n_w+1]
        delete_lines_pc_r+=1  
 
  #プレイヤー操作--------------------------------------------------------
  for event in pygame.event.get():
   if event.type == KEYDOWN:
    #ブロック移動
    right_me,left_me,down_me,drop_me,p_rotate_me,m_rotate_me = move_state()
    if right_me==True or left_me==True or down_me==True or drop_me==True:    
      i_me,j_me,BlockLoca_me,BackDisp_me = block_move(i_me,j_me,BlockLoca_me,BackDisp_me,right_me,left_me,down_me,drop_me)
      if drop_me==True:
       block_choice=random.randint(1,block_N)  
       i_me,j_me,BlockLoca_me=ini_block(block_choice)#ブロック初期配置
    #ブロック回転
    elif p_rotate_me==True:    
      i_me,j_me,BlockLoca_me=block_90deg_rotate(i_me,j_me,b_n,BlockLoca_me)
    elif m_rotate_me==True:
      i_me,j_me,BlockLoca_me=block_m90deg_rotate(i_me,j_me,b_n,BlockLoca_me)

    #ブロック消し
    for k in range (1,n_h+1,1):        
      if np.all(BackDisp_me[k,1:n_w+1])==np.all(np.ones([1,n_w])):
        BackDisp_me[1:k+1,1:n_w+1]=BackDisp_me[0:k,1:n_w+1]
        delete_lines_me+=1   

    #画面写し
    show_display(i_me,j_me,put_me=True,put_pc=False)

    #画面クローズ
    if event.type == QUIT or event.key == K_ESCAPE: escape()

