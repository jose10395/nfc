#import subprocess
#import time
import MySQLdb
#import time
#import RPi.GPIO as GPIO

#def nfc_raw():
    #lines=subprocess.check_output("/usr/bin/nfc-poll", stderr=open('/dev/null','w'))
    #return lines

#def read_nfc():
    #lines=nfc_raw()
    #return lines

try:
	
    id_str = '0416126a'
    #db=MySQLdb.connect(host='localhost',user='root',passwd='',db='scal')
    db = MySQLdb.connect(host='172.28.101.230', user='root', passwd='root', db='scal')
    cursor = db.cursor()
    consulta = "select a.id_horario from horarios a,profesor b,materia c,laboratorio d,curso e where (a.profesor_id=b.id_profesor and c.id_materia=a.materia_id and d.id_laboratorio=a.laboratorio_id and a.curso_id=e.id_curso) and b.estado='ACT' and (now() between a.inicio and a.fin)and b.tag_profesor='" + id_str + "'"
    cursor.execute(consulta)
    data = cursor.fetchall()
    if(len(data) > 0):
        print(data[0])
        #query_i="insert into registro_acceso(fecha_registro_acceso,horario_id)values(now(),"+data[0]+")"
        for values in data:
            cursor.execute("insert into registro_acceso(fecha_registro_acceso,horario_id)values(now()," + str(values[0]) + ")")
            print(values[0])
    #query_i="insert into registro_acceso(fecha_registro_acceso,horario_id)values(now(),"+values[0]+")"
    db.commit()
    cursor.close()
    db.close()  
    #print (id_str)
		
except KeyboardInterrupt:
        pass
