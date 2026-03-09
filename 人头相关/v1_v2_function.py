

def servo_function(pwm_dic, id_dic) :

    i = 0
    step_length = 11.1

    for servo_id in id_dic[0] :
        pwm_list = pwm_dic[servo_id]
        pwm_mid = round( (pwm_list[0] - 500)/step_length )
        pwm_high = round( (pwm_list[2] - 500)/step_length )
        pwm_low = round( (pwm_list[1] - 500)/step_length )

        if pwm_high > pwm_low :
            servo_high = pwm_high 
            servo_low = pwm_low

        if pwm_high < pwm_low :
            servo_high = pwm_low
            servo_low = pwm_high

        # print(id_dic[2][i] ,'=', 'Servo(', servo_id ,',', pwm_mid ,',', servo_high,',', servo_low ,', 11.1, 0, 0, ',id_dic[1][i] ,')')
        # print(id_dic[2][i] ,'=', 'Servo(', servo_id ,',', pwm_mid ,',', servo_high,',', servo_low ,', 11.1, 0, 0, ',id_dic[1][i] ,') \t  #' , 
        #       round((float(pwm_mid)-float(servo_low)) / (float(servo_high) - float(servo_low)) ,2 ))

        if id_dic[1][i] == 0 :
            print(id_dic[2][i] ,'\t=', 'Servo(', servo_id ,',', pwm_mid ,',', servo_high,',', servo_low ,', 11.1, 0, 0, ',id_dic[1][i] ,') \t  #' , 
                round((float(pwm_mid)-float(servo_low)) / (float(servo_high) - float(servo_low)) ,2 ))


        if id_dic[1][i] == 1 :
            print(id_dic[2][i] ,'\t=', 'Servo(', servo_id ,',', pwm_mid ,',', servo_high,',', servo_low ,', 11.1, 0, 0, ',id_dic[1][i] ,') \t  #' , 
                round((float(servo_high)-float(pwm_mid)) / (float(servo_high) - float(servo_low)) ,2 ))

        
        i = i+1




if __name__ == '__main__':

    v1_head = [[1500,1200,1800] ,
            
            [1500,1750,1250],
            [1500,2500,500],
            [0,0,0],
            [0,0,0],
            [1500,1000,1900],

            [1500,1500,2300],
            [1500,1500,2000],
            [1500,1800,1200],
            [1500,1250,1270],
            [1500,1050,1900],

            [1500,2500,500],
            [1500,1500,1000],
            [1500,1500,800],  
            [1500,2000,1100],
            [0,0,0]]
    v1_head_id = [[14,0,1,12,13,    5,8,9,7,6,  10,11,2],
                  [ 0,0,0, 1, 0,    1,1,0,0,1,  1, 0,0],
                  ['left_blink','left_eye_erect' ,'left_eye_level' ,'left_eyebrow_erect' ,'left_eyebrow_level' ,
                   'right_blink' ,'right_eye_erect' ,'right_eye_level' ,'right_eyebrow_erect' ,'right_eyebrow_level' ,
                   'head_dian' ,'head_yao'  ,'head_bai' ]]

    v1_mouth = [[1500,500,2500] ,
            
            [1500,2000,1000],
            [1500,1500,2000],
            [0,0,0],
            [0,0,0],
            [1500,1400,1900],

            [1500,1400,2500],
            [1500,2500,500],
            [1500,2500,500],
            [1500,1000,2000],
            [1500,1500,1000],

            [0,0,0],
            [1500,500,2500],
            [1500,1600,500],  
            [1500,1600,1100],
            [0,0,0]]
    v1_mouth_id = [[13,6,5,14,  0,8,12,7,   2,10,1,9],
                   [1,0,0,1,    1,0,1,0,    0,1,0,1],
                   ['mouthUpperUpLeft' ,   'mouthUpperUpRight ' ,  'mouthLowerDownLeft ', 'mouthLowerDownRight ', 
                    'mouthCornerUpLeft ','mouthCornerUpRight ','mouthCornerDownLeft ', 'mouthCornerDownRight', 
                    'jawFrontLeft ', 'jawFrontRight ', 'jawBackLeft  ', 'jawBackRight  '] ]



    v2_head =  [[1500,1200,1800] ,
                
                [1500,1750,1250],
                [1500,2500,500],
                [0,0,0],
                [0,0,0],
                [1500,1000,1900],

                [1500,1500,800],
                [1500,1500,2000],
                [1500,1800,1200],
                [1500,1250,1750],
                [1500,1050,1900],

                [1500,2500,500],
                [1500,1500,1000],
                [1500,1500,2300],  
                [1500,2000,1100],
                [0,0,0]]
    v2_head_id = [[14,0,1,12,13,    5,8,9,7,6,  10,11,2],
                  [ 0,0,0, 1, 0,    1,1,0,0,1,  1, 0,0],
                  ['left_blink','left_eye_erect' ,'left_eye_level' ,'left_eyebrow_erect' ,'left_eyebrow_level' ,
                   'right_blink' ,'right_eye_erect' ,'right_eye_level' ,'right_eyebrow_erect' ,'right_eyebrow_level' ,
                   'head_dian' ,'head_yao'  ,'head_bai' ]]



    v2_mouth = [[1500,500,1800] ,
            
            [1500,2000,1000],
            [1500,1500,2000],
            [0,0,0],
            [0,0,0],
            [1500,1400,1900],

            [1500,1750,700],
            [1500,2000,1000],
            [1500,2500,1200],
            [1500,1000,2000],
            [1500,1500,1000],

            [0,0,0],
            [1500,1000,2000],
            [1500,1250,2300],  
            [1500,1600,1100],
            [0,0,0]]
    # v2_mouth_id = [13,6,5,14, 0,8,12,7, 2,10,1,9]
    v2_mouth_id = [[13,6,5,14,  0,8,12,7,   2,10,1,9],
                   [1,0,0,1,    1,0,1,0,    0,1,0,1],
                   ['mouthUpperUpLeft' ,   'mouthUpperUpRight ' ,  'mouthLowerDownLeft ', 'mouthLowerDownRight ', 
                    'mouthCornerUpLeft ','mouthCornerUpRight ','mouthCornerDownLeft ', 'mouthCornerDownRight', 
                    'jawFrontLeft ', 'jawFrontRight ', 'jawBackLeft  ', 'jawBackRight  '] ]    

    print('v1_head')
    servo_function(v1_head, v1_head_id)
    print('v1_mouth')
    servo_function(v1_mouth, v1_mouth_id)

    print('\n\nv2_head')
    servo_function(v2_head, v2_head_id)
    print('v2_mouth')
    servo_function(v2_mouth, v2_mouth_id)




'''
left_blink      = Servo( 14 , 90 , 135 , 54 , 11.1, 0, 0,  0 )    # 0.44
left_eye_erect  = Servo( 0 , 90 , 117 , 63 , 11.1, 0, 0,  0 )     # 0.5
left_eye_level  = Servo( 1 , 90 , 113 , 68 , 11.1, 0, 0,  0 )     # 0.49
left_eyebrow_erect      = Servo( 12 , 90 , 90 , 45 , 11.1, 0, 0,  1 )     # 0.0
left_eyebrow_level      = Servo( 13 , 90 , 90 , 27 , 11.1, 0, 0,  0 )     # 1.0
right_blink     = Servo( 5 , 90 , 126 , 45 , 11.1, 0, 0,  1 )     # 0.44
right_eye_erect         = Servo( 8 , 90 , 117 , 63 , 11.1, 0, 0,  1 )     # 0.5
right_eye_level         = Servo( 9 , 90 , 69 , 68 , 11.1, 0, 0,  0 )      # 22.0
right_eyebrow_erect     = Servo( 7 , 90 , 135 , 90 , 11.1, 0, 0,  0 )     # 0.0
right_eyebrow_level     = Servo( 6 , 90 , 162 , 90 , 11.1, 0, 0,  1 )     # 1.0
head_dian       = Servo( 10 , 90 , 126 , 50 , 11.1, 0, 0,  1 )    # 0.47
head_yao        = Servo( 11 , 90 , 180 , 0 , 11.1, 0, 0,  0 )     # 0.5
head_bai        = Servo( 2 , 90 , 180 , 0 , 11.1, 0, 0,  0 )      # 0.5
v1_mouth
mouthUpperUpLeft        = Servo( 13 , 90 , 99 , 0 , 11.1, 0, 0,  1 )      # 0.09
mouthUpperUpRight       = Servo( 6 , 90 , 180 , 81 , 11.1, 0, 0,  0 )     # 0.09
mouthLowerDownLeft      = Servo( 5 , 90 , 126 , 81 , 11.1, 0, 0,  0 )     # 0.2
mouthLowerDownRight     = Servo( 14 , 90 , 99 , 54 , 11.1, 0, 0,  1 )     # 0.2
mouthCornerUpLeft       = Servo( 0 , 90 , 180 , 0 , 11.1, 0, 0,  1 )      # 0.5
mouthCornerUpRight      = Servo( 8 , 90 , 180 , 0 , 11.1, 0, 0,  0 )      # 0.5
mouthCornerDownLeft     = Servo( 12 , 90 , 180 , 0 , 11.1, 0, 0,  1 )     # 0.5
mouthCornerDownRight    = Servo( 7 , 90 , 180 , 0 , 11.1, 0, 0,  0 )      # 0.5
jawFrontLeft    = Servo( 2 , 90 , 135 , 90 , 11.1, 0, 0,  0 )     # 0.0
jawFrontRight   = Servo( 10 , 90 , 90 , 45 , 11.1, 0, 0,  1 )     # 0.0
jawBackLeft     = Servo( 1 , 90 , 135 , 45 , 11.1, 0, 0,  0 )     # 0.5
jawBackRight    = Servo( 9 , 90 , 135 , 45 , 11.1, 0, 0,  1 )     # 0.5


v2_head
left_blink      = Servo( 14 , 90 , 135 , 54 , 11.1, 0, 0,  0 )    # 0.44
left_eye_erect  = Servo( 0 , 90 , 117 , 63 , 11.1, 0, 0,  0 )     # 0.5
left_eye_level  = Servo( 1 , 90 , 113 , 68 , 11.1, 0, 0,  0 )     # 0.49
left_eyebrow_erect      = Servo( 12 , 90 , 90 , 45 , 11.1, 0, 0,  1 )     # 0.0
left_eyebrow_level      = Servo( 13 , 90 , 162 , 90 , 11.1, 0, 0,  0 )    # 0.0
right_blink     = Servo( 5 , 90 , 126 , 45 , 11.1, 0, 0,  1 )     # 0.44
right_eye_erect         = Servo( 8 , 90 , 117 , 63 , 11.1, 0, 0,  1 )     # 0.5
right_eye_level         = Servo( 9 , 90 , 113 , 68 , 11.1, 0, 0,  0 )     # 0.49
right_eyebrow_erect     = Servo( 7 , 90 , 135 , 90 , 11.1, 0, 0,  0 )     # 0.0
right_eyebrow_level     = Servo( 6 , 90 , 90 , 27 , 11.1, 0, 0,  1 )      # 0.0
head_dian       = Servo( 10 , 90 , 126 , 50 , 11.1, 0, 0,  1 )    # 0.47
head_yao        = Servo( 11 , 90 , 180 , 0 , 11.1, 0, 0,  0 )     # 0.5
head_bai        = Servo( 2 , 90 , 180 , 0 , 11.1, 0, 0,  0 )      # 0.5
v2_mouth
mouthUpperUpLeft        = Servo( 13 , 90 , 162 , 68 , 11.1, 0, 0,  1 )    # 0.77
mouthUpperUpRight       = Servo( 6 , 90 , 113 , 18 , 11.1, 0, 0,  0 )     # 0.76
mouthLowerDownLeft      = Servo( 5 , 90 , 126 , 81 , 11.1, 0, 0,  0 )     # 0.2
mouthLowerDownRight     = Servo( 14 , 90 , 99 , 54 , 11.1, 0, 0,  1 )     # 0.2
mouthCornerUpLeft       = Servo( 0 , 90 , 117 , 0 , 11.1, 0, 0,  1 )      # 0.23
mouthCornerUpRight      = Servo( 8 , 90 , 180 , 63 , 11.1, 0, 0,  0 )     # 0.23
mouthCornerDownLeft     = Servo( 12 , 90 , 135 , 45 , 11.1, 0, 0,  1 )    # 0.5
mouthCornerDownRight    = Servo( 7 , 90 , 135 , 45 , 11.1, 0, 0,  0 )     # 0.5
jawFrontLeft    = Servo( 2 , 90 , 135 , 90 , 11.1, 0, 0,  0 )     # 0.0
jawFrontRight   = Servo( 10 , 90 , 90 , 45 , 11.1, 0, 0,  1 )     # 0.0
jawBackLeft     = Servo( 1 , 90 , 135 , 45 , 11.1, 0, 0,  0 )     # 0.5
jawBackRight    = Servo( 9 , 90 , 135 , 45 , 11.1, 0, 0,  1 )     # 0.5

'''



