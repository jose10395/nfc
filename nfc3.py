import subprocess
import time
import MySQLdb
import time
import RPi.GPIO as GPIO


def nfc_raw():
	lines=subprocess.check_output("/usr/bin/nfc-poll", stderr=open('/dev/null','w'))
	return lines

def read_nfc():
	lines=nfc_raw()
	return lines

try:
	while True:
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(36,GPIO.OUT)		
		print ("Acerque el dispositivo al lector NFC:")
		myLines=read_nfc()
		buffer=[]
		for line in myLines.splitlines():
			line_content=line.split()
			if(not line_content[0] == b'UID'):
				pass
			else:
				buffer.append(line_content)
		str=buffer[0]
		id_str=str[2]+str[3]+str[4]+str[5]
		db=MySQLdb.connect(host='172.28.101.230',user='root',passwd='root',db='scal') 
                cursor=db.cursor()        
		#query="insert into una(valor_tag)values('"+id_str+"')"
		#cursor.execute(query)
		#db.commit()
		consulta="select a.id_horario from horarios a,profesor b,materia c,laboratorio d,curso e where (a.profesor_id=b.id_profesor and c.id_materia=a.materia_id and d.id_laboratorio=a.laboratorio_id and a.curso_id=e.id_curso) and b.estado='ACT' and (now() between a.inicio and a.fin) and b.tag_profesor='"+id_str+"'"
		cursor.execute(consulta)
		data=cursor.fetchall();
		if(len(data) > 0):                    
                    #print (data)                    
                    #for values in data:
			#query_insert="insert into registro_acceso(fecha_registro_acceso,horario_id)values(now(),"+values[1]+")"
                        #query_insert="insert into registro_acceso(fecha_registro_acceso,horario_id)values(now(),29)"
			#cursor.execute(query_insert)
			#db.commit()
                        #print(values[1])
                    GPIO.output(36,GPIO.HIGH)
                    time.sleep(1)
                    GPIO.output(36,GPIO.LOW)                    
                else:                    
                    print("False")
		cursor.close()
		db.close()  
		#print (id_str)
		
except KeyboardInterrupt:
        pass
